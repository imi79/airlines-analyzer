"""Checks of the M0 classifier on a small synthetic xBRL-JSON document (values are made up)."""

from datetime import date

from spikes.m0 import xbrl

NAMESPACES = {
    "ifrs-full": "https://xbrl.ifrs.org/taxonomy/2022-03-24/ifrs-full",
    "abc": "http://www.example-airline.com/xbrl/2023",
}
ENTITY = "scheme:529900EXAMPLE0000000"
FY = "2023-01-01T00:00:00/2024-01-01T00:00:00"
FY_END = "2024-01-01T00:00:00"


def fact(concept, period, value="100", unit="iso4217:EUR", **extra_dims):
    dims = {"concept": concept, "entity": ENTITY, "period": period, "unit": unit, **extra_dims}
    return {"value": value, "decimals": -6, "dimensions": dims}


DOCUMENT = {
    "documentInfo": {"namespaces": NAMESPACES},
    "facts": {
        "f1": fact("ifrs-full:Revenue", FY, "1000"),
        "f2": fact("ifrs-full:Revenue", "2022-01-01T00:00:00/2023-01-01T00:00:00", "900"),
        "f3": fact("ifrs-full:Revenue", FY, "600", **{"ifrs-full:SegmentsAxis": "abc:Cargo"}),
        "f4": fact("ifrs-full:CashAndCashEquivalents", FY_END, "250"),
        "f5": fact("abc:NoncurrentLeaseDebt", FY_END, "400"),
        "f6": fact("abc:FuelAndOilCosts", FY, "300"),
        "f7": {
            "value": "<p>Borrowings note</p>",
            "dimensions": {
                "concept": "ifrs-full:DisclosureOfBorrowingsExplanatory",
                "entity": ENTITY,
                "period": FY,
                "language": "en",
            },
        },
    },
}

LINES = {
    "revenue": {"period": "duration", "concepts": ["ifrs-full:Revenue"], "keywords": [["revenue"]]},
    "cash": {"period": "instant", "concepts": ["ifrs-full:CashAndCashEquivalents"]},
    "lease_nc": {
        "period": "instant",
        "concepts": ["ifrs-full:NoncurrentLeaseLiabilities"],
        "keywords": [["noncurrent", "lease"]],
    },
    "fuel": {"period": "duration", "concepts": [], "keywords": [["fuel"]]},
    "equity": {"period": "instant", "concepts": ["ifrs-full:Equity"], "keywords": []},
}


def classify(line_id):
    facts = xbrl.load_facts(DOCUMENT)
    return xbrl.classify_line(line_id, LINES[line_id], facts, date(2023, 12, 31))


def test_period_end_is_the_last_day_covered():
    assert xbrl.parse_period(FY) == (date(2023, 1, 1), date(2023, 12, 31))
    assert xbrl.parse_period(FY_END) == (None, date(2023, 12, 31))


def test_standard_concept_found_for_the_right_year_and_without_breakdown():
    result = classify("revenue")
    assert result.status == "found"
    assert result.concept == "ifrs-full:Revenue"
    assert result.value == "1000"  # not the prior year, not the cargo segment


def test_instant_concept_found():
    assert classify("cash").status == "found"


def test_company_specific_concept_reported_as_extension():
    result = classify("lease_nc")
    assert result.status == "extension"
    assert result.candidates == ["abc:NoncurrentLeaseDebt"]


def test_line_with_no_standard_concept_can_still_match_an_extension():
    assert classify("fuel").candidates == ["abc:FuelAndOilCosts"]


def test_missing_line():
    assert classify("equity").status == "missing"


def test_text_block_and_language():
    facts = xbrl.load_facts(DOCUMENT)
    concepts = ["ifrs-full:DisclosureOfBorrowingsExplanatory"]
    assert xbrl.has_text_block(concepts, facts) == concepts[0]
    assert xbrl.main_language(facts) == "en"


def test_critical_requirements_accept_either_split_or_total():
    critical = {"borrowings": [["current", "noncurrent"], ["total"]], "cash": [["cash"]]}
    assert xbrl.critical_met({"total": "found", "cash": "found"}, critical) == []
    assert xbrl.critical_met({"current": "found", "cash": "extension"}, critical) == ["borrowings"]


def test_report_terms_acronyms_are_whole_words():
    text = "Capacity (ASK) rose. We ask for more. Load factor was high."
    assert xbrl.find_terms(text, ["ASK"])[0] == 1
    assert xbrl.find_terms(text, ["load factor"])[0] == 1
