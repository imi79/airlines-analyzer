"""Half-year statements (M10, decision 0025): the first-half figures, read from the PDF report.

Half-year reports are not in the filings database, so the three condensed statements are read
from the report's pages. The work is split as everywhere else in the tool:

- the AI says, for each statement line the database already holds for the last full year,
  WHICH ROW of the half-year statements carries it (a fixed form, prompt `halfyear-v1`);
- code reads the amounts from that row of the page itself, decides which column is which, and
  checks every line before it counts:
    1. the row is on the page of its statement, word for word;
    2. columns: the first half, the same half a year before and, where printed, the full year
       are identified from the header by code; on the balance sheet the year-end column is
       the one whose figures equal the database's, line by line;
    3. the row is the right one: its year-end column (balance sheet) or full-year column
       (income statement, cash flow) equals the database's figure; where the report prints no
       full year, the row's label must be the one under which the annual report prints the
       database's figure;
    4. the statements add up: total assets = total equity and liabilities; opening cash +
       movements = closing cash.
A line that fails a check is unverified, with every reason kept, and stays off the page until
Imane approves or corrects it (config/half_year_reviews.yaml).

Where a PDF shows its figures but does not give them as text, the lines are entered by hand
(config/half_year_entries.yaml) and go through the same controls against the database.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from itertools import combinations, product
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ValidationError

from tearsheet.config import CONFIG, ROOT, Issuer
from tearsheet.extract.documents import Document, _cached, file_sha256
from tearsheet.extract.numbers import SCALE_FACTORS, number_tokens, parse_number, squash
from tearsheet.llm import LLM, LLMError, NotRecorded, ToolResult, ToolSpec
from tearsheet.normalize.mapper import MappedFact

HERE = Path(__file__).parent
SETTINGS = HERE / "half_year.yaml"
REGISTER = CONFIG / "half_year_reports.yaml"
ENTRIES = CONFIG / "half_year_entries.yaml"
REVIEWS = CONFIG / "half_year_reviews.yaml"
DOCUMENT_DIR = ROOT / "documents" / "half-year"
PROMPT_VERSION = "halfyear-v1"  # bump with every change to the prompt, the form or the request
NOT_RUN = "half-year statements not read yet: no recorded AI answer (run `tearsheet extract`)"
DASHES = {"-", "–", "—", "−"}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def load_settings(path: Path = SETTINGS) -> dict:
    return yaml.safe_load(path.read_text())


# --- The register of reports -------------------------------------------------------------------


@dataclass(frozen=True)
class Report:
    id: str
    issuer: str
    period_end: date
    base_fiscal_year: int
    language: str
    document: str
    file: str
    sha256: str
    url: str | None = None
    read_by: str = "ai"  # ai | hand
    audit: str = "unaudited"

    @property
    def h1_label(self) -> str:
        return f"H1 to {MONTHS[self.period_end.month - 1]} {self.period_end.year}"

    @property
    def ltm_label(self) -> str:
        return f"LTM {MONTHS[self.period_end.month - 1]} {self.period_end.year}"

    @property
    def prior_end(self) -> date:
        return self.period_end.replace(year=self.period_end.year - 1)


def load_reports(path: Path = REGISTER) -> list[Report]:
    if not path.exists():
        return []
    known = set(Report.__dataclass_fields__)
    out = []
    for raw in (yaml.safe_load(path.read_text()) or {}).get("reports") or []:
        values = {k: v for k, v in raw.items() if k in known}
        values["period_end"] = date.fromisoformat(str(values["period_end"]))
        out.append(Report(**values))
    return out


def report_for(issuer_id: str, path: Path = REGISTER) -> Report | None:
    """The latest registered half-year report of a company."""
    mine = [r for r in load_reports(path) if r.issuer == issuer_id]
    return max(mine, key=lambda r: r.period_end) if mine else None


def layout_pages(pdf: Path) -> list[str]:
    """Pages of text with the columns kept in place (`pdftotext -layout`): a statement row
    stays on one line, its amounts under their headers."""
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext (poppler-utils) is needed to read PDF reports")
    out = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, check=True
    ).stdout.decode("utf-8", errors="replace")
    return [p.replace(" ", " ").replace(" ", " ") for p in out.split("\f")]


def document(report: Report, folder: Path = DOCUMENT_DIR) -> Document:
    """The report as pages of laid-out text, after checking the file's fingerprint."""
    pdf = folder / report.file
    if not pdf.exists():
        raise FileNotFoundError(f"{pdf} is registered in {REGISTER.name} but missing")
    digest = file_sha256(pdf)
    if digest != report.sha256:
        raise ValueError(f"{pdf.name}: fingerprint differs from {REGISTER.name}")
    pages, _ = _cached(f"pdfl-{digest[:24]}", lambda: (layout_pages(pdf), "page"))
    return Document(
        report.id,
        report.issuer,
        report.period_end.year,
        report.language,
        "half-year report (PDF)",
        report.file,
        digest,
        tuple(pages),
        "page",
    )


# --- Reading a row of a statement (code) -------------------------------------------------------


@dataclass(frozen=True)
class Cell:
    text: str
    value: Decimal
    start: int
    end: int


def parse_cell(text: str, language: str | None) -> Decimal | None:
    """A printed amount: '1,694.8', '(1 045)' (negative), '-34.2', '–' (nil). None if the
    cell is not an amount (a label, a percentage, a note reference such as '4&8')."""
    t = text.strip()
    if t in DASHES:
        return Decimal(0)
    negative = False
    inner = re.fullmatch(r"\((.+)\)", t)
    if inner:
        negative, t = True, inner.group(1).strip()
    if t[:1] in "-−–":
        negative, t = not negative, t[1:].strip()
    if not t or t.endswith("%"):
        return None
    value = parse_number(t, language)
    if value is None:
        return None
    return -value if negative else value


def value_cells(line: str, language: str | None) -> list[Cell]:
    """The amounts at the end of a laid-out line, left to right. Columns are two or more
    spaces apart; in languages that do not use a space inside numbers, one space is enough."""
    runs = [(m.group(0), m.start(), m.end()) for m in re.finditer(r"\S+(?: \S+)*", line)]
    cells: list[Cell] = []
    for text, start, end in reversed(runs):
        value = parse_cell(text, language)
        if value is not None:
            cells.append(Cell(text, value, start, end))
            continue
        if language != "fr":  # "(1,591) (1,654)": two amounts one space apart
            parts = [
                (m.group(0), start + m.start(), start + m.end()) for m in re.finditer(r"\S+", text)
            ]
            tail = []
            for ptext, pstart, pend in reversed(parts):
                pvalue = parse_cell(ptext, language)
                if pvalue is None:
                    break
                tail.append(Cell(ptext, pvalue, pstart, pend))
            cells.extend(tail)
        break
    return list(reversed(cells))


YEAR = re.compile(r"(?<![\d.,/])20[2-3]\d(?![\d.,])|(?<=\d/)20[2-3]\d(?![\d.,])")


def is_value_row(line: str, language: str | None) -> bool:
    """A statement row: at least two amounts at the end, which are not just the header's
    years ('2026   2025')."""
    cells = value_cells(line, language)
    if len(cells) < 2:
        return False
    return not all(re.fullmatch(r"20[2-3]\d", c.text) for c in cells)


TITLES = {
    "income": r"income statement|statement of comprehensive income|statement of profit or loss|"
    r"compte de r[ée]sultat|cuenta de resultados|gewinn- und verlustrechnung",
    "balance": r"balance sheet|statement of financial position|"
    r"[ée]tat (?:consolid[ée] )?de (?:la )?situation financi[èe]re|"
    r"estado de situaci[óo]n financiera|bilan consolid|konzern-?bilanz",
    "cash_flow": r"cash flows? statement|statement of cash flows?|flux de tr[ée]sorerie|"
    r"flujos de efectivo|geldflussrechnung",
}
COMPREHENSIVE = (
    r"comprehensive|recognized income|r[ée]sultat global|resultado global|gesamtergebnis"
)
OTHER_TITLES = (
    r"changes in equity|variation des capitaux propres|cambios en el patrimonio|"
    r"eigenkapital|notes to the|notes annexes|notas (?:a los|explicativas)"
)


def _title_at(line: str, kind: str) -> bool:
    text = line.strip()
    if not text or len(text) > 130 or re.search(r"[.…]{3,}\s*\d*$|\s{2,}\d{1,3}$", text):
        return False  # empty, or a table-of-contents line
    if text.endswith((".", ",", ";", ":")) or text[0].islower() or text[0] in "•-–▶«(":
        return False  # running text, not a heading
    if len(text.split()) > 16:
        return False
    return bool(re.search(TITLES[kind], text, re.I))


@dataclass(frozen=True)
class Region:
    """Where a statement sits: the lines from its title to the end of the page, and the next
    page down to the next statement's title."""

    kind: str
    page: int
    lines: tuple[tuple[int, int, str], ...]  # page index, line index, text

    @property
    def pages(self) -> tuple[int, ...]:
        return tuple(dict.fromkeys(p for p, _, _ in self.lines))


def find_statements(doc: Document, settings: dict | None = None) -> dict[str, Region]:
    """The three statements: the pages whose title names them and that hold rows of amounts;
    where a title appears more than once (a summary in the management report), the three
    pages that sit closest together are the financial statements."""
    settings = settings or load_settings()
    minimum = settings["pages"]["rows_minimum"]
    candidates: dict[str, list[tuple[int, int]]] = {k: [] for k in TITLES}
    for p, page in enumerate(doc.pages):
        lines = page.split("\n")
        for kind in TITLES:
            for i, line in enumerate(lines):
                if not _title_at(line, kind):
                    continue
                rows = sum(is_value_row(x, doc.language) for x in lines[i:])
                foot = len([x for x in lines[i:] if x.strip()]) <= 14
                if rows < minimum and foot and p + 1 < len(doc.pages):  # title at a page's foot
                    rows += sum(is_value_row(x, doc.language) for x in doc.pages[p + 1].split("\n"))
                if rows >= minimum:
                    candidates[kind].append((p, i))
                    break
    # "Statement of comprehensive income" names the income statement only where the report
    # has no income statement of its own.
    plain = [
        (p, i)
        for p, i in candidates["income"]
        if not re.search(COMPREHENSIVE, doc.pages[p].split("\n")[i], re.I)
    ]
    candidates["income"] = plain or candidates["income"]
    if not all(candidates.values()):
        return {}

    def span(t) -> int:
        return max(x[0] for x in t) - min(x[0] for x in t)

    triples = list(product(*(candidates[k] for k in TITLES)))
    close = [t for t in triples if span(t) <= 6]  # the statements follow one another
    best = min(
        close or triples,
        key=lambda t: (min(x[0] for x in t), span(t)) if close else (span(t), min(x[0] for x in t)),
    )
    starts = dict(zip(TITLES, best, strict=True))
    out = {}
    for kind, (p, i) in starts.items():
        lines = [(p, n, x) for n, x in enumerate(doc.pages[p].split("\n")) if n >= i]
        cut = _next_title(lines[1:], kind)
        if cut is not None:
            lines = lines[: cut + 1]
        elif p + 1 < len(doc.pages) and not any(s[0] == p + 1 for s in starts.values()):
            more = [(p + 1, n, x) for n, x in enumerate(doc.pages[p + 1].split("\n"))]
            cut = _next_title(more, kind)
            lines += more if cut is None else more[:cut]
        out[kind] = Region(kind, p, tuple(lines))
    return out


def _next_title(lines: list[tuple[int, int, str]], kind: str) -> int | None:
    for n, (_, _, text) in enumerate(lines):
        if any(_title_at(text, k) for k in TITLES if k != kind):
            return n
        if len(text.split()) <= 16 and re.search(COMPREHENSIVE, text, re.I):
            if not is_value_row(text, None) and not text.strip()[:1].islower():
                return n  # the statement of comprehensive income repeats the profit row
        if len(text.strip()) < 130 and re.search(OTHER_TITLES, text, re.I):
            if not is_value_row(text, None):
                return n
    return None


# --- Which column is which (code) --------------------------------------------------------------

HALF = r"\bh1\b|q1\s*[-–]\s*q2|six|half|semest|jan\w*\.?\s*[-–]\s*jun|1\s*[-–]\s*6\b"
QUARTER = r"\bq[1-4]\b|quarter|three months|trimestr|quartal"
FULL = r"full|year|\bfy\b|12 months|jan\w*\.?\s*[-–]\s*de[cz]|annual|exercice|ejercicio"
SIX_MONTHS = (
    r"six[- ]months?|half[- ]year|first half|semest|january 1(?:st)? to june 30|"
    r"1 january to 30 june|\bh1\b|seis meses|halbjahr"
)
MONTH_WORDS = {
    1: r"jan|ene",
    2: r"feb|fév",
    3: r"mar",
    4: r"apr|avr|abr",
    5: r"may|mai",
    6: r"jun|juin",
    7: r"jul|juil",
    8: r"aug|août|ago",
    9: r"sep",
    10: r"oct|okt",
    11: r"nov",
    12: r"dec|déc|dic|dez",
}


@dataclass
class Columns:
    """For one statement: how many amount columns its rows have, and which is which, counted
    from the left (0) among the last `count` amounts of a row."""

    count: int = 0
    current: int | None = None
    prior: int | None = None  # the same half a year before (income statement, cash flow)
    base: int | None = None  # the year-end column (balance sheet) or the full year
    labels: dict[str, str] = field(default_factory=dict)
    how: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)


def _header(region: Region, language: str | None):
    """The header block (lines between the title and the first row), and the year marks that
    head the columns: the last line with two or more years, else every year of the block,
    left to right. Each mark comes with the words printed just before it."""
    block = []
    for _, _, text in region.lines[1:]:
        if is_value_row(text, language):
            break
        block.append(text)
    block = block[-10:]
    # Column heads stand above the amounts: a year further left belongs to a title line.
    starts = [
        value_cells(t, language)[0].start for _, _, t in region.lines if is_value_row(t, language)
    ]
    left = (sorted(starts)[len(starts) // 2] - 30) if starts else 0
    marks: list[tuple[int, int, str]] = []  # x position, year, words before it on its line
    for text in reversed(block):
        found = [m for m in YEAR.finditer(text) if m.end() > left]
        if len(found) >= 2:
            previous = 0
            for m in found:
                marks.append((m.end(), int(m.group(0)), text[previous : m.end()]))
                previous = m.end()
            break
    if not marks:
        for text in block:
            for m in YEAR.finditer(text):
                if m.end() > left:
                    marks.append((m.end(), int(m.group(0)), text[max(0, m.start() - 24) : m.end()]))
        marks.sort()
    title = region.lines[0][2] if region.lines else ""
    return " ".join([title] + block), marks


def _row_counts(region: Region, language: str | None) -> list[int]:
    return [len(value_cells(t, language)) for _, _, t in region.lines if is_value_row(t, language)]


def flow_columns(region: Region, report: Report, settings: dict) -> Columns:
    """Income statement and cash flow: the columns are named by the header's years. 'Q1-Q2
    2026' or a bare '2026' under 'Six months to 30 June' is the first half; 'Q2 2026' a
    quarter; 'Full Year 2025', or a bare '2025' beside labelled halves, the full year."""
    cols = Columns()
    block, marks = _header(region, report.language)
    counts = _row_counts(region, report.language)
    if len(marks) < 2 or not counts:
        cols.failures.append("the column header of the statement could not be read")
        return cols
    n, share = len(marks), settings["tolerance"]["column_share"]
    per_year = 1
    for m in (3, 2):
        if sum(c >= n * m for c in counts) >= share * len(counts):
            per_year = m
            break
    cols.count = n * per_year
    if per_year > 1:  # several columns under each year: the last must be the total
        totals = max(len(re.findall(r"\btotal\b", t, re.I)) for _, _, t in region.lines[:12])
        if totals < n:
            cols.failures.append(
                f"{per_year} columns under each year and no 'Total' heading to choose one"
            )
            return cols
        cols.how.append(f"{per_year} columns under each year: the 'Total' column is read")
    kinds = []
    for _, _, words in marks:
        w = words.lower()
        if re.search(HALF, w):
            kinds.append("half")
        elif re.search(QUARTER, w):
            kinds.append("quarter")
        elif re.search(FULL, w):
            kinds.append("full")
        else:
            kinds.append("bare")
    if "bare" in kinds:
        if any(k != "bare" for k in kinds):
            kinds = ["full" if k == "bare" else k for k in kinds]
        elif re.search(SIX_MONTHS, block, re.I):
            kinds = ["half"] * n
        else:
            cols.failures.append("the header does not say that the columns are six months")
            return cols

    def pick(kind: str, year: int) -> int | None:
        hits = [
            i
            for i, (k, (_, y, _)) in enumerate(zip(kinds, marks, strict=True))
            if k == kind and y == year
        ]
        return hits[0] * per_year + per_year - 1 if len(hits) == 1 else None

    cols.current = pick("half", report.period_end.year)
    cols.prior = pick("half", report.period_end.year - 1)
    full = [i for i, k in enumerate(kinds) if k == "full"]
    if len(full) == 1:
        cols.base = full[0] * per_year + per_year - 1
        cols.labels["base"] = " ".join(marks[full[0]][2].split()[-3:])
    if cols.current is None or cols.prior is None:
        cols.failures.append("the header does not show one column for each of the two halves")
    for role in ("current", "prior"):
        i = getattr(cols, role)
        if i is not None:
            cols.labels[role] = " ".join(marks[i // per_year][2].split()[-3:])
    cols.how.append("columns named by the header's years")
    return cols


def balance_columns(
    region: Region,
    report: Report,
    rows: dict[str, list[list[Cell]]],
    held: dict[str, Decimal],
    scale: Decimal,
    settings: dict,
) -> Columns:
    """Balance sheet: the year-end column is the one whose figures equal the database's, line
    by line. With two columns the other one is the half-year date; with three (the half-year
    date a year before is printed too) the header's dates decide."""
    cols = Columns()
    _, marks = _header(region, report.language)
    cols.count = 3 if len(marks) == 3 else 2
    tol = settings["tolerance"]
    matches = [0] * cols.count
    compared = 0
    for line, components in rows.items():
        if line not in held or any(len(c) < cols.count for c in components):
            continue
        compared += 1
        for i in range(cols.count):
            total = sum((c[len(c) - cols.count + i].value for c in components), Decimal(0))
            if _agrees(
                abs(total) * scale, abs(held[line]), scale, len(components), components, tol
            ):
                matches[i] += 1
    best = max(range(cols.count), key=lambda i: matches[i])
    needed = max(tol["anchor_minimum"], tol["anchor_share"] * compared)
    if matches[best] < needed or sorted(matches)[-2] == matches[best]:
        cols.failures.append(
            f"no column of the balance sheet agrees with the database's year-end figures "
            f"({matches[best]} of {compared} lines at best)"
        )
        return cols
    cols.base = best
    cols.how.append(
        f"year-end column: {matches[best]} of {compared} lines equal the database's figures"
    )
    if cols.count == 2:
        cols.current = 1 - best
        cols.how.append("the other column is the half-year date")
        return cols
    dated = []
    for _, year, words in marks:
        month = next(
            (
                m
                for m, pat in MONTH_WORDS.items()
                if re.search(pat, words.lower()) or f"/{m:02d}/" in words
            ),
            None,
        )
        dated.append((month, year))
    want = (report.period_end.month, report.period_end.year)
    hits = [i for i, d in enumerate(dated) if d == want]
    if len(hits) != 1 or hits[0] == best:
        cols.failures.append("three balance sheet columns and the header's dates are unclear")
        return cols
    cols.current = hits[0]
    cols.how.append("half-year column named by the header's date")
    return cols


def _unit(components: list[list[Cell]], language: str | None = None) -> Decimal:
    """The smallest printed step of the amounts read (1 for whole millions, 0.1...)."""
    places = 0
    for cells in components:
        for c in cells:
            m = re.search(r"[.,](\d{1,2})\)?$", c.text)
            if m and not re.search(r"[.,]\d{3}\)?$", c.text):
                places = max(places, len(m.group(1)))
    return Decimal(1).scaleb(-places)


def _agrees(read: Decimal, held: Decimal, scale: Decimal, n: int, components, tol: dict) -> bool:
    allowed = Decimal(str(tol["units_per_row"])) * _unit(components) * scale * n / 2
    return abs(read - held) <= allowed + Decimal("0.000001")


# --- The form ----------------------------------------------------------------------------------


class RawComponent(BaseModel):
    label: str
    quote: str
    operation: Literal["add", "subtract"] = "add"


class RawLine(BaseModel):
    line: str
    components: list[RawComponent]
    comment: str | None = None


class RawMissing(BaseModel):
    line: str
    reason: str | None = None


def tool(line_ids: list[str]) -> ToolSpec:
    component = {
        "type": "object",
        "properties": {
            "label": {"type": "string", "description": "Row label, verbatim, without amounts."},
            "quote": {"type": "string", "description": "The whole row, verbatim, with amounts."},
            "operation": {"type": "string", "enum": ["add", "subtract"]},
        },
        "required": ["label", "quote", "operation"],
    }
    return ToolSpec(
        name="record_half_year_rows",
        description="Record which statement rows hold each line, or that a line is not there.",
        schema={
            "type": "object",
            "properties": {
                "scale": {"type": "string", "enum": ["one", "thousand", "million"]},
                "lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "line": {"type": "string", "enum": line_ids},
                            "components": {"type": "array", "minItems": 1, "items": component},
                            "comment": {"type": "string"},
                        },
                        "required": ["line", "components"],
                    },
                },
                "not_found": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "line": {"type": "string", "enum": line_ids},
                            "reason": {"type": "string"},
                        },
                        "required": ["line"],
                    },
                },
            },
            "required": ["scale", "lines"],
        },
    )


def system_prompt(version: str = PROMPT_VERSION) -> str:
    return (HERE / "prompts" / f"{version.replace('-', '_')}.md").read_text()


def _money(value: Decimal, scale: Decimal) -> str:
    return f"{value / scale:,.1f}".rstrip("0").rstrip(".")


def user_message(
    issuer: Issuer,
    report: Report,
    doc: Document,
    regions: dict[str, Region],
    held: dict[str, Decimal],
    settings: dict,
    base_label: str,
) -> str:
    wanted = []
    for line, spec in settings["lines"].items():
        if line in held:
            wanted.append(
                f"- {line} ({spec['statement'].replace('_', ' ')}): {spec['ask']} "
                f"Database, {base_label}: {_money(abs(held[line]), Decimal(1_000_000))} million."
            )
    for line, spec in settings["controls"].items():
        wanted.append(f"- {line} ({spec['statement'].replace('_', ' ')}): {spec['ask']}")
    pages = sorted({p for r in regions.values() for p in r.pages})
    text, budget = [], settings["pages"]["max_chars"]
    for p in pages:
        page = re.sub(r" {4,}", "   ", doc.pages[p])  # narrower; code reads the original page
        page = "\n".join(x.rstrip() for x in page.split("\n") if x.strip())
        if budget - len(page) < 0:
            break
        budget -= len(page)
        text.append(f"=== page {p + 1} ===\n{page}")
    return "\n".join(
        [
            f"Company: {issuer.name} ({issuer.type}). Reporting currency: {issuer.currency}.",
            f"Report: {report.document}, language: {report.language}.",
            f"Half year ended {report.period_end.isoformat()}; last full fiscal year in the "
            f"database: {base_label}.",
            "",
            "Lines wanted:",
            *wanted,
            "",
            "Pages of the report holding the three statements:",
            "",
            "\n\n".join(text),
        ]
    )


# --- The checks --------------------------------------------------------------------------------


@dataclass
class RowRead:
    label: str
    operation: str
    page: int | None = None  # index
    text: str | None = None  # the row as it stands on the page
    cells: list[Cell] = field(default_factory=list)


@dataclass
class LineRead:
    line: str
    statement: str
    rows: list[RowRead] = field(default_factory=list)
    current: Decimal | None = None  # full units, the database's sign convention
    prior: Decimal | None = None
    base: Decimal | None = None  # the report's own year-end or full-year column
    held: Decimal | None = None  # the database's figure for the last full year
    control: str | None = None  # which control confirmed the row
    decimals: int | None = None
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    review: dict | None = None
    manual: bool = False

    @property
    def is_flow(self) -> bool:
        return self.statement != "balance"

    @property
    def complete(self) -> bool:
        return self.current is not None and (self.prior is not None or not self.is_flow)

    @property
    def status(self) -> str:
        if not self.complete:
            return "unverified"
        if self.review is not None:
            return "overridden" if self.review.get("action") == "correct" else "verified"
        return "unverified" if self.failures else "verified"

    @property
    def location(self) -> str:
        pages = sorted({r.page + 1 for r in self.rows if r.page is not None})
        return "page " + ", ".join(str(p) for p in pages) if pages else ""


@dataclass
class HalfYearRun:
    report: Report
    doc: Document | None = None
    lines: list[LineRead] = field(default_factory=list)
    not_found: dict[str, str] = field(default_factory=dict)  # line -> reason
    columns: dict[str, Columns] = field(default_factory=dict)
    statement_failures: dict[str, list[str]] = field(default_factory=dict)
    scale: Decimal = Decimal(1_000_000)
    invalid: list[str] = field(default_factory=list)
    result: ToolResult | None = None
    error: str | None = None

    def get(self, line: str) -> LineRead | None:
        return next((x for x in self.lines if x.line == line), None)


def locate_row(region: Region, component: RawComponent, language: str | None) -> RowRead:
    """The row on the page: by its quote, word for word (spaces ignored); failing that, by the
    one row of the statement that starts with the label. The amounts are then read from the
    page, never from the AI's copy."""
    row = RowRead(component.label, component.operation)
    quote, label = squash(component.quote), squash(component.label)
    rows = [(p, n, t) for p, n, t in region.lines if is_value_row(t, language)]
    hits = []
    if quote:
        for i, (p, _n, t) in enumerate(region.lines):
            if not is_value_row(t, language):
                continue
            here = squash(t)
            before = squash(region.lines[i - 1][2]) if i else ""
            after = squash(region.lines[i + 1][2]) if i + 1 < len(region.lines) else ""
            if quote == here or (
                len(quote) > 12
                and quote in before + here + after
                and (here in quote or quote in here)
            ):
                hits.append((p, t))
    if len(hits) != 1 and label:
        starts = [(p, t) for p, _n, t in rows if squash(t).startswith(label)]
        if len(starts) == 1 or (not hits and _same_amounts(starts, language)):
            hits = starts[:1]
    if len(hits) > 1 and _same_amounts(hits, language):
        hits = hits[:1]  # the row is printed twice with the same amounts (a reconciliation)
    if len(hits) == 1:
        row.page, row.text = hits[0]
        row.cells = value_cells(row.text, language)
    return row


def _same_amounts(hits: list[tuple[int, str]], language: str | None) -> bool:
    amounts = {tuple(c.value for c in value_cells(t, language)) for _, t in hits}
    return bool(hits) and len(amounts) == 1


def _signed(settings: dict, line: str) -> bool:
    spec = settings["lines"].get(line) or settings["controls"].get(line) or {}
    return bool(spec.get("signed")) or line.startswith("control_")


def _column_value(rows: list[RowRead], cols: Columns, index: int, signed: bool, scale: Decimal):
    total = Decimal(0)
    for r in rows:
        v = r.cells[len(r.cells) - cols.count + index].value
        total += -v if r.operation == "subtract" else v
    return (total if signed else abs(total)) * scale


def annual_label_agrees(
    labels: list[str], held: Decimal, docs: list[Document], settings: dict
) -> bool:
    """Is the database's full-year figure printed in the annual report under the same row
    label(s)? For one row: the figure stands right after the label. For several rows: one
    amount right after each label, adding up to the figure."""
    tried = set()
    for variant in LABEL_VARIANTS:
        targets = tuple(variant(squash(x)) for x in labels)
        if targets not in tried and _label_agrees(list(targets), held, docs, settings):
            return True
        tried.add(targets)
    return False


# A half-year row is headed "for the period" where the annual one says "for the year", and a
# loss-making half prints "Operating loss" where the profitable year printed "Operating profit".
LABEL_VARIANTS = (
    lambda s: s,
    lambda s: _yearly(s),
    lambda s: s.replace("loss", "profit"),
    lambda s: _yearly(s).replace("loss", "profit"),
    lambda s: _yearly(s).replace("loss", "profit/(loss)"),
    lambda s: _yearly(s).replace("profit", "profit/(loss)") if "loss" not in s else s,
)


def _yearly(s: str) -> str:
    for half, year in (
        ("fortheperiod", "fortheyear"),
        ("delapériode", "del'exercice"),
        ("delperiodo", "delejercicio"),
        ("delperíodo", "delejercicio"),
    ):
        s = s.replace(half, year)
    return s


def _label_agrees(targets: list[str], held: Decimal, docs: list[Document], settings: dict):
    window = settings["tolerance"]["label_window"]
    first = settings["tolerance"]["label_amounts"]
    if not targets or not all(len(t) >= 4 for t in targets):
        return False
    for doc in docs:
        options: list[set[Decimal]] = [set() for _ in targets]
        for n, page in enumerate(doc.pages):
            flat, index = _flat_page(doc, n)
            for k, target in enumerate(targets):
                at = flat.find(target)
                while at >= 0:
                    end = index[at + len(target) - 1] + 1
                    # The figure must stand right after the label: the first amount, or the
                    # second after a note number. Further on, the amounts are other rows'.
                    # Words between the label and the amount mean a longer label ("Amortization"
                    # is not "Amortization, depreciation and provisions").
                    after = page[end : end + window]
                    for tok in number_tokens(after, doc.language)[:first]:
                        if not re.search(r"[^\W\d_]", after[: tok.start]):
                            options[k].add(abs(tok.value))
                    at = flat.find(target, at + 1)
        if not all(options) or any(len(o) > 400 for o in options):
            continue
        for scale in (Decimal(1_000_000), Decimal(1_000), Decimal(1)):
            want = abs(held) / scale
            if len(targets) == 1:
                ok = any(_same_printed(v, want) for v in options[0])
            else:
                slack = Decimal(len(targets)) / 2
                ok = any(
                    abs(sum(combo) - want) <= slack and all(v > 0 for v in combo)
                    for combo in product(*[sorted(o)[:60] for o in options])
                )
            if ok:
                return True
    return False


_FLAT: dict[tuple[str, int], tuple[str, list[int]]] = {}


def _flat_page(doc: Document, n: int) -> tuple[str, list[int]]:
    key = (f"{doc.doc_id}:{doc.sha256}", n)
    if key not in _FLAT:
        _FLAT[key] = _flat(doc.pages[n])
    return _FLAT[key]


def _same_printed(printed: Decimal, want: Decimal) -> bool:
    """A printed figure equals the database's once the database's is rounded like it."""
    places = max(0, -printed.as_tuple().exponent)
    return printed == want.quantize(Decimal(1).scaleb(-places)) and printed != 0


def _flat(page: str) -> tuple[str, list[int]]:
    flat, index = [], []
    for i, ch in enumerate(page):
        if not ch.isspace():
            flat.append(squash(ch) or ch)
            index.append(i)
    return "".join(flat), index


def check(
    report: Report,
    doc: Document,
    regions: dict[str, Region],
    raw_lines: list[RawLine],
    held: dict[str, Decimal],
    annual_docs: list[Document],
    scale: Decimal,
    settings: dict,
) -> HalfYearRun:
    run = HalfYearRun(report, doc, scale=scale)
    tol = settings["tolerance"]
    by_statement: dict[str, list[LineRead]] = {k: [] for k in TITLES}
    for raw in raw_lines:
        spec = settings["lines"].get(raw.line) or settings["controls"].get(raw.line)
        if spec is None:
            run.invalid.append(f"unknown line '{raw.line}'")
            continue
        read = LineRead(raw.line, spec["statement"], held=held.get(raw.line))
        region = regions.get(read.statement)
        for component in raw.components:
            row = (
                locate_row(region, component, report.language)
                if region
                else RowRead(component.label, component.operation)
            )
            read.rows.append(row)
            if row.text is None:
                read.failures.append(
                    f"row '{component.label}' not found in the "
                    f"{read.statement.replace('_', ' ')} statement of the report"
                )
        by_statement[read.statement].append(read)
        run.lines.append(read)

    # 2. Columns.
    for kind, region in regions.items():
        found = [x for x in by_statement[kind] if all(r.text for r in x.rows)]
        if kind == "balance":
            rows = {
                x.line: [r.cells for r in x.rows]
                for x in found
                if not x.line.startswith("control_")
            }
            cols = balance_columns(region, report, rows, held, scale, settings)
        else:
            cols = flow_columns(region, report, settings)
        run.columns[kind] = cols
        for x in found:
            if cols.current is None:
                x.failures += cols.failures or ["the statement's columns could not be read"]
                continue
            if any(len(r.cells) < cols.count for r in x.rows):
                x.failures.append("the row does not have an amount in every column")
                continue
            signed = _signed(settings, x.line)
            cells = [r.cells for r in x.rows]
            x.decimals = -int(scale.log10()) + (-_unit(cells).as_tuple().exponent)
            x.current = _column_value(x.rows, cols, cols.current, signed, scale)
            if kind != "balance" and cols.prior is not None:
                x.prior = _column_value(x.rows, cols, cols.prior, signed, scale)
            if cols.base is not None:
                x.base = _column_value(x.rows, cols, cols.base, signed, scale)

    # 3. The right row: against the database.
    for x in run.lines:
        if x.line.startswith("control_") or not x.complete:
            continue
        cells = [r.cells for r in x.rows]
        _compare_with_database(x, report, cells, scale, annual_docs, settings, tol)

    _combined_debt(run, held, scale, tol)

    # 4. The statements add up.
    run.statement_failures = _add_up(run, scale, tol)
    for kind, problems in run.statement_failures.items():
        for x in by_statement[kind]:
            if not x.line.startswith("control_"):
                x.failures += problems
    return run


def _combined_debt(run: HalfYearRun, held: dict, scale: Decimal, tol: dict) -> None:
    """A condensed balance sheet may print borrowings and lease liabilities as one row ("Current
    debt", "Non-current debt") where the annual one splits them. The rows then fail the
    line-by-line control; but if together they equal the database's borrowings plus lease
    liabilities at year end, they are the company's debt including leases."""
    parts = (
        "borrowings_current",
        "borrowings_noncurrent",
        "lease_liabilities_current",
        "lease_liabilities_noncurrent",
    )
    cur, non = run.get("borrowings_current"), run.get("borrowings_noncurrent")
    if not cur or not non or not all(p in held for p in parts):
        return
    if cur.status == "verified" or cur.base is None or non.base is None or not non.complete:
        return
    rows = cur.rows + non.rows
    total = sum((abs(held[p]) for p in parts), Decimal(0))
    if not _agrees(cur.base + non.base, total, scale, len(rows), [r.cells for r in rows], tol):
        return
    both = LineRead("debt_including_leases", "balance", rows=rows, held=total)
    both.current, both.base, both.decimals = cur.current + non.current, total, cur.decimals
    both.control = (
        "the two debt rows together equal the database's borrowings and lease liabilities at "
        "year end"
    )
    both.notes.append("the half-year balance sheet prints borrowings and leases as one row")
    run.lines = [x for x in run.lines if x.line not in parts] + [both]
    for p in parts:
        run.not_found[p] = "shown together with the other debt in the half-year balance sheet"


def _compare_with_database(x: LineRead, report, cells, scale, annual_docs, settings, tol) -> None:
    year = f"FY{report.base_fiscal_year}"
    if x.held is None:
        x.failures.append(f"the database holds no {year} figure to check this row against")
        return
    n = len(x.rows)
    if x.base is not None:
        what = "year-end column" if not x.is_flow else "full-year column"
        target = x.held if _signed(settings, x.line) else abs(x.held)
        if _agrees(x.base, target, scale, n, cells, tol):
            x.control = f"the report's {what} equals the database's {year} figure"
        else:
            x.failures.append(
                f"the report's {what} gives {_money(x.base, scale)}, the database holds "
                f"{_money(x.held, scale)} for {year}: another row, or a restated figure"
            )
        return
    if not x.is_flow:
        x.failures.append("no year-end column to compare with the database")
        return
    if annual_label_agrees([r.label for r in x.rows], x.held, annual_docs, settings):
        x.control = (
            f"the {year} annual report prints the database's figure "
            f"({_money(x.held, scale)}) under the same row label"
        )
    else:
        x.failures.append(
            f"the report prints no full year, and the {year} annual report does not print the "
            f"database's figure ({_money(x.held, scale)}) under this row label: the row cannot "
            "be confirmed"
        )


def _add_up(run: HalfYearRun, scale: Decimal, tol: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}

    def gap_ok(a: Decimal, b: Decimal, rows: list[RowRead]) -> bool:
        cells = [r.cells for r in rows]
        return abs(a - b) <= _unit(cells) * scale * (len(rows) + 1)

    assets, both = run.get("total_assets"), run.get("control_total_equity_and_liabilities")
    confirmed = (
        assets
        and both
        and both.base is not None
        and assets.held is not None
        and gap_ok(abs(both.base), abs(assets.held), both.rows)
    )  # the row is the balance sheet's second total: at year end it equals total assets
    if confirmed and assets.current is not None and both.current is not None:
        if not gap_ok(assets.current, abs(both.current), assets.rows + both.rows):
            out.setdefault("balance", []).append(
                f"total assets {_money(assets.current, scale)} do not equal total equity and "
                f"liabilities {_money(abs(both.current), scale)} at the half-year date"
            )
    start, moves, end = (run.get(f"control_cash_{k}") for k in ("start", "movements", "end"))
    cols = run.columns.get("cash_flow")
    if start and moves and end and cols:
        for column in ("current", "prior"):
            a, b, c = (getattr(x, column) for x in (start, moves, end))
            index = getattr(cols, column)
            if a is None or b is None or c is None or index is None:
                continue
            # The net change row may or may not already include the exchange-rate rows the
            # AI listed beside it: some set of those rows must bridge opening to closing.
            parts = [r.cells[len(r.cells) - cols.count + index].value * scale for r in moves.rows]
            sums = {
                sum(combo) for k in range(1, len(parts) + 1) for combo in combinations(parts, k)
            }
            b = min(sums, key=lambda s: abs(a + s - c))
            if not gap_ok(a + b, c, start.rows + moves.rows + end.rows):
                out.setdefault("cash_flow", []).append(
                    f"cash flow statement, {column} half: opening cash {_money(a, scale)} + "
                    f"movements {_money(b, scale)} do not give the closing cash "
                    f"{_money(c, scale)}"
                )
    return out


# --- One report --------------------------------------------------------------------------------


def base_label(issuer: Issuer, report: Report) -> str:
    month, day = (int(x) for x in issuer.fiscal_year_end.split("-"))
    end = date(report.base_fiscal_year, month, day)
    return f"FY{report.base_fiscal_year} (year ended {end.isoformat()})"


def held_figures(facts: list[MappedFact], year: int, settings: dict) -> dict[str, Decimal]:
    """The statement lines the database holds for the last full fiscal year."""
    return {
        f.line: f.value
        for f in facts
        if f.primary and f.fiscal_year == year and f.line in settings["lines"]
    }


def read_report(
    llm: LLM,
    issuer: Issuer,
    report: Report,
    facts: list[MappedFact],
    annual_docs: list[Document],
    settings: dict | None = None,
    folder: Path = DOCUMENT_DIR,
) -> HalfYearRun:
    settings = settings or load_settings()
    held = held_figures(facts, report.base_fiscal_year, settings)
    annual = [d for d in annual_docs if d.fiscal_year == report.base_fiscal_year]
    if report.read_by == "hand":
        return hand_run(report, held, settings)
    doc = document(report, folder)
    regions = find_statements(doc, settings)
    run = HalfYearRun(report, doc)
    if len(regions) < 3:
        run.error = "the three statements were not found in the report's text"
        return run
    message = user_message(issuer, report, doc, regions, held, settings, base_label(issuer, report))
    ids = [x for x in settings["lines"] if x in held] + list(settings["controls"])
    try:
        result = llm.call_tool(
            "extraction",
            system_prompt(),
            message,
            tool(ids),
            PROMPT_VERSION,
            label=f"{issuer.id} half year {report.id}",
        )
    except NotRecorded:
        run.error = NOT_RUN
        return run
    except LLMError as exc:
        run.error = str(exc)
        return run
    answer = result.arguments
    scale = SCALE_FACTORS.get(str(answer.get("scale")), Decimal(1_000_000))
    raw_lines, invalid, seen = [], [], set()
    for n, item in enumerate(answer.get("lines") or []):
        try:
            raw = RawLine.model_validate(item)
        except ValidationError as exc:
            invalid.append(f"line {n + 1}: {exc.errors()[0]['msg']}")
            continue
        if raw.line in seen or raw.line not in ids:
            invalid.append(f"line {n + 1}: '{raw.line}' given twice or not asked for")
            continue
        seen.add(raw.line)
        raw_lines.append(raw)
    run = check(report, doc, regions, raw_lines, held, annual, scale, settings)
    run.result, run.invalid = result, invalid + run.invalid
    for item in answer.get("not_found") or []:
        try:
            missing = RawMissing.model_validate(item)
        except ValidationError:
            continue
        if missing.line not in seen:
            run.not_found[missing.line] = missing.reason or "not on the face of the statements"
    for line in held:
        if line not in seen and line not in run.not_found:
            run.not_found[line] = "not given by the AI"
    apply_reviews(run)
    return run


# --- Entered by hand ---------------------------------------------------------------------------


def hand_run(report: Report, held: dict[str, Decimal], settings: dict, path: Path = ENTRIES):
    """Lines typed from the report's pages where the PDF gives no text for its figures. Each
    line: [first half, same half a year before, year-end or full-year column, page, label].
    The same controls against the database apply; unverified until Imane has reviewed."""
    run = HalfYearRun(report)
    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    entry = next((e for e in (data or {}).get("entries") or [] if e["report"] == report.id), None)
    if entry is None:
        run.error = "the report's figures are not available as text and are not entered yet"
        return run
    scale = Decimal(str(entry["scale"]))
    run.scale = scale
    tol = settings["tolerance"]
    unit = Decimal(str(entry.get("printed_unit", 1)))
    for line, (current, prior, base, page, label) in entry["lines"].items():
        spec = settings["lines"][line]
        x = LineRead(line, spec["statement"], held=held.get(line), manual=True)
        x.rows = [RowRead(label, "add", page - 1, None)]
        signed = bool(spec.get("signed"))

        def amount(raw, signed=signed):
            if raw is None:
                return None
            parts = raw if isinstance(raw, list) else [raw]
            total = sum((Decimal(str(p)) for p in parts), Decimal(0)) * scale
            return total if signed else abs(total)

        x.current, x.prior, x.base = amount(current), amount(prior), amount(base)
        x.decimals = -int(scale.log10()) + (-unit.as_tuple().exponent)
        year = f"FY{report.base_fiscal_year}"
        if x.held is None:
            x.failures.append(f"the database holds no {year} figure to check this row against")
        elif x.base is None:
            x.notes.append("the report prints no full-year column for this row")
        elif abs(x.base - (x.held if signed else abs(x.held))) <= (
            Decimal(str(tol["units_per_row"])) * unit * scale / 2
        ):
            what = "full-year column" if x.is_flow else "year-end column"
            x.control = f"the report's {what} equals the database's {year} figure"
        else:
            x.failures.append(
                f"the column entered gives {_money(x.base, scale)}, the database holds "
                f"{_money(x.held, scale)} for {year}"
            )
        if not entry.get("reviewed_by"):
            x.failures.append("entered by hand, not reviewed yet: waiting for Imane")
        else:
            x.notes.append(f"entered by hand, reviewed by {entry['reviewed_by']}")
        run.lines.append(x)
    for line in held:
        if run.get(line) is None:
            reasons = entry.get("not_found") or {}
            run.not_found[line] = reasons.get(line, "not on the face of the statements")
    apply_reviews(run)
    return run


# --- Imane's reviews ---------------------------------------------------------------------------


def load_reviews(path: Path = REVIEWS) -> list[dict]:
    if not path.exists():
        return []
    return (yaml.safe_load(path.read_text()) or {}).get("reviews") or []


def apply_reviews(run: HalfYearRun, reviews: list[dict] | None = None) -> None:
    """Approvals and corrections of flagged lines: `approve` shows the line as read, with the
    failed checks kept on record; `correct` replaces its values (in the report's printed
    unit) and marks it overridden. Each carries who, when and why."""
    for r in load_reviews() if reviews is None else reviews:
        if r["report"] != run.report.id:
            continue
        x = run.get(r["line"])
        if x is None:
            continue
        if r["action"] == "correct":
            for column in ("current", "prior"):
                if r.get(column) is not None:
                    setattr(x, column, Decimal(str(r[column])) * run.scale)
        elif r["action"] != "approve":
            raise ValueError("half_year_reviews.yaml: action must be approve or correct")
        x.review = r
        x.notes.append(f"{r['action']}d by {r['by']} on {r['on']}: {r['reason']}")


# --- Facts -------------------------------------------------------------------------------------


def to_facts(issuer: Issuer, run: HalfYearRun) -> list[MappedFact]:
    """One fact per line and period read: `H1` (the half just ended, or the half-year date)
    and `H1_prior` (the same half a year before). The period is carried in `rule_source`."""
    facts = []
    report = run.report
    models = {}
    if run.result is not None:
        models = {
            "provider": run.result.provider,
            "model": run.result.model,
            "prompt_version": run.result.prompt_version,
            "request_hash": run.result.request_hash,
        }
    for x in run.lines:
        if x.line.startswith("control_"):
            continue
        cols = run.columns.get(x.statement)
        ref = {
            "document": report.id,
            "document_title": report.document,
            "document_sha256": report.sha256,
            "source": report.file,
            "url": report.url,
            "audit": report.audit,
            "locations": [x.location],
            "rows": [{"label": r.label, "operation": r.operation, "text": r.text} for r in x.rows],
            "quotes": [" ".join(r.text.split()) for r in x.rows if r.text],
            "columns": dict(cols.labels) if cols else {},
            "column_method": list(cols.how) if cols else [],
            "report_base_column": None if x.base is None else str(x.base),
            "database_base_figure": None if x.held is None else str(x.held),
            "control": x.control,
            "checks_failed": list(x.failures),
            "notes": list(x.notes),
            "review": x.review,
            **models,
        }
        periods = [("H1", report.period_end, x.current)]
        if x.is_flow:
            periods.append(("H1_prior", report.prior_end, x.prior))
        for period, end, value in periods:
            if value is None:
                continue
            what = "entered by hand from" if x.manual else "read from"
            facts.append(
                MappedFact(
                    issuer=issuer.id,
                    fiscal_year=end.year,
                    period_end=end,
                    line=x.line,
                    value=value,
                    value_tagged=value,
                    decimals=x.decimals,
                    currency=issuer.currency,
                    filing_id=report.id,
                    comparative=period == "H1_prior",
                    concepts=tuple(r.label for r in x.rows),
                    fact_ids=(x.location,),
                    rule_source=period,
                    sign=1,
                    note=f"{'Six months' if x.is_flow else 'At'} to {end.isoformat()}, {what} "
                    f"the {report.audit} half-year report ({x.location})"
                    if x.is_flow
                    else f"At {end.isoformat()}, {what} the {report.audit} half-year report "
                    f"({x.location})",
                    warnings=tuple(x.failures),
                    source_type="manual" if x.manual else "extracted",
                    status=x.status,
                    ref=ref,
                )
            )
    return facts
