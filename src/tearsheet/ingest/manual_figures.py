"""Figures entered by hand from published statements (decision 0007).

Each document in config/manual_figures.yaml becomes a pseudo-filing, and its lines become facts
with source type "manual". They are "unverified" until the entries have been reviewed. The
prior-year column of each document is not loaded; it is a control against the figures the
database already holds for that year.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

import yaml

from tearsheet.config import CONFIG, Issuer
from tearsheet.ingest.filings import Filing
from tearsheet.normalize.mapper import MappedFact

MANUAL_FIGURES = CONFIG / "manual_figures.yaml"
ORIGIN = "published statements (PDF), entered by hand"


@dataclass(frozen=True)
class Control:
    issuer: str
    fiscal_year: int
    line: str
    printed: Decimal  # prior-year figure as printed in the document (full units)
    page: int


def _documents(issuer: Issuer, path: Path) -> list[dict]:
    if not path.exists():
        return []
    docs = yaml.safe_load(path.read_text()).get("documents") or []
    return [d for d in docs if d["issuer"] == issuer.id]


def manual_figures(
    issuer: Issuer, path: Path = MANUAL_FIGURES
) -> tuple[list[Filing], list[MappedFact], list[Control]]:
    filings, facts, controls = [], [], []
    for doc in _documents(issuer, path):
        end = date.fromisoformat(str(doc["period_end"]))
        filing_id = f"{issuer.lei}-{end.isoformat()}-manual-pdf"
        filings.append(
            Filing(
                filing_id=filing_id,
                issuer=issuer.id,
                fiscal_year=int(doc["fiscal_year"]),
                period_end=end,
                origin=ORIGIN,
                sha256=doc["sha256"],
                json_url=None,
                viewer_url=None,
                report_url=None,
                package_url=doc["file"],
                error_count=None,
                date_added=str(doc["entered_on"]),
                language=None,
                choice_reason=f"{doc['document']}; entered by {doc['entered_by']}",
            )
        )
        scale = Decimal(str(doc["scale"]))
        decimals = -(len(str(doc["scale"])) - 1)
        pending = set(doc.get("pending_review") or [])
        as_fact = set(doc.get("prior_year_as_fact") or [])
        footnotes = doc.get("footnotes") or {}
        prior_end = end.replace(year=end.year - 1)
        for line, (value, prior, page, label) in doc["lines"].items():
            reviewed = doc.get("reviewed_by") and line not in pending
            years = [(int(doc["fiscal_year"]), end, value, False)]
            if line in as_fact:
                years.append((prior_end.year, prior_end, prior, True))
            else:
                controls.append(
                    Control(issuer.id, prior_end.year, line, _amount(prior, scale), page)
                )
            for fiscal_year, period_end, raw, comparative in years:
                amount = _amount(raw, scale)
                facts.append(
                    MappedFact(
                        issuer=issuer.id,
                        fiscal_year=fiscal_year,
                        period_end=period_end,
                        line=line,
                        value=amount,
                        value_tagged=amount,
                        decimals=decimals,
                        currency=issuer.currency,
                        filing_id=filing_id,
                        comparative=comparative,
                        concepts=(label,),
                        fact_ids=(f"page {page}",),
                        rule_source="manual",
                        sign=1,
                        note=f"Entered by hand from the published statements, page {page}"
                        + (f" ({_parts(raw)})." if isinstance(raw, list) else "."),
                        footnote=footnotes.get(line),
                        source_type="manual",
                        status="verified" if reviewed else "unverified",
                    )
                )
    return filings, facts, controls


def _amount(raw, scale: Decimal) -> Decimal:
    """A printed amount, or the sum of a list of printed amounts, in full units."""
    parts = raw if isinstance(raw, list) else [raw]
    return sum((Decimal(str(p)) for p in parts), Decimal(0)) * scale


def _parts(raw: list) -> str:
    return " + ".join(f"{p:,}" for p in raw)
