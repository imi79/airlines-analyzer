"""Find each issuer's annual filings and choose one per fiscal year."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from tearsheet.config import FIRST_FISCAL_YEAR, Issuer
from tearsheet.ingest.client import Client
from tearsheet.ingest.xbrl_json import Report, load_report

DATABASE = "filings.xbrl.org"


@dataclass(frozen=True)
class Filing:
    filing_id: str
    issuer: str
    fiscal_year: int
    period_end: date
    origin: str  # filings.xbrl.org, or the company website for a package loaded by hand
    sha256: str | None
    json_url: str | None
    viewer_url: str | None
    report_url: str | None
    package_url: str | None
    error_count: int | None
    date_added: str | None
    language: str | None = None
    choice_reason: str = ""
    local_json: str | None = None  # xBRL-JSON on disk, for packages loaded by hand

    def report(self, client: Client) -> Report:
        if self.local_json:
            return load_report(Path(self.local_json))
        return load_report(client.download(self.json_url, "xbrl-json"))


def list_filings(client: Client, issuer: Issuer) -> list[Filing]:
    """Annual filings from FIRST_FISCAL_YEAR whose period ends on the issuer's year-end date."""
    filings = []
    for item in client.get_all(f"/api/entities/{issuer.lei}/filings"):
        f = item["attributes"]
        period_end = f.get("period_end")
        if not period_end or not f.get("json_url"):
            continue
        end = date.fromisoformat(period_end[:10])
        if end.year < FIRST_FISCAL_YEAR or period_end[5:10] != issuer.fiscal_year_end:
            continue  # out of scope, or an interim report
        filings.append(
            Filing(
                filing_id=f.get("fxo_id") or item["id"],
                issuer=issuer.id,
                fiscal_year=end.year,
                period_end=end,
                origin=DATABASE,
                sha256=f.get("sha256"),
                json_url=f.get("json_url"),
                viewer_url=f.get("viewer_url"),
                report_url=f.get("report_url"),
                package_url=f.get("package_url"),
                error_count=f.get("error_count"),
                date_added=f.get("date_added"),
            )
        )
    return filings


def choose(client: Client, filings: list[Filing]) -> list[Filing]:
    """One filing per fiscal year: English first, then fewest errors, then most recently added."""
    by_year: dict[int, list[Filing]] = {}
    for filing in filings:
        by_year.setdefault(filing.fiscal_year, []).append(filing)
    chosen = []
    for year in sorted(by_year):
        group = by_year[year]
        group = [replace(f, language=f.report(client).language) for f in group]
        ordered = sorted(group, key=lambda f: f.date_added or "", reverse=True)
        ordered = sorted(ordered, key=lambda f: f.error_count or 0)
        if len(group) > 1:
            ordered = sorted(ordered, key=lambda f: f.language != "en")
        best = ordered[0]
        if len(group) == 1:
            reason = "only filing"
        else:
            reason = (
                f"{len(group)} filings: chose language={best.language}, "
                f"errors={best.error_count}, added={best.date_added}"
            )
        chosen.append(replace(best, choice_reason=reason))
    return chosen
