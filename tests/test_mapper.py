"""Mapper rules on small synthetic filings (values are made up)."""

from datetime import date
from decimal import Decimal

from tearsheet.config import Issuer
from tearsheet.ingest.filings import Filing
from tearsheet.ingest.xbrl_json import parse_period, parse_report
from tearsheet.normalize.mapper import Line, Mapping, Rule, consolidate, map_report

NS = {
    "ifrs-full": "https://xbrl.ifrs.org/taxonomy/2023-03-23/ifrs-full",
    "abc": "http://www.example.com/xbrl/2024",
}
ISSUER = Issuer(
    id="abc",
    name="Example Air",
    type="airline",
    lei="X",
    currency="EUR",
    fiscal_year_end="12-31",
    country="FR",
    status="v1",
)


def period(year: int, instant: bool = False) -> str:
    end = f"{year + 1}-01-01T00:00:00"
    return end if instant else f"{year}-01-01T00:00:00/{end}"


def report(*facts):
    doc = {"documentInfo": {"namespaces": NS}, "facts": {}}
    for i, (concept, per, value, *dims) in enumerate(facts):
        d = {"concept": concept, "entity": "lei:X", "period": per, "unit": "iso4217:EUR"}
        d.update(*dims)
        doc["facts"][f"f{i}"] = {"value": str(value), "decimals": -6, "dimensions": d}
    return parse_report(doc)


def filing(year: int) -> Filing:
    return Filing(
        filing_id=f"F{year}",
        issuer="abc",
        fiscal_year=year,
        period_end=date(year, 12, 31),
        origin="test",
        sha256=None,
        json_url=None,
        viewer_url=None,
        report_url=None,
        package_url=None,
        error_count=0,
        date_added=None,
    )


def line(line_id, *rules, period="duration", **kw) -> Line:
    return Line(id=line_id, label=line_id, statement="income", period=period, rules=rules, **kw)


def mapping(*lines, **kw) -> Mapping:
    return Mapping(lines={ln.id: ln for ln in lines}, debt_coverage=DEBT, **kw)


DEBT = {"leases_in_borrowings": "in borrowings", "debt_including_leases": "one line"}


def values(mapped):
    return {(m.fiscal_year, m.line): m.value for m in mapped}


def test_period_bounds_are_inclusive_last_days():
    assert parse_period(period(2024)) == (date(2024, 1, 1), date(2024, 12, 31))
    assert parse_period(period(2024, instant=True)) == (None, date(2024, 12, 31))


def test_company_concepts_are_matched_whatever_their_prefix():
    r = report(("abc:Capex", period(2024), 10))
    assert r.facts[0].concept == "ext:Capex"
    assert r.facts[0].tagged_concept == "abc:Capex"


def test_own_year_and_prior_year_comparative_are_both_mapped():
    r = report(("ifrs-full:Revenue", period(2024), 100), ("ifrs-full:Revenue", period(2023), 90))
    m = mapping(line("revenue", Rule(("ifrs-full:Revenue",))))
    mapped = map_report(ISSUER, filing(2024), r, m)
    assert values(mapped) == {(2024, "revenue"): 100, (2023, "revenue"): 90}
    assert [x.comparative for x in mapped] == [False, True]


def test_breakdowns_and_other_currencies_are_ignored():
    r = report(
        ("ifrs-full:Revenue", period(2024), 60, {"ifrs-full:SegmentsAxis": "abc:Cargo"}),
        ("ifrs-full:Revenue", period(2024), 5, {"unit": "iso4217:USD"}),
    )
    m = mapping(line("revenue", Rule(("ifrs-full:Revenue",))))
    assert map_report(ISSUER, filing(2024), r, m) == []


def test_parts_are_added_and_sign_flipped():
    r = report(("abc:Dep", period(2024), -70), ("abc:Amort", period(2024), -5))
    m = mapping(line("dda", Rule(("ext:Dep", "ext:Amort"), sign=-1)))
    (fact,) = [x for x in map_report(ISSUER, filing(2024), r, m) if x.fiscal_year == 2024]
    assert fact.value == 75
    assert fact.value_tagged == -75
    assert fact.concepts == ("abc:Dep", "abc:Amort")


def test_optional_parts_are_added_only_when_tagged_and_subtract_parts_are_taken_away():
    r = report(
        ("abc:Lease", period(2024), 50),
        ("abc:Other", period(2024), 7),
        ("abc:Capex", period(2024), 1089),
        ("abc:PayablesChange", period(2024), -80),
    )
    m = mapping(
        line("interest", Rule(("ext:Lease",), add_if_tagged=("ext:Other", "ext:Missing"))),
        line("capex", Rule(("ext:Capex",), subtract=("ext:PayablesChange",))),
    )
    got = values(map_report(ISSUER, filing(2024), r, m))
    assert got[(2024, "interest")] == 57
    assert got[(2024, "capex")] == 1169


def test_first_complete_rule_wins_and_rules_can_be_limited_to_later_filings():
    r = report(("ifrs-full:InterestPaid", period(2024), -12))
    m = mapping(
        line(
            "interest_paid",
            Rule(("ifrs-full:InterestPaid",), sign=-1, from_filing_year=2025),
            Rule(("ifrs-full:InterestPaid",)),
        )
    )
    assert values(map_report(ISSUER, filing(2024), r, m))[(2024, "interest_paid")] == -12
    later = map_report(
        ISSUER, filing(2025), report(("ifrs-full:InterestPaid", period(2025), -12)), m
    )
    assert values(later)[(2025, "interest_paid")] == 12


def test_negative_value_on_a_positive_line_is_warned():
    r = report(("ifrs-full:Capex", period(2024), -5))
    m = mapping(line("capex", Rule(("ifrs-full:Capex",)), expect="positive"))
    (fact,) = [x for x in map_report(ISSUER, filing(2024), r, m) if x.fiscal_year == 2024]
    assert "expected positive" in fact.warnings[0]


def run(m, *filings_and_reports):
    filings = [f for f, _ in filings_and_reports]
    mapped = [x for f, r in filings_and_reports for x in map_report(ISSUER, f, r, m)]
    return consolidate(ISSUER, mapped, filings, m)


def test_latest_filing_wins_and_restatement_is_flagged():
    m = mapping(line("revenue", Rule(("ifrs-full:Revenue",))))
    facts, _ = run(
        m,
        (filing(2023), report(("ifrs-full:Revenue", period(2023), 90_000_000))),
        (filing(2024), report(("ifrs-full:Revenue", period(2023), 95_000_000))),
    )
    primary = [f for f in facts if f.primary and f.fiscal_year == 2023]
    assert primary[0].value == 95_000_000 and primary[0].restated
    assert primary[0].filing_id == "F2024"
    assert [f.value for f in facts if not f.primary] == [Decimal(90_000_000)]


def test_rounding_and_opposite_sign_are_not_restatements():
    m = mapping(line("capex", Rule(("ifrs-full:Capex",))))
    rounded = report(("ifrs-full:Capex", period(2023), "1247000000"))
    precise = {
        "documentInfo": {"namespaces": NS},
        "facts": {
            "x": {
                "value": "1247300000",
                "decimals": -5,
                "dimensions": {
                    "concept": "ifrs-full:Capex",
                    "period": period(2023),
                    "unit": "iso4217:EUR",
                },
            }
        },
    }
    facts, _ = run(m, (filing(2023), parse_report(precise)), (filing(2024), rounded))
    assert not any(f.restated for f in facts)
    facts, _ = run(
        m,
        (filing(2023), report(("ifrs-full:Capex", period(2023), -2_202_000_000))),
        (filing(2024), report(("ifrs-full:Capex", period(2023), 2_202_000_000))),
    )
    assert not any(f.restated for f in facts)
    assert "opposite sign" in [f for f in facts if not f.primary][0].warnings[-1]


def test_gaps_are_explained():
    issuer = Issuer(**{**ISSUER.__dict__, "leases_in_borrowings": True})
    m = mapping(
        line("revenue", Rule(("ifrs-full:Revenue",))),
        line(
            "lease_liabilities_current",
            Rule(("ifrs-full:CurrentLeaseLiabilities",)),
            period="instant",
            group="debt",
        ),
        line("deposits", Rule(("ifrs-full:Deposits",)), period="instant", optional=True),
        line("fuel_cost", Rule(("ifrs-full:FuelExpense",))),
        not_applicable={"fuel_cost": "Not shown by this issuer."},
    )
    f = filing(2024)
    mapped = map_report(issuer, f, report(("ifrs-full:Revenue", period(2024), 1)), m)
    _, gaps = consolidate(issuer, mapped, [f], m)
    reasons = {g.line: (g.reason, g.counts_as_missing) for g in gaps if g.fiscal_year == 2024}
    assert reasons["lease_liabilities_current"] == ("in borrowings", False)
    assert reasons["deposits"] == ("Not reported by this issuer.", False)
    assert reasons["fuel_cost"] == ("Not shown by this issuer.", False)
