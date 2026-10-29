"""Read the numeric facts of an xBRL-JSON report."""

from __future__ import annotations

import gzip
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

# Dimensions every fact carries; any other key is a breakdown (segment, equity component...).
CORE_DIMENSIONS = {"concept", "entity", "period", "unit", "language", "noteId"}

STANDARD_NAMESPACE_PREFIXES = (
    "http://xbrl.ifrs.org/",
    "https://xbrl.ifrs.org/",
    "http://www.esma.europa.eu/taxonomy/",
    "https://www.esma.europa.eu/taxonomy/",
    "http://xbrl.frc.org.uk/",
    "https://xbrl.frc.org.uk/",
    "http://www.xbrl.org/",
    "https://www.xbrl.org/",
)


@dataclass(frozen=True)
class Fact:
    fact_id: str
    concept: str  # "ifrs-full:Local" for IFRS concepts, "ext:Local" for company concepts
    tagged_concept: str  # the concept exactly as written in the filing
    value: Decimal
    decimals: int | None  # None means "INF" (exact)
    unit: str | None
    start: date | None  # None for a balance-sheet (instant) fact
    end: date  # last day covered, inclusive
    breakdown: bool
    dimensions: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Report:
    facts: list[Fact]
    language: str | None


def parse_period(period: str) -> tuple[date | None, date]:
    """xBRL-JSON bounds are midnight instants: an end at 00:00 means the day before."""

    def moment(text: str) -> datetime:
        return datetime.fromisoformat(text.strip().replace("Z", ""))

    def last_day(text: str) -> date:
        m = moment(text)
        return (m - timedelta(days=1)).date() if m.time() == datetime.min.time() else m.date()

    if "/" in period:
        start_text, end_text = period.split("/", 1)
        return moment(start_text).date(), last_day(end_text)
    return None, last_day(period)


def canonical_concept(concept: str, namespaces: dict[str, str]) -> str | None:
    if ":" not in concept:
        return None
    prefix, local = concept.split(":", 1)
    uri = namespaces.get(prefix, "")
    if "xbrl.ifrs.org" in uri:
        return f"ifrs-full:{local}"
    if uri.startswith(STANDARD_NAMESPACE_PREFIXES):
        return f"{prefix}:{local}"
    # Company concept: the prefix changes between years, the local name doesn't.
    return f"ext:{local}"


def _decimals(raw) -> int | None:
    if raw is None or str(raw).upper() == "INF":
        return None
    return int(raw)


def parse_report(document: dict) -> Report:
    namespaces = document.get("documentInfo", {}).get("namespaces", {})
    facts, languages = [], Counter()
    for fact_id, raw in document.get("facts", {}).items():
        dims = raw.get("dimensions", {})
        if dims.get("language"):
            languages[dims["language"].split("-")[0].lower()] += 1
        concept, period, value = dims.get("concept"), dims.get("period"), raw.get("value")
        unit = dims.get("unit")
        if not concept or not period or value is None or not unit:
            continue  # text facts and malformed facts are not loaded here
        canonical = canonical_concept(concept, namespaces)
        try:
            number = Decimal(str(value))
        except InvalidOperation:
            continue
        if canonical is None:
            continue
        start, end = parse_period(period)
        extra = tuple(sorted((k, str(v)) for k, v in dims.items() if k not in CORE_DIMENSIONS))
        facts.append(
            Fact(
                fact_id=fact_id,
                concept=canonical,
                tagged_concept=concept,
                value=number,
                decimals=_decimals(raw.get("decimals")),
                unit=unit,
                start=start,
                end=end,
                breakdown=bool(extra),
                dimensions=extra,
            )
        )
    language = languages.most_common(1)[0][0] if languages else None
    return Report(facts=facts, language=language)


def load_report(path: Path) -> Report:
    if path.suffix == ".gz":
        return parse_report(json.loads(gzip.decompress(path.read_bytes())))
    return parse_report(json.loads(path.read_text()))
