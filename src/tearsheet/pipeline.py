"""Load every v1 issuer's filings into the facts database."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tearsheet.config import DB_PATH, Issuer, load_issuers
from tearsheet.extract import half_year
from tearsheet.extract.extractor import fiscal_label
from tearsheet.extract.fx import ecb_month_end
from tearsheet.extract.maturity import MaturityRun
from tearsheet.extract.maturity import read_issuer as read_maturity
from tearsheet.extract.run import IssuerExtraction, documents_for, extract_issuer
from tearsheet.ingest.client import Client
from tearsheet.ingest.filings import Filing, choose, list_filings
from tearsheet.ingest.manual import manual_filings
from tearsheet.ingest.manual_figures import Control, manual_figures
from tearsheet.llm import LLM
from tearsheet.metrics.engine import Result, compute, load_catalog
from tearsheet.metrics.ltm import InterimLoad
from tearsheet.metrics.ltm import build as build_ltm
from tearsheet.normalize.mapper import Gap, MappedFact, consolidate, load_mapping, map_report
from tearsheet.store import db


@dataclass
class IssuerLoad:
    issuer: Issuer
    filings: list[Filing]
    facts: list[MappedFact]
    gaps: list[Gap]
    controls: list[Control]
    metrics: list[Result]
    extraction: IssuerExtraction | None = None
    maturity: list[MaturityRun] | None = None  # the debt maturity wall (M8)
    interim: InterimLoad | None = None  # half-year and LTM figures (M10)


def load_issuer(client: Client, issuer: Issuer, llm: LLM | None = None) -> tuple[IssuerLoad, dict]:
    """Map one issuer, then add the figures read from its report text (if `llm` is given).
    Returns the result and each filing's parsed report."""
    filings = choose(client, list_filings(client, issuer) + manual_filings(issuer))
    mapping = load_mapping(issuer.id)
    reports, mapped = {}, []
    for filing in filings:
        report = filing.report(client)
        reports[filing.filing_id] = report
        mapped.extend(map_report(issuer, filing, report, mapping))
    hand_filings, hand_facts, controls = manual_figures(issuer)
    filings, mapped = filings + hand_filings, mapped + hand_facts
    facts, gaps = consolidate(issuer, mapped, filings, mapping)
    extraction, maturity = None, None
    if llm is not None:
        extraction = extract_issuer(issuer, filings, facts, llm, client, ecb_month_end(client))
        facts = facts + extraction.facts
        docs, _ = documents_for(issuer, filings, client)
        maturity, wall = read_maturity(issuer, docs, facts, llm, fiscal_label)
        facts = facts + wall
    metrics = compute(issuer, facts)
    interim = None
    report = half_year.report_for(issuer.id)
    if llm is not None and report is not None:
        # M10: the latest half-year report, read beside the fiscal years (never into them).
        run = half_year.read_report(llm, issuer, report, facts, docs)
        interim = build_ltm(issuer, run, facts)
    load = IssuerLoad(
        issuer, filings, facts, gaps, controls, metrics, extraction, maturity, interim
    )
    return load, reports


def load_all(
    client: Client, db_path: Path = DB_PATH, llm: LLM | None = None, only: set[str] | None = None
) -> list[IssuerLoad]:
    """Rebuild the database. Without `llm`, figures are read from recorded AI answers only
    (no API call). `only` limits live AI calls to some issuers; the others use records."""
    con = db.create(db_path)
    units = {k: v["unit"] for k, v in load_catalog().items()}
    recorded = LLM(offline=True)
    results = []
    for issuer in load_issuers():
        use = llm if llm is not None and (not only or issuer.id in only) else recorded
        result, reports = load_issuer(client, issuer, use)
        db.write_filings(con, result.filings)
        for filing in result.filings:
            if filing.filing_id in reports:  # entered-by-hand documents have no tagged facts
                db.write_raw_facts(con, filing.filing_id, reports[filing.filing_id].facts)
        hashes = {f.filing_id: f.sha256 for f in result.filings}
        db.write_facts(con, result.facts, hashes)
        db.write_gaps(con, result.gaps)
        db.write_metrics(con, result.metrics, result.issuer.currency, units)
        if result.extraction is not None:
            db.write_extraction(con, result.extraction)
        if result.maturity is not None:
            db.write_maturity(con, result.issuer.id, result.maturity)
        if result.interim is not None:
            db.write_interim(con, result.interim, result.issuer.currency, units)
        results.append(result)
    con.close()
    return results
