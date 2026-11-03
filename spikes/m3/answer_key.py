"""M3 answer key, read by code without AI (decision 0012), at Imane's request.

Kept apart from the tool on purpose:
- No AI, and none of the extraction code (no locator, no grounding checks, no number reader
  from `tearsheet.extract`). The report text is rebuilt here from the downloaded file with a
  plain tag stripper (web reports) or `pdftotext` (PDFs supplied by Imane).
- Each figure is found by a fixed anchor written by reading the report: the words printed
  around the figure, with the number captured. An anchor must match exactly once in the
  report, so a wrong or ambiguous anchor stops the build instead of guessing.
- Written before the AI was run on the reports, and not changed after seeing its answers.

    uv run python -m spikes.m3.answer_key

Writes docs/m3/answer_key.csv (one line per figure, with the printed number, its page and the
text around it, so that Imane can spot-check any line by searching the report for it).
Needs the reports in the local cache (`tearsheet load` downloads them).
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

import duckdb
import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "m3" / "answer_key.csv"
SCALES = {"one": 1, "thousand": 10**3, "million": 10**6, "billion": 10**9}
UNITS = {
    "passengers": "count",
    "ask": "count",
    "rpk": "count",
    "fleet_count": "count",
    "fuel_hedge_ratio": "pct",
    "undrawn_facilities": "amount",
}
PAGE_START = re.compile(
    r"<div\b[^>]*\bclass=\"[^\"]*\b(?:pageView|pf|page|pdf-page)\b[^\"]*\"", re.IGNORECASE
)
HIDDEN = re.compile(r"(?is)<(script|style|ix:header|head)\b[^>]*>.*?</\1\s*>")
TAG = re.compile(r"(?s)<[^>]+>")
SPACE = re.compile(r"[ \t\r\n   ]+")


@dataclass(frozen=True)
class Anchor:
    issuer: str
    fiscal_year: int  # the year the figure belongs to
    item: str
    document: str  # "report FY2024" (the filing's report) or a supplied PDF's id
    pattern: str  # regex on the report text (spaces collapsed); group "v" is the number
    scale: str = "one"  # what the printed number counts in
    language: str = "en"  # number format: en "1,234.5"; fr "1 234,5"
    currency: str | None = None  # amounts: currency printed, if not the reporting currency
    group: str = "first"  # "first": built before the first run; "holdout": before the second


def loose(text: str) -> str:
    """Regex for printed words in a report whose text layer splits words at random
    ('eas yJet ha s'): any spacing between the characters."""
    return r"\s*".join(re.escape(ch) for ch in text if not ch.isspace())


# --- Anchors ----------------------------------------------------------------------------------
# One per figure (two anchors for the same figure are added up). Written by reading each
# report, before the AI read it.

ANCHORS: list[Anchor] = [
    # Air France-KLM: the latest report with operating figures is the FY2024 universal
    # registration document (French). The FY2025 PDF Imane supplied holds the financial
    # statements only (no traffic). The group's total ASK and RPK are not printed as text
    # (only Réseaux and Transavia separately), and the fuel hedge is a policy ("68 % de la
    # consommation annuelle"), not a ratio at the year end: no key line for those.
    Anchor("afkl", 2024, "passengers", "report FY2024",
           r"(?P<v>\d+,\d) millions de passagers transportés en 2024 \(contre", "million", "fr"),
    Anchor("afkl", 2024, "fleet_count", "report FY2024",
           r"la flotte du groupe Air France-KLM comprend \d+ avions dont (?P<v>\d+) avions en "
           r"exploitation", language="fr"),
    Anchor("afkl", 2024, "undrawn_facilities", "report FY2024",
           r"\(incluant (?P<v>\d+,\d) milliards d’euros de lignes de crédit non tirées",
           "billion", "fr"),
    # IAG FY2025 annual report and accounts. No next-year hedge ratio is printed (only the
    # policy, "up to 75% of anticipated requirements in near-term").
    Anchor("iag", 2025, "passengers", "report FY2025",
           r"Passengers carried ‘000 (?P<v>\d{3},\d{3}) \d{3},\d{3}", "thousand"),
    Anchor("iag", 2025, "ask", "report FY2025",
           r"Available seat km \(ASK\) million (?P<v>\d{3},\d{3}) \d{3},\d{3}", "million"),
    Anchor("iag", 2025, "rpk", "report FY2025",
           r"Revenue passenger km \(RPK\) million (?P<v>\d{3},\d{3}) \d{3},\d{3}", "million"),
    Anchor("iag", 2025, "fleet_count", "report FY2025",
           r"Number of aircraft in service 2025 2024 .{0,120}?Total (?P<v>\d{3}) \d{3}"),
    Anchor("iag", 2025, "undrawn_facilities", "report FY2025",
           r"In total, the Group had € (?P<v>\d,\d{3}) million of committed and undrawn",
           "million"),
    # Finnair FY2025. The report's text layer splits words and numbers ("3 0 , 2 2 7. 3"),
    # so the table anchors use the neighbouring cells of the "Total" row. The hedge is printed
    # by half-year (79% for H1 2026, 51 per cent for H2): no key line. Fleet: the scope is all
    # aircraft operated for Finnair, so the key adds the two printed fleet totals (Finnair's
    # own operating certificate, 55, and Norra's contract flying, 24).
    Anchor("finnair", 2025, "passengers", "report FY2025",
           r"passengers incr eased by 2\.0% t o (?P<v>\d+,\d+ ?, ?\d+) passengers"),
    Anchor("finnair", 2025, "ask", "report FY2025",
           r"To t a l 2, 4 4 5\.8 2, 4 19\.0 (?P<v>\d\d,\d{3}\.\d) 38, 259\.3", "million"),
    Anchor("finnair", 2025, "rpk", "report FY2025",
           r"38, 259\.3 (?P<v>[\d ,.]+?) 29 ,000\.2 76\.9", "million"),
    Anchor("finnair", 2025, "fleet_count", "report FY2025",
           r"To t a l (?P<v>\d\d) \W?1 38 17 14 \. 3 1 \* Finnair’ s Air Operat or"),  # icon glyph
    Anchor("finnair", 2025, "fleet_count", "report FY2025",
           r"Embr aer E190 100 12 - 9 3 17 \.5 - To t a l (?P<v>\d\d) - 15 9"),
    Anchor("finnair", 2025, "undrawn_facilities", "report FY2025",
           r"Revolving credit facility of (?P<v>\d+) million euros was undrawn on 31 December",
           "million"),
    # easyJet FY2025 (year to 30 September 2025). The hedge is printed by half-year ("80%
    # hedged for H1 FY26", "c.54% hedged for H2 FY26"), not for the next twelve months: no
    # key line. The text converter of the report splits some words and numbers ("122 ,02 1").
    Anchor("easyjet", 2025, "passengers", "report FY2025",
           r"passengers carried in the year increased by 4% to (?P<v>\d+\.\d) million \(2024",
           "million"),
    Anchor("easyjet", 2025, "ask", "report FY2025",
           r"\(A SK\) increasing by 9% to (?P<v>\d{3},\d{3}) million \(2024", "million"),
    Anchor("easyjet", 2025, "rpk", "report FY2025",
           r"\(RPK \) \( millions \) (?P<v>\d+ ?,\d+ ?\d*) \d", "million"),
    Anchor("easyjet", 2025, "fleet_count", "report FY2025",
           r"giving a total fleet of (?P<v>\d+) at 30 September 2025"),
    Anchor("easyjet", 2025, "undrawn_facilities", "report FY2025",
           r"easy ?Jet issued a \$(?P<v>\d\.\d) billion RCF which is undrawn at 30 September",
           "billion", currency="USD"),
    # Norwegian FY2025. ASK and RPK are printed per airline (Norwegian, Widerøe), not for the
    # group, and no undrawn facility is given: no key line for those.
    Anchor("norwegian", 2025, "passengers", "report FY2025",
           r"The Norwegian Group welcomed a total of (?P<v>\d+\.\d) million passengers in 2025",
           "million"),
    Anchor("norwegian", 2025, "fleet_count", "report FY2025",
           r"contributing to a total group fleet of (?P<v>\d+) aircraft"),
    Anchor("norwegian", 2025, "fuel_hedge_ratio", "report FY2025",
           r"At the end of 2025, the group had hedged approximately (?P<v>\d+) percent of the "
           r"estimated fuel consumption for 2026"),
    # Wizz Air FY2026 (year to 31 March 2026). The hedge is printed by half-year (F27 H1 84 %,
    # F27 H2 71 %), and no undrawn facility is given: no key line for those.
    Anchor("wizz", 2026, "passengers", "report FY2026",
           r"We carried (?P<v>\d+\.\d) million passengers, up 10 per cent", "million"),
    Anchor("wizz", 2026, "ask", "report FY2026",
           r"Total ASKs \(’000 km\) (?P<v>\d{3},\d{3},\d{3}) \d", "thousand"),
    Anchor("wizz", 2026, "rpk", "report FY2026",
           r"RPKs \(revenue passenger kilometres\) \(’000 km\) (?P<v>\d{3},\d{3},\d{3}) \d",
           "thousand"),
    Anchor("wizz", 2026, "fleet_count", "report FY2026",
           r"Its fleet consists of (?P<v>\d+) aircraft"),
]  # fmt: skip

# Held-out lines (decision 0014), written before the second run (prompt extract-v2) and scored
# apart, so that the improvement round is not judged only on the lines that guided it. Same
# rule: every one of the six figures printed as one number on the scope wanted, in each
# airline's report for the year before (Air France-KLM: FY2022, its other report with
# operating figures). Left out, with the reason:
# - Air France-KLM FY2022 passengers ("plus de 83 millions": a lower bound) and group ASK (the
#   row "Capacités produites exprimées en SKO 282 826" prints no unit); no group RPK.
# - IAG FY2024 RPK (not printed in this version of the report) and hedge (policy only).
# - Finnair FY2024 fleet (only as pie-chart labels) and hedge (per half-year).
# - easyJet FY2024 hedge (per half-year). Wizz Air FY2025 hedge (10 months, then 8 months).
# - Norwegian FY2024 ASK and RPK (per airline only) and undrawn facilities (none given).
HOLDOUT: list[Anchor] = [
    Anchor("afkl", 2022, "fleet_count", "report FY2022",
           r"la flotte du Groupe Air France-KLM comprend \d+ avions \(dont (?P<v>\d+) avions en "
           r"exploitation\)", language="fr", group="holdout"),
    Anchor("afkl", 2022, "fuel_hedge_ratio", "report FY2022",  # the 2023 column (next year)
           r"\(en millions de dollars US\) 2022 2023 2024 Dépense brute avant couverture .{0,40}?"
           r"Pourcentage de couverture \d+ % (?P<v>\d+) % \d+ %", language="fr", group="holdout"),
    Anchor("afkl", 2022, "undrawn_facilities", "report FY2022",
           r"et (?P<v>\d,\d) milliards d'euros de lignes de crédit non tirées \(voir Notes",
           "billion", "fr", group="holdout"),
    Anchor("iag", 2024, "passengers", "report FY2024",
           r"countries (?P<v>\d+) million passengers [\d,]+ employees", "million", group="holdout"),
    Anchor("iag", 2024, "ask", "report FY2024",
           r"ASKs \(millions\) (?P<v>\d{3},\d{3}) – \d{3},\d{3} \d{3},\d{3}", "million",
           group="holdout"),
    Anchor("iag", 2024, "fleet_count", "report FY2024",
           r"Number of fleet in-service 2024 2023 .{0,90}?% (?P<v>\d{3}) \d{3} [\d.]+ %",
           group="holdout"),
    Anchor("iag", 2024, "undrawn_facilities", "report FY2024",
           r"In total, the Gr ?oup had € (?P<v>\d,\d{3}) million of committed and undrawn",
           "million", group="holdout"),
    Anchor("finnair", 2024, "passengers", "report FY2024",
           r"Finnair transported (?P<v>\d+\.\d) million passengers \(11\.0\)", "million",
           group="holdout"),
    Anchor("finnair", 2024, "ask", "report FY2024",
           r"T ota l 2, 419 \. 0 2 , 4 1 1\.6 (?P<v>[\d ,.]+?) 36, 154\.5", "million",
           group="holdout"),
    Anchor("finnair", 2024, "rpk", "report FY2024",
           r"36, 154\.5 (?P<v>[\d ,.]+?) 27 ,62 6\. 4", "million", group="holdout"),
    Anchor("finnair", 2024, "undrawn_facilities", "report FY2024",
           r"Revolving credit facility of (?P<v>\d+) million euro was undrawn on 31 December 2024",
           "million", group="holdout"),
    Anchor("easyjet", 2024, "passengers", "report FY2024",
           loose("in the financial year increased by 8% to") + r"\s*(?P<v>[\d ]+\.\s?\d)\s*"
           + loose("million (2023:"), "million", group="holdout"),
    Anchor("easyjet", 2024, "ask", "report FY2024",
           loose("(ASK) (millions)") + r"\s*(?P<v>[\d ]+,[\d ]+?)\s+113,33 4", "million",
           group="holdout"),
    Anchor("easyjet", 2024, "rpk", "report FY2024",
           loose("(RPK) (millions)") + r"\s*(?P<v>[\d ]+,[\d ]+?)\s+10 2 ,984", "million",
           group="holdout"),
    Anchor("easyjet", 2024, "fleet_count", "report FY2024",
           loose("giving a total fleet of") + r"\s*(?P<v>[\d ]+?)\s*" + loose("at 30 September"),
           group="holdout"),
    Anchor("easyjet", 2024, "undrawn_facilities", "report FY2024",
           loose("This amounted to £") + r"\s*(?P<v>\d\s?\.\s?\d)\s*" + loose("billion at 30"),
           "billion", group="holdout"),
    Anchor("norwegian", 2024, "passengers", "report FY2024",
           loose("The Norwegian Group had") + r"\s*(?P<v>\d+\.\s?\d)\s*"
           + loose("million passengers in 2024 , up 28"), "million", group="holdout"),
    Anchor("norwegian", 2024, "fleet_count", "report FY2024",
           loose("The fleet for the Norwegian Group comprised of") + r"\s*(?P<v>\d+)\s*"
           + loose("aircraft at year-end"), group="holdout"),
    Anchor("norwegian", 2024, "fuel_hedge_ratio", "report FY2024",
           loose("the Group has hedged around") + r"\s*(?P<v>\d+)\s*"
           + loose("per cent of its planned fuel consumption in 2025"), group="holdout"),
    Anchor("wizz", 2025, "passengers", "report FY2025",
           r"carried a record (?P<v>\d+\.\d) million passengers \( F24", "million",
           group="holdout"),
    Anchor("wizz", 2025, "ask", "report FY2025",
           r"Total ASKs \(’000 km\) (?P<v>\d{3},\d{3},\d{3}) \d", "thousand", group="holdout"),
    Anchor("wizz", 2025, "rpk", "report FY2025",
           r"RPKs \(revenue passenger kilometres\) \(’000 km\) (?P<v>\d{3},\d{3},\d{3}) \d",
           "thousand", group="holdout"),
    Anchor("wizz", 2025, "fleet_count", "report FY2025",
           r"Its fleet consists of (?P<v>\d+) aircraft", group="holdout"),
]  # fmt: skip


# --- Text ------------------------------------------------------------------------------------


def html_pages(html: str) -> list[str]:
    marked = PAGE_START.sub(lambda m: "\f" + m.group(0), html)
    text = TAG.sub(" ", HIDDEN.sub(" ", marked))
    pages = [SPACE.sub(" ", unescape(p)).strip() for p in text.split("\f")]
    if pages and not pages[0]:
        pages = pages[1:]
    return pages or [""]


def pdf_pages(path: Path) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        txt = Path(tmp) / "out.txt"
        subprocess.run(["pdftotext", str(path), str(txt)], check=True, capture_output=True)
        raw = txt.read_text()
    return [SPACE.sub(" ", p).strip() for p in raw.split("\f")]


# --- Numbers ---------------------------------------------------------------------------------


def number(printed: str, language: str) -> tuple[Decimal, int]:
    """The printed number and its count of decimal places ("98,0" in French = 98.0, 1)."""
    s = printed.strip().replace(" ", " ").replace(" ", " ")
    if language == "en":
        s = s.replace(",", "").replace(" ", "")
    else:
        s = s.replace(" ", "").replace(".", "").replace(",", ".")
    if not re.fullmatch(r"\d+(?:\.\d+)?", s):
        raise ValueError(f"not a plain number: {printed!r}")
    places = len(s.split(".")[1]) if "." in s else 0
    return Decimal(s), places


def full_value(printed: str, a: Anchor) -> tuple[Decimal, Decimal]:
    """Value in full units (fractions for percentages) and half a unit of the last digit."""
    value, places = number(printed, a.language)
    half = Decimal(5) / Decimal(10) ** (places + 1)
    if UNITS[a.item] == "pct":
        return value / 100, half / 100
    if a.scale == "one" and places == 0:
        return value, Decimal(0)  # a count of aircraft or passengers is exact
    factor = Decimal(SCALES[a.scale])
    return value * factor, half * factor


def find(pages: list[str], pattern: str) -> tuple[re.Match, int]:
    """The single match of the anchor, and its page (1-based)."""
    regex = re.compile(pattern)
    hits = [(m, i + 1) for i, p in enumerate(pages) for m in regex.finditer(p)]
    if len(hits) != 1:
        raise LookupError(f"anchor matches {len(hits)} times, not once: {pattern}")
    return hits[0]


# --- Sources ---------------------------------------------------------------------------------


def report_path(url: str) -> Path:
    """Where `tearsheet load` cached the report (same naming as the download cache)."""
    from tearsheet.ingest.client import FILINGS_BASE, Client

    full = urljoin(FILINGS_BASE, url)
    suffix = Path(full.split("?")[0]).suffix or ".bin"
    return Client(offline=True)._cache_path("report", full, None, suffix)


def documents() -> dict[tuple[str, str], tuple[str, Path, str, date]]:
    """(issuer, document) -> (document id, file, kind, period end)."""
    con = duckdb.connect(str(ROOT / "data" / "tearsheet.duckdb"), read_only=True)
    rows = con.execute(
        "SELECT issuer, fiscal_year, filing_id, report_url, period_end FROM filings "
        "WHERE report_url IS NOT NULL"
    ).fetchall()
    con.close()
    out = {}
    for issuer, year, filing_id, url, end in rows:
        out[(issuer, f"report FY{year}")] = (filing_id, report_path(url), "html", end)
    supplied = yaml.safe_load((ROOT / "config" / "report_documents.yaml").read_text())
    for d in supplied["documents"]:
        end = date(int(d["fiscal_year"]), 12, 31)
        out[(d["issuer"], d["id"])] = (d["id"], ROOT / "documents" / d["file"], "pdf", end)
    return out


def ecb_rate(source: str, target: str, period_end: date) -> Decimal:
    """ECB end-of-month reference rate, target per source (decision 0002)."""
    from tearsheet.ingest.client import Client

    def per_eur(currency: str) -> Decimal:
        if currency == "EUR":
            return Decimal(1)
        text = Client().ecb_series("EXR", f"M.{currency}.EUR.SP00.E", "2020-01")
        month = f"{period_end.year}-{period_end.month:02d}"
        for row in csv.DictReader(text.splitlines()):
            if row.get("TIME_PERIOD") == month and row.get("OBS_VALUE"):
                return Decimal(row["OBS_VALUE"])
        raise KeyError(f"no ECB {currency} rate for {month}")

    return per_eur(target) / per_eur(source)


# --- Build -----------------------------------------------------------------------------------


def build(anchors: list[Anchor] | None = None, out: Path = OUT) -> list[dict]:
    anchors = ANCHORS + HOLDOUT if anchors is None else anchors
    from tearsheet.config import load_issuers

    currency = {i.id: i.currency for i in load_issuers()}
    docs = documents()
    texts: dict[str, list[str]] = {}
    rows: dict[tuple[str, int, str], dict] = {}
    for a in anchors:
        doc_id, path, kind, end = docs[(a.issuer, a.document)]
        if doc_id not in texts:
            texts[doc_id] = pdf_pages(path) if kind == "pdf" else html_pages(path.read_text())
        m, page = find(texts[doc_id], a.pattern)
        value, tolerance = full_value(m.group("v"), a)
        if a.currency and a.currency != currency[a.issuer]:
            rate = ecb_rate(a.currency, currency[a.issuer], end)
            value, tolerance = value * rate, tolerance * rate
        text = texts[doc_id][page - 1]
        snippet = text[max(0, m.start() - 120) : m.end() + 60]
        key = (a.issuer, a.fiscal_year, a.item)
        printed = f"{m.group('v')}" + ("" if a.scale == "one" else f" {a.scale}")
        if a.currency:
            printed += f" {a.currency}"
        if key in rows:  # a further component of the same figure
            row = rows[key]
            row["value"] += value
            row["tolerance"] += tolerance
            row["printed"] += f" + {printed}"
            row["location"] += f"; page {page}"
            row["snippet"] += f" || {snippet}"
            continue
        rows[key] = {
            "issuer": a.issuer,
            "fiscal_year": a.fiscal_year,
            "item": a.item,
            "unit": UNITS[a.item],
            "value": value,
            "tolerance": tolerance,
            "printed": printed,
            "document": doc_id,
            "location": f"page {page}",
            "snippet": snippet,
            "set": a.group,
        }
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["issuer", "fiscal_year", "item", "unit", "value", "tolerance", "printed",
              "document", "location", "snippet", "set"]  # fmt: skip
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for row in rows.values():
            w.writerow(row | {"value": _plain(row["value"]), "tolerance": _plain(row["tolerance"])})
    return list(rows.values())


def _plain(d: Decimal) -> str:
    q = d.quantize(Decimal("0.000001")) if d != d.to_integral() else d.to_integral()
    return f"{q.normalize():f}"


def main() -> None:
    rows = build()
    print(f"answer key: {len(rows)} figures -> {OUT.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
