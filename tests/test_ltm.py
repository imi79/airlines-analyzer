"""Last-twelve-months figures (M10): the arithmetic, the statuses and the missing cases."""

from datetime import date
from decimal import Decimal

from tearsheet.config import load_issuers
from tearsheet.extract import half_year as h
from tearsheet.extract.half_year import HalfYearRun, LineRead, RowRead
from tearsheet.metrics import ltm
from tearsheet.metrics.engine import compute
from tearsheet.normalize.mapper import MappedFact

M = Decimal(1_000_000)
ISSUERS = {i.id: i for i in load_issuers()}
FINNAIR = ISSUERS["finnair"]
REPORT = h.Report(
    "finnair-h1", "finnair", date(2026, 6, 30), 2025, "en", "Half-year report", "x.pdf", "0" * 64
)
STATEMENTS = {k: v["statement"] for k, v in h.load_settings()["lines"].items()}

# line: (FY2025, first half 2026 or 30 June 2026, first half 2025), in millions
FIGURES = {
    "revenue": ("3106.2", "1694.8", "1481.9"),
    "operating_profit": ("64.2", "90.2", "-34.2"),
    "dda": ("343.7", "170.1", "172.8"),
    "finance_costs": ("81.9", "41.1", "44.8"),
    "cfo": ("401.9", "456.5", "235.8"),
    "capex": ("209.0", "173.3", "124.4"),
    "disposal_proceeds": ("8.3", "11.1", "0.4"),
    "lease_payments": ("150.4", "66.3", "78.3"),
    "interest_paid": ("87.4", "30.3", "62.7"),
    "tax_paid": ("0.1", "0.0", "0.1"),
    "cash": ("529.6", "234.2", None),
    "other_current_financial_assets": ("531.4", "1017.8", None),
    "borrowings_current": ("51.5", "21.2", None),
    "borrowings_noncurrent": ("968.6", "958.3", None),
    "lease_liabilities_current": ("130.4", "127.0", None),
    "lease_liabilities_noncurrent": ("632.3", "604.4", None),
}


def annual(line: str, value: str, status: str = "verified", year: int = 2025) -> MappedFact:
    return MappedFact(
        issuer="finnair",
        fiscal_year=year,
        period_end=date(year, 12, 31),
        line=line,
        value=Decimal(value) * M,
        value_tagged=Decimal(value) * M,
        decimals=-5,
        currency="EUR",
        filing_id="annual",
        comparative=False,
        concepts=("ifrs-full:X",),
        fact_ids=("f",),
        rule_source="common",
        sign=1,
        status=status,
    )


def read(line: str, current: str, prior: str | None, failures=()) -> LineRead:
    x = LineRead(line, STATEMENTS[line], rows=[RowRead(line, "add", 27, "row")])
    x.current = Decimal(current) * M
    x.prior = None if prior is None else Decimal(prior) * M
    x.failures = list(failures)
    x.decimals = -5
    return x


def load(figures=None, flagged=(), drop=(), unverified_annual=(), report=REPORT, issuer=FINNAIR):
    figures = figures or FIGURES
    facts = [
        annual(k, v[0], "unverified" if k in unverified_annual else "verified")
        for k, v in figures.items()
    ]
    run = HalfYearRun(report)
    for k, (_, current, prior) in figures.items():
        if k in drop:
            run.not_found[k] = "not a row of the condensed statement"
            continue
        run.lines.append(read(k, current, prior, ["flagged"] if k in flagged else ()))
    return ltm.build(issuer, run, facts), facts


def value(result, concept: str) -> Decimal | None:
    line = next((f.value for f in result.ltm if f.line == concept), None)
    if line is not None:
        return line
    return next((r.value for r in result.metrics if r.metric == concept), None)


def metric(result, concept: str):
    return next(r for r in result.metrics if r.metric == concept)


def test_earnings_add_the_half_and_take_away_last_years_half():
    result, _ = load()
    # The plan's worked example: 3,106.2 + 1,694.8 - 1,481.9 and 64.2 + 90.2 - (-34.2).
    assert value(result, "revenue") == Decimal("3319.1") * M
    assert value(result, "operating_profit") == Decimal("188.6") * M
    assert value(result, "cfo") == Decimal("622.6") * M


def test_a_first_half_doubled_is_not_ltm():
    result, _ = load()
    assert value(result, "operating_profit") != 2 * Decimal("90.2") * M


def test_balance_sheet_lines_are_taken_at_the_half_year_date():
    result, _ = load()
    assert value(result, "cash") == Decimal("234.2") * M
    cash = next(f for f in result.ltm if f.line == "cash")
    assert cash.period_end == date(2026, 6, 30) and "half-year balance sheet" in cash.note


def test_ltm_metrics_use_the_same_formulas():
    result, _ = load()
    ebitda = Decimal("188.6") + Decimal("343.7") + Decimal("170.1") - Decimal("172.8")
    assert value(result, "ebitda") == ebitda * M
    debt = Decimal("21.2") + Decimal("958.3") + Decimal("127.0") + Decimal("604.4")
    net_debt = debt - Decimal("234.2") - Decimal("1017.8")
    assert value(result, "net_debt") == net_debt * M
    assert value(result, "net_leverage") == net_debt / ebitda  # debt at 30 June over LTM EBITDA
    assert metric(result, "net_leverage").status == "verified"
    assert "LTM" not in (metric(result, "net_leverage").note or "")  # the formula's own words


def test_the_parts_of_an_ltm_figure_are_on_its_record():
    result, _ = load()
    revenue = next(f for f in result.ltm if f.line == "revenue")
    parts = revenue.ref["parts"]
    assert [p["period"] for p in parts] == ["FY2025", "H1", "H1_prior"]
    assert [p["sign"] for p in parts] == ["+", "+", "-"]
    assert revenue.ref["audit"] == "unaudited" and "3,106" in revenue.note


def test_an_unverified_half_makes_the_ltm_figure_unverified():
    result, _ = load(flagged=("operating_profit",))
    assert next(f for f in result.ltm if f.line == "operating_profit").status == "unverified"
    assert metric(result, "ebitda").status == "unverified"
    assert metric(result, "net_leverage").status == "unverified"
    assert metric(result, "net_debt").status == "verified"  # debt and cash are not touched


def test_an_unverified_full_year_makes_the_ltm_figure_unverified():
    result, _ = load(unverified_annual=("dda",))
    assert next(f for f in result.ltm if f.line == "dda").status == "unverified"


def test_a_line_missing_at_the_half_year_is_never_counted_as_zero():
    result, _ = load(drop=("other_current_financial_assets",))
    net_debt = metric(result, "net_debt")
    assert net_debt.value is None and net_debt.kind == "missing"
    assert (
        "LTM Jun 2026" in net_debt.reason and "not in the half-year statements" in net_debt.reason
    )
    assert metric(result, "net_leverage").value is None
    assert metric(result, "ebitda").value is not None


def test_missing_disposal_proceeds_do_not_overstate_net_capex():
    result, _ = load(drop=("disposal_proceeds",))
    assert metric(result, "net_capex").value is None
    assert metric(result, "fcf_after_leases").value is None
    assert metric(result, "fcf").value is not None  # free cash flow does not use them


def test_the_same_half_a_year_before_is_needed():
    figures = dict(FIGURES) | {"revenue": ("3106.2", "1694.8", None)}
    facts = [annual(k, v[0]) for k, v in figures.items()]
    run = HalfYearRun(REPORT)
    for k, (_, current, prior) in figures.items():
        run.lines.append(read(k, current, prior))
    result = ltm.build(FINNAIR, run, facts)
    assert value(result, "revenue") is None
    assert metric(result, "ebitda_margin").value is None


def test_metrics_that_need_the_annual_report_text_are_missing_with_the_reason():
    result, _ = load()
    liquidity = metric(result, "liquidity")
    assert liquidity.value is None and "half-year reports are condensed" in liquidity.reason


def test_non_december_year_end():
    easyjet = ISSUERS["easyjet"]
    report = h.Report("easyjet-h1", "easyjet", date(2026, 3, 31), 2025, "en", "d", "f", "0")
    figures = {"revenue": ("10106", "3954", "3534"), "cash": ("1504", "2288", None)}
    facts = [
        MappedFact(
            issuer="easyjet",
            fiscal_year=2025,
            period_end=date(2025, 9, 30),
            line=k,
            value=Decimal(v[0]) * M,
            value_tagged=Decimal(v[0]) * M,
            decimals=-6,
            currency="GBP",
            filing_id="annual",
            comparative=False,
            concepts=(),
            fact_ids=(),
            rule_source="c",
            sign=1,
        )
        for k, v in figures.items()
    ]
    run = HalfYearRun(report)
    for k, (_, current, prior) in figures.items():
        run.lines.append(read(k, current, prior))
    result = ltm.build(easyjet, run, facts)
    assert report.ltm_label == "LTM Mar 2026"
    assert value(result, "revenue") == (10106 + 3954 - 3534) * M  # April 2025 to March 2026
    revenue = next(f for f in result.ltm if f.line == "revenue")
    assert revenue.period_end == date(2026, 3, 31) and "2025-03-31" in revenue.note


def test_the_fiscal_year_metrics_are_not_changed_by_the_half_year():
    result, facts = load()
    before = compute(FINNAIR, facts)
    again = compute(FINNAIR, facts)
    assert before == again
    assert all(r.fiscal_year == 2025 for r in before)
    assert {f.rule_source for f in result.h1 + result.ltm} == {"H1", "H1_prior", "LTM"}


def test_report_that_was_not_read_gives_no_figures_and_says_why():
    facts = [annual(k, v[0]) for k, v in FIGURES.items()]
    run = HalfYearRun(REPORT, error=h.NOT_RUN)
    result = ltm.build(FINNAIR, run, facts)
    assert not result.ltm
    assert "not read yet" in metric(result, "ebitda").reason
