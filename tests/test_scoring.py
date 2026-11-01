"""Answer key scoring (M3 checklist): each outcome, the tolerance and the pass rule."""

from __future__ import annotations

from decimal import Decimal

from tearsheet.extract.scoring import Extracted, KeyLine, matches, score, summarise


def key(item="passengers", value="93400000", tolerance="50000", unit="count", year=2025):
    return KeyLine("easyjet", year, item, unit, Decimal(value), Decimal(tolerance), "93.4",
                   "doc", "page 1", "93.4 million passengers")  # fmt: skip


def got(value, status="verified", decimals=None):
    return Extracted(Decimal(value), decimals, status)


def test_each_outcome():
    k = [
        key("passengers"),
        key("ask", "134451000000", "500000"),
        key("rpk", "121830000000", "500000"),
        key("fleet_count", "356", "0"),
        key("fuel_hedge_ratio", "0.80", "0.005", "pct"),
    ]
    extracted = {
        ("easyjet", 2025, "passengers"): got("93400000"),
        ("easyjet", 2025, "ask"): got("122885000000"),  # last year's figure, verified
        ("easyjet", 2025, "rpk"): got("121830000000", "unverified"),
        ("easyjet", 2025, "fleet_count"): got("347", "unverified"),
    }
    outcomes = [s.outcome for s in score(k, extracted)]
    assert outcomes == [
        "verified_correct",
        "verified_wrong",
        "unverified_correct",
        "unverified_wrong",
        "missing",
    ]


def test_more_precise_reading_of_the_same_figure_matches():
    # Key read "93.4 million"; the tool read the table "93,412" thousand: same figure.
    ok, _ = matches(key(), got("93412000", decimals=-3))
    assert ok


def test_coarser_reading_by_the_tool_matches_within_its_rounding():
    # Key read "93,412 thousand" exactly; the tool read "93.4 million".
    ok, _ = matches(key(value="93412000", tolerance="500"), got("93400000", decimals=-5))
    assert ok


def test_difference_beyond_rounding_does_not_match():
    ok, diff = matches(key(), got("93600000", decimals=-5))
    assert not ok and diff == Decimal("200000")


def test_percentages_match_within_a_twentieth_of_a_point():
    k = key("fuel_hedge_ratio", "0.80", "0.005", "pct")
    assert matches(k, got("0.8"))[0]
    assert not matches(k, got("0.75"))[0]


def test_pass_rule():
    k = [key(year=y) for y in range(2016, 2026)]
    nine_good = {("easyjet", y, "passengers"): got("93400000") for y in range(2016, 2025)}
    s = summarise(score(k, nine_good))
    assert s.counts["verified_correct"] == 9 and s.counts["missing"] == 1
    assert s.share_verified == Decimal("0.9") and s.passed

    one_wrong = nine_good | {("easyjet", 2025, "passengers"): got("1000000")}
    s = summarise(score(k, one_wrong))
    assert not s.no_wrong_verified and not s.passed

    seven_good = {("easyjet", y, "passengers"): got("93400000") for y in range(2016, 2023)}
    s = summarise(score(k, seven_good))
    assert s.no_wrong_verified and not s.enough_verified and not s.passed


def test_empty_key_does_not_pass():
    assert not summarise([]).passed
