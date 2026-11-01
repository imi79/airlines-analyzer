"""The answer key reader (decision 0012): its own text, numbers and anchors, no AI."""

from decimal import Decimal

import pytest

from spikes.m3.answer_key import Anchor, find, full_value, html_pages, number


def test_web_report_pages_and_hidden_parts():
    html = (
        "<html><head><title>x</title></head><body><ix:header>99 hidden</ix:header>"
        '<div class="page"><p>Total fleet of <b>356</b>&nbsp;aircraft</p></div>'
        '<div class="pf w0"><script>var a=1</script><p>2024: 347</p></div></body></html>'
    )
    assert html_pages(html) == ["Total fleet of 356 aircraft", "2024: 347"]


@pytest.mark.parametrize(
    "printed, language, expected",
    [
        ("134,451", "en", (Decimal("134451"), 0)),
        ("39,306.6", "en", (Decimal("39306.6"), 1)),
        ("3 0 , 2 2 7. 3", "en", (Decimal("30227.3"), 1)),  # split by the converter
        ("98,0", "fr", (Decimal("98.0"), 1)),
        ("1 422", "fr", (Decimal("1422"), 0)),
    ],
)
def test_numbers(printed, language, expected):
    assert number(printed, language) == expected


def test_number_refuses_text():
    with pytest.raises(ValueError):
        number("12a", "en")


def test_value_and_tolerance():
    a = Anchor("x", 2025, "passengers", "doc", "", "million")
    assert full_value("93.4", a) == (Decimal("93400000"), Decimal("50000"))
    fleet = Anchor("x", 2025, "fleet_count", "doc", "")
    assert full_value("356", fleet) == (Decimal("356"), Decimal(0))
    hedge = Anchor("x", 2025, "fuel_hedge_ratio", "doc", "")
    assert full_value("45", hedge) == (Decimal("0.45"), Decimal("0.005"))


def test_anchor_must_match_once():
    pages = ["93.4 million passengers (2024: 89.7 million)", "93.4 million passengers"]
    with pytest.raises(LookupError):
        find(pages, r"(?P<v>\d+\.\d) million passengers")
    m, page = find(pages, r"(?P<v>\d+\.\d) million passengers \(2024")
    assert m.group("v") == "93.4" and page == 1
