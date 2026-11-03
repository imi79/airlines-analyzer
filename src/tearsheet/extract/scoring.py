"""Score the AI extraction against the answer key (the M3 checklist).

The answer key (`docs/m3/answer_key.csv`) is built by `spikes/m3/answer_key.py`, a reader that
uses no AI and none of the extraction code (decision 0012). Each key line is one figure for one
company and year, with the value as printed and the tolerance its printed digits allow.

Each key line ends in one of five outcomes:
  verified_correct    the tool verified it and the value matches the key
  verified_wrong      the tool verified it but the value differs: the failure M3 must avoid
  unverified_correct  the value matches, but a check did not pass, so it waits for review
  unverified_wrong    a wrong value, caught by the checks (kept off the tearsheet)
  missing             the tool has no value for it

Checklist: no `verified_wrong` on any line, and at least 80% `verified_correct` both on all
lines and on the held-out lines alone (written before the second run, decision 0014).

The score uses the status the checks gave, before any review by Imane: it measures what the
checks do on their own. A key line whose figure has been reviewed is shown as such.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import duckdb

from tearsheet.config import DB_PATH, ROOT

KEY = ROOT / "docs" / "m3" / "answer_key.csv"
OUTCOMES = (
    "verified_correct",
    "verified_wrong",
    "unverified_correct",
    "unverified_wrong",
    "missing",
)
TARGET_SHARE = Decimal("0.80")
UNIT_TOLERANCE = {"pct": Decimal("0.0005"), "years": Decimal("0.05")}  # 0.05 point, 0.05 year


@dataclass(frozen=True)
class KeyLine:
    issuer: str
    fiscal_year: int
    item: str
    unit: str  # count | pct | years | amount
    value: Decimal  # full units; fractions for percentages; reporting currency
    tolerance: Decimal  # half a unit of the last printed digit
    printed: str
    document: str
    location: str
    snippet: str
    group: str = "first"  # "first" or "holdout" (decision 0014)


@dataclass(frozen=True)
class Extracted:
    value: Decimal
    decimals: int | None
    status: str  # verified | unverified | overridden (status after the checks)
    reviewed: bool = False


@dataclass(frozen=True)
class Scored:
    key: KeyLine
    outcome: str
    extracted: Extracted | None
    difference: Decimal | None


def load_key(path: Path = KEY) -> list[KeyLine]:
    with path.open(newline="") as fh:
        return [
            KeyLine(
                issuer=row["issuer"],
                fiscal_year=int(row["fiscal_year"]),
                item=row["item"],
                unit=row["unit"],
                value=Decimal(row["value"]),
                tolerance=Decimal(row["tolerance"]),
                printed=row["printed"],
                document=row["document"],
                location=row["location"],
                snippet=row["snippet"],
                group=row.get("set") or "first",
            )
            for row in csv.DictReader(fh)
        ]


def extracted_from_db(db_path: Path = DB_PATH) -> dict[tuple[str, int, str], Extracted]:
    """The value the tearsheet would use for each extracted figure (the primary one)."""
    con = duckdb.connect(str(db_path), read_only=True)
    rows = con.execute(
        "SELECT issuer, fiscal_year, concept, value, decimals, status, source_ref FROM facts "
        "WHERE source_type = 'extracted' AND is_primary"
    ).fetchall()
    con.close()
    out = {}
    for issuer, year, item, value, decimals, status, ref in rows:
        review = (json.loads(ref) or {}).get("review") if ref else None
        if review:
            # Before the review, the checks had left it unverified (a review only touches
            # figures that need it); an approval or correction is not the checks' doing.
            status = "unverified"
        out[(issuer, int(year), item)] = Extracted(
            Decimal(str(value)), decimals, status, reviewed=bool(review)
        )
    return out


def tolerance_of(unit: str, decimals: int | None) -> Decimal:
    if unit in UNIT_TOLERANCE:
        return UNIT_TOLERANCE[unit]
    if decimals is None:
        return Decimal(0)
    return Decimal(5) * Decimal(10) ** (-decimals - 1)


def matches(key: KeyLine, got: Extracted) -> tuple[bool, Decimal]:
    """Equal within the rounding of the coarser of the two printed figures."""
    difference = got.value - key.value
    allowed = max(key.tolerance, tolerance_of(key.unit, got.decimals))
    return abs(difference) <= allowed, difference


def score(key: list[KeyLine], extracted: dict[tuple[str, int, str], Extracted]) -> list[Scored]:
    out = []
    for k in key:
        got = extracted.get((k.issuer, k.fiscal_year, k.item))
        if got is None:
            out.append(Scored(k, "missing", None, None))
            continue
        ok, difference = matches(k, got)
        verified = got.status == "verified"
        outcome = ("verified_" if verified else "unverified_") + ("correct" if ok else "wrong")
        out.append(Scored(k, outcome, got, difference))
    return out


@dataclass(frozen=True)
class Summary:
    total: int
    counts: dict[str, int]

    @property
    def share_verified(self) -> Decimal:
        if not self.total:
            return Decimal(0)
        return Decimal(self.counts["verified_correct"]) / Decimal(self.total)

    @property
    def no_wrong_verified(self) -> bool:
        return self.counts["verified_wrong"] == 0

    @property
    def enough_verified(self) -> bool:
        return self.share_verified >= TARGET_SHARE

    @property
    def passed(self) -> bool:
        return self.total > 0 and self.no_wrong_verified and self.enough_verified


def summarise(scored: list[Scored]) -> Summary:
    counts = {o: 0 for o in OUTCOMES}
    for s in scored:
        counts[s.outcome] += 1
    return Summary(len(scored), counts)
