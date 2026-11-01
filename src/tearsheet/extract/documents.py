"""The annual report as plain text, page by page.

Two sources:
- the report inside each electronic filing (iXBRL web page), downloaded in M1;
- PDFs supplied by Imane where no electronic filing exists (`config/report_documents.yaml`),
  read with `pdftotext` (poppler), as in the gate 1 model (decision 0009).

Pages are kept so every quote can be located. Where a web report has no page marks, the text
is cut into numbered parts of about the same length, and locations read "part N".
The text is cached under data/text/ so the slow conversion runs once per report.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

import yaml

from tearsheet.config import CONFIG, DATA, ROOT

TEXT_CACHE = DATA / "text"
REPORT_DOCUMENTS = CONFIG / "report_documents.yaml"
DOCUMENT_DIR = ROOT / "documents"
PART_CHARS = 4000
TEXT_VERSION = 1  # bump when the conversion changes, so cached text is rebuilt

PAGE_CLASSES = re.compile(r"^(?:pageView|pf|page|pdf-page)$")
SKIP_TAGS = {"style", "script", "head", "title", "noscript", "svg"}
BLOCK_TAGS = {
    "p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section",
    "article", "header", "footer", "ul", "ol", "dd", "dt", "blockquote",
}  # fmt: skip
CELL_TAGS = {"td", "th"}


@dataclass(frozen=True)
class Document:
    doc_id: str  # filing id, or the PDF's register id
    issuer: str
    fiscal_year: int
    language: str | None
    origin: str  # "filings.xbrl.org report" or "PDF supplied by Imane"
    source: str  # URL or file name
    sha256: str | None
    pages: tuple[str, ...]
    location_kind: str  # "page" or "part"

    def location(self, index: int) -> str:
        return f"{self.location_kind} {index + 1}"

    @property
    def text(self) -> str:
        return "\n".join(self.pages)


class _TextParser(HTMLParser):
    """HTML to text: drops styles, scripts, images and the hidden iXBRL header; starts a new
    page at each page container; keeps line breaks at block ends and spaces between cells."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pages: list[list[str]] = [[]]
        self.skip_depth = 0
        self.stack: list[tuple[str, bool, bool]] = []  # tag, skipping, is_page
        self.page_marks = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        hidden = "display:none" in (attrs.get("style") or "").replace(" ", "")
        skipping = tag in SKIP_TAGS or tag == "ix:header" or hidden
        classes = (attrs.get("class") or "").split()
        is_page = tag == "div" and any(PAGE_CLASSES.match(c) for c in classes)
        if is_page and not self.skip_depth:
            self.page_marks += 1
            if any(s.strip() for s in self.pages[-1]):
                self.pages.append([])
        if tag in ("br", "img", "hr", "meta", "link", "input"):
            if tag == "br" and not self.skip_depth:
                self.pages[-1].append("\n")
            return
        if skipping:
            self.skip_depth += 1
        self.stack.append((tag, skipping, is_page))

    def handle_endtag(self, tag):
        tag = tag.lower()
        while self.stack:
            open_tag, skipping, _ = self.stack.pop()
            if skipping:
                self.skip_depth -= 1
            if open_tag == tag:
                break
        if self.skip_depth:
            return
        if tag in BLOCK_TAGS:
            self.pages[-1].append("\n")
        elif tag in CELL_TAGS:
            self.pages[-1].append(" ")

    def handle_data(self, data):
        if not self.skip_depth:
            self.pages[-1].append(data)


def _tidy(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"[ \t\r\f\v   ]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{2,}", "\n", text).strip()


def html_pages(html: str) -> tuple[list[str], str]:
    """Pages of text from an iXBRL report, and the location kind ('page' or 'part')."""
    html = re.sub(r"data:[a-z]+/[^\"')\s]+", "", html)  # embedded images, often most of the file
    parser = _TextParser()
    parser.feed(html)
    parser.close()
    pages = [_tidy("".join(p)) for p in parser.pages]
    pages = [p for p in pages if p]
    if parser.page_marks >= 5:
        return pages, "page"
    return split_parts("\n".join(pages)), "part"


def split_parts(text: str, size: int = PART_CHARS) -> list[str]:
    """Cut text without page marks into parts of about `size` characters, at line ends."""
    parts, current, length = [], [], 0
    for line in text.split("\n"):
        current.append(line)
        length += len(line) + 1
        if length >= size:
            parts.append("\n".join(current))
            current, length = [], 0
    if current:
        parts.append("\n".join(current))
    return parts


def pdf_pages(path: Path) -> list[str]:
    """Pages of text from a PDF, in reading order (columns one after the other)."""
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext (poppler-utils) is needed to read PDF reports")
    out = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True, check=True
    ).stdout.decode("utf-8", errors="replace")
    return [_tidy(p) for p in out.split("\f")]


def _cached(key: str, build) -> tuple[list[str], str]:
    path = TEXT_CACHE / f"{key}.json"
    if path.exists():
        data = json.loads(path.read_text())
        if data.get("version") == TEXT_VERSION:
            return data["pages"], data["location_kind"]
    pages, kind = build()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": TEXT_VERSION, "location_kind": kind, "pages": pages}
    path.write_text(json.dumps(payload, ensure_ascii=False))
    return pages, kind


def from_report(
    doc_id: str,
    issuer: str,
    fiscal_year: int,
    language: str | None,
    report_path: Path,
    source: str,
    sha256: str | None,
) -> Document:
    key = hashlib.sha256(f"{report_path.name}:{report_path.stat().st_size}".encode()).hexdigest()
    pages, kind = _cached(
        key[:24], lambda: html_pages(report_path.read_text(encoding="utf-8", errors="replace"))
    )
    return Document(
        doc_id,
        issuer,
        fiscal_year,
        language,
        "filings.xbrl.org report",
        source,
        sha256,
        tuple(pages),
        kind,
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def supplied_documents(issuer: str, path: Path = REPORT_DOCUMENTS) -> list[Document]:
    """PDFs supplied by Imane for this issuer, checked against their registered fingerprint."""
    entries = (yaml.safe_load(path.read_text()) or {}).get("documents") or []
    docs = []
    for e in entries:
        if e["issuer"] != issuer:
            continue
        pdf = DOCUMENT_DIR / e["file"]
        if not pdf.exists():
            raise FileNotFoundError(f"{pdf} is registered in {path.name} but missing")
        digest = file_sha256(pdf)
        if digest != e["sha256"]:
            raise ValueError(f"{pdf.name}: fingerprint differs from {path.name}")
        pages, kind = _cached(f"pdf-{digest[:24]}", lambda pdf=pdf: (pdf_pages(pdf), "page"))
        docs.append(
            Document(
                e["id"],
                issuer,
                int(e["fiscal_year"]),
                e.get("language"),
                f"PDF supplied by {e.get('supplied_by', 'Imane')}",
                e["file"],
                digest,
                tuple(pages),
                kind,
            )
        )
    return docs
