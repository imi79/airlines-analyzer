"""Peer views: line up each issuer's comparable year, then median and rank per metric.

Year alignment (decision 0008, choice 5a): an issuer's fiscal year is compared with the peer
year whose 31 December falls within six months of its year end. Wizz Air's year to March 2026
and easyJet's year to September 2025 both sit in peer year 2025.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from statistics import median


def peer_year(period_end: date) -> int:
    return period_end.year if period_end.month >= 7 else period_end.year - 1


def months_from_december(period_end: date) -> int:
    """Signed months between the year end and the peer year's 31 December (Mar 2026: +3)."""
    return (period_end.year - peer_year(period_end)) * 12 + period_end.month - 12


def fiscal_label(fiscal_year: int, period_end: date) -> str:
    if period_end.month == 12:
        return f"FY{fiscal_year}"
    start = date(period_end.year - 1, period_end.month % 12 + 1, 1)
    return f"FY{fiscal_year} ({start:%b %Y} to {period_end:%b %Y})"


@dataclass(frozen=True)
class Entry:
    issuer: str
    fiscal_year: int
    period_end: date
    value: Decimal | None
    reason: str | None  # why there is no value (n.m., missing)


@dataclass(frozen=True)
class Row:
    metric: str
    entries: dict[str, Entry | None]  # issuer -> entry for the peer year (None: no year)
    median: Decimal | None
    ranks: dict[str, int]  # issuer -> 1 for the best value; empty when the metric isn't ranked


def peer_row(metric: str, entries: dict[str, Entry | None], higher_is_better) -> Row:
    values = {i: e.value for i, e in entries.items() if e is not None and e.value is not None}
    mid = median(values.values()) if values else None
    ranks = {}
    if higher_is_better is not None and values:
        ordered = sorted(values, key=lambda i: values[i], reverse=bool(higher_is_better))
        ranks = {issuer: position for position, issuer in enumerate(ordered, start=1)}
    return Row(metric, entries, mid, ranks)


def pick_year(entries: list[Entry], year: int) -> Entry | None:
    """The issuer's entry whose fiscal year falls in the given peer year."""
    hits = [e for e in entries if peer_year(e.period_end) == year]
    return hits[0] if hits else None
