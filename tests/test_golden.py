"""Every v1 issuer's mapped statement lines, rebuilt from recorded fixtures, must match the
golden files exactly. A diff means a mapping change: review it, then rebuild the golden files
with `uv run python -m tests.fixtures.build`."""

import csv
import json
from dataclasses import fields
from datetime import date

import pytest

from tearsheet.config import load_issuers
from tearsheet.ingest.filings import Filing
from tearsheet.normalize.mapper import consolidate, load_mapping, map_report
from tests.fixtures.build import FIXTURES, GOLDEN, golden_rows

ISSUERS = {issuer.id: issuer for issuer in load_issuers()}


def recorded_filings(issuer_id: str) -> list[Filing]:
    folder = FIXTURES / issuer_id
    names = {f.name for f in fields(Filing)}
    filings = []
    for record in json.loads((folder / "filings.json").read_text()):
        record = {k: v for k, v in record.items() if k in names}
        record["period_end"] = date.fromisoformat(record["period_end"])
        record["local_json"] = str(folder / record["local_json"])
        filings.append(Filing(**record))
    return filings


@pytest.mark.parametrize("issuer_id", sorted(ISSUERS))
def test_mapped_lines_match_golden_file(issuer_id):
    issuer = ISSUERS[issuer_id]
    mapping = load_mapping(issuer_id)
    filings = recorded_filings(issuer_id)
    mapped = [m for f in filings for m in map_report(issuer, f, f.report(None), mapping)]
    facts, _ = consolidate(issuer, mapped, filings, mapping)
    actual = [{k: str(v) for k, v in row.items()} for row in golden_rows(facts)]
    with (GOLDEN / f"{issuer_id}.csv").open() as f:
        expected = list(csv.DictReader(f))
    assert actual == expected


@pytest.mark.parametrize("issuer_id", sorted(ISSUERS))
def test_no_core_line_missing_without_a_stated_reason(issuer_id):
    issuer = ISSUERS[issuer_id]
    mapping = load_mapping(issuer_id)
    filings = recorded_filings(issuer_id)
    mapped = [m for f in filings for m in map_report(issuer, f, f.report(None), mapping)]
    _, gaps = consolidate(issuer, mapped, filings, mapping)
    assert all(g.reason for g in gaps)
