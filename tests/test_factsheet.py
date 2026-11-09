"""Fact sheet: ids, verified-only, directions against the thresholds, peer median and rank."""

from __future__ import annotations

from datetime import date
from decimal import Decimal as D

import pytest

from tearsheet.config import load_issuers
from tearsheet.narrative import render
from tearsheet.narrative.factsheet import (
    NOT_VERIFIED,
    FactSheet,
    Figure,
    assess,
    build,
    load_specs,
    movement,
)

ISSUERS = {i.id: i for i in load_issuers()}
SPECS = load_specs()
DEC = {2024: date(2024, 12, 31), 2025: date(2025, 12, 31)}


def fig(issuer, concept, year, value, status="verified", end=None, reason=None):
    v = None if value is None else D(value)
    return Figure(issuer, concept, year, end or DEC[year], v, status if v is not None else None,
                  reason)  # fmt: skip


def universe(extra=()):
    figures = [
        fig("afkl", "net_leverage", 2024, "1.88"),
        fig("afkl", "net_leverage", 2025, "1.71"),
        fig("iag", "net_leverage", 2025, "0.78"),
        fig("finnair", "net_leverage", 2025, "1.77"),
        fig("afkl", "ebitda_margin", 2024, "0.131"),
        fig("afkl", "ebitda_margin", 2025, "0.153"),
        fig("iag", "ebitda_margin", 2025, "0.230"),
        fig("finnair", "ebitda_margin", 2025, "0.131", status="unverified"),
        fig("afkl", "revenue", 2024, "31500000000"),
        fig("afkl", "revenue", 2025, "32000000000"),
        fig("afkl", "fcf", 2024, "-200000000"),
        fig("afkl", "fcf", 2025, "300000000"),
        fig("afkl", "liquidity", 2025, "9000000000", status="unverified"),
        fig("afkl", "rask", 2025, None, reason="ASK not printed for the group"),
        *extra,
    ]
    return figures


@pytest.fixture
def sheet() -> FactSheet:
    return build(ISSUERS["afkl"], 2025, universe())


def test_ids_and_rendering(sheet):
    item = sheet.items["net_leverage@FY2025"]
    assert item.rendered == "1.71x"
    assert sheet.items["net_leverage@FY2024"].rendered == "1.88x"
    assert sheet.items["revenue@FY2025"].rendered == "EUR 32.0bn"
    assert sheet.items["ebitda_margin@FY2025"].rendered == "15.3%"
    assert sheet.period_label == "FY2025"
    assert sheet.peer_year == 2025
    assert sheet.peer_group == "Network airlines"


def test_change_direction_and_assessment(sheet):
    lev = sheet.items["net_leverage.change@FY2025"]
    assert (lev.direction, lev.assessment, lev.rendered) == ("down", "better", "0.17x")
    assert sheet.items["net_leverage@FY2025"].direction == "down"
    margin = sheet.items["ebitda_margin.change@FY2025"]
    assert (margin.direction, margin.assessment, margin.rendered) == ("up", "better", "2.2 points")
    revenue = sheet.items["revenue.change@FY2025"]  # +1.6%: below the 2% threshold
    assert (revenue.direction, revenue.assessment, revenue.rendered) == ("flat", "neutral", "1.6%")


def test_sign_change_has_direction_but_no_percentage(sheet):
    assert sheet.items["fcf@FY2025"].direction == "up"
    assert sheet.items["fcf@FY2025"].assessment == "better"
    assert "fcf.change@FY2025" not in sheet.items
    assert "not meaningful" in sheet.unavailable["fcf.change@FY2025"]


def test_only_verified_figures(sheet):
    assert "liquidity@FY2025" not in sheet.items
    assert sheet.unavailable["liquidity@FY2025"] == NOT_VERIFIED
    assert sheet.unavailable["rask@FY2025"] == "ASK not printed for the group"
    assert sheet.unavailable["liquidity.change@FY2025"] == "needs both years verified"
    assert sheet.unavailable["ask@FY2025"] == "no figure for this year"


def test_peer_median_and_rank(sheet):
    median = sheet.items["net_leverage.peer_median@FY2025"]
    assert median.value == D("1.71") and median.vs_peers == "in_line"
    rank = sheet.items["net_leverage.peer_rank@FY2025"]
    assert (rank.rank, rank.rank_of, rank.rendered) == (2, 3, "2nd of 3")
    assert sheet.items["net_leverage@FY2025"].vs_peers == "in_line"


def test_peer_median_withheld_when_a_peer_is_unverified(sheet):
    assert "ebitda_margin.peer_median@FY2025" not in sheet.items
    assert "finnair" in sheet.unavailable["ebitda_margin.peer_median@FY2025"]


def test_peer_rank_best_and_lower_is_better():
    figures = universe([fig("afkl", "net_leverage", 2025, "0.50")])
    figures = [f for f in figures if not (f.concept == "net_leverage" and f.value == D("1.71"))]
    sheet = build(ISSUERS["afkl"], 2025, figures)
    rank = sheet.items["net_leverage.peer_rank@FY2025"]
    assert (rank.rank, rank.note) == (1, "best in the group")
    assert sheet.items["net_leverage@FY2025"].vs_peers == "below"
    assert sheet.items["net_leverage@FY2025"].peer_assessment == "better"


def test_wizz_peer_year_follows_year_end():
    end = date(2026, 3, 31)
    figures = [
        Figure("wizz", "net_leverage", 2026, end, D("4.1"), "verified"),
        Figure("wizz", "net_leverage", 2025, date(2025, 3, 31), D("4.28"), "verified"),
        Figure("easyjet", "net_leverage", 2025, date(2025, 9, 30), D("-0.2"), "verified"),
        Figure("norwegian", "net_leverage", 2025, DEC[2025], D("0.6"), "verified"),
    ]
    sheet = build(ISSUERS["wizz"], 2026, figures)
    assert sheet.peer_year == 2025
    assert sheet.period_label == "FY2026 (Apr 2025 to Mar 2026)"
    assert sheet.items["net_leverage.peer_rank@FY2026"].rendered == "3rd of 3"
    assert "peer year 2025" in sheet.items["net_leverage.peer_rank@FY2026"].label
    assert sheet.items["net_leverage.change@FY2026"].direction == "down"


@pytest.mark.parametrize(
    ("metric", "prior", "current", "direction"),
    [
        ("net_leverage", "1.80", "1.71", "flat"),  # 0.09x < 0.1x
        ("net_leverage", "1.80", "1.70", "down"),  # 0.10x: not below the threshold
        ("ebitda_margin", "0.150", "0.154", "flat"),  # 0.4 point < 0.5 point
        ("ebitda_margin", "0.150", "0.156", "up"),
        ("revenue", "100", "101.9", "flat"),  # 1.9% < 2%
        ("revenue", "100", "97.9", "down"),
        ("rask", "0.080", "0.0808", "up"),  # 1%: not below the 1% threshold
        ("rask", "0.080", "0.0805", "flat"),
        ("passengers", "100", "103", "up"),
    ],
)
def test_flat_thresholds(metric, prior, current, direction):
    assert movement(SPECS[metric], D(prior), D(current))[0] == direction


def test_assessment_follows_higher_is_better():
    assert assess("down", False) == "better"
    assert assess("down", True) == "worse"
    assert assess("up", None) == "neutral"
    assert assess("flat", True) == "neutral"


def test_round_trip_and_fingerprint(sheet):
    again = FactSheet.from_dict(sheet.to_dict())
    assert again.to_json() == sheet.to_json()
    assert again.fingerprint() == sheet.fingerprint()


@pytest.mark.parametrize(
    ("value", "unit", "currency", "text"),
    [
        ("1.615", "x", "", "1.62x"),
        ("-0.13", "x", "", "-0.13x"),
        ("0.1834", "pct", "", "18.3%"),
        ("1234000000", "amount", "EUR", "EUR 1.2bn"),
        ("37600000000", "amount", "NOK", "NOK 37.6bn"),
        ("845400000", "amount", "EUR", "EUR 845m"),
        ("45340000", "amount", "GBP", "GBP 45.3m"),
        ("98540000", "count", "", "98.5m"),
        ("301200000000", "count", "", "301.2bn"),
        ("616", "count", "", "616"),
        ("11.24", "years", "", "11.2 years"),
        ("0.0845", "per_km", "EUR", "8.45 euro cents"),
        ("0.0712", "per_km", "GBP", "7.12 pence"),
        ("23.1", "per_passenger", "EUR", "EUR 23.10"),
        ("-0.0004", "pct", "", "0.0%"),
    ],
)
def test_value_text(value, unit, currency, text):
    assert render.value_text(D(value), unit, currency) == text


def test_change_and_rank_text():
    assert render.change_text(D("-0.0912"), "x") == "0.09x"
    assert render.change_text(D("0.012"), "points") == "1.2 points"
    assert render.change_text(D("0.045"), "relative") == "4.5%"
    assert render.rank_text(1, 3) == "1st of 3"
    assert render.rank_text(3, 3) == "3rd of 3"
    assert render.ordinal(11) == "11th" and render.ordinal(22) == "22nd"


def test_fill():
    text = "Net leverage fell to {{net_leverage@FY2025}}."
    assert render.fill(text, {"net_leverage@FY2025": "1.71x"}) == "Net leverage fell to 1.71x."


def test_absolute_change_adds_up_as_printed():
    assert render.change_between(D("1.8814"), D("1.7165"), "x") == "0.16x"  # 1.88x - 1.72x
    assert render.change_between(D("1.8849"), D("1.7149"), "x") == "0.17x"  # 1.88x - 1.71x
    assert render.change_between(D("0.13149"), D("0.15251"), "points") == "2.2 points"


# --- Fix B (decision 0018) ---------------------------------------------------------------------


def test_negative_net_debt_becomes_net_cash():
    figures = universe([fig("afkl", "net_debt", 2024, "-500000000"),
                        fig("afkl", "net_debt", 2025, "-602000000")])  # fmt: skip
    sheet = build(ISSUERS["afkl"], 2025, figures)
    assert sheet.items["net_cash@FY2025"].rendered == "EUR 602m"
    assert sheet.items["net_cash.change@FY2025"].direction == "up"
    assert sheet.items["net_cash.change@FY2025"].assessment == "better"
    assert "net cash" in sheet.unavailable["net_debt@FY2025"]


def test_positive_net_debt_has_no_net_cash():
    sheet = build(ISSUERS["afkl"], 2025, universe([fig("afkl", "net_debt", 2025, "8700000000")]))
    assert sheet.items["net_debt@FY2025"].rendered == "EUR 8.7bn"
    assert "net_cash@FY2025" in sheet.unavailable


def test_ratios_to_debt_left_out_when_debt_is_tiny():
    extra = [
        fig("afkl", "gross_leverage", 2025, "0.14"),
        fig("afkl", "ffo_to_debt", 2025, "4.42"),
        fig("afkl", "ffo_to_debt", 2024, "6.44"),
        fig("iag", "ffo_to_debt", 2025, "0.455"),
        fig("finnair", "ffo_to_debt", 2025, "0.18"),
    ]
    sheet = build(ISSUERS["afkl"], 2025, universe(extra))
    assert "ffo_to_debt@FY2025" not in sheet.items
    assert "very small" in sheet.unavailable["ffo_to_debt.peer_median@FY2025"]
    peer = build(
        ISSUERS["iag"], 2025, universe(extra + [fig("iag", "gross_leverage", 2025, "1.86")])
    )
    median = peer.items["ffo_to_debt.peer_median@FY2025"]
    assert median.label.endswith("(2 companies)")  # afkl's ratio to almost no debt left out


def test_median_company_is_flagged(sheet):
    assert "middle of the group" in sheet.items["net_leverage.peer_median@FY2025"].note


def test_the_same_figure_under_two_names_is_offered_once():
    extra = [fig("afkl", "cash_like", 2024, "6900000000"),
             fig("afkl", "cash_like", 2025, "6950000000"),
             fig("afkl", "cash_liquidity", 2024, "6900000000"),
             fig("afkl", "cash_liquidity", 2025, "6950000000")]  # fmt: skip
    sheet = build(ISSUERS["afkl"], 2025, universe(extra))
    assert "cash_like@FY2025" in sheet.items and "cash_like.change@FY2025" in sheet.items
    assert "cash_liquidity@FY2025" not in sheet.items
    assert "cash_like@FY2025" in sheet.unavailable["cash_liquidity@FY2025"]
    assert "cash_liquidity.change@FY2025" not in sheet.items


def test_different_figures_keep_both_names():
    extra = [fig("afkl", "cash_like", 2025, "6950000000"),
             fig("afkl", "cash_liquidity", 2025, "9000000000")]  # fmt: skip
    sheet = build(ISSUERS["afkl"], 2025, universe(extra))
    assert "cash_liquidity@FY2025" in sheet.items
