"""The ratings box (M8, decision 0022): credit ratings entered by hand, with source and date.

Each entry in `config/ratings.yaml` is copied from the company's own annual report: the agency,
the long-term rating, the outlook, the date the report gives them at, and the exact sentence.
Code checks that the sentence is in the report word for word and that it shows each agency's
name and rating; Imane reviews every entry. Until both hold, the entry stays off the page.

The box is a record of a public rating, not an opinion: it is never ranked or compared, and it
is flagged when older than twelve months. No agency research is reproduced (spec, legal).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from tearsheet.config import CONFIG

RATINGS = CONFIG / "ratings.yaml"
STALE_DAYS = 365
AGENCY_NAMES = {
    "S&P": ["S&P", "Standard & Poor", "Standard and Poor", "S&P Global"],
    "Moody's": ["Moody"],
    "Fitch": ["Fitch"],
}
SCALES = {
    "S&P": r"(?:AAA|AA|A|BBB|BB|B|CCC)[+-]?",
    "Fitch": r"(?:AAA|AA|A|BBB|BB|B|CCC)[+-]?",
    "Moody's": r"(?:Aaa|Aa[1-3]|A[1-3]|Baa[1-3]|Ba[1-3]|B[1-3]|Caa[1-3])",
}
OUTLOOKS = ("stable", "positive", "negative", "developing", "watch positive", "watch negative")
NOT_REVIEWED = "not reviewed yet: waiting for Imane's review"


@dataclass(frozen=True)
class Rating:
    agency: str
    rating: str
    outlook: str | None


@dataclass
class RatingEntry:
    issuer: str
    as_at: date
    ratings: list[Rating]
    document: str  # the report's filing id, or a supplied PDF's id
    fiscal_year: int
    location: str
    quote: str
    entered_by: str
    entered_on: date
    reviewed_by: str | None
    not_stated: bool = False  # the report gives no rating (not a claim that none exists)
    scope: str = "issuer"
    comment: str | None = None
    failures: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        if self.failures:
            return "unverified"
        return "verified" if self.reviewed_by else "unverified"

    @property
    def reason(self) -> str | None:
        if self.failures:
            return "; ".join(self.failures)
        return None if self.reviewed_by else NOT_REVIEWED

    def stale(self, today: date) -> bool:
        return (today - self.as_at).days > STALE_DAYS

    def text(self) -> str:
        """'S&P BBB+ (stable), Moody's Baa2 (stable)', or that the report gives none."""
        if self.not_stated:
            return f"No rating given in the FY{self.fiscal_year} annual report"
        return ", ".join(
            f"{r.agency} {r.rating}" + (f" ({r.outlook})" if r.outlook else "")
            for r in self.ratings
        )


def load_entries(path: Path = RATINGS) -> list[RatingEntry]:
    data = yaml.safe_load(path.read_text()) or {}
    out = []
    for issuer, e in (data.get("issuers") or {}).items():
        ratings = [
            Rating(r["agency"], r["rating"], r.get("outlook")) for r in e.get("ratings") or []
        ]
        out.append(
            RatingEntry(
                issuer=issuer,
                as_at=e["as_at"],
                ratings=ratings,
                document=e["document"],
                fiscal_year=int(e["fiscal_year"]),
                location=e["location"],
                quote=" ".join(e["quote"].split()),
                entered_by=e["entered_by"],
                entered_on=e["entered_on"],
                reviewed_by=e.get("reviewed_by"),
                not_stated=bool(e.get("not_stated")),
                scope=e.get("scope") or "issuer",
                comment=e.get("comment"),
            )
        )
    return out


def check_entry(entry: RatingEntry, report_text: str | None) -> RatingEntry:
    """The quote is in the report word for word, and names each agency, rating and outlook."""
    entry.failures = []
    if entry.not_stated:
        return entry  # nothing to find: Imane's review confirms the report gives no rating
    if report_text is None:
        entry.failures.append("the report is not available to check the quote against")
        return entry
    flat = _squash(report_text)
    if _squash(entry.quote) not in flat:
        entry.failures.append("quote not found word for word in the report")
        return entry
    for r in entry.ratings:
        if r.agency not in SCALES:
            entry.failures.append(f"unknown agency '{r.agency}'")
            continue
        if not re.fullmatch(SCALES[r.agency], r.rating):
            entry.failures.append(f"'{r.rating}' is not on the {r.agency} rating scale")
        if not any(name.lower() in entry.quote.lower() for name in AGENCY_NAMES[r.agency]):
            entry.failures.append(f"the quote does not name {r.agency}")
        if not re.search(rf"(?<![A-Za-z]){re.escape(r.rating)}(?![A-Za-z0-9+-])", entry.quote):
            entry.failures.append(f"the quote does not show the {r.agency} rating {r.rating}")
        if r.outlook and r.outlook.lower() not in OUTLOOKS:
            entry.failures.append(f"unknown outlook '{r.outlook}'")
        elif r.outlook:
            stem = r.outlook.lower().split()[-1][:6]  # stable, positi, negati (any language)
            words = entry.quote.lower().replace("é", "e")
            if stem not in words:
                entry.failures.append(f"the quote does not show the {r.outlook} outlook")
    return entry


def _squash(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", "", text).lower()


def report_text(document: str, db_path=None) -> str | None:
    """The text of the report a rating was copied from (cached by `tearsheet load`)."""
    import duckdb

    from tearsheet.config import DB_PATH
    from tearsheet.extract.documents import from_report
    from tearsheet.ingest.client import Client

    con = duckdb.connect(str(db_path or DB_PATH), read_only=True)
    row = con.execute(
        "SELECT issuer, fiscal_year, language, report_url, sha256 FROM filings "
        "WHERE filing_id = ? AND report_url IS NOT NULL",
        [document],
    ).fetchone()
    con.close()
    if row is None:
        return None
    issuer, year, language, url, sha = row
    try:
        path = Client(offline=True).download(url, "report")
    except FileNotFoundError:
        return None
    return from_report(document, issuer, year, language, path, url, sha).text


def checked_entries(db_path=None, path: Path = RATINGS) -> dict[str, RatingEntry]:
    """Every entry, checked against its report."""
    return {e.issuer: check_entry(e, report_text(e.document, db_path)) for e in load_entries(path)}


def record(issuer: str, today: date, db_path=None) -> dict | None:
    """What the tearsheet header shows for the company (stored with the pre-built tearsheets,
    so the demo needs no report): the ratings once reviewed, else "awaiting review"."""
    entries = checked_entries(db_path)
    e = entries.get(issuer)
    if e is None:
        return None
    shown = e.status == "verified"
    return {
        "text": e.text() if shown else "awaiting review",
        "status": e.status,
        "reason": e.reason,
        "as_at": str(e.as_at),
        "stale": shown and not e.not_stated and e.stale(today),
        "scope": e.scope,
        "source": f"FY{e.fiscal_year} annual report, {e.location}",
        "quote": e.quote,
        "document": e.document,
    }


def header_text(rating: dict | None) -> str | None:
    """The header line: "Ratings: S&P BBB (stable), Moody's Baa2 (stable), as at 26 Feb 2026"."""
    if not rating:
        return None
    if rating["status"] != "verified":
        return "Ratings: awaiting review"
    if rating["text"].startswith("No rating"):
        return rating["text"]
    as_at = date.fromisoformat(rating["as_at"])
    scope = "" if rating["scope"] == "issuer" else f" ({rating['scope']})"
    stale = " (more than a year old)" if rating["stale"] else ""
    return f"Ratings{scope}: {rating['text']}, as at {as_at:%d %b %Y}{stale}"
