"""Grounding checks, including adversarial answers: each wrong answer must stay unverified.

The report passages are short excerpts as printed in the real reports (easyJet FY2025,
Air France-KLM FY2024 in French, Finnair FY2025 with its split words, Wizz Air FY2026)."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import DocumentIndex, RawFigure, check_figure
from tearsheet.extract.locator import load_items
from tearsheet.extract.numbers import parse_number

ITEMS = load_items()

EASYJET = (
    "aircraft allocation enabled capacity growth of 4%\nto 104.0 million seats (2024: 100.4 "
    "million). With a\nload factor of 90% (2024: 89%), this translated into\n93.4 million "
    "passengers carried (2024: 89.7 million),\nan increase of 4% on the prior year.",
    "KEY PERFORMANCE INDICATORS 2025 2024 Change\n"
    "Available seat kilometres (ASK) (millions) 134,451 122,885 9%\n"
    "Revenue passenger kilometres (RPK) (millions) 121,830 110,276 10%",
    "secured a $1.7 billion revolving credit facility (RCF) which\nis undrawn at 30 September "
    "2025. We have continued our hedging\nprogramme throughout the year and are\n80% hedged for "
    "H1 FY26. giving a total fleet of 356 at 30 September 2025 (2024: 347).",
)
AFKL = (
    "Au total, le groupe a transporté 98,0 millions de passagers transportés en 2024 (contre "
    "93,6 millions en 2023).\nLa ligne de crédit à 1,4 milliard d’euros est actuellement non "
    "tirée.",
    "Au 31 décembre 2024, l'âge moyen de la flotte en exploitation est de 12,1 ans.",
)
FINNAIR = (
    "tr affic capac ity , measur ed by available seat kilometr es (ASK), in cr eased by 2. 7 %",
)


def doc(pages, language="en", year=2025, issuer="easyjet") -> DocumentIndex:
    d = Document("doc-1", issuer, year, language, "test", "test", None, tuple(pages), "page")
    return DocumentIndex(d)


def figure(**kw) -> RawFigure:
    base = {"found": True, "fiscal_year": 2025, "scale": "one"}
    return RawFigure(**(base | kw))


def run(raw, index, currency="GBP", revenue=Decimal("10_000_000_000")):
    return check_figure(raw, index, ITEMS[raw.item], currency, revenue)


# --- Correct answers are verified -------------------------------------------------------------


def test_sentence_with_comparative_in_brackets_is_verified():
    raw = figure(
        item="passengers",
        printed_value="93.4",
        scale="million",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    c = run(raw, doc(EASYJET))
    assert c.verified, c.failures
    assert c.value == Decimal("93400000")
    assert c.decimals == -5
    assert c.location == "page 1"


def test_prior_year_from_the_brackets_is_verified_as_prior_year():
    raw = figure(
        item="passengers",
        fiscal_year=2024,
        printed_value="89.7",
        scale="million",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    assert run(raw, doc(EASYJET)).verified


def test_table_row_with_header_is_verified():
    raw = figure(
        item="ask",
        printed_value="134,451",
        scale="million",
        quote="Available seat kilometres (ASK) (millions) 134,451 122,885 9%",
        table_header="KEY PERFORMANCE INDICATORS 2025 2024 Change",
    )
    c = run(raw, doc(EASYJET))
    assert c.verified, c.failures
    assert c.value == Decimal("134451000000")


def test_french_sentence_is_verified():
    raw = figure(
        item="passengers",
        fiscal_year=2024,
        printed_value="98,0",
        scale="million",
        quote="98,0 millions de passagers transportés en 2024 (contre 93,6 millions en 2023)",
    )
    c = run(raw, doc(AFKL, "fr", 2024, "afkl"), "EUR")
    assert c.verified, c.failures
    assert c.value == Decimal("98000000")


def test_french_amount_in_milliards_is_verified():
    raw = figure(
        item="undrawn_facilities",
        fiscal_year=2024,
        printed_value="1,4",
        scale="billion",
        currency="EUR",
        quote="La ligne de crédit à 1,4 milliard d’euros est actuellement non tirée.",
    )
    c = run(raw, doc(AFKL, "fr", 2024, "afkl"), "EUR", Decimal("31_000_000_000"))
    assert c.verified, c.failures
    assert c.value == Decimal("1400000000")


def test_split_words_and_numbers_are_matched():
    raw = figure(
        item="ask",
        printed_value="2.7",
        quote="available seat kilometr es (ASK), in cr eased by 2. 7 %",
    )
    c = run(raw, doc(FINNAIR, issuer="finnair"))
    # the quote and the number are found despite the split; it then fails on the range,
    # because 2.7 is a growth rate, not a number of seat-kilometres
    assert "quote not found word for word in the report" not in c.failures
    assert "value 2.7 is not printed in the quote" not in c.failures
    assert not c.verified


def test_forward_hedge_ratio_names_next_year():
    raw = figure(
        item="fuel_hedge_ratio",
        printed_value="80",
        quote="are\n80% hedged for H1 FY26.",
    )
    c = run(raw, doc(EASYJET))
    assert c.verified, c.failures
    assert c.value == Decimal("0.8")


def test_foreign_currency_amount_is_kept_in_its_currency():
    raw = figure(
        item="undrawn_facilities",
        printed_value="1.7",
        scale="billion",
        currency="USD",
        quote="secured a $1.7 billion revolving credit facility (RCF) which\nis undrawn at 30 "
        "September 2025.",
    )
    c = run(raw, doc(EASYJET))
    assert c.verified, c.failures
    assert c.currency == "USD"


def test_years_unit_in_french():
    raw = figure(
        item="fleet_age",
        fiscal_year=2024,
        printed_value="12,1",
        quote="Au 31 décembre 2024, l'âge moyen de la flotte en exploitation est de 12,1 ans.",
    )
    c = run(raw, doc(AFKL, "fr", 2024, "afkl"), "EUR")
    assert c.verified, c.failures
    assert c.value == Decimal("12.1")


# --- Adversarial answers stay unverified -----------------------------------------------------


def test_made_up_quote_is_rejected():
    raw = figure(
        item="passengers",
        printed_value="95.1",
        scale="million",
        quote="95.1 million passengers carried in 2025",
    )
    c = run(raw, doc(EASYJET))
    assert not c.verified
    assert c.failures == ["quote not found word for word in the report"]


def test_number_not_in_quote_is_rejected():
    raw = figure(
        item="passengers",
        printed_value="94.3",
        scale="million",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    c = run(raw, doc(EASYJET))
    assert "value 94.3 is not printed in the quote" in c.failures


def test_prior_year_figure_passed_off_as_this_year_is_rejected():
    raw = figure(
        item="passengers",
        printed_value="89.7",
        scale="million",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    c = run(raw, doc(EASYJET))
    assert not c.verified
    assert any("ties the value to 2024" in f for f in c.failures)


def test_prior_year_column_in_a_table_is_rejected():
    raw = figure(
        item="ask",
        printed_value="122,885",
        scale="million",
        quote="Available seat kilometres (ASK) (millions) 134,451 122,885 9%",
        table_header="KEY PERFORMANCE INDICATORS 2025 2024 Change",
    )
    c = run(raw, doc(EASYJET))
    assert any("table header ties the value to 2024" in f for f in c.failures)


def test_table_row_without_header_is_ambiguous():
    raw = figure(
        item="ask",
        printed_value="134,451",
        scale="million",
        quote="Available seat kilometres (ASK) (millions) 134,451 122,885 9%",
    )
    c = run(raw, doc(EASYJET))
    assert not c.verified
    assert any("several similar figures" in f for f in c.failures)


def test_wrong_scale_is_rejected():
    raw = figure(
        item="passengers",
        printed_value="93.4",
        scale="billion",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    c = run(raw, doc(EASYJET))
    assert not c.verified
    assert any("scale" in f or "range" in f for f in c.failures)


def test_units_when_quote_says_million_is_rejected():
    raw = figure(
        item="passengers",
        printed_value="93.4",
        scale="one",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    assert not run(raw, doc(EASYJET)).verified


def test_quote_about_another_figure_is_rejected():
    raw = figure(
        item="passengers",
        printed_value="104.0",
        scale="million",
        quote="to 104.0 million seats (2024: 100.4 million)",
    )
    c = run(raw, doc(EASYJET))
    assert "quote does not mention passengers" in c.failures


def test_load_factor_offered_as_hedge_ratio_is_rejected():
    raw = figure(
        item="fuel_hedge_ratio",
        printed_value="90",
        quote="load factor of 90% (2024: 89%)",
    )
    c = run(raw, doc(EASYJET))
    assert not c.verified


def test_wrong_currency_is_rejected():
    raw = figure(
        item="undrawn_facilities",
        printed_value="1.7",
        scale="billion",
        currency="GBP",
        quote="secured a $1.7 billion revolving credit facility (RCF) which\nis undrawn at 30 "
        "September 2025.",
    )
    c = run(raw, doc(EASYJET))
    assert "the quote does not show the currency (GBP)" in c.failures


def test_year_outside_the_report_is_rejected():
    raw = figure(
        item="passengers",
        fiscal_year=2023,
        printed_value="93.4",
        scale="million",
        quote="93.4 million passengers carried (2024: 89.7 million)",
    )
    assert not run(raw, doc(EASYJET)).verified


def test_out_of_range_value_is_rejected():
    raw = figure(
        item="fleet_count",
        printed_value="2025",
        quote="giving a total fleet of 356 at 30 September 2025 (2024: 347).",
    )
    c = run(raw, doc(EASYJET))
    assert not c.verified


def test_fleet_count_is_verified():
    raw = figure(
        item="fleet_count",
        printed_value="356",
        quote="giving a total fleet of 356 at 30 September 2025 (2024: 347).",
    )
    c = run(raw, doc(EASYJET))
    assert c.verified, c.failures


def test_overlong_quote_is_rejected():
    raw = figure(item="passengers", printed_value="93.4", scale="million", quote="x " * 400)
    assert not run(raw, doc(EASYJET)).verified


# --- Number reading ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "printed,language,expected",
    [
        ("134,451", "en", "134451"),
        ("93.4", "en", "93.4"),
        ("98,0", "fr", "98.0"),
        ("1 405", "fr", "1405"),
        ("1 405,5", "fr", "1405.5"),
        ("1.405,5", "de", "1405.5"),
        ("1.405", "es", "1405"),
        ("132,030,723", "en", "132030723"),
        ("12,1", "fr", "12.1"),
        ("80", "en", "80"),
    ],
)
def test_parse_number(printed, language, expected):
    assert parse_number(printed, language) == Decimal(expected)


def test_parse_number_refuses_text():
    assert parse_number("about 93", "en") is None
    assert parse_number("93.4 million", "en") is None
