"""Last-twelve-months figures (M10, decision 0025).

For a line of the income statement or the cash flow statement:

    LTM = last full fiscal year + the first half just ended - the same half a year before

For a balance sheet line, the figure at the half-year date. The catalog's formulas then run on
these figures unchanged (EBITDA, net debt, leverage, coverage...), so net leverage at LTM is net
debt at the half-year date over the EBITDA of the last twelve months.

An LTM figure is verified only if its three parts are. A line the full year holds but the
half-year report does not give makes the metrics that need it missing, with the reason; it is
never counted as zero. Nothing here touches the fiscal-year figures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from tearsheet.config import Issuer
from tearsheet.extract import half_year
from tearsheet.extract.half_year import HalfYearRun, Report
from tearsheet.metrics.engine import Result, _run, labels, load_catalog, load_settings
from tearsheet.metrics.formulas import Context, m
from tearsheet.normalize.mapper import MappedFact

OK = ("verified", "overridden")
NOT_AT_HALF_YEAR = "half-year reports are condensed and do not give it"


class Reasons(dict):
    """Why a line is missing at LTM; any line not read at the half year has the same reason."""

    def __contains__(self, key) -> bool:
        return True

    def __getitem__(self, key) -> str:
        return self.get(key, NOT_AT_HALF_YEAR)


@dataclass
class InterimLoad:
    report: Report
    run: HalfYearRun
    h1: list[MappedFact] = field(default_factory=list)  # H1 and H1_prior lines
    ltm: list[MappedFact] = field(default_factory=list)
    metrics: list[Result] = field(default_factory=list)
    gaps: dict[str, str] = field(default_factory=dict)  # line -> why there is no LTM figure


def ltm_lines(
    issuer: Issuer,
    report: Report,
    h1: list[MappedFact],
    base: dict[str, MappedFact],
    statements: dict[str, str],
) -> tuple[list[MappedFact], dict[str, str]]:
    """`h1`: the facts of half_year.to_facts; `base`: the last full year's primary lines;
    `statements`: line -> income | balance | cash_flow."""
    current = {f.line: f for f in h1 if f.rule_source == "H1"}
    prior = {f.line: f for f in h1 if f.rule_source == "H1_prior"}
    year = f"FY{report.base_fiscal_year}"
    out, gaps = [], {}
    for line, now in current.items():
        if statements.get(line) == "balance":
            parts = [{"period": "H1", "line": line, "value": str(now.value)}]
            value, status = now.value, now.status
            note = f"At {report.period_end.isoformat()}: {m(value)} (half-year balance sheet)"
            concepts = now.concepts
        else:
            full, before = base.get(line), prior.get(line)
            if full is None or before is None:
                gaps[line] = (
                    f"no {year} figure in the database"
                    if full is None
                    else "the same half a year before was not read"
                )
                continue
            value = full.value + now.value - before.value
            status = (
                "verified"
                if all(s in OK for s in (full.status, now.status, before.status))
                else "unverified"
            )
            parts = [
                {"period": year, "line": line, "value": str(full.value), "sign": "+"},
                {"period": "H1", "line": line, "value": str(now.value), "sign": "+"},
                {"period": "H1_prior", "line": line, "value": str(before.value), "sign": "-"},
            ]
            note = (
                f"{year} {m(full.value)} + first half to {report.period_end.isoformat()} "
                f"{m(now.value)} − first half to {report.prior_end.isoformat()} "
                f"{m(before.value)} = {m(value)}"
            )
            concepts = full.concepts  # where interest paid sits follows the annual statement
        out.append(
            MappedFact(
                issuer=issuer.id,
                fiscal_year=report.period_end.year,
                period_end=report.period_end,
                line=line,
                value=value,
                value_tagged=value,
                decimals=now.decimals,
                currency=issuer.currency,
                filing_id=report.id,
                comparative=False,
                concepts=concepts,
                fact_ids=(),
                rule_source="LTM",
                sign=1,
                note=note,
                warnings=now.warnings,
                source_type="computed",
                status=status,
                ref={"formula": "ltm", "parts": parts, "audit": report.audit},
            )
        )
    return out, gaps


def build(
    issuer: Issuer,
    run: HalfYearRun,
    facts: list[MappedFact],
    catalog: dict | None = None,
    settings: dict | None = None,
    hy_settings: dict | None = None,
) -> InterimLoad:
    """The half-year facts, the LTM lines and every catalog metric at LTM for one company."""
    report = run.report
    load = InterimLoad(report, run)
    catalog = catalog or load_catalog()
    settings = settings if settings is not None else load_settings(issuer)
    hy = hy_settings or half_year.load_settings()
    statements = {k: v["statement"] for k, v in hy["lines"].items()}
    base = {f.line: f for f in facts if f.primary and f.fiscal_year == report.base_fiscal_year}
    load.h1 = half_year.to_facts(issuer, run)
    load.ltm, load.gaps = ltm_lines(issuer, report, load.h1, base, statements)
    reasons = Reasons(load.gaps)
    for line, why in run.not_found.items():
        reasons[line] = f"not in the half-year statements ({why})"
    if run.error:
        for line in base:
            reasons.setdefault(line, run.error)
    for x in run.lines:
        if not x.complete and not x.line.startswith("control_"):
            reasons[x.line] = "; ".join(x.failures) or "not read"
    lines = {f.line: f for f in load.ltm}
    names = labels(catalog)
    ctx = Context(
        issuer.type,
        report.base_fiscal_year + 1,
        lines,
        names,
        settings,
        prior=base,
        period_label=report.ltm_label,
        reasons=reasons,
    )
    for metric_id, spec in catalog.items():
        if spec.get("applies_to") and issuer.type not in spec["applies_to"]:
            continue
        if spec.get("needs") == "M3":
            continue
        result = _run(issuer, report.period_end.year, report.period_end, metric_id, ctx)
        ctx.results[metric_id] = result
        load.metrics.append(result)
    return load


def as_decimal(value) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))
