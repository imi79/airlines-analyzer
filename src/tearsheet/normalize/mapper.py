"""Map each filing's tagged facts onto the canonical statement lines.

Each filing gives values for its own fiscal year and, through its comparative column, for the
year before. When two filings give the same year, the most recent filing wins (decision 0004:
latest restated figure), and the older value is kept with a "restated" flag when it differs.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date
from decimal import Decimal
from pathlib import Path

import yaml

from tearsheet.config import FIRST_FISCAL_YEAR, Issuer
from tearsheet.ingest.filings import Filing
from tearsheet.ingest.xbrl_json import Fact, Report

HERE = Path(__file__).parent
CONCEPT_MAP = HERE / "concept_map.yaml"
OVERRIDES = HERE / "overrides"

MATCH_TOLERANCE_DAYS = 7
DURATION_DAYS = (300, 400)


@dataclass(frozen=True)
class Rule:
    concepts: tuple[str, ...]
    add_if_tagged: tuple[str, ...] = ()  # added to the total when tagged for the year
    subtract: tuple[str, ...] = ()  # required, and taken away from the total
    sign: int = 1
    source: str = "common"
    note: str | None = None  # shown in the coverage report and the audit trail
    footnote: str | None = None  # to be printed on the tearsheet
    reason: str | None = None  # why this override exists
    checked: str | None = None  # where it was checked
    years: frozenset[int] | None = None  # fiscal years the rule applies to (all if None)
    from_filing_year: int | None = None  # applies only to filings from this fiscal year on


@dataclass(frozen=True)
class Line:
    id: str
    label: str
    statement: str
    period: str  # duration | instant
    rules: tuple[Rule, ...]
    expect: str | None = None
    applies_to: frozenset[str] | None = None
    optional: bool = False
    group: str | None = None
    missing_reason: str | None = None


@dataclass(frozen=True)
class Mapping:
    lines: dict[str, Line]
    debt_coverage: dict[str, str]
    not_applicable: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MappedFact:
    issuer: str
    fiscal_year: int
    period_end: date
    line: str
    value: Decimal  # canonical sign
    value_tagged: Decimal  # as tagged in the filing (sum of parts if several)
    decimals: int | None
    currency: str
    filing_id: str
    comparative: bool  # taken from the prior-year column of the next filing
    concepts: tuple[str, ...]  # concepts exactly as tagged
    fact_ids: tuple[str, ...]
    rule_source: str
    sign: int
    note: str | None = None
    footnote: str | None = None
    primary: bool = True
    restated: bool = False  # another filing gives a different value for the same year
    warnings: tuple[str, ...] = ()
    source_type: str = "tagged"  # tagged | manual (by hand) | extracted (read by the AI, M3)
    status: str = "verified"  # verified | unverified | overridden
    ref: dict | None = field(default=None, compare=False)  # extra audit trail (extracted facts)


@dataclass(frozen=True)
class Gap:
    issuer: str
    fiscal_year: int
    line: str
    reason: str
    counts_as_missing: bool  # False for lines that are optional or covered elsewhere


def _rule(raw: dict, source: str) -> Rule:
    years = raw.get("years")
    return Rule(
        concepts=tuple(raw["concepts"]),
        add_if_tagged=tuple(raw.get("add_if_tagged") or ()),
        subtract=tuple(raw.get("subtract") or ()),
        sign=int(raw.get("sign", 1)),
        source=source,
        note=raw.get("note"),
        footnote=raw.get("footnote"),
        reason=raw.get("reason"),
        checked=raw.get("checked"),
        years=frozenset(years) if years else None,
        from_filing_year=raw.get("from_filing_year"),
    )


def load_mapping(issuer_id: str, concept_map: Path = CONCEPT_MAP, overrides: Path = OVERRIDES):
    """Common concept map with the issuer's overrides tried first."""
    common = yaml.safe_load(concept_map.read_text())
    path = overrides / f"{issuer_id}.yaml"
    override = yaml.safe_load(path.read_text()) if path.exists() else {}
    override_lines = override.get("lines") or {}
    unknown = set(override_lines) - set(common["lines"])
    if unknown:
        raise ValueError(f"{path.name}: unknown lines {sorted(unknown)}")
    lines = {}
    for line_id, raw in common["lines"].items():
        own = [
            _rule(r, f"override:{issuer_id}")
            for r in override_lines.get(line_id, {}).get("rules", [])
        ]
        shared = [_rule(r, "common") for r in raw.get("rules") or []]
        lines[line_id] = Line(
            id=line_id,
            label=raw["label"],
            statement=raw["statement"],
            period=raw["period"],
            rules=tuple(own + shared),
            expect=raw.get("expect"),
            applies_to=frozenset(raw["applies_to"]) if raw.get("applies_to") else None,
            optional=bool(raw.get("optional")),
            group=raw.get("group"),
            missing_reason=raw.get("missing_reason"),
        )
    return Mapping(
        lines=lines,
        debt_coverage=common.get("debt_coverage", {}),
        not_applicable=override.get("not_applicable") or {},
    )


def _prior_year_end(end: date) -> date:
    return end.replace(year=end.year - 1, day=28 if end.month == 2 else end.day)


def _in_period(fact: Fact, line: Line, target: date) -> bool:
    if fact.breakdown or abs((fact.end - target).days) > MATCH_TOLERANCE_DAYS:
        return False
    if line.period == "instant":
        return fact.start is None
    if fact.start is None:
        return False
    return DURATION_DAYS[0] <= (fact.end - fact.start).days + 1 <= DURATION_DAYS[1]


def _pick(facts: list[Fact]) -> tuple[Fact, str | None]:
    """The same concept can be tagged twice (statement and note); warn if the values differ."""
    ordered = sorted(facts, key=lambda f: f.fact_id)
    values = {f.value for f in ordered}
    warning = None
    if len(values) > 1:
        warning = f"{ordered[0].concept} tagged with different values: {sorted(values)}"
    return ordered[0], warning


def map_report(
    issuer: Issuer, filing: Filing, report: Report, mapping: Mapping
) -> list[MappedFact]:
    """Values for the filing's own year and for the prior year (comparatives)."""
    unit = f"iso4217:{issuer.currency}"
    by_concept: dict[str, list[Fact]] = {}
    for fact in report.facts:
        by_concept.setdefault(fact.concept, []).append(fact)

    targets = [(filing.fiscal_year, filing.period_end, False)]
    prior_end = _prior_year_end(filing.period_end)
    if prior_end.year >= FIRST_FISCAL_YEAR:
        targets.append((filing.fiscal_year - 1, prior_end, True))

    mapped = []
    for fiscal_year, target, comparative in targets:
        for line in mapping.lines.values():
            if line.applies_to and issuer.type not in line.applies_to:
                continue
            for rule in line.rules:
                if rule.years and fiscal_year not in rule.years:
                    continue
                if rule.from_filing_year and filing.fiscal_year < rule.from_filing_year:
                    continue
                parts, warnings = [], []
                required = rule.concepts + rule.subtract
                for concept in required + rule.add_if_tagged:
                    hits = [
                        f
                        for f in by_concept.get(concept, [])
                        if _in_period(f, line, target) and f.unit == unit
                    ]
                    if not hits:
                        if concept in required:
                            break
                        continue
                    fact, warning = _pick(hits)
                    parts.append(fact)
                    if warning:
                        warnings.append(warning)
                found = {f.concept for f in parts}
                if not set(required) <= found:
                    continue
                tagged = sum(
                    (-f.value if f.concept in rule.subtract else f.value for f in parts),
                    Decimal(0),
                )
                value = tagged * rule.sign
                if line.expect == "positive" and value < 0:
                    warnings.append(f"negative value {value} for a line expected positive")
                decimals = [f.decimals for f in parts if f.decimals is not None]
                mapped.append(
                    MappedFact(
                        issuer=issuer.id,
                        fiscal_year=fiscal_year,
                        period_end=target,
                        line=line.id,
                        value=value,
                        value_tagged=tagged,
                        decimals=min(decimals) if decimals else None,
                        currency=issuer.currency,
                        filing_id=filing.filing_id,
                        comparative=comparative,
                        concepts=tuple(f.tagged_concept for f in parts),
                        fact_ids=tuple(f.fact_id for f in parts),
                        rule_source=rule.source,
                        sign=rule.sign,
                        note=rule.note,
                        footnote=rule.footnote,
                        warnings=tuple(warnings),
                    )
                )
                break
    return mapped


def consolidate(
    issuer: Issuer, mapped: list[MappedFact], filings: list[Filing], mapping: Mapping
) -> tuple[list[MappedFact], list[Gap]]:
    """Choose one value per year and line, flag restatements, and explain every gap."""
    filing_year = {f.filing_id: f.fiscal_year for f in filings}
    groups: dict[tuple[int, str], list[MappedFact]] = {}
    for fact in mapped:
        groups.setdefault((fact.fiscal_year, fact.line), []).append(fact)

    facts = []
    for group in groups.values():
        ordered = sorted(group, key=lambda f: filing_year[f.filing_id], reverse=True)
        latest = ordered[0]
        restated, older = False, []
        for fact in ordered[1:]:
            if _same_amount(fact, latest):
                older.append(fact)
            elif fact.value == -latest.value:
                warning = "tagged with the opposite sign in this filing (same amount)"
                older.append(replace(fact, warnings=fact.warnings + (warning,)))
            else:
                restated = True
                older.append(fact)
        facts.append(replace(latest, primary=True, restated=restated))
        facts.extend(replace(f, primary=False, restated=restated) for f in older)

    years = sorted({f.fiscal_year for f in facts})
    present = {(f.fiscal_year, f.line) for f in facts}
    gaps = []
    for year in years:
        for line in mapping.lines.values():
            if line.applies_to and issuer.type not in line.applies_to:
                continue
            if (year, line.id) in present:
                continue
            reason, counts = _gap_reason(issuer, year, line, present, mapping)
            gaps.append(Gap(issuer.id, year, line.id, reason, counts))
    facts.sort(
        key=lambda f: (f.fiscal_year, list(mapping.lines).index(f.line), -filing_year[f.filing_id])
    )
    return facts, gaps


def _same_amount(a: MappedFact, b: MappedFact) -> bool:
    """Equal within the rounding of the less precise figure (millions vs hundred-thousands).
    A line added up from several tagged parts carries the rounding of each part."""
    known = [d for d in (a.decimals, b.decimals) if d is not None]
    if not known:
        return a.value == b.value
    parts = max(len(a.concepts), len(b.concepts))
    return abs(a.value - b.value) <= parts * Decimal(10) ** (-min(known)) / 2


def _gap_reason(
    issuer: Issuer, year: int, line: Line, present: set, mapping: Mapping
) -> tuple[str, bool]:
    if line.id in mapping.not_applicable:
        return mapping.not_applicable[line.id], False
    if line.group == "debt":
        if (year, "debt_including_leases") in present:
            return mapping.debt_coverage["debt_including_leases"], False
        lease_line = line.id.startswith("lease_liabilities")
        if lease_line and issuer.leases_in_borrowings:
            return mapping.debt_coverage["leases_in_borrowings"], False
        if line.id.endswith("_total") and (
            (year, line.id.replace("_total", "_current")) in present
            and (year, line.id.replace("_total", "_noncurrent")) in present
        ):
            return "Reported as current and non-current parts only.", False
        if line.id in ("borrowings_current", "borrowings_noncurrent") and (
            (year, "borrowings_total") in present
        ):
            return "Reported as a total only.", False
        if lease_line and (year, "lease_liabilities_total") in present:
            return "Reported as a total only.", False
    if line.optional:
        return "Not reported by this issuer.", False
    return line.missing_reason or "Not tagged in the filing.", True
