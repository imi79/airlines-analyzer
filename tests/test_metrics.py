"""One test per metric, on made-up figures calculated by hand.

The example airline (FY2024):
    revenue 1,000   operating profit 100   D&A 50   fuel 270
    borrowings 300 non-current + 100 current   leases 150 non-current + 50 current
    cash 200   short-term deposits 50   advance ticket sales 125
    interest expense 20   interest paid 18   tax paid 10   cash from operations 160   capex 90
"""

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


def test_metrics_needing_report_text_wait_for_m3():
    results = run()
    assert results["ask"].kind == "needs_m3"
    assert results["liquidity"].kind == "needs_m3"


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
