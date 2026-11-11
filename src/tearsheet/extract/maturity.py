"""The debt maturity wall (M8, decision 0022): when the debt falls due, read from the debt note.

Maturity tables sit in the notes, which ESEF tags only as blocks of text, so the AI reads them,
as it reads the traffic figures (M3). It answers through a fixed form: per table, the layer
(borrowings or leases), the basis (principal, carrying amount, or contractual cash flows with
interest), the caption, and for each column its label, its value and the exact row quote.

Nothing is trusted on the model's word. Code checks, per table:
  1. the caption and every quote are in the report word for word (spaces ignored), the quotes
     on the caption's page or the next one; the scale and the currency are shown;
  2. every value is printed in its quote, next to its column label (in the quote or in the
     table's header line), and, where the row shows years, in the fiscal year's column;
  3. code, not the AI, turns each column label into a time span ("1-2 years", "2027", "plus
     de 5 ans"), and the spans must cover the whole debt: from today, without gaps, to an
     open end;
  4. the table must foot: the columns add up to the total printed in the same table;
  5. the table must agree with the balance sheet: the first bucket with the tagged current
     debt, the total with the tagged debt of that layer (tolerances in maturity.yaml).
A table that fails any check stays unverified, with every reason kept, and off the page.

The wall is shown in four standard buckets (within 1 year, 1 to 2, 2 to 5, over 5 years);
narrower columns are added into them, and a column that straddles a boundary merges the
buckets it spans.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ValidationError

from tearsheet.config import Issuer
from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import DocumentIndex, _locate_value, _table_year, attached_year
from tearsheet.extract.locator import Window, _merge_and_cap, find_terms
from tearsheet.extract.numbers import (
    CURRENCY_WORDS,
    SCALE_FACTORS,
    Token,
    contains_any,
    decimals_of,
    number_tokens,
    parse_number,
    scale_named,
    squash,
    year_marks,
)
from tearsheet.llm import LLM, LLMError, NotRecorded, ToolResult, ToolSpec
from tearsheet.normalize.mapper import MappedFact

HERE = Path(__file__).parent
CONFIG = HERE / "maturity.yaml"
PROMPT_VERSION = "maturity-v1"  # bump with every change to the prompt, the form or the request
NOT_RUN = "maturity tables not read yet: no recorded AI answer (run `tearsheet extract`)"
BEFORE, AFTER = 400, 2200  # a maturity table follows its title: keep more text after a hit
WINDOWS = 12
MAX_CHARS = 40_000
MAX_QUOTE = 400
LAYERS = ("borrowings", "leases")
BASES = ("principal", "carrying_amount", "contractual_cash_flows")
DASHES = {"-", "–", "—", "−", "_"}
OPEN = None  # an open-ended span ("more than five years")


def load_config(path: Path = CONFIG) -> dict:
    return yaml.safe_load(path.read_text())


# --- Column labels to time spans (code, not the AI) ------------------------------------------

WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "twelve": 12, "un": 1, "une": 1, "deux": 2, "trois": 3,
    "quatre": 4, "cinq": 5, "dix": 10, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "diez": 10, "ein": 1, "einem": 1, "eins": 1, "zwei": 2, "drei": 3, "vier": 4,
    "fünf": 5, "zehn": 10,
}  # fmt: skip
UNDER = (
    r"less than|within|up to|under|below|not later than|no later than|moins d[e']|"
    r"à moins d[e']|inférieur(?:e|es|s)? à|jusqu'à|menos de|hasta|inferior a|"
    r"bis(?: zu)?|unter|innerhalb(?: von)?|kleiner als|weniger als|<|≤"
)
OVER = (
    r"more than|over|after|beyond|later than|greater than|thereafter|plus de|"
    r"au-delà de|au delà de|supérieur(?:e|es|s)? à|après|más de|superior a|posterior a|über|"
    r"mehr als|nach|später als|>|≥"
)
UNIT_YEARS = r"\b(?:years?|yrs?|ans?|années?|años?|año|jahren?|jahre?)\b"
UNIT_MONTHS = r"\b(?:months?|mois|meses|mes|monaten?|monate)\b"


@dataclass(frozen=True)
class Span:
    start: Decimal  # years from the fiscal year end
    end: Decimal | None  # None: open-ended

    def label(self) -> str:
        return bucket_label(self.start, self.end)


def _num(text: str) -> Decimal | None:
    text = text.strip().lower()
    if text in WORD_NUMBERS:
        return Decimal(WORD_NUMBERS[text])
    if re.fullmatch(r"\d+(?:[.,]\d+)?", text):
        return Decimal(text.replace(",", "."))
    return None


NUM = r"(\d+(?:[.,]\d+)?|" + "|".join(sorted(WORD_NUMBERS, key=len, reverse=True)) + ")"


def parse_label(label: str, fiscal_year_end: date) -> Span | None:
    """The time span a column label covers, in years from the fiscal year end, or None if the
    label can't be read safely. Examples: 'Less than 1 year' -> 0 to 1; '1-2 years' -> 1 to 2;
    'Plus de 5 ans' -> 5 onwards; '2027' (year end Dec 2025) -> 1 to 2; 'N+1' -> 0 to 1."""
    raw = " ".join(label.replace("\n", " ").split())
    text = raw.lower().replace("–", "-").replace("—", "-").replace("’", "'")
    text = re.sub(r"\s+", " ", text).strip(" :")
    if not text:
        return None
    # Relative years: N+1, N+2 à N+5, au-delà de N+5 / > N+5 (French), Y+1 (English)
    rel = re.findall(r"(?<![a-z])[ny]\s*\+\s*(\d+)", text)  # N+1 (French), Y+1 (English)
    if rel:
        values = [int(v) for v in rel]
        if re.search(OVER, text) and len(values) == 1:
            return Span(Decimal(values[0]), OPEN)
        if len(values) == 1:
            return Span(Decimal(values[0] - 1), Decimal(values[0]))
        if len(values) == 2:
            return Span(Decimal(values[0] - 1), Decimal(values[1]))
        return None
    # Calendar years (only for a December year end, where a year column is a fiscal year).
    years = [int(m) for m in re.findall(r"(?<!\d)(20[2-6]\d)(?!\d)", text)]
    if years:
        if fiscal_year_end.month != 12 or len(years) > 2:
            return None
        base = fiscal_year_end.year
        first = Decimal(years[0] - base - 1)
        if first < 0:
            return None
        if len(years) == 2:
            return Span(first, Decimal(years[1] - base))
        onwards = (
            r"and (?:after|beyond|later|onwards|thereafter)|onwards|\+|"
            r"et (?:au-delà|après|suivantes?)|y (?:siguientes|posteriores)|ff\.?|und später"
        )
        if re.search(OVER, text) and not re.search(onwards, text):
            return Span(Decimal(years[0] - base), OPEN)  # "beyond 2030" starts after 2030
        if re.search(onwards, text) or re.search(r"\bab\b", text):
            return Span(first, OPEN)  # "2031 and after", "ab 2031"
        return Span(first, first + 1)
    scale = Decimal(1)
    if re.search(UNIT_MONTHS, text) and not re.search(UNIT_YEARS, text):
        scale = Decimal(1) / Decimal(12)
    elif not re.search(UNIT_YEARS, text) and not re.search(r"\d\s*\+|\+\s*\d", text):
        return None  # a number without a unit: not a time span we can read safely
    nums = [_num(n) for n in re.findall(NUM, text)]
    nums = [n for n in nums if n is not None]
    if "+" in text and len(nums) == 1 and not re.search(UNDER, text):
        return Span(nums[0] * scale, OPEN)  # "5+ years", "+5 years"
    between = r"between|entre|from|de |von|-|to | à | a | y | und | bis "
    if len(nums) == 2 and re.search(between, text):
        lo, hi = sorted(nums)
        return Span(lo * scale, hi * scale)
    if len(nums) == 1:
        n = nums[0] * scale
        if re.search(UNDER, text):
            return Span(Decimal(0), n)
        if re.search(OVER, text):
            return Span(n, OPEN)
    return None


LATER = re.compile(
    r"^(?:later|thereafter|after|beyond|subsequent(?: years)?|and after|plus tard|au-delà|"
    r"ultérieurement|posteriores?|más adelante|siguientes|años siguientes|resto|später|danach|"
    r"thereafter years)$"
)


def parse_labels(labels: list[str], fiscal_year_end: date) -> list[Span | None]:
    """Each label read on its own, except a bare 'Later' or 'Thereafter', which starts where
    the column before it ends ('2030', 'Later' -> 5 years onwards)."""
    spans: list[Span | None] = []
    for label in labels:
        span = parse_label(label, fiscal_year_end)
        text = " ".join(label.lower().split()).strip(" :")
        if span is None and LATER.match(text) and spans and spans[-1] is not None:
            if spans[-1].end is not None:
                span = Span(spans[-1].end, OPEN)
        spans.append(span)
    return spans


def bucket_id(start: Decimal, end: Decimal | None) -> str:
    def f(v: Decimal) -> str:
        return str(int(v)) if v == int(v) else str(v)

    return f"{f(start)}_plus" if end is None else f"{f(start)}_{f(end)}"


def bucket_label(start: Decimal, end: Decimal | None) -> str:
    def f(v: Decimal) -> str:
        return str(int(v)) if v == int(v) else f"{v:.1f}"

    if end is None:
        return f"over {f(start)} years"
    if start == 0:
        return f"within {f(end)} year" + ("" if end == 1 else "s")
    return f"{f(start)} to {f(end)} years"


def standard_buckets(
    columns: list[tuple[Span, Decimal]], boundaries: list[int]
) -> list[tuple[Decimal, Decimal | None, Decimal]]:
    """Add the columns into the standard buckets; a column straddling a boundary merges the
    buckets it spans. Returns (start, end, amount) in order."""
    edges = [Decimal(b) for b in boundaries] + [None]
    std = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    group = list(range(len(std)))  # each standard bucket's group (merged buckets share one)

    def index(point: Decimal, is_end: bool) -> int:
        for i, (_, hi) in enumerate(std):
            if is_end:
                if hi is None or point <= hi:
                    return i
            elif hi is None or point < hi:
                return i
        return len(std) - 1

    for span, _ in columns:
        first = index(span.start, False)
        last = len(std) - 1 if span.end is None else index(span.end, True)
        for i in range(first + 1, last + 1):
            old, new = group[i], group[first]
            group = [new if g == old else g for g in group]
    totals: dict[int, Decimal] = {}
    for span, value in columns:
        g = group[index(span.start, False)]
        totals[g] = totals.get(g, Decimal(0)) + value
    out = []
    for g in sorted(set(group)):
        members = [i for i, gg in enumerate(group) if gg == g]
        out.append((std[members[0]][0], std[members[-1]][1], totals.get(g, Decimal(0))))
    return out


def covers_everything(spans: list[Span]) -> str | None:
    """None if the spans run from today, without gap or overlap, to an open end."""
    ordered = sorted(spans, key=lambda s: s.start)
    if not ordered or ordered[0].start != 0:
        return "the columns do not start at the fiscal year end"
    for a, b in zip(ordered, ordered[1:], strict=False):
        if a.end is None or a.end != b.start:
            return f"the columns '{a.label()}' and '{b.label()}' leave a gap or overlap"
    if ordered[-1].end is not None:
        return f"the last column ends at {ordered[-1].end} years: the debt beyond is missing"
    return None


# --- The form ----------------------------------------------------------------------------------


class RawCell(BaseModel):
    label: str
    printed_value: str
    quote: str


class RawRow(BaseModel):
    """One row of the layer: the table's total row, or one of several rows that make up the
    layer when the table prints no subtotal (bank loans, bonds, asset financing...)."""

    name: str
    columns: list[RawCell]
    total: RawCell


class RawTable(BaseModel):
    layer: Literal["borrowings", "leases"]
    basis: Literal["principal", "carrying_amount", "contractual_cash_flows"]
    fiscal_year: int
    caption: str
    header: str | None = None
    scale: Literal["one", "thousand", "million", "billion"] = "million"
    currency: str | None = None
    rows: list[RawRow]
    location: str | None = None
    comment: str | None = None

    @property
    def cells(self) -> list[RawCell]:
        return [c for r in self.rows for c in r.columns + [r.total]]


def tool(max_tables: int) -> ToolSpec:
    cell = {
        "type": "object",
        "properties": {
            "label": {"type": "string", "description": "Column or row label, verbatim."},
            "printed_value": {"type": "string", "description": "The number as printed."},
            "quote": {
                "type": "string",
                "description": "The table row holding the value, verbatim, with its label.",
            },
        },
        "required": ["label", "printed_value", "quote"],
    }
    table = {
        "type": "object",
        "properties": {
            "layer": {"type": "string", "enum": list(LAYERS)},
            "basis": {"type": "string", "enum": list(BASES)},
            "fiscal_year": {"type": "integer"},
            "caption": {
                "type": "string",
                "description": "Title or unit line printed just above the table, verbatim.",
            },
            "header": {
                "type": "string",
                "description": "The header line with the column labels, verbatim.",
            },
            "scale": {"type": "string", "enum": ["one", "thousand", "million", "billion"]},
            "currency": {"type": "string", "description": "ISO code."},
            "rows": {
                "type": "array",
                "description": "The layer's total row; or, if the table has no subtotal for "
                "the layer, each of the rows that make it up.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Row label, verbatim."},
                        "columns": {"type": "array", "items": cell},
                        "total": cell,
                    },
                    "required": ["name", "columns", "total"],
                },
            },
            "location": {"type": "string"},
            "comment": {"type": "string"},
        },
        "required": ["layer", "basis", "fiscal_year", "caption", "rows"],
    }
    return ToolSpec(
        name="record_maturity_tables",
        description="Record each debt maturity table with its exact quotes, or none if absent.",
        schema={
            "type": "object",
            "properties": {"tables": {"type": "array", "maxItems": max_tables, "items": table}},
            "required": ["tables"],
        },
    )


def system_prompt(version: str = PROMPT_VERSION) -> str:
    return (HERE / "prompts" / f"{version.replace('-', '_')}.md").read_text()


def passages(doc: Document, config: dict) -> str:
    """The windows around maturity words that hold the most numbers and bucket words."""
    terms = list(config["terms"].get(doc.language or "en", []))
    terms += [t for t in config["terms"]["en"] if t not in terms]
    candidates = []
    for p, page in enumerate(doc.pages):
        for pos, _ in find_terms(page, terms):
            start = page.rfind("\n", 0, max(0, pos - BEFORE)) + 1
            end = page.find("\n", min(len(page), pos + AFTER))
            end = len(page) if end < 0 else end
            text = page[start:end]
            distinct = len({t for _, t in find_terms(text, terms)})
            numbers = len(number_tokens(text, doc.language))
            years = {m.year for m in year_marks(text)}
            score = 2 * distinct + min(numbers, 40) / 5 + (3 if doc.fiscal_year in years else 0)
            score += (
                4
                if re.search(
                    r"borrowing|debt|emprunt|dette|deuda|préstamo|Finanzverbindlich|Anleihe|bond|loan|lease|location|arrendamiento|Leasing",
                    text,
                    re.I,
                )
                else 0
            )  # noqa: E501
            candidates.append(Window(p, start, end, score, {"maturity"}))
    candidates.sort(key=lambda w: -w.score)
    kept: list[Window] = []
    for w in candidates:
        if len(kept) == WINDOWS:
            break
        if any(k.page == w.page and k.start < w.end and w.start < k.end for k in kept):
            continue
        kept.append(w)
    windows = _merge_and_cap(kept)
    total, chosen = 0, []
    for w in sorted(windows, key=lambda w: -w.score):
        if total + (w.end - w.start) > MAX_CHARS:
            continue
        chosen.append(w)
        total += w.end - w.start
    chosen.sort(key=lambda w: (w.page, w.start))
    return "\n\n".join(
        f"=== {doc.location(w.page)} ===\n{doc.pages[w.page][w.start : w.end].strip()}"
        for w in chosen
    )


def user_message(issuer: Issuer, doc: Document, text: str, label: str) -> str:
    scope = (
        "This company's balance sheet counts lease liabilities inside borrowings: for the "
        "borrowings layer, take the table that includes them."
        if issuer.leases_in_borrowings
        else "This company's balance sheet shows lease liabilities apart from borrowings: for "
        "the borrowings layer, take the table without them."
    )
    return "\n".join(
        [
            f"Company: {issuer.name} ({issuer.type}). Reporting currency: {issuer.currency}.",
            scope,
            f"Report: annual report for {label}, language: {doc.language or 'en'}.",
            f"Fiscal year wanted: FY{doc.fiscal_year} only (the tables at the fiscal year end "
            "of this report, not the prior-year comparatives).",
            "",
            "Passages from the report:",
            "",
            text,
        ]
    )


# --- The checks --------------------------------------------------------------------------------


@dataclass
class CheckedTable:
    raw: RawTable
    doc: Document
    columns: list[tuple[Span, Decimal]] = field(default_factory=list)
    total: Decimal | None = None
    decimals: int | None = None
    location: str | None = None
    buckets: list[tuple[Decimal, Decimal | None, Decimal]] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    review: dict | None = None

    @property
    def verified(self) -> bool:
        return self.total is not None and not self.failures

    @property
    def layer(self) -> str:
        return self.raw.layer

    @property
    def status(self) -> str:
        if self.review is not None:
            return "overridden"
        return "verified" if self.verified else "unverified"


def _value(cell: RawCell, language: str | None) -> Decimal | None:
    """The amount, as a positive figure: maturity tables often print payments as outflows,
    in brackets or with a minus sign."""
    printed = cell.printed_value.strip()
    if printed in DASHES or printed in ("0", "nil", "néant"):
        return Decimal(0)
    number = parse_number(printed.strip("()").lstrip("-−–"), language)
    return None if number is None else abs(number)


def squash_find(text: str, label: str) -> int | None:
    """Where the label ends in the text, ignoring spaces (None if it is not there)."""
    target = squash(label)
    if not target:
        return None
    flat, index = [], []
    for i, ch in enumerate(text):
        if not ch.isspace():
            flat.append(squash(ch) or ch)
            index.append(i)
    joined = "".join(flat)
    at = joined.find(target)
    if at < 0:
        return None
    return index[at + len(target) - 1] + 1


def _check_cell(
    cell: RawCell,
    index: DocumentIndex,
    header: str,
    pages: list[int],
    doc: Document,
    what: str,
    total: bool = False,
) -> tuple[Decimal | None, list[str]]:
    failures = []
    if len(cell.quote) > MAX_QUOTE:
        return None, [f"{what}: quote longer than {MAX_QUOTE} characters"]
    quote_pages = index.pages_of(cell.quote)
    if not quote_pages:
        return None, [f"{what}: quote not found word for word in the report"]
    if pages and not any(0 <= q - p <= 1 for q in quote_pages for p in pages):
        failures.append(f"{what}: quote is not on the caption's page or the next one")
    # A total row is often printed without a label; its value is checked by the foot instead
    # (fix after the first run).
    in_text = squash(cell.label) in squash(cell.quote) or squash(cell.label) in squash(header)
    if not total and not in_text:
        failures.append(f"{what}: label '{cell.label}' is not in the quote or the header")
    value = _value(cell, doc.language)
    if value is None:
        return None, failures + [f"{what}: '{cell.printed_value}' is not a single number"]
    printed = cell.printed_value.strip().strip("()").lstrip("-−–")
    if value == 0 and cell.printed_value.strip() in DASHES:
        if not any(d in cell.quote for d in DASHES):
            failures.append(f"{what}: no dash printed in the quote")
        return value, failures
    token = _locate_value(cell.quote, printed, value, doc.language)
    if token is None:
        failures.append(f"{what}: value {cell.printed_value} is not printed in the quote")
        return value, failures
    # The year, where the row shows several years (a table with a column per year). Numbers
    # inside the row's label ("N+1", "1-2 years") are not columns (fix after the first run).
    year = attached_year(cell.quote, token)
    if year is None and header and not re.search(r"(?<!\d)20[2-6]\d(?!\d)", cell.label):
        at = squash_find(cell.quote, cell.label)
        rest = cell.quote[at:] if at is not None else cell.quote
        shifted = Token(token.text, token.value, token.start - (len(cell.quote) - len(rest)),
                        token.end - (len(cell.quote) - len(rest)))  # fmt: skip
        if shifted.start >= 0:
            year = _table_year(rest, shifted, header, doc.language)
    if year is not None and year != doc.fiscal_year:
        failures.append(f"{what}: the quote ties the value to {year}, not FY{doc.fiscal_year}")
    return value, failures


def check_table(
    raw: RawTable,
    index: DocumentIndex,
    issuer: Issuer,
    fiscal_year_end: date,
    tagged: dict[str, Decimal | None],
    config: dict,
) -> CheckedTable:
    """`tagged`: current and total of the layer from the balance sheet (None if not tagged)."""
    doc = index.doc
    t = CheckedTable(raw, doc)
    if raw.fiscal_year != doc.fiscal_year:
        t.failures.append(
            f"FY{raw.fiscal_year} table in the FY{doc.fiscal_year} report: only the report's "
            "own year end is read"
        )
        return t
    caption_pages = index.pages_of(raw.caption)
    if not caption_pages:
        t.failures.append("caption not found word for word in the report")
    else:
        t.location = doc.location(caption_pages[0])
    # The AI marks cell boundaries in the header with "|", which the report does not print
    # (fix after the first run, decision 0022).
    header = " ".join((raw.header or "").replace("|", " ").split())
    if header and not index.pages_of(header):
        t.failures.append("header not found word for word in the report")
        header = ""
    context = " ".join([raw.caption, header] + [c.quote for c in raw.cells])
    # The unit may be printed once at the top of the page ("Importes en miles de euros",
    # "in T€"), not above each table: the quote's page counts too (fix after the first run).
    pages = sorted({p for c in raw.cells for p in index.pages_of(c.quote)})
    context += " " + " ".join(doc.pages[p] for p in pages[:2])
    if not scale_named(context, raw.scale):
        t.failures.append(f"the table does not show its scale ({raw.scale})")
    currency = (raw.currency or issuer.currency).upper()
    if currency != issuer.currency:
        t.failures.append(f"the table is in {currency}, not the reporting currency")
    words = CURRENCY_WORDS.get(currency, [currency.lower()])
    if not contains_any(context, words):
        t.failures.append(f"the table does not show the currency ({currency})")

    def cell_check(cell, what, total=False):
        return _check_cell(cell, index, header, caption_pages, doc, what, total)

    _rows(t, raw, fiscal_year_end, config, doc.language, cell_check)
    if t.buckets:  # 5. Agreement with the balance sheet.
        t.failures += cross_check(t, tagged, config["cross_check"])
    return t


def _rows(t: CheckedTable, raw: RawTable, end: date, config: dict, language, cell_check) -> None:
    """Read every row: labels to spans, values checked by `cell_check`, each row footed; then
    add the rows up column by column into the layer's wall."""
    factor = SCALE_FACTORS[raw.scale]
    if not raw.rows or not all(r.columns for r in raw.rows):
        t.failures.append("no columns given")
        return
    spans_by_row, values_by_row, totals = [], [], []
    for row in raw.rows:
        where = f"row '{row.name}'" if len(raw.rows) > 1 else "row"
        spans, values = parse_labels([c.label for c in row.columns], end), []
        for n, (cell, span) in enumerate(zip(row.columns, spans, strict=True), start=1):
            what = f"{where}, column {n} ('{cell.label}')"
            value, failures = cell_check(cell, what)
            t.failures += failures
            if span is None:
                t.failures.append(f"{what}: code cannot read the label as a time span")
            values.append(None if value is None else value * factor)
        total, failures = cell_check(row.total, f"{where}, total", True)
        t.failures += failures
        spans_by_row.append(spans)
        values_by_row.append(values)
        totals.append(None if total is None else total * factor)
    if any(v is None for v in totals) or any(None in v for v in values_by_row):
        return
    if any(None in s for s in spans_by_row):
        return
    first = spans_by_row[0]
    if any(s != first for s in spans_by_row[1:]):
        t.failures.append("the rows do not have the same columns")
        return
    gap = covers_everything(first)
    if gap:
        t.failures.append(gap)
        return
    decimals = [
        decimals_of(c.printed_value.strip("()").lstrip("-−–"), language, raw.scale)
        for c in raw.cells
        if c.printed_value.strip() not in DASHES
    ]
    t.decimals = min(decimals) if decimals else None
    unit = Decimal(10) ** (-(t.decimals or 0)) if t.decimals is not None else factor
    # 4. Each row foots: its columns add up to the total printed in the same row.
    for row, values, total in zip(raw.rows, values_by_row, totals, strict=True):
        summed = sum(values, Decimal(0))
        if abs(summed - total) > (len(values) + 1) * unit / 2:
            where = f"row '{row.name}': " if len(raw.rows) > 1 else ""
            t.failures.append(
                f"{where}the columns add up to {_m(summed)}, not the total of {_m(total)} "
                "printed in the table"
            )
    t.columns = [
        (span, sum((v[i] for v in values_by_row), Decimal(0))) for i, span in enumerate(first)
    ]
    t.total = sum(totals, Decimal(0))
    t.buckets = standard_buckets(t.columns, config["boundaries"])


def _m(value: Decimal) -> str:
    return f"{value / Decimal(1_000_000):,.1f}m"


def cross_check(t: CheckedTable, tagged: dict, tolerances: dict) -> list[str]:
    current, whole = tagged.get("current"), tagged.get("total")
    name = "borrowings" if t.layer == "borrowings" else "lease liabilities"
    if current is None or whole is None:
        return [f"no tagged current and total {name} to check the table against"]
    first = sum((v for s, v in t.columns if s.end is not None and s.end <= 1), Decimal(0))
    if not any(s.start == 0 and s.end is not None and s.end <= 1 for s, _ in t.columns):
        return ["no column for the first year: cannot check against the current debt"]
    out = []
    if t.raw.basis in ("principal", "carrying_amount"):
        tol = tolerances["principal"]
        allowed = max(Decimal(str(tol["first_bucket_share_of_current"])) * current,
                      Decimal(str(tol["first_bucket_share_of_total"])) * whole)  # fmt: skip
        if abs(first - current) > allowed:
            out.append(
                f"within one year {_m(first)} does not agree with the current {name} of "
                f"{_m(current)} on the balance sheet"
            )
        if abs(t.total - whole) > Decimal(str(tol["total_share"])) * whole:
            out.append(
                f"the table total {_m(t.total)} does not agree with the {name} of {_m(whole)} "
                "on the balance sheet"
            )
    else:
        tol = tolerances["contractual"]
        floor = Decimal(str(tol["first_bucket_floor"])) * current
        ceiling = current + Decimal(str(tol["first_bucket_interest"])) * whole
        if not floor <= first <= ceiling:
            out.append(
                f"within one year {_m(first)} (with interest) is not between {_m(floor)} and "
                f"{_m(ceiling)}, from the current {name} of {_m(current)}"
            )
        lo = Decimal(str(tol["total_floor"])) * whole
        hi = Decimal(str(tol["total_ceiling"])) * whole
        if not lo <= t.total <= hi:
            out.append(
                f"the table total {_m(t.total)} (with interest) is not between {_m(lo)} and "
                f"{_m(hi)}, from the {name} of {_m(whole)}"
            )
    return out


# --- One report --------------------------------------------------------------------------------


BASIS_ORDER = {"principal": 0, "carrying_amount": 1, "contractual_cash_flows": 2}


@dataclass
class MaturityRun:
    doc: Document
    tables: list[CheckedTable] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)
    result: ToolResult | None = None
    error: str | None = None

    def chosen(self, layer: str) -> CheckedTable | None:
        """The table shown for a layer: a checked one first, principal before carrying amounts
        before contractual cash flows."""
        tables = [t for t in self.tables if t.layer == layer]
        if not tables:
            return None
        return sorted(tables, key=lambda t: (not t.verified, BASIS_ORDER[t.raw.basis]))[0]


def read_document(
    llm: LLM,
    issuer: Issuer,
    doc: Document,
    fiscal_year_end: date,
    tagged: dict[str, dict],
    period_label: str,
    config: dict | None = None,
) -> MaturityRun:
    """`tagged`: per layer, {"current": ..., "total": ...} from the balance sheet."""
    config = config or load_config()
    run = MaturityRun(doc)
    message = user_message(issuer, doc, passages(doc, config), period_label)
    try:
        run.result = llm.call_tool(
            "extraction",
            system_prompt(),
            message,
            tool(config["max_tables"]),
            PROMPT_VERSION,
            label=f"{issuer.id} FY{doc.fiscal_year} maturity {doc.doc_id}",
        )
    except NotRecorded:
        run.error = NOT_RUN
        return run
    except LLMError as exc:
        run.error = str(exc)
        return run
    index = DocumentIndex(doc)
    for n, line in enumerate(run.result.arguments.get("tables") or []):
        try:
            raw = RawTable.model_validate(line)
        except ValidationError as exc:
            run.invalid.append(f"table {n + 1}: {exc.errors()[0]['msg']}")
            continue
        run.tables.append(
            check_table(raw, index, issuer, fiscal_year_end, tagged.get(raw.layer, {}), config)
        )
    return run


def to_facts(
    issuer: Issuer, run: MaturityRun, period_end: date, manual: bool = False
) -> list[MappedFact]:
    """One fact per standard bucket of each layer, plus the layer total."""
    facts = []
    doc = run.doc
    models = {}
    if run.result is not None:
        models = {
            "provider": run.result.provider,
            "model": run.result.model,
            "prompt_version": run.result.prompt_version,
            "request_hash": run.result.request_hash,
        }
    for layer in LAYERS:
        t = run.chosen(layer)
        if t is None or t.total is None or not t.buckets:
            continue
        quotes = list(dict.fromkeys(c.quote for c in t.raw.cells))
        ref = {
            "document": doc.doc_id,
            "document_sha256": doc.sha256,
            "source": doc.source,
            "locations": [t.location or ""],
            "caption": t.raw.caption,
            "header": t.raw.header,
            "quotes": quotes,
            "rows": [
                {
                    "name": r.name,
                    "columns": [
                        {"label": c.label, "printed": c.printed_value} for c in r.columns
                    ],  # fmt: skip
                    "total": r.total.printed_value,
                }
                for r in t.raw.rows
            ],
            "spans": [s.label() for s, _ in t.columns],
            "printed": " + ".join(r.total.printed_value for r in t.raw.rows) + f" {t.raw.scale}",
            "basis": t.raw.basis,
            "checks_failed": list(t.failures),
            "notes": list(t.notes),
            "review": t.review,
            **models,
        }
        rows = [(bucket_id(a, b), a, b, v) for a, b, v in t.buckets]
        rows.append(("total", None, None, t.total))
        for bid, a, b, value in rows:
            what = "total" if bid == "total" else bucket_label(a, b)
            facts.append(
                MappedFact(
                    issuer=issuer.id,
                    fiscal_year=doc.fiscal_year,
                    period_end=period_end,
                    line=f"maturity_{layer}_{bid}",
                    value=value,
                    value_tagged=value,
                    decimals=t.decimals,
                    currency=issuer.currency,
                    filing_id=doc.doc_id,
                    comparative=False,
                    concepts=tuple(quotes),
                    fact_ids=(t.location or "",),
                    rule_source="manual" if manual else "extracted",
                    sign=1,
                    note=(
                        f"{layer.capitalize()} due {what} ({t.raw.basis.replace('_', ' ')}), "
                        f"from the maturity table “{t.raw.caption.strip()}” of the "
                        f"FY{doc.fiscal_year} report ({t.location})"
                        + (", entered by hand" if manual else "")
                    ),
                    warnings=tuple(t.failures),
                    source_type="manual" if manual else "extracted",
                    status=t.status,
                    ref=ref,
                )
            )
    return facts


def line_labels(config: dict | None = None) -> dict[str, str]:
    """Labels of every possible wall line: each layer, each standard or merged bucket, total."""
    config = config or load_config()
    edges = [Decimal(b) for b in config["boundaries"]] + [None]
    out = {}
    for layer in LAYERS:
        name = "Borrowings" if layer == "borrowings" else "Lease liabilities"
        for i in range(len(edges) - 1):
            for j in range(i + 1, len(edges)):
                a, b = edges[i], edges[j]
                out[f"maturity_{layer}_{bucket_id(a, b)}"] = f"{name} due {bucket_label(a, b)}"
        out[f"maturity_{layer}_total"] = f"{name}, total of the maturity table"
    return out


# --- One company: the tearsheet years ---------------------------------------------------------

ENTRIES = HERE.parents[2] / "config" / "maturity_entries.yaml"
YEARS_READ = 2  # the years with a tearsheet: the latest two


def tagged_debt(facts: list[MappedFact], year: int, leases_in_borrowings: bool) -> dict:
    """Per layer, the current part and the total from the balance sheet (None if not tagged).
    Where the balance sheet counts lease liabilities inside borrowings, the borrowings table
    must include them too to agree; the leases then have no tagged figure of their own."""
    lines = {f.line: f.value for f in facts if f.primary and f.fiscal_year == year}

    def pair(current: str, noncurrent: str, total: str) -> dict:
        cur = lines.get(current)
        whole = lines.get(total)
        if whole is None and cur is not None and lines.get(noncurrent) is not None:
            whole = cur + lines[noncurrent]
        return {"current": cur, "total": whole}

    borrowings = pair("borrowings_current", "borrowings_noncurrent", "borrowings_total")
    leases = pair("lease_liabilities_current", "lease_liabilities_noncurrent",
                  "lease_liabilities_total")  # fmt: skip
    if leases_in_borrowings:
        leases = {"current": None, "total": None}
    return {"borrowings": borrowings, "leases": leases}


def hand_runs(
    issuer: Issuer, facts: list[MappedFact], docs: list[Document], config: dict,
    path: Path = ENTRIES,
) -> list[MaturityRun]:  # fmt: skip
    """Tables entered by hand from a supplied PDF (decision 0007: no electronic report), run
    through the same label, foot and balance sheet checks; unverified until Imane reviews."""
    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    runs = []
    for e in (data or {}).get("entries") or []:
        if e["issuer"] != issuer.id:
            continue
        doc = next(d for d in docs if d.doc_id == e["document"])
        end = period_end_of(issuer, int(e["fiscal_year"]))
        run = MaturityRun(doc)
        for t in e["tables"]:
            raw = RawTable(
                layer=t["layer"],
                basis=t["basis"],
                fiscal_year=int(e["fiscal_year"]),
                caption=t["caption"],
                header=t.get("header"),
                scale=t["scale"],
                currency=t.get("currency", issuer.currency),
                rows=[
                    RawRow(
                        name=r["name"],
                        columns=[
                            RawCell(label=k, printed_value=str(v), quote=r["name"])
                            for k, v in r["columns"]
                        ],  # fmt: skip
                        total=RawCell(
                            label="Total", printed_value=str(r["total"]), quote=r["name"]
                        ),  # fmt: skip
                    )
                    for r in t["rows"]
                ],
                location=f"page {t['page']}",
            )
            tagged = tagged_debt(facts, raw.fiscal_year, issuer.leases_in_borrowings)
            checked = _check_hand(raw, doc, end, tagged.get(raw.layer, {}), config)
            checked.location = f"page {t['page']}"
            if not e.get("reviewed_by"):
                checked.failures.append("entered by hand, not reviewed yet: waiting for Imane")
            run.tables.append(checked)
        runs.append(run)
    return runs


def _check_hand(raw: RawTable, doc: Document, end: date, tagged: dict, config: dict):
    """A hand entry has no quote to find (the PDF's tables lose their rows when converted to
    text): the labels, the foot and the balance sheet checks still apply."""
    t = CheckedTable(raw, doc)

    def cell_check(cell, what, total=False):
        value = _value(cell, doc.language)
        return value, ([] if value is not None else [f"{what}: '{cell.printed_value}' unread"])

    _rows(t, raw, end, config, doc.language, cell_check)
    if t.buckets:
        t.failures += cross_check(t, tagged, config["cross_check"])
    return t


def period_end_of(issuer: Issuer, year: int) -> date:
    month, day = (int(x) for x in issuer.fiscal_year_end.split("-"))
    return date(year, month, day)


def read_issuer(
    issuer: Issuer, docs: list[Document], facts: list[MappedFact], llm: LLM,
    fiscal_label, config: dict | None = None,
) -> tuple[list[MaturityRun], list[MappedFact]]:  # fmt: skip
    """The maturity wall of the latest two years: from the year's own electronic report (AI and
    checks), or from hand entries where only a supplied PDF exists."""
    config = config or load_config()
    revenue_years = sorted({f.fiscal_year for f in facts if f.primary and f.line == "revenue"})
    years = revenue_years[-YEARS_READ:]
    hand = {r.doc.fiscal_year: r for r in hand_runs(issuer, facts, docs, config)}
    runs, out = [], []
    for year in years:
        end = period_end_of(issuer, year)
        if year in hand:
            run = hand[year]
        else:
            own = [d for d in docs if d.fiscal_year == year and d.origin.endswith("report")]
            if not own:
                continue
            tagged = tagged_debt(facts, year, issuer.leases_in_borrowings)
            run = read_document(llm, issuer, own[0], end, tagged, fiscal_label(issuer, year),
                                config)  # fmt: skip
        runs.append(run)
        out += to_facts(issuer, run, end, manual=year in hand)
    return runs, out
