"""Read xBRL-JSON facts and classify core lines as found, extension or missing."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

# Dimensions every fact carries; any other key is a breakdown (segment, component of equity...).
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

MATCH_TOLERANCE_DAYS = 7
DURATION_DAYS = (300, 400)


@dataclass
class Fact:
    concept: str  # canonical "prefix:Local" with standard IFRS concepts as "ifrs-full:..."
    local_name: str
    standard: bool
    value: str | None
    decimals: int | str | None
    unit: str | None
    start: date | None  # None for instants
    end: date  # last day covered (inclusive)
    breakdown: bool
    language: str | None


@dataclass
class LineResult:
    line: str
    status: str  # found | extension | missing
    concept: str | None = None
    value: str | None = None
    decimals: int | str | None = None
    unit: str | None = None
    candidates: list[str] = field(default_factory=list)


def _parse_datetime(text: str) -> date:
    """xBRL-JSON period bounds are midnight instants; an end at 00:00 means the day before."""
    text = text.strip()
    if "T" not in text:
        return date.fromisoformat(text)
    moment = datetime.fromisoformat(text.replace("Z", ""))
    if moment.time() == datetime.min.time():
        return (moment - timedelta(days=1)).date()
    return moment.date()


def parse_period(period: str) -> tuple[date | None, date]:
    """Return (start, end) with inclusive dates; start is None for an instant."""
    if "/" in period:
        start_text, end_text = period.split("/", 1)
        start = datetime.fromisoformat(start_text.strip().replace("Z", "")).date()
        return start, _parse_datetime(end_text)
    return None, _parse_datetime(period)


def _canonical_prefix(prefix: str, namespaces: dict[str, str]) -> tuple[str, bool]:
    uri = namespaces.get(prefix, "")
    standard = uri.startswith(STANDARD_NAMESPACE_PREFIXES)
    if "xbrl.ifrs.org" in uri:
        return "ifrs-full", True
    return prefix, standard


def load_facts(document: dict) -> list[Fact]:
    namespaces = document.get("documentInfo", {}).get("namespaces", {})
    facts = []
    for raw in document.get("facts", {}).values():
        dims = raw.get("dimensions", {})
        concept = dims.get("concept")
        period = dims.get("period")
        if not concept or not period or ":" not in concept:
            continue
        prefix, local = concept.split(":", 1)
        canonical, standard = _canonical_prefix(prefix, namespaces)
        start, end = parse_period(period)
        facts.append(
            Fact(
                concept=f"{canonical}:{local}",
                local_name=local,
                standard=standard,
                value=raw.get("value"),
                decimals=raw.get("decimals"),
                unit=dims.get("unit"),
                start=start,
                end=end,
                breakdown=any(key not in CORE_DIMENSIONS for key in dims),
                language=dims.get("language"),
            )
        )
    return facts


def main_language(facts: list[Fact]) -> str | None:
    counts = Counter(f.language.split("-")[0].lower() for f in facts if f.language)
    return counts.most_common(1)[0][0] if counts else None


def _in_period(fact: Fact, period_type: str, fy_end: date) -> bool:
    if abs((fact.end - fy_end).days) > MATCH_TOLERANCE_DAYS:
        return False
    if period_type == "instant":
        return fact.start is None
    if fact.start is None:
        return False
    length = (fact.end - fact.start).days + 1
    return DURATION_DAYS[0] <= length <= DURATION_DAYS[1]


def _plain(text: str) -> str:
    """Lower case without accents, so "RésultatOpérationnel" matches "resultat"."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).lower()


def _matches_keywords(local_name: str, keyword_groups: list[list[str]]) -> bool:
    name = _plain(local_name)
    return any(all(word.lower() in name for word in group) for group in keyword_groups)


def classify_line(line_id: str, spec: dict, facts: list[Fact], fy_end: date) -> LineResult:
    """Classify one core line for the fiscal year ending on fy_end."""
    period_type = spec["period"]
    candidates = [f for f in facts if not f.breakdown and _in_period(f, period_type, fy_end)]

    for concept in spec.get("concepts", []):
        parts = concept if isinstance(concept, list) else [concept]
        hits = [next((f for f in candidates if f.concept == part), None) for part in parts]
        if all(hits):
            if len(hits) == 1:
                fact = hits[0]
                return LineResult(
                    line_id, "found", fact.concept, fact.value, fact.decimals, fact.unit
                )
            return LineResult(
                line_id,
                "found",
                " + ".join(parts),
                " + ".join(str(f.value) for f in hits),
                hits[0].decimals,
                hits[0].unit,
            )

    keyword_groups = spec.get("keywords") or []
    extensions = sorted(
        {
            f.concept
            for f in candidates
            if not f.standard
            and f.unit
            and f.unit.lower().startswith("iso4217:")
            and _matches_keywords(f.local_name, keyword_groups)
        }
    )
    if extensions:
        return LineResult(line_id, "extension", candidates=extensions)
    return LineResult(line_id, "missing")


def has_text_block(concepts: list[str], facts: list[Fact]) -> str | None:
    present = {f.concept for f in facts}
    for concept in concepts:
        if concept in present:
            return concept
    return None


def critical_met(statuses: dict[str, str], critical: dict[str, list[list[str]]]) -> list[str]:
    """Return the critical requirements that are NOT met (empty list means usable year)."""
    failed = []
    for name, alternatives in critical.items():
        ok = any(
            all(statuses.get(line) in ("found", "extension") for line in option)
            for option in alternatives
        )
        if not ok:
            failed.append(name)
    return failed


_TAG = re.compile(r"<[^>]+>")
_SPACE = re.compile(r"\s+")


def html_to_text(html: str) -> str:
    return _SPACE.sub(" ", _TAG.sub(" ", html))


def find_terms(text: str, terms: list[str]) -> tuple[int, str | None]:
    """Count term hits (acronyms case-sensitive as whole words) and return one snippet."""
    total, snippet = 0, None
    for term in terms:
        if term.isupper():
            pattern = re.compile(rf"\b{re.escape(term)}\b")
        else:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
        matches = list(pattern.finditer(text))
        total += len(matches)
        if matches and snippet is None:
            m = matches[0]
            snippet = text[max(0, m.start() - 80) : m.end() + 80].strip()
    return total, snippet
