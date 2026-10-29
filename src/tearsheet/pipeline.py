"""Load every v1 issuer's filings into the facts database."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tearsheet.config import DB_PATH, Issuer, load_issuers
from tearsheet.ingest.client import Client
from tearsheet.ingest.filings import Filing, choose, list_filings
from tearsheet.ingest.manual import manual_filings
from tearsheet.normalize.mapper import Gap, MappedFact, consolidate, load_mapping, map_report
from tearsheet.store import db


@dataclass
class IssuerLoad:
    issuer: Issuer
    filings: list[Filing]
    facts: list[MappedFact]
    gaps: list[Gap]


def load_issuer(client: Client, issuer: Issuer) -> tuple[IssuerLoad, dict]:
    """Map one issuer. Returns the result and each filing's parsed report."""
    filings = choose(client, list_filings(client, issuer) + manual_filings(issuer))
    mapping = load_mapping(issuer.id)
    reports, mapped = {}, []
    for filing in filings:
        report = filing.report(client)
        reports[filing.filing_id] = report
        mapped.extend(map_report(issuer, filing, report, mapping))
    facts, gaps = consolidate(issuer, mapped, filings, mapping)
    return IssuerLoad(issuer, filings, facts, gaps), reports


def load_all(client: Client, db_path: Path = DB_PATH) -> list[IssuerLoad]:
    con = db.create(db_path)
    results = []
    for issuer in load_issuers():
        result, reports = load_issuer(client, issuer)
        db.write_filings(con, result.filings)
        for filing in result.filings:
            db.write_raw_facts(con, filing.filing_id, reports[filing.filing_id].facts)
        hashes = {f.filing_id: f.sha256 for f in result.filings}
        db.write_facts(con, result.facts, hashes)
        db.write_gaps(con, result.gaps)
        results.append(result)
    con.close()
    return results
