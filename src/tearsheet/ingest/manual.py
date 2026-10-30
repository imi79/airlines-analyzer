"""Filings loaded by hand: ESEF packages the database doesn't have (decision 0004, choice 4b).

Each package is listed in filings/manual.yaml with where it came from, and its converted
xBRL-JSON (gzipped) sits next to it in filings/. The package's own SHA-256 is recorded, so the
facts can be traced to the exact file the company published.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from tearsheet.config import MANUAL_FILINGS, Issuer
from tearsheet.ingest.filings import Filing

REGISTER = MANUAL_FILINGS / "manual.yaml"


def manual_filings(
    issuer: Issuer, register: Path | None = None, folder: Path | None = None
) -> list[Filing]:
    register = register or REGISTER
    folder = folder or MANUAL_FILINGS
    if not register.exists():
        return []
    entries = yaml.safe_load(register.read_text()).get("filings") or []
    filings = []
    for entry in entries:
        if entry["issuer"] != issuer.id:
            continue
        end = date.fromisoformat(str(entry["period_end"]))
        filings.append(
            Filing(
                filing_id=entry["filing_id"],
                issuer=issuer.id,
                fiscal_year=end.year,
                period_end=end,
                origin=entry["origin"],
                sha256=entry["package_sha256"],
                json_url=None,
                viewer_url=None,
                report_url=None,
                package_url=entry.get("source_url"),
                error_count=entry.get("error_count"),
                date_added=str(entry["downloaded_on"]),
                local_json=str(folder / entry["xbrl_json"]),
            )
        )
    return filings
