"""One function per metric in catalog.yaml.

Each function reads the issuer-year's figures through a Context and returns the value with a
short note saying what was used ("Net debt 7,332 ÷ EBITDA 4,109"). A missing input raises
Missing, and a ratio whose denominator is zero or negative raises NotMeaningful.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal

ZERO = Decimal(0)


class Missing(Exception):
    """An input is not available; the message says which and why."""


class NotMeaningful(Exception):
    """The ratio exists but means nothing (for example leverage on negative EBITDA)."""


@dataclass(frozen=True)
class Input:
    name: str  # canonical line id or metric id
    label: str
    value: Decimal
    source: str  # filing id for a figure, "metric" for another metric
    status: str  # verified | unverified


@dataclass
class Context:
    """The figures and settings for one issuer and fiscal year."""

    issuer_type: str
    fiscal_year: int
    lines: dict  # line id -> MappedFact (primary)
    labels: dict[str, str]  # line or metric id -> label
    settings: dict
    results: dict = field(default_factory=dict)  # metric id -> Result, filled as computed
    used: list[Input] = field(default_factory=list)
    prior: dict = field(default_factory=dict)  # line id -> MappedFact for the year before

    def has(self, line: str) -> bool:
        return line in self.lines

    def line(self, line: str) -> Decimal:
        fact = self.lines.get(line)
        if fact is None:
            raise Missing(f"{self.labels[line]} not available for FY{self.fiscal_year}")
        self.used.append(Input(line, self.labels[line], fact.value, fact.filing_id, fact.status))
        return fact.value

    def prior_line(self, line: str) -> Decimal:
        fact = self.prior.get(line)
        if fact is None:
            raise Missing(f"{self.labels[line]} not available for FY{self.fiscal_year - 1}")
        self.used.append(Input(line, self.labels[line], fact.value, fact.filing_id, fact.status))
        return fact.value

    def metric(self, metric: str) -> Decimal:
        result = self.results[metric]
        if result.value is None:
            raise Missing(f"{self.labels[metric]}: {result.reason}")
        self.used.append(Input(metric, self.labels[metric], result.value, "metric", result.status))
        return result.value


def m(value: Decimal) -> str:
    """Millions for a note: 7,332 or 4.3."""
    millions = value / Decimal(1_000_000)
    return f"{millions:,.1f}" if abs(millions) < 100 else f"{millions:,.0f}"


def ratio(top: Decimal, bottom: Decimal) -> Decimal:
    if bottom <= 0:
        raise NotMeaningful("denominator is zero or negative")
    return top / bottom


def big(value: Decimal) -> str:
    """Counts for a note: 134.5bn, 93.4m, 356."""
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.1f}bn"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.1f}m"
    return f"{value:,.0f}"


def cents(value: Decimal) -> str:
    return f"{value * 100:.2f} cents"


def x(value: Decimal) -> str:
    return f"{value:.2f}x"


def pct(value: Decimal) -> str:
    return f"{value * 100:.1f}%"


# --- Credit metrics ---------------------------------------------------------------------------


def ebitda(c: Context) -> tuple[Decimal, str]:
    op, dda = c.line("operating_profit"), c.line("dda")
    if c.settings.get("associates_in_operating_profit"):
        assoc = c.line("share_of_associates")
        value = op - assoc + dda
        return value, (
            f"Operating profit {m(op)} − share of associates ({m(assoc)}) + D&A {m(dda)}"
            f" = {m(value)}"
        )
    return op + dda, f"Operating profit {m(op)} + D&A {m(dda)} = {m(op + dda)}"


def ebitda_margin(c: Context) -> tuple[Decimal, str]:
    e, rev = c.metric("ebitda"), c.line("revenue")
    value = ratio(e, rev)
    return value, f"EBITDA {m(e)} ÷ revenue {m(rev)} = {pct(value)}"


def total_debt(c: Context) -> tuple[Decimal, str]:
    parts = []
    if c.has("debt_including_leases"):
        debt = c.line("debt_including_leases")
        return debt, f"Borrowings and lease liabilities (one line) {m(debt)}"
    if c.has("borrowings_current") or c.has("borrowings_noncurrent"):
        borrowings = ZERO
        for line in ("borrowings_noncurrent", "borrowings_current"):
            if c.has(line):
                v = c.line(line)
                borrowings += v
                parts.append(f"{c.labels[line].lower()} {m(v)}")
    elif c.has("borrowings_total"):
        borrowings = c.line("borrowings_total")
        parts.append(f"borrowings {m(borrowings)}")
    else:
        raise Missing(f"Borrowings not available for FY{c.fiscal_year}")

    leases = ZERO
    if c.settings.get("leases_in_borrowings"):
        note = "lease liabilities included in borrowings"
    elif c.has("lease_liabilities_current") or c.has("lease_liabilities_noncurrent"):
        for line in ("lease_liabilities_noncurrent", "lease_liabilities_current"):
            if c.has(line):
                v = c.line(line)
                leases += v
                parts.append(f"{c.labels[line].lower()} {m(v)}")
        note = None
    elif c.has("lease_liabilities_total"):
        leases = c.line("lease_liabilities_total")
        parts.append(f"lease liabilities {m(leases)}")
        note = None
    else:
        raise Missing(f"Lease liabilities not available for FY{c.fiscal_year}")
    value = borrowings + leases
    text = " + ".join(parts) + f" = {m(value)}"
    return value, text[0].upper() + text[1:] + (f" ({note})" if note else "")


def cash_like(c: Context) -> tuple[Decimal, str]:
    total, parts = ZERO, []
    for item in c.settings["cash_like"]:
        line = item["line"]
        if c.has(line):
            v = c.line(line)
            total += v
            parts.append(f"{c.labels[line].lower()} {m(v)}")
        elif line == "cash" or c.fiscal_year < item.get("unavailable_before", 0):
            raise Missing(f"{c.labels[line]} not available for FY{c.fiscal_year}")
        else:
            parts.append(f"{c.labels[line].lower()} not reported (0)")
    text = " + ".join(parts) + f" = {m(total)}"
    return total, text[0].upper() + text[1:]


def net_debt(c: Context) -> tuple[Decimal, str]:
    debt, cash = c.metric("total_debt"), c.metric("cash_like")
    value = debt - cash
    return value, f"Total debt {m(debt)} − cash and cash-like {m(cash)} = {m(value)}"


def _leverage(c: Context, numerator: str) -> tuple[Decimal, str]:
    top, e = c.metric(numerator), c.metric("ebitda")
    if e <= 0:
        raise NotMeaningful(f"EBITDA is negative ({m(e)})")
    value = top / e
    return value, f"{c.labels[numerator]} {m(top)} ÷ EBITDA {m(e)} = {x(value)}"


def net_leverage(c: Context) -> tuple[Decimal, str]:
    return _leverage(c, "net_debt")


def gross_leverage(c: Context) -> tuple[Decimal, str]:
    return _leverage(c, "total_debt")


def interest_coverage(c: Context) -> tuple[Decimal, str]:
    e = c.metric("ebitda")
    if c.settings.get("interest_basis") == "finance_costs":
        # interest paid is printed net of interest received (metric_settings, decision 0018)
        interest, basis = c.line("finance_costs"), "finance costs (interest paid is net)"
    elif c.has("interest_expense"):
        interest, basis = c.line("interest_expense"), "interest expense"
    else:
        interest, basis = c.line("interest_paid"), "interest paid (interest expense not tagged)"
    if e <= 0:
        raise NotMeaningful(f"EBITDA is negative ({m(e)})")
    if interest <= 0:
        raise NotMeaningful(f"interest is zero or negative ({m(interest)})")
    value = e / interest
    return value, f"EBITDA {m(e)} ÷ {basis} {m(interest)} = {x(value)}"


def ffo(c: Context) -> tuple[Decimal, str]:
    e, interest, tax = c.metric("ebitda"), c.line("interest_paid"), c.line("tax_paid")
    value = e - interest - tax
    return value, (f"EBITDA {m(e)} − interest paid {m(interest)} − tax paid {m(tax)} = {m(value)}")


def _to_debt(c: Context, numerator: str) -> tuple[Decimal, str]:
    top, debt = c.metric(numerator), c.metric("total_debt")
    value = ratio(top, debt)
    return value, f"{c.labels[numerator]} {m(top)} ÷ total debt {m(debt)} = {pct(value)}"


def ffo_to_debt(c: Context) -> tuple[Decimal, str]:
    return _to_debt(c, "ffo")


def fcf(c: Context) -> tuple[Decimal, str]:
    cfo, capex = c.line("cfo"), c.line("capex")
    value = cfo - capex
    return value, f"Cash from operations {m(cfo)} − capex {m(capex)} = {m(value)}"


def fcf_to_debt(c: Context) -> tuple[Decimal, str]:
    return _to_debt(c, "fcf")


# --- Cash flow after leases (M8) -------------------------------------------------------------


def net_capex(c: Context) -> tuple[Decimal, str]:
    capex = c.line("capex")
    if not c.has("disposal_proceeds"):
        return capex, f"Capex {m(capex)} − disposal proceeds not reported (0) = {m(capex)}"
    sold = c.line("disposal_proceeds")
    value = capex - sold
    return value, f"Capex {m(capex)} − disposal proceeds {m(sold)} = {m(value)}"


def interest_paid_in_financing(c: Context) -> bool:
    """Where the year's interest paid sits in the cash flow statement: read from the tagged
    concept ("...ClassifiedAsFinancingActivities"); for a company concept or a figure entered
    by hand, from metric_settings.yaml, with the evidence (decision 0022)."""
    fact = c.lines.get("interest_paid")
    concepts = " ".join(fact.concepts) if fact is not None else ""
    if "FinancingActivities" in concepts:
        return True
    if "OperatingActivities" in concepts:
        return False
    setting = c.settings.get("interest_paid_in_financing")
    if setting is None:
        raise Missing(
            f"cannot tell whether interest paid sits in operating or financing cash flows for "
            f"FY{c.fiscal_year}"
        )
    return bool(setting)


def fcf_after_leases(c: Context) -> tuple[Decimal, str]:
    """Interest paid is deducted only where the company shows it in financing cash flows:
    elsewhere it is already inside cash from operations (decision 0022)."""
    cfo, capex, leases = c.line("cfo"), c.metric("net_capex"), c.line("lease_payments")
    value = cfo - capex - leases
    text = f"Cash from operations {m(cfo)} − net capex {m(capex)} − lease payments {m(leases)}"
    if interest_paid_in_financing(c):
        interest = c.line("interest_paid")
        value -= interest
        text += f" − interest paid (in financing) {m(interest)}"
    return value, f"{text} = {m(value)}"


def fcf_after_leases_to_debt(c: Context) -> tuple[Decimal, str]:
    return _to_debt(c, "fcf_after_leases")


def capex_intensity(c: Context) -> tuple[Decimal, str]:
    capex, rev = c.line("capex"), c.line("revenue")
    value = ratio(capex, rev)
    return value, f"Capex {m(capex)} ÷ revenue {m(rev)} = {pct(value)}"


def cash_liquidity(c: Context) -> tuple[Decimal, str]:
    value = c.metric("cash_like")
    return value, f"Cash and cash-like {m(value)} (without undrawn facilities)"


def cash_liquidity_to_revenue(c: Context) -> tuple[Decimal, str]:
    liq, rev = c.metric("cash_liquidity"), c.line("revenue")
    value = ratio(liq, rev)
    return value, f"Cash liquidity {m(liq)} ÷ revenue {m(rev)} = {pct(value)}"


def advance_ticket_cover(c: Context) -> tuple[Decimal, str]:
    ats, cash = c.line("contract_liabilities"), c.metric("cash_like")
    value = ratio(ats, cash)
    return value, f"Advance ticket sales {m(ats)} ÷ cash and cash-like {m(cash)} = {pct(value)}"


def fuel_share_of_costs(c: Context) -> tuple[Decimal, str]:
    fuel, rev, op = c.line("fuel_cost"), c.line("revenue"), c.line("operating_profit")
    costs = rev - op
    value = ratio(fuel, costs)
    return value, (
        f"Fuel {m(fuel)} ÷ operating costs {m(costs)} (revenue {m(rev)} − operating profit "
        f"{m(op)}) = {pct(value)}"
    )


def liquidity(c: Context) -> tuple[Decimal, str]:
    cash, undrawn = c.metric("cash_like"), c.line("undrawn_facilities")
    value = cash + undrawn
    return value, (
        f"Cash and cash-like {m(cash)} + undrawn committed facilities {m(undrawn)} = {m(value)}"
    )


def liquidity_to_revenue(c: Context) -> tuple[Decimal, str]:
    liq, rev = c.metric("liquidity"), c.line("revenue")
    value = ratio(liq, rev)
    return value, f"Liquidity {m(liq)} ÷ revenue {m(rev)} = {pct(value)}"


# --- Refinancing (M8) ------------------------------------------------------------------------


def debt_due_1y(c: Context) -> tuple[Decimal, str]:
    """The current part of total debt, as the balance sheet shows it."""
    if not c.has("borrowings_current"):
        raise Missing(f"Current borrowings not reported separately for FY{c.fiscal_year}")
    borrowings = c.line("borrowings_current")
    if c.settings.get("leases_in_borrowings"):
        return borrowings, (
            f"Current borrowings {m(borrowings)} (lease liabilities included in borrowings)"
        )
    if not c.has("lease_liabilities_current"):
        raise Missing(f"Current lease liabilities not reported separately for FY{c.fiscal_year}")
    leases = c.line("lease_liabilities_current")
    value = borrowings + leases
    return value, (
        f"Current borrowings {m(borrowings)} + current lease liabilities {m(leases)} = {m(value)}"
    )


def short_term_debt_cover(c: Context) -> tuple[Decimal, str]:
    liq, due = c.metric("liquidity"), c.metric("debt_due_1y")
    value = ratio(liq, due)
    return value, f"Liquidity {m(liq)} ÷ debt due within one year {m(due)} = {x(value)}"


def cash_short_term_debt_cover(c: Context) -> tuple[Decimal, str]:
    cash, due = c.metric("cash_liquidity"), c.metric("debt_due_1y")
    value = ratio(cash, due)
    return value, (f"Cash liquidity {m(cash)} ÷ debt due within one year {m(due)} = {x(value)} "
                   "(without undrawn lines)")  # fmt: skip


# --- Operating metrics (figures read from the report text, M3) ------------------------------


def _figure(c: Context, line: str, unit: str = "count") -> tuple[Decimal, str]:
    value = c.line(line)
    shown = big(value) if unit == "count" else f"{value:.1f} years"
    return value, f"{c.labels[line]} {shown}, read from the report"


def passengers(c: Context) -> tuple[Decimal, str]:
    return _figure(c, "passengers")


def ask(c: Context) -> tuple[Decimal, str]:
    return _figure(c, "ask")


def rpk(c: Context) -> tuple[Decimal, str]:
    return _figure(c, "rpk")


def fleet(c: Context) -> tuple[Decimal, str]:
    return _figure(c, "fleet_count")


def fleet_age(c: Context) -> tuple[Decimal, str]:
    return _figure(c, "fleet_age", "years")


def fuel_hedge_ratio(c: Context) -> tuple[Decimal, str]:
    value = c.line("fuel_hedge_ratio")
    return value, f"Fuel hedged for the next twelve months {pct(value)}, read from the report"


def load_factor(c: Context) -> tuple[Decimal, str]:
    traffic, capacity = c.line("rpk"), c.line("ask")
    value = ratio(traffic, capacity)
    return value, f"RPK {big(traffic)} ÷ ASK {big(capacity)} = {pct(value)}"


def passenger_yield(c: Context) -> tuple[Decimal, str]:
    revenue, traffic = c.line("passenger_revenue"), c.line("rpk")
    value = ratio(revenue, traffic)
    return value, f"Passenger revenue {m(revenue)} ÷ RPK {big(traffic)} = {cents(value)}"


def rask(c: Context) -> tuple[Decimal, str]:
    rev, capacity = c.line("revenue"), c.line("ask")
    value = ratio(rev, capacity)
    return value, f"Revenue {m(rev)} ÷ ASK {big(capacity)} = {cents(value)}"


def cask(c: Context) -> tuple[Decimal, str]:
    rev, op, capacity = c.line("revenue"), c.line("operating_profit"), c.line("ask")
    value = ratio(rev - op, capacity)
    return value, (
        f"Operating costs {m(rev - op)} (revenue {m(rev)} − operating profit {m(op)}) ÷ ASK "
        f"{big(capacity)} = {cents(value)}"
    )


def cask_ex_fuel(c: Context) -> tuple[Decimal, str]:
    rev, op, fuel = c.line("revenue"), c.line("operating_profit"), c.line("fuel_cost")
    capacity = c.line("ask")
    costs = rev - op - fuel
    value = ratio(costs, capacity)
    return value, (
        f"Operating costs excluding fuel {m(costs)} (revenue {m(rev)} − operating profit "
        f"{m(op)} − fuel {m(fuel)}) ÷ ASK {big(capacity)} = {cents(value)}"
    )


def traffic_growth(c: Context) -> tuple[Decimal, str]:
    now, before = c.line("passengers"), c.prior_line("passengers")
    if before <= 0:
        raise NotMeaningful("no passengers the year before")
    value = now / before - 1
    return value, (
        f"Passengers {big(now)} ÷ prior-year passengers {big(before)} − 1 = {pct(value)}"
    )


def revenue_per_passenger(c: Context) -> tuple[Decimal, str]:
    reason = c.settings.get("revenue_per_passenger_not_meaningful")
    if reason:
        raise NotMeaningful(reason.strip())
    rev, pax = c.line("revenue"), c.line("passengers")
    value = ratio(rev, pax)
    return value, f"Revenue {m(rev)} ÷ passengers {big(pax)} = {value:.2f}"


def aero_revenue_per_passenger(c: Context) -> tuple[Decimal, str]:
    aero, pax = c.line("aero_revenue"), c.line("passengers")
    value = ratio(aero, pax)
    return value, f"Aeronautical revenue {m(aero)} ÷ passengers {big(pax)} = {value:.2f}"


def non_aero_share(c: Context) -> tuple[Decimal, str]:
    reason = c.settings.get("non_aero_share_not_meaningful")
    if reason:
        raise NotMeaningful(reason.strip())
    rev, aero = c.line("revenue"), c.line("aero_revenue")
    value = ratio(rev - aero, rev)
    return value, (
        f"(Revenue {m(rev)} − aeronautical revenue {m(aero)}) ÷ revenue {m(rev)} = {pct(value)}"
    )


FORMULAS: dict[str, Callable[[Context], tuple[Decimal, str]]] = {
    "ebitda": ebitda,
    "ebitda_margin": ebitda_margin,
    "total_debt": total_debt,
    "cash_like": cash_like,
    "net_debt": net_debt,
    "net_leverage": net_leverage,
    "gross_leverage": gross_leverage,
    "interest_coverage": interest_coverage,
    "ffo": ffo,
    "ffo_to_debt": ffo_to_debt,
    "fcf": fcf,
    "fcf_to_debt": fcf_to_debt,
    "net_capex": net_capex,
    "fcf_after_leases": fcf_after_leases,
    "fcf_after_leases_to_debt": fcf_after_leases_to_debt,
    "capex_intensity": capex_intensity,
    "cash_liquidity": cash_liquidity,
    "cash_liquidity_to_revenue": cash_liquidity_to_revenue,
    "advance_ticket_cover": advance_ticket_cover,
    "fuel_share_of_costs": fuel_share_of_costs,
    "liquidity": liquidity,
    "liquidity_to_revenue": liquidity_to_revenue,
    "debt_due_1y": debt_due_1y,
    "short_term_debt_cover": short_term_debt_cover,
    "cash_short_term_debt_cover": cash_short_term_debt_cover,
    "passengers": passengers,
    "ask": ask,
    "rpk": rpk,
    "load_factor": load_factor,
    "passenger_yield": passenger_yield,
    "rask": rask,
    "cask": cask,
    "cask_ex_fuel": cask_ex_fuel,
    "fleet": fleet,
    "fleet_age": fleet_age,
    "fuel_hedge_ratio": fuel_hedge_ratio,
    "traffic_growth": traffic_growth,
    "revenue_per_passenger": revenue_per_passenger,
    "aero_revenue_per_passenger": aero_revenue_per_passenger,
    "non_aero_share": non_aero_share,
}


# --- From the maturity wall (M8) --------------------------------------------------------------


def borrowings_due_2y(c: Context) -> tuple[Decimal, str]:
    """Borrowings (leases left out) falling due within two years, from the maturity table."""
    if c.has("maturity_borrowings_0_2"):
        value = c.line("maturity_borrowings_0_2")
        return value, f"Borrowings due within 2 years {m(value)}, from the maturity table"
    if c.has("maturity_borrowings_0_1") and c.has("maturity_borrowings_1_2"):
        first, second = c.line("maturity_borrowings_0_1"), c.line("maturity_borrowings_1_2")
        value = first + second
        return value, (
            f"Borrowings due within 1 year {m(first)} + in 1 to 2 years {m(second)} = {m(value)},"
            " from the maturity table"
        )
    if any(k.startswith("maturity_borrowings_") for k in c.lines):
        raise Missing("the maturity table does not show the second year on its own")
    raise Missing(f"No checked maturity table of borrowings for FY{c.fiscal_year}")


def liquidity_to_borrowings_due_2y(c: Context) -> tuple[Decimal, str]:
    liq, due = c.metric("liquidity"), c.metric("borrowings_due_2y")
    value = ratio(liq, due)
    return value, f"Liquidity {m(liq)} ÷ borrowings due within 2 years {m(due)} = {x(value)}"


FORMULAS["borrowings_due_2y"] = borrowings_due_2y
FORMULAS["liquidity_to_borrowings_due_2y"] = liquidity_to_borrowings_due_2y
