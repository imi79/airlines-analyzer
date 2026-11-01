"""Run extraction for one issuer: its reports, the AI reading, the checks, one value per year.

`tearsheet load` uses recorded AI answers only (no API call, no cost); `tearsheet extract`
asks the model for any report without a recorded answer. Either way every figure goes through
the same checks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from tearsheet.config import FIRST_FISCAL_YEAR, Issuer
from tearsheet.extract.consolidate import (
    Candidate,
    apply_reviews,
    build_candidates,
    cross_check,
    load_reviews,
    to_facts,
    with_model,
)
from tearsheet.extract.documents import Document, from_report, supplied_documents
from tearsheet.extract.extractor import (
    DocumentRun,
    extract_document,
    load_factor_basis,
    load_scopes,
)
from tearsheet.extract.fx import Converter
from tearsheet.extract.locator import items_for
from tearsheet.ingest.client import Client
from tearsheet.ingest.filings import Filing
from tearsheet.llm import LLM
from tearsheet.normalize.mapper import MappedFact


@dataclass
class IssuerExtraction:
    issuer: Issuer
    facts: list[MappedFact] = field(default_factory=list)
    runs: list[DocumentRun] = field(default_factory=list)
    candidates: list[Candidate] = field(default_factory=list)
    skipped: list[tuple[str, int, str]] = field(default_factory=list)  # doc, year, reason
    unmatched_reviews: list[str] = field(default_factory=list)


def period_end(issuer: Issuer, year: int) -> date:
    month, day = (int(x) for x in issuer.fiscal_year_end.split("-"))
    return date(year, month, day)


def documents_for(
    issuer: Issuer, filings: list[Filing], client: Client
) -> tuple[list[Document], list[tuple[str, int, str]]]:
    docs, skipped = [], []
    for f in filings:
        if not f.report_url:
            continue
        try:
            path = client.download(f.report_url, "report")
        except FileNotFoundError:
            skipped.append((f.filing_id, f.fiscal_year, "report not downloaded (offline)"))
            continue
        docs.append(
            from_report(
                f.filing_id, issuer.id, f.fiscal_year, f.language, path, f.report_url, f.sha256
            )
        )
    docs.extend(supplied_documents(issuer.id))
    return docs, skipped


def extract_issuer(
    issuer: Issuer,
    filings: list[Filing],
    facts: list[MappedFact],
    llm: LLM,
    client: Client,
    convert: Converter | None,
    reviews: list[dict] | None = None,
) -> IssuerExtraction:
    out = IssuerExtraction(issuer)
    items = items_for(issuer.type)
    scopes = load_scopes().get(issuer.id, {})
    revenue = {f.fiscal_year: f.value for f in facts if f.primary and f.line == "revenue"}
    docs, out.skipped = documents_for(issuer, filings, client)
    for doc in docs:
        out.runs.append(extract_document(llm, issuer, doc, revenue, items, scopes))
    figures = [f for run in out.runs for f in run.figures]
    years = {f.fiscal_year for f in figures} | {d.fiscal_year for d in docs}
    # Figures for years before the v1 range (the FY2020 comparatives in the FY2021 report)
    # serve the cross-checks only; they are not stored as facts.
    ends = {y: period_end(issuer, y) for y in years if y >= FIRST_FISCAL_YEAR}
    out.candidates = build_candidates(figures, issuer, items, ends, revenue, convert)
    cross_check(out.candidates, items, load_factor_basis(issuer.id))
    out.unmatched_reviews = apply_reviews(
        issuer, out.candidates, load_reviews() if reviews is None else reviews
    )
    models = {
        run.doc.doc_id: {
            "provider": run.result.provider,
            "model": run.result.model,
            "prompt_version": run.result.prompt_version,
            "request_hash": run.result.request_hash,
        }
        for run in out.runs
        if run.result is not None
    }
    out.facts = with_model(to_facts(issuer, out.candidates, ends, scopes), models)
    return out
