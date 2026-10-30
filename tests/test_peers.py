"""Peer year alignment, labels, median and rank."""

from datetime import date
from decimal import Decimal

from tearsheet.metrics.peers import Entry, fiscal_label, peer_row, peer_year, pick_year


def test_year_ends_are_placed_in_the_nearest_december():
    assert peer_year(date(2025, 12, 31)) == 2025
    assert peer_year(date(2025, 9, 30)) == 2025  # easyJet: 3 months before
    assert peer_year(date(2026, 3, 31)) == 2025  # Wizz Air: 3 months after
    assert peer_year(date(2025, 3, 31)) == 2024


def test_fiscal_label_spells_out_non_december_years():
    assert fiscal_label(2025, date(2025, 12, 31)) == "FY2025"
    assert fiscal_label(2026, date(2026, 3, 31)) == "FY2026 (Apr 2025 to Mar 2026)"
    assert fiscal_label(2025, date(2025, 9, 30)) == "FY2025 (Oct 2024 to Sep 2025)"


def entry(issuer, value, reason=None):
    return Entry(
        issuer, 2025, date(2025, 12, 31), None if value is None else Decimal(value), reason
    )


def test_median_and_rank_lower_is_better():
    row = peer_row(
        "net_leverage",
        {"a": entry("a", "1.5"), "b": entry("b", "3.0"), "c": entry("c", "0.8")},
        higher_is_better=False,
    )
    assert row.median == Decimal("1.5")
    assert row.ranks == {"c": 1, "a": 2, "b": 3}


def test_not_meaningful_values_are_left_out_of_median_and_rank():
    row = peer_row(
        "ebitda_margin",
        {"a": entry("a", "0.10"), "b": entry("b", None, "n.m."), "c": entry("c", "0.20")},
        higher_is_better=True,
    )
    assert row.median == Decimal("0.15")
    assert row.ranks == {"c": 1, "a": 2}


def test_unranked_metric_has_a_median_but_no_rank():
    row = peer_row("capex_intensity", {"a": entry("a", "0.1"), "b": entry("b", "0.3")}, None)
    assert row.median == Decimal("0.2") and row.ranks == {}


def test_pick_year_uses_the_peer_year():
    wizz = [
        Entry("wizz", 2025, date(2025, 3, 31), Decimal(1), None),
        Entry("wizz", 2026, date(2026, 3, 31), Decimal(2), None),
    ]
    assert pick_year(wizz, 2025).fiscal_year == 2026
    assert pick_year(wizz, 2023) is None
