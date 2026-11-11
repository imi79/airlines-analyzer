"""One test per metric, on made-up figures calculated by hand.

The example airline (FY2024):
    revenue 1,000   operating profit 100   D&A 50   fuel 270
    borrowings 300 non-current + 100 current   leases 150 non-current + 50 current
    cash 200   short-term deposits 50   advance ticket sales 125
    interest expense 20   interest paid 18   tax paid 10   cash from operations 160   capex 90
  read from the report text (M3):
    ASK 20,000   RPK 16,000   passenger revenue 800   passengers 500   fleet 50 aircraft
    average age 9.5 years   fuel hedged 60%   undrawn committed facilities 150

The example airport (FY2024): revenue 1,000, aeronautical revenue 600, passengers 40 (FY2023: 32).
"""

from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from tearsheet.config import Issuer
from tearsheet.metrics.engine import compute
from tearsheet.normalize.mapper import MappedFact

AIRLINE = Issuer(
    id="abc",
    name="Example Air",
    type="airline",
    lei="X",
    currency="EUR",
    fiscal_year_end="12-31",
    country="FR",
    status="v1",
)
AIRPORT = Issuer(
    id="apt",
    name="Example Airport",
    type="airport",
    lei="Y",
    currency="EUR",
    fiscal_year_end="12-31",
    country="FR",
    status="v1",
)
SETTINGS = {
    "interest_paid_in_financing": False,
    "cash_like": [{"line": "cash"}, {"line": "short_term_deposits"}],
    "associates_in_operating_profit": False,
    "leases_in_borrowings": False,
}
FIGURES = {
    "revenue": 1000,
    "operating_profit": 100,
    "dda": 50,
    "fuel_cost": 270,
    "borrowings_noncurrent": 300,
    "borrowings_current": 100,
    "lease_liabilities_noncurrent": 150,
    "lease_liabilities_current": 50,
    "cash": 200,
    "short_term_deposits": 50,
    "contract_liabilities": 125,
    "interest_expense": 20,
    "interest_paid": 18,
    "tax_paid": 10,
    "cfo": 160,
    "capex": 90,
    "ask": 20000,
    "rpk": 16000,
    "passenger_revenue": 800,
    "passengers": 500,
    "fleet_count": 50,
    "fleet_age": Decimal("9.5"),
    "fuel_hedge_ratio": Decimal("0.6"),
    "undrawn_facilities": 150,
}


def fact(line, value, year=2024, status="verified"):
    return MappedFact(
        issuer="abc",
        fiscal_year=year,
        period_end=date(year, 12, 31),
        line=line,
        value=Decimal(value),
        value_tagged=Decimal(value),
        decimals=0,
        currency="EUR",
        filing_id=f"F{year}",
        comparative=False,
        concepts=(line,),
        fact_ids=("f",),
        rule_source="common",
        sign=1,
        status=status,
    )


def run(figures=None, settings=None, issuer=AIRLINE, drop=()):
    figures = {**FIGURES, **(figures or {})}
    facts = [fact(k, v) for k, v in figures.items() if k not in drop]
    results = compute(issuer, facts, settings={**SETTINGS, **(settings or {})})
    return {r.metric: r for r in results}


def value(results, metric):
    return results[metric].value


@pytest.mark.parametrize(
    "metric, expected",
    [
        ("ebitda", Decimal(150)),  # 100 + 50
        ("ebitda_margin", Decimal("0.15")),  # 150 / 1,000
        ("total_debt", Decimal(600)),  # 300 + 100 + 150 + 50
        ("cash_like", Decimal(250)),  # 200 + 50
        ("net_debt", Decimal(350)),  # 600 - 250
        ("net_leverage", Decimal(350) / Decimal(150)),  # 2.33x
        ("gross_leverage", Decimal(4)),  # 600 / 150
        ("interest_coverage", Decimal("7.5")),  # 150 / 20
        ("ffo", Decimal(122)),  # 150 - 18 - 10
        ("ffo_to_debt", Decimal(122) / Decimal(600)),  # 20.3%
        ("fcf", Decimal(70)),  # 160 - 90
        ("fcf_to_debt", Decimal(70) / Decimal(600)),  # 11.7%
        ("capex_intensity", Decimal("0.09")),  # 90 / 1,000
        ("cash_liquidity", Decimal(250)),
        ("cash_liquidity_to_revenue", Decimal("0.25")),  # 250 / 1,000
        ("advance_ticket_cover", Decimal("0.5")),  # 125 / 250
        ("fuel_share_of_costs", Decimal("0.3")),  # 270 / (1,000 - 100)
        ("liquidity", Decimal(400)),  # 250 + 150
        ("liquidity_to_revenue", Decimal("0.4")),  # 400 / 1,000
        ("passengers", Decimal(500)),
        ("ask", Decimal(20000)),
        ("rpk", Decimal(16000)),
        ("load_factor", Decimal("0.8")),  # 16,000 / 20,000
        ("passenger_yield", Decimal("0.05")),  # 800 / 16,000
        ("rask", Decimal("0.05")),  # 1,000 / 20,000
        ("cask", Decimal("0.045")),  # (1,000 - 100) / 20,000
        ("cask_ex_fuel", Decimal("0.0315")),  # (1,000 - 100 - 270) / 20,000
        ("fleet", Decimal(50)),
        ("fleet_age", Decimal("9.5")),
        ("fuel_hedge_ratio", Decimal("0.6")),
    ],
)
def test_metric_on_the_example_airline(metric, expected):
    result = run()[metric]
    assert result.kind == "value"
    assert result.value == expected
    assert result.note  # every value says what was used


def test_note_says_what_was_used():
    results = run({k: v * 1_000_000 for k, v in FIGURES.items()})  # amounts in millions
    assert results["net_leverage"].note == "Net debt 350 ÷ EBITDA 150 = 2.33x"
    assert results["interest_coverage"].note == "EBITDA 150 ÷ interest expense 20.0 = 7.50x"


def test_associates_inside_operating_profit_are_taken_out_of_ebitda():
    results = run({"share_of_associates": -30}, {"associates_in_operating_profit": True})
    assert value(results, "ebitda") == Decimal(180)  # 100 - (-30) + 50
    assert "share of associates" in results["ebitda"].note


def test_leases_included_in_borrowings_are_not_counted_twice():
    results = run({}, {"leases_in_borrowings": True})
    assert value(results, "total_debt") == Decimal(400)
    assert "included in borrowings" in results["total_debt"].note


def test_borrowings_and_leases_on_one_line():
    results = run({"debt_including_leases": 555})
    assert value(results, "total_debt") == Decimal(555)


def test_interest_paid_is_used_when_interest_expense_is_not_tagged():
    results = run(drop=("interest_expense",))
    assert value(results, "interest_coverage") == Decimal(150) / Decimal(18)
    assert "interest expense not tagged" in results["interest_coverage"].note


def test_finance_costs_are_used_where_interest_paid_is_net():
    # Finnair prints "financial expenses paid, net" (after interest received): decision 0018
    results = run(
        {"finance_costs": 30},
        settings={"interest_basis": "finance_costs"},
        drop=("interest_expense",),
    )
    assert value(results, "interest_coverage") == Decimal(150) / Decimal(30)
    assert "finance costs" in results["interest_coverage"].note


def test_negative_ebitda_makes_leverage_not_meaningful():
    results = run({"operating_profit": -200})  # EBITDA -150
    for metric in ("net_leverage", "gross_leverage", "interest_coverage"):
        assert results[metric].kind == "not_meaningful"
        assert results[metric].value is None
    assert value(results, "ebitda") == Decimal(-150)


def test_cash_like_line_unavailable_before_a_year_leaves_net_debt_missing():
    settings = {
        "cash_like": [{"line": "cash"}, {"line": "other_cash_like", "unavailable_before": 2025}]
    }
    results = run({}, settings)
    assert results["net_debt"].kind == "missing"
    assert "not available for FY2024" in results["net_debt"].reason


def test_cash_like_line_not_reported_counts_as_zero():
    results = run(drop=("short_term_deposits",))
    assert value(results, "cash_like") == Decimal(200)
    assert "not reported (0)" in results["cash_like"].note


def test_missing_input_gives_a_reason_never_zero():
    results = run(drop=("tax_paid",))
    assert results["ffo"].kind == "missing" and results["ffo"].value is None
    assert "Income tax paid not available" in results["ffo"].reason


AIRPORT_FIGURES = {"aero_revenue": 600, "passengers": 40}
AIRPORT_DROP = ("contract_liabilities", "fuel_cost", "ask", "rpk", "passenger_revenue")


def airport(prior=32, settings=None):
    figures = {**FIGURES, **AIRPORT_FIGURES}
    facts = [fact(k, v) for k, v in figures.items() if k not in AIRPORT_DROP]
    if prior is not None:
        facts.append(fact("passengers", prior, year=2023))
    results = compute(AIRPORT, facts, settings={**SETTINGS, **(settings or {})})
    return {r.metric: r for r in results if r.fiscal_year == 2024}


@pytest.mark.parametrize(
    "metric, expected",
    [
        ("traffic_growth", Decimal("0.25")),  # 40 / 32 - 1
        ("revenue_per_passenger", Decimal(25)),  # 1,000 / 40
        ("aero_revenue_per_passenger", Decimal(15)),  # 600 / 40
        ("non_aero_share", Decimal("0.4")),  # (1,000 - 600) / 1,000
    ],
)
def test_metric_on_the_example_airport(metric, expected):
    result = airport()[metric]
    assert result.kind == "value", result.reason
    assert result.value == expected
    assert result.note


def test_traffic_growth_needs_the_prior_year():
    result = airport(prior=None)["traffic_growth"]
    assert result.kind == "missing"
    assert "Passengers not available for FY2023" in result.reason


def test_revenue_per_passenger_can_be_set_not_meaningful():
    reason = "group revenue includes airports outside the passenger scope"
    result = airport(settings={"revenue_per_passenger_not_meaningful": reason})
    assert result["revenue_per_passenger"].kind == "not_meaningful"
    assert reason in result["revenue_per_passenger"].reason


def test_non_aero_share_can_be_set_not_meaningful():
    reason = "group revenue includes airports outside the aeronautical segment"
    result = airport(settings={"non_aero_share_not_meaningful": reason})
    assert result["non_aero_share"].kind == "not_meaningful"
    assert reason in result["non_aero_share"].reason


def test_liquidity_without_undrawn_facilities_is_missing_not_cash_only():
    results = run(drop=("undrawn_facilities",))
    assert results["liquidity"].kind == "missing"
    assert "Undrawn committed credit facilities not available" in results["liquidity"].reason
    assert results["cash_liquidity"].value == Decimal(250)  # the partial figure stays


def test_operating_notes_show_the_working():
    results = run({k: v * 1_000_000 for k, v in FIGURES.items() if k in ("revenue", "ask")})
    assert results["rask"].note == "Revenue 1,000 ÷ ASK 20.0bn = 5.00 cents"


def test_unverified_extracted_figure_makes_the_ratio_unverified():
    facts = [fact(k, v) for k, v in FIGURES.items() if k != "ask"]
    facts.append(fact("ask", 20000, status="unverified"))
    results = {r.metric: r for r in compute(AIRLINE, facts, settings=SETTINGS)}
    assert results["rask"].status == "unverified"
    assert results["fleet"].status == "verified"


def test_overridden_figure_counts_as_reviewed():
    facts = [fact(k, v) for k, v in FIGURES.items() if k != "ask"]
    facts.append(fact("ask", 20000, status="overridden"))
    results = {r.metric: r for r in compute(AIRLINE, facts, settings=SETTINGS)}
    assert results["rask"].status == "verified"


def test_airline_only_metrics_are_skipped_for_airports():
    results = run(issuer=AIRPORT, drop=("contract_liabilities", "fuel_cost"))
    assert "advance_ticket_cover" not in results and "fuel_share_of_costs" not in results
    assert "traffic_growth" in results


def test_unreviewed_input_makes_the_metric_unverified():
    facts = [fact(k, v) for k, v in FIGURES.items() if k != "cash"]
    facts.append(fact("cash", 200, status="unverified"))
    results = {r.metric: r for r in compute(AIRLINE, facts, settings=SETTINGS)}
    assert results["net_debt"].status == "unverified"
    assert results["ebitda"].status == "verified"


# --- M8: cash flow after leases and refinancing -----------------------------------------------
# The example airline also has: disposal proceeds 30, lease payments 40.
M8 = {"disposal_proceeds": 30, "lease_payments": 40}


@pytest.mark.parametrize(
    "metric, expected",
    [
        ("net_capex", Decimal(60)),  # 90 - 30
        ("fcf_after_leases", Decimal(60)),  # 160 - 60 - 40
        ("fcf_after_leases_to_debt", Decimal("0.1")),  # 60 / 600
        ("debt_due_1y", Decimal(150)),  # 100 + 50
        ("short_term_debt_cover", Decimal(400) / Decimal(150)),  # 2.67x
    ],
)
def test_m8_metric_on_the_example_airline(metric, expected):
    result = run(M8)[metric]
    assert result.kind == "value", result.reason
    assert result.value == expected
    assert result.note


def test_net_capex_without_disposals_counts_them_as_zero():
    results = run({"lease_payments": 40})
    assert value(results, "net_capex") == Decimal(90)
    assert "not reported (0)" in results["net_capex"].note


def test_fcf_after_leases_takes_out_interest_shown_in_financing():
    results = run(M8, settings={"interest_paid_in_financing": True})
    assert value(results, "fcf_after_leases") == Decimal(42)  # 160 - 60 - 40 - 18
    assert "interest paid (in financing)" in results["fcf_after_leases"].note


def test_the_tagged_concept_says_where_interest_paid_sits():
    facts = [fact(k, v) for k, v in {**FIGURES, **M8}.items() if k != "interest_paid"]
    paid = fact("interest_paid", 18)
    financing = ("ifrs-full:InterestPaidClassifiedAsFinancingActivities",)
    facts.append(replace(paid, concepts=financing))
    results = {r.metric: r for r in compute(AIRLINE, facts, settings=SETTINGS)}
    assert results["fcf_after_leases"].value == Decimal(42)
    operating = ("ifrs-full:InterestPaidClassifiedAsOperatingActivities",)
    facts[-1] = replace(paid, concepts=operating)
    settings = {**SETTINGS, "interest_paid_in_financing": True}  # the concept wins
    results = {r.metric: r for r in compute(AIRLINE, facts, settings=settings)}
    assert results["fcf_after_leases"].value == Decimal(60)


def test_fcf_after_leases_needs_the_lease_payments():
    results = run({"disposal_proceeds": 30})
    assert results["fcf_after_leases"].kind == "missing"
    assert "Lease payments" in results["fcf_after_leases"].reason


def test_debt_due_within_a_year_where_leases_sit_in_borrowings():
    results = run(M8, settings={"leases_in_borrowings": True})
    assert value(results, "debt_due_1y") == Decimal(100)
    assert "included in borrowings" in results["debt_due_1y"].note


def test_debt_due_within_a_year_needs_the_current_part():
    results = run({**M8, "borrowings_total": 400}, drop=("borrowings_current",))
    assert results["debt_due_1y"].kind == "missing"


WALL = {"maturity_borrowings_0_1": 100, "maturity_borrowings_1_2": 80,
        "maturity_borrowings_2_5": 150, "maturity_borrowings_5_plus": 70}  # fmt: skip


def test_borrowings_due_within_two_years_from_the_maturity_wall():
    results = run({**M8, **WALL})
    assert value(results, "borrowings_due_2y") == Decimal(180)  # 100 + 80
    assert value(results, "liquidity_to_borrowings_due_2y") == Decimal(400) / Decimal(180)


def test_a_wall_without_the_second_year_on_its_own_gives_no_two_year_figure():
    wall = {"maturity_borrowings_0_1": 100, "maturity_borrowings_1_5": 230,
            "maturity_borrowings_5_plus": 70}  # fmt: skip
    results = run({**M8, **wall})
    assert results["borrowings_due_2y"].kind == "missing"
    assert "second year" in results["borrowings_due_2y"].reason


def test_an_unverified_wall_makes_the_two_year_figure_unverified():
    facts = [fact(k, v) for k, v in {**FIGURES, **M8}.items()]
    facts += [fact(k, v, status="unverified") for k, v in WALL.items()]
    results = {r.metric: r for r in compute(AIRLINE, facts, settings=SETTINGS)}
    assert results["borrowings_due_2y"].status == "unverified"
