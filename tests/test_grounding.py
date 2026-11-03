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


IAG = (
    "Total Group operations\n2025\n2024\n2023\n20221\n2021\n"
    "Passengers carried\n‘000\n121,560\n122,047\n115,559\n94,726\n38,864",
)


@pytest.mark.parametrize("year, printed", [(2025, "121,560"), (2024, "122,047")])
def test_thousands_marker_after_the_row_label_is_not_a_column(year, printed):
    # IAG FY2025: the "‘000" after the label says thousands; it is not the first column.
    raw = figure(
        item="passengers",
        fiscal_year=year,
        printed_value=printed,
        scale="thousand",
        quote="Passengers carried\n‘000\n121,560\n122,047\n115,559\n94,726\n38,864",
        table_header="Total Group operations\n2025\n2024\n2023\n20221\n2021",
    )
    c = run(raw, doc(IAG), currency="EUR")
    assert c.verified, c.failures


def test_thousands_marker_does_not_hide_a_wrong_column():
    raw = figure(
        item="passengers",
        fiscal_year=2025,
        printed_value="122,047",
        scale="thousand",
        quote="Passengers carried\n‘000\n121,560\n122,047\n115,559\n94,726\n38,864",
        table_header="Total Group operations\n2025\n2024\n2023\n20221\n2021",
    )
    c = run(raw, doc(IAG), currency="EUR")
    assert not c.verified
    assert any("2024" in f for f in c.failures)


def test_number_split_by_spaces_is_found_between_its_neighbours():
    # Finnair FY2025: the text layer prints RPK as "3 0, 2 2 7. 3" between two other cells.
    quote = "Tota l 2,445.8 2,419.0 39,306.6 38,259.3 3 0, 2 2 7. 3 29,000.2 76.9 1.1"
    raw = figure(
        item="rpk",
        printed_value="3 0, 2 2 7. 3",
        scale="million",
        quote=quote,
        table_header="Passenger revenue ASK RPK PLF",
    )
    c = run(raw, doc((quote,), issuer="finnair"), currency="EUR")
    assert c.value == Decimal("30227300000")
    assert not any("not printed in the quote" in f for f in c.failures)
    assert not c.verified  # the header names no year, so the year cannot be confirmed


FINNAIR_HEDGE = (
    "At the end of the financial year, Finnair had hedged 8 per cent of its forecasted fuel "
    "purchases for the first six months of 2022 and 3 per cent of the purchases for the second "
    "half of the year.",
    "At the end of 2022, the Group has hedged around 15 percent of its planned fuel consumption "
    "in 2023 at an average price of USD 891 per metric ton.",
)


def test_half_year_hedge_is_not_a_twelve_month_ratio():
    raw = figure(
        item="fuel_hedge_ratio",
        fiscal_year=2021,
        printed_value="8",
        quote=FINNAIR_HEDGE[0],
    )
    c = run(raw, doc(FINNAIR_HEDGE, year=2021, issuer="finnair"), currency="EUR")
    assert not c.verified
    assert any("part of a year" in f for f in c.failures)


def test_quote_cut_short_does_not_hide_a_half_year():
    # Finnair FY2022: the AI's quote stops at "for the first"; the report goes on "six months".
    page = (
        "At the end of the financial year, Finnair had hedged 41 per cent of its forecasted fuel "
        "purchases for the first six months of 2023 and 25 per cent for the second half.",
    )
    raw = figure(
        item="fuel_hedge_ratio",
        fiscal_year=2022,
        printed_value="41",
        quote="At the end of the financial year, Finnair had hedged 41 per cent of its forecasted "
        "fuel purchases for the first",
    )
    c = run(raw, doc(page, year=2022, issuer="finnair"), currency="EUR")
    assert not c.verified
    assert any("six months" in f for f in c.failures)


AFKL_HEDGE = (
    "(en millions de dollars US) 2022 2023 2024 Dépense brute avant couverture 8 486 8 060 "
    "7 654 Pourcentage de couverture 73 % 51 % 4 %",
)


@pytest.mark.parametrize("printed, verified", [("73", False), ("51", True)])
def test_hedge_table_needs_the_next_year_column(printed, verified):
    # Air France-KLM FY2022: 73 % is 2022 (the year just ended), 51 % is 2023 (the next year).
    raw = figure(
        item="fuel_hedge_ratio",
        fiscal_year=2022,
        printed_value=printed,
        quote="Pourcentage de couverture 73 % 51 % 4 %",
        table_header="(en millions de dollars US) 2022 2023 2024",
    )
    c = run(raw, doc(AFKL_HEDGE, language="fr", year=2022, issuer="afkl"), currency="EUR")
    assert c.verified is verified, c.failures


def test_bare_number_quote_is_rejected_even_with_a_header():
    # Groupe ADP 2025 PDF: "107,0" sits in a list of airports; the quote must name the row.
    page = (
        "Passagers en millions PAX (1) Évolution en % par rapport au 31/12/2024 107,0 +3,4 % "
        "Ankara Esenboga - TAV Airports 14,0 +8,3%",
    )
    raw = figure(
        item="passengers",
        printed_value="107,0",
        scale="million",
        quote="107,0",
        table_header="Passagers en millions PAX (1)",
    )
    c = run(raw, doc(page, language="fr", issuer="adp"), currency="EUR")
    assert "the quote is only numbers, without the row label" in c.failures


AENA_PAGES = (
    "Segmento Aeropuertos (Miles de euros) 2024 2023 Servicios aeronáuticos 3.147.517 2.768.254",
    "Otra tabla",
    "Otra tabla más",
)


def aena_row(caption):
    return figure(
        item="aero_revenue",
        fiscal_year=2024,
        printed_value="3.147.517",
        scale="thousand",
        currency="EUR",
        quote="Servicios aeronáuticos 3.147.517 2.768.254",
        table_header="2024 2023",
        caption=caption,
    )


def test_caption_on_the_same_page_gives_scale_and_currency():
    index = doc(AENA_PAGES, language="es", year=2024, issuer="aena")
    without = run(aena_row(None), index, currency="EUR")
    assert not without.verified  # no scale or currency in the row or the header
    c = run(aena_row("Segmento Aeropuertos (Miles de euros)"), index, currency="EUR")
    assert c.verified, c.failures
    assert c.value == Decimal("3147517000")


def test_caption_from_another_page_is_not_used():
    pages = ("(Miles de euros)", "x", "x", "2024 2023 Servicios aeronáuticos 3.147.517 2.768.254")
    index = doc(pages, language="es", year=2024, issuer="aena")
    c = run(aena_row("(Miles de euros)"), index, currency="EUR")
    assert "caption is not on the quote's page or the page before" in c.failures
    assert not c.verified


def test_made_up_caption_is_rejected():
    index = doc(AENA_PAGES, language="es", year=2024, issuer="aena")
    c = run(aena_row("(Miles de euros, Aeronáutico)"), index, currency="EUR")
    assert "caption not found word for word in the report" in c.failures
    assert not c.verified


FINNAIR_TRAFFIC = (
    "Passenger revenue ASK RPK PLF 2025 MEUR 2024 MEUR 2025 Mill. km 2024 Mill. km 2025 Mill. "
    "km 2024 Mill. km % Change %-p Tota l 2,445.8 2,419.0 39,306.6 38,259.3 30,227.3 29,000.2 "
    "76.9 1.1",
)
FINNAIR_HEADER = (
    "2025\nMEUR\n2024\nMEUR\n2025\nMill. km\n2024\nMill. km\n2025\nMill. km\n2024\nMill. km"
)


@pytest.mark.parametrize(
    "item, year, printed, verified",
    [
        ("ask", 2025, "39,306.6", True),
        ("rpk", 2025, "30,227.3", True),
        ("ask", 2025, "38,259.3", False),
    ],
)
def test_header_repeating_the_years_over_each_measure(item, year, printed, verified):
    # Finnair FY2025: revenue, ASK and RPK each have a 2025 and a 2024 column.
    raw = figure(
        item=item,
        fiscal_year=year,
        printed_value=printed,
        scale="million",
        quote="Tota l 2,445.8 2,419.0 39,306.6 38,259.3 30,227.3 29,000.2 76.9 1.1",
        table_header=FINNAIR_HEADER,
        caption="Passenger revenue ASK RPK PLF",  # the column names sit in a line of their own
    )
    c = run(raw, doc(FINNAIR_TRAFFIC, issuer="finnair"), currency="EUR")
    assert c.verified is verified, c.failures


def test_icon_glyph_in_the_report_does_not_break_the_quote():
    # Finnair FY2025 fleet table: an icon character sits between two cells in the report.
    page = ("Fleet operated by Finnair 31 Dec 2025 To t a l 55 \ue61f1 38 17 14 . 3 1",)
    raw = figure(
        item="fleet_count",
        printed_value="55",
        quote="Tota l 55 1 38 17 14.3 1",
        table_header="31 Dec 2025",
        caption="Fleet operated by Finnair",
        component=True,
    )
    c = run(raw, doc(page, issuer="finnair"), currency="EUR")
    assert c.location == "page 1"
    assert c.verified, c.failures


def test_hedge_for_the_next_year_is_verified():
    raw = figure(
        item="fuel_hedge_ratio", fiscal_year=2022, printed_value="15", quote=FINNAIR_HEDGE[1]
    )
    c = run(raw, doc(FINNAIR_HEDGE, year=2022, issuer="norwegian"), currency="NOK")
    assert c.verified, c.failures
    assert c.value == Decimal("0.15")


def test_hedge_from_a_table_for_one_half_year_is_rejected():
    raw = figure(
        item="fuel_hedge_ratio",
        fiscal_year=2026,
        printed_value="84",
        quote="Hedge coverage for the period 84 % 71 % 17 %",
        table_header="Period covered F27 H1 F27 H2 F28 5 months 6 months 7 months",
    )
    page = (raw.table_header + " " + raw.quote,)
    c = run(raw, doc(page, year=2026, issuer="wizz"), currency="EUR")
    assert not c.verified


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


def test_forward_hedge_ratio_for_the_next_half_year_only_is_rejected():
    # "80% hedged for H1 FY26" covers six months, not the next twelve (decision 0013).
    raw = figure(
        item="fuel_hedge_ratio",
        printed_value="80",
        quote="are\n80% hedged for H1 FY26.",
    )
    c = run(raw, doc(EASYJET))
    assert c.value == Decimal("0.8")
    assert c.failures == [
        "the quote gives the figure for part of a year ('H1'), not the next twelve months"
    ]


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
