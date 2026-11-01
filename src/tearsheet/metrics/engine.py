"""Compute every catalog metric for an issuer, year by year, from its primary facts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

import yaml

from tearsheet.config import CONFIG, Issuer
from tearsheet.metrics.formulas import FORMULAS, Context, Input, Missing, NotMeaningful
from tearsheet.normalize.mapper import CONCEPT_MAP, MappedFact

CATALOG = Path(__file__).with_name("catalog.yaml")
SETTINGS = CONFIG / "metric_settings.yaml"
NEEDS_M3 = "Needs figures extracted from the report text (M3)."


@dataclass(frozen=True)
class Result:
    issuer: str
    fiscal_year: int
    period_end: date
    metric: str
    value: Decimal | None
    kind: str  # value | missing | not_meaningful | needs_m3
    reason: str | None
    note: str | None  # what was used, in plain words
    inputs: tuple[Input, ...]
    status: str  # verified only if every input is verified


def load_catalog(path: Path = CATALOG) -> dict[str, dict]:
    return yaml.safe_load(path.read_text())["metrics"]


def load_settings(issuer: Issuer, path: Path = SETTINGS) -> dict:
    settings = dict(yaml.safe_load(path.read_text())["issuers"][issuer.id])
    settings["leases_in_borrowings"] = issuer.leases_in_borrowings
    return settings


def labels(catalog: dict[str, dict]) -> dict[str, str]:
    lines = yaml.safe_load(CONCEPT_MAP.read_text())["lines"]
    return {k: v["label"] for k, v in lines.items()} | {k: v["label"] for k, v in catalog.items()}


def compute(
    issuer: Issuer,
    facts: list[MappedFact],
    catalog: dict | None = None,
    settings: dict | None = None,
) -> list[Result]:
    catalog = catalog or load_catalog()
    settings = settings if settings is not None else load_settings(issuer)
    names = labels(catalog)
    primary = [f for f in facts if f.primary]
    by_year: dict[int, dict[str, MappedFact]] = {}
    for fact in primary:
        by_year.setdefault(fact.fiscal_year, {})[fact.line] = fact

    results = []
    for year in sorted(by_year):
        lines = by_year[year]
        period_end = max(f.period_end for f in lines.values())
        ctx = Context(issuer.type, year, lines, names, settings)
        for metric_id, spec in catalog.items():
            if spec.get("applies_to") and issuer.type not in spec["applies_to"]:
                continue
            if spec.get("needs") == "M3":
                result = Result(
                    issuer.id,
                    year,
                    period_end,
                    metric_id,
                    None,
                    "needs_m3",
                    NEEDS_M3,
                    None,
                    (),
                    "verified",
                )
            else:
                result = _run(issuer, year, period_end, metric_id, ctx)
            ctx.results[metric_id] = result
            results.append(result)
    return results


def _run(issuer: Issuer, year: int, period_end: date, metric_id: str, ctx: Context) -> Result:
    ctx.used = []
    try:
        value, note = FORMULAS[metric_id](ctx)
        kind, reason = "value", None
    except Missing as missing:
        value, note, kind, reason = None, None, "missing", str(missing)
    except NotMeaningful as nm:
        value, note, kind, reason = None, None, "not_meaningful", f"n.m.: {nm}"
    inputs = tuple(ctx.used)
    ok = ("verified", "overridden")  # an override carries Imane's name, date and reason
    status = "verified" if all(i.status in ok for i in inputs) else "unverified"
    return Result(issuer.id, year, period_end, metric_id, value, kind, reason, note, inputs, status)
