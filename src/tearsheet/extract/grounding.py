"""Grounding checks: code confirms each figure the AI read before it can be marked verified.

Per figure (this module):
  1. the quote is in the report, word for word (spaces ignored);
  2. the quote is about the figure (it contains one of the figure's terms);
  3. the value is printed in the quote, and its scale (thousand, million...) and unit (%, the
     currency) are shown there too;
  4. the year is right: the value is not the comparative printed next to it;
  5. the value is in a plausible range.
Across figures (consolidate.py): agreement with the next year's report, RPK ÷ ASK against the
printed load factor, and plausible year-on-year changes.

A figure that fails any check stays unverified, with every reason kept.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

from tearsheet.extract.documents import Document
from tearsheet.extract.numbers import (
    CURRENCY_WORDS,
    PERCENT_WORDS,
    SCALE_FACTORS,
    Token,
    contains_any,
    decimals_of,
    number_tokens,
    parse_number,
    scale_named,
    scale_words_near,
    squash,
    year_marks,
)

MAX_QUOTE = 700


class RawFigure(BaseModel):
    """One line of the form the AI fills in (see extractor.TOOL)."""

    item: str
    fiscal_year: int
    found: bool
    printed_value: str | None = None
    scale: Literal["one", "thousand", "million", "billion"] | None = "one"
    currency: str | None = None
    quote: str | None = None
    table_header: str | None = None
    caption: str | None = None  # title or unit line of the table (extract-v2)
    location: str | None = None
    scope: str | None = None
    component: bool = False
    comment: str | None = None


@dataclass
class Checked:
    """A figure after the checks."""

    raw: RawFigure
    doc: Document
    value: Decimal | None = None  # full units; fractions for percentages
    decimals: int | None = None
    currency: str | None = None
    location: str | None = None  # found by code, not taken from the AI
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def verified(self) -> bool:
        return self.value is not None and not self.failures

    @property
    def item(self) -> str:
        return self.raw.item

    @property
    def fiscal_year(self) -> int:
        return self.raw.fiscal_year


class DocumentIndex:
    """The report squashed once (no whitespace, lower case), with each page's span."""

    def __init__(self, doc: Document):
        self.doc = doc
        self.flat_pages = [squash(p) for p in doc.pages]
        self.flat = "".join(self.flat_pages)
        self.offsets = []
        pos = 0
        for p in self.flat_pages:
            self.offsets.append(pos)
            pos += len(p)

    def pages_of(self, text: str) -> list[int]:
        """Every page (0-based) holding the text word for word; a text running over a page
        break counts on the page where it starts."""
        needle = squash(text)
        if not needle:
            return []
        hits = [i for i, page in enumerate(self.flat_pages) if needle in page]
        if hits:
            return hits
        at = self.flat.find(needle)
        if at < 0:
            return []
        return [max(i for i, o in enumerate(self.offsets) if o <= at)]

    def find(self, text: str) -> str | None:
        """Location of the text in the report, or None if it is not there word for word."""
        pages = self.pages_of(text)
        return self.doc.location(pages[0]) if pages else None


def check_figure(
    raw: RawFigure,
    index: DocumentIndex,
    item: dict,
    reporting_currency: str,
    revenue: Decimal | None = None,
) -> Checked:
    doc = index.doc
    c = Checked(raw, doc)
    if raw.fiscal_year not in (doc.fiscal_year, doc.fiscal_year - 1):
        c.failures.append(
            f"FY{raw.fiscal_year} cannot be read from the FY{doc.fiscal_year} report "
            "(only its own year and the prior-year comparative)"
        )
        return c
    if not raw.quote or not raw.printed_value:
        c.failures.append("no quote or no value given")
        return c
    if len(raw.quote) > MAX_QUOTE:
        c.failures.append(f"quote longer than {MAX_QUOTE} characters")
        return c

    # 1. The quote is in the report.
    c.location = index.find(raw.quote)
    if c.location is None:
        c.failures.append("quote not found word for word in the report")
        return c
    header = raw.table_header or ""
    if header and index.find(header) is None:
        c.failures.append("table header not found word for word in the report")
        header = ""
    # The caption (a table's title or unit line, "in thousands of euros") counts only if it
    # is printed on the quote's page or the page before, so it cannot be borrowed from
    # another table elsewhere in the report.
    caption = raw.caption or ""
    if caption:
        quote_pages = index.pages_of(raw.quote)
        caption_pages = index.pages_of(caption)
        if not caption_pages:
            c.failures.append("caption not found word for word in the report")
            caption = ""
        elif not any(0 <= q - p <= 1 for q in quote_pages for p in caption_pages):
            c.failures.append("caption is not on the quote's page or the page before")
            caption = ""
    context = (header + " " + caption).strip()

    # 2. The quote is about this figure. A bare number ("107,0") cannot say whose figure it is,
    # even with a header: the row label must be in the quote.
    if not re.search(r"[A-Za-zÀ-ÿ]{3,}", raw.quote):
        c.failures.append("the quote is only numbers, without the row label")
    terms = [t for lang_terms in item["terms"].values() for t in lang_terms]
    if not contains_any(raw.quote + " " + context, terms):
        c.failures.append(f"quote does not mention {item['label'].lower()}")

    # 3. The value, scale and unit are printed in the quote.
    number = parse_number(raw.printed_value, doc.language)
    if number is None:
        c.failures.append(f"'{raw.printed_value}' is not a single number")
        return c
    token = _locate_value(raw.quote, raw.printed_value, number, doc.language)
    if token is None:
        c.failures.append(f"value {raw.printed_value} is not printed in the quote")
        return c
    scale = raw.scale or "one"
    unit = item["unit"]
    if unit == "pct":
        after = raw.quote[token.end : token.end + 12]
        if not (contains_any(after, PERCENT_WORDS) or contains_any(context, PERCENT_WORDS)):
            c.failures.append("no % sign or 'per cent' next to the value")
        value = number / 100
        decimals = None
    elif unit == "years":
        value, decimals = number, None
    else:
        near = scale_words_near(raw.quote, token.end)
        if scale == "one":
            if near:
                c.failures.append(f"the quote says {sorted(near)[0]} but the form says units")
        elif scale not in near and not (
            scale_named(context, scale) or (not near and scale_named(raw.quote, scale))
        ):
            c.failures.append(f"the quote does not show the scale ({scale})")
        value = number * SCALE_FACTORS[scale]
        decimals = decimals_of(raw.printed_value, doc.language, scale)
    if unit == "amount":
        currency = (raw.currency or reporting_currency).upper()
        words = CURRENCY_WORDS.get(currency, [currency.lower()])
        if not contains_any(raw.quote + " " + context, words):
            c.failures.append(f"the quote does not show the currency ({currency})")
        c.currency = currency
    c.value, c.decimals = value, decimals

    # 4. The year is right.
    reason = _check_year(raw, token, header, item["period"], doc)
    if reason:
        if reason.startswith("note:"):
            c.notes.append(reason[5:].strip())
        else:
            c.failures.append(reason)

    # 4b. A forward figure (hedge ratio) covers twelve months, not part of the year.
    if item["period"] == "forward":
        rest = _sentence_rest(doc, raw.quote)  # a quote cut short must not hide the period
        part = _part_of_year(raw.quote + " " + rest + " " + context)
        if part:
            c.failures.append(
                f"the quote gives the figure for part of a year ('{part}'), not the next "
                "twelve months"
            )

    # 5. Plausible range.
    reason = _check_range(c, item, revenue, reporting_currency)
    if reason:
        c.failures.append(reason)
    if raw.component:
        c.notes.append("one part among several (summed with the others)")
    return c


def _locate_value(quote: str, printed: str, number: Decimal, language: str | None) -> Token | None:
    """The printed value inside the quote: a number with the same value, or (for reports that
    split numbers with spaces, '2. 7 %') the same digits once spaces are removed."""
    for token in number_tokens(quote, language):
        if token.value == number and squash(token.text) == squash(printed):
            return token
    for token in number_tokens(quote, language):
        if token.value == number:
            return token
    # The printed text exactly as given, spaces included ('3 0, 2 2 7. 3'), between non-digits.
    for m in re.finditer(re.escape(printed.strip()), quote):
        before = quote[m.start() - 1] if m.start() > 0 else " "
        after = quote[m.end()] if m.end() < len(quote) else " "
        if not (before.isdigit() or after.isdigit()) and before not in ".," and printed.strip():
            return Token(m.group(0), number, m.start(), m.end())
    target = re.sub(r"\s+", "", printed)
    flat, index = [], []
    for i, ch in enumerate(quote):
        if not ch.isspace():
            flat.append(ch)
            index.append(i)
    flat_text = "".join(flat)
    at = flat_text.find(target)
    while at >= 0:
        before = flat_text[at - 1] if at > 0 else ""
        after = flat_text[at + len(target)] if at + len(target) < len(flat_text) else ""
        boundary_ok = not (before.isdigit() or before in ".,") and not after.isdigit()
        if after in ".," and at + len(target) + 1 < len(flat_text):
            boundary_ok = boundary_ok and not flat_text[at + len(target) + 1].isdigit()
        if boundary_ok:
            start = index[at]
            end = index[at + len(target) - 1] + 1
            return Token(quote[start:end], number, start, end)
        at = flat_text.find(target, at + 1)
    return None


COMPARATIVE_WORDS = [
    "prior year", "previous year", "last year", "year before", "compared with", "compared to",
    "versus", "vs", "année précédente", "exercice précédent", "contre", "par rapport à",
    "año anterior", "frente a", "ejercicio anterior", "vorjahr", "im vergleich",
]  # fmt: skip


def _paren_span(text: str, pos: int) -> tuple[int, int] | None:
    """The parentheses or brackets around position pos, if any."""
    depth, start = 0, None
    for i in range(pos - 1, -1, -1):
        if text[i] in ")]":
            depth += 1
        elif text[i] in "([":
            if depth == 0:
                start = i
                break
            depth -= 1
    if start is None:
        return None
    depth = 0
    for j in range(pos, len(text)):
        if text[j] in "([":
            depth += 1
        elif text[j] in ")]":
            if depth == 0:
                return start, j
            depth -= 1
    return start, len(text)


def attached_year(quote: str, token: Token) -> int | None:
    """The year the value belongs to, read from the quote: inside brackets, the year at the
    start of the brackets ('(2024: 89.7 million)'); otherwise the nearest year in the same
    clause, ignoring years inside other brackets. None if the quote names no year."""
    marks = [m for m in year_marks(quote) if not (token.start <= m.start < token.end)]
    span = _paren_span(quote, token.start)
    if span:
        inside = [m for m in marks if span[0] < m.start < span[1]]
        before = [m for m in inside if m.start < token.start]
        if before:
            return before[-1].year
        if inside:
            return inside[0].year
    starts = [quote.rfind(sep, 0, token.start) for sep in (";", ". ")]
    clause_start = max(starts) + 1
    ends = [quote.find(sep, token.end) for sep in (";", ". ")]
    ends = [e for e in ends if e >= 0]
    clause_end = min(ends) if ends else len(quote)
    candidates = []
    for m in marks:
        if not (clause_start <= m.start < clause_end):
            continue
        other = _paren_span(quote, m.start)
        if other and not (span and other == span):
            continue  # a year inside other brackets belongs to the figures in those brackets
        candidates.append(m)
    if not candidates:
        return None

    def distance(m) -> int:
        return min(abs(m.start - token.start), abs(m.end - token.end))

    return min(candidates, key=distance).year


def _table_year(quote: str, token: Token, header: str, language: str | None) -> int | None:
    """In a table row, the year of the value's column, from the header's years in order."""
    every = [m.year for m in year_marks(header)]
    years = []
    for y in every:
        if y not in years:
            years.append(y)
    if not years:
        return None
    # A table with several measures repeats the years over each ("2025 2024 | 2025 2024"):
    # then every column has its own year.
    repeated = len(every) > len(years) and len(every) % len(years) == 0
    if repeated and every == years * (len(every) // len(years)):
        years = every
    first_digit = re.search(r"\d", quote)
    label_end = first_digit.start() if first_digit else 0
    numbers = [
        t
        for t in number_tokens(quote, language)
        if t.start >= label_end and not _unit_marker(quote, t)
    ]
    positions = [t.start for t in numbers]
    if token.start not in positions:
        return None
    k = positions.index(token.start)
    if len(numbers) < len(years):
        return None
    return years[k] if k < len(years) else None


UNIT_MARK = re.compile(r"[‘’'`´(]\s*$")


def _unit_marker(quote: str, token: Token) -> bool:
    """A "‘000" or "(000)" after a row label says the row counts in thousands: not a value."""
    return token.text.strip() == "000" and bool(UNIT_MARK.search(quote[: token.start]))


def _check_year(raw: RawFigure, token: Token, header: str, period: str, doc: Document) -> str:
    claimed = raw.fiscal_year
    allowed = {claimed, claimed + 1} if period == "forward" else {claimed}
    quote = raw.quote or ""
    year = attached_year(quote, token)
    source = "the quote"
    if year is None and header:
        year = _table_year(quote, token, header, doc.language)
        source = "the table header"
        if period == "forward":
            # A hedge table's columns are the years the fuel is used: at the end of FY2022,
            # the position for the next twelve months is the 2023 column.
            allowed = {claimed + 1}
    if year is not None:
        if year in allowed:
            return ""
        if period == "forward" and source == "the table header":
            return (
                f"the value is in the {year} column; the hedge held at the end of FY{claimed} "
                f"for the next twelve months is the {claimed + 1} column"
            )
        return f"{source} ties the value to {year}, not FY{claimed}"
    # No year in the quote: only the report's own year can be assumed, and only if the quote
    # holds no other figure of the same size that could be the comparative.
    if claimed != doc.fiscal_year:
        return "the quote names no year, so it cannot be confirmed as the prior-year figure"
    # Brackets that carry a year hold the comparative ('(2024: 89.7 million)'); a value
    # outside them is the report's own year.
    spans = []
    for m in year_marks(quote):
        span = _paren_span(quote, m.start)
        if span and span not in spans:
            spans.append(span)
    outside = quote
    for a, b in sorted(spans, reverse=True):
        outside = outside[:a] + " " * (min(b, len(outside) - 1) - a + 1) + outside[b + 1 :]
    if year_marks(outside):
        return "the quote names years, none of them next to the value"
    lowered = outside.lower()
    words = (rf"(?<![a-zà-ÿ]){re.escape(w)}(?![a-zà-ÿ])" for w in COMPARATIVE_WORDS)
    if any(re.search(w, lowered) for w in words):
        return "the quote compares years but names none, so the year cannot be confirmed"
    rivals = [
        t
        for t in number_tokens(quote, doc.language)
        if t.start != token.start and t.value > 0 and token.value > 0
        and Decimal("0.5") <= t.value / token.value <= Decimal(2)
        and not any(a < t.start < b for a, b in spans)
    ]  # fmt: skip
    if rivals:
        return "the quote holds several similar figures and names no year to tell them apart"
    if spans:
        return "note: the year in brackets is the comparative; the value is the report's own year"
    return "note: the quote names no year; taken as the report's own year"


PART_OF_YEAR = re.compile(
    r"(?i)(?<![a-zà-ÿ])(first|second|1st|2nd)\s+(six\s+months|half|quarter)|"
    r"(?<![a-z0-9])(H1|H2|Q[1-4])(?![a-z0-9])|"
    r"(premier|second|1er|2e)\s+(semestre|trimestre)|"
    r"(primer|segundo)\s+(semestre|trimestre)|(erste|zweite)[ns]?\s+(halbjahr|quartal)|"
    r"(?<![a-z])\d+\s+months(?![a-z])"
)


def _sentence_rest(doc: Document, quote: str, limit: int = 200) -> str:
    """The report's own text right after the quote, to the end of its sentence."""
    tail = [ch for ch in quote[-80:] if not ch.isspace()]
    if not tail:
        return ""
    pattern = re.compile(r"\s*".join(re.escape(ch) for ch in tail))
    for page in doc.pages:
        m = pattern.search(page)
        if m:
            after = page[m.end() : m.end() + limit]
            stop = re.search(r"[.;](\s|$)", after)
            return after[: stop.start()] if stop else after
    return ""


def _part_of_year(text: str) -> str | None:
    """Words that limit a figure to part of a year ('first six months', 'H1 FY26', '5 months').
    '12 months' and 'twelve months' are a full year and are not caught."""
    for m in PART_OF_YEAR.finditer(text):
        months = re.match(r"(\d+)\s+months", m.group(0), re.IGNORECASE)
        if months and int(months.group(1)) >= 12:
            continue
        return m.group(0)
    return None


def _check_range(c: Checked, item: dict, revenue: Decimal | None, currency: str) -> str:
    value = c.value
    if value is None:
        return ""
    if "range" in item:
        low, high = (Decimal(str(x)) for x in item["range"])
        if not (low <= value <= high):
            return f"value {value:,} is outside the plausible range for {item['label'].lower()}"
    if "range_of_revenue" in item:
        if revenue is None or revenue <= 0:
            c.notes.append("revenue not available to check the size")
            return ""
        if c.currency and c.currency != currency:
            return ""  # checked after conversion, in consolidate
        low, high = (Decimal(str(x)) for x in item["range_of_revenue"])
        share = value / revenue
        if not (low <= share <= high):
            return f"value is {share:.0%} of revenue, outside the plausible {low:.0%}-{high:.0%}"
    return ""
