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

    def has(self, line: str) -> bool:
        return line in self.lines

    def line(self, line: str) -> Decimal:
        fact = self.lines.get(line)
        if fact is None:
            raise Missing(f"{self.labels[line]} not available for FY{self.fiscal_year}")
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
    if c.has("interest_expense"):
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


def capex_intensity(c: Context) -> tuple[Decimal, str]:
    capex, rev = c.line("capex"), c.line("revenue")
    value = ratio(capex, rev)
    return value, f"Capex {m(capex)} ÷ revenue {m(rev)} = {pct(value)}"


def cash_liquidity(c: Context) -> tuple[Decimal, str]:
    value = c.metric("cash_like")
    return value, f"Cash and cash-like {m(value)} (undrawn facilities added in M3)"


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
    "capex_intensity": capex_intensity,
    "cash_liquidity": cash_liquidity,
    "cash_liquidity_to_revenue": cash_liquidity_to_revenue,
    "advance_ticket_cover": advance_ticket_cover,
    "fuel_share_of_costs": fuel_share_of_costs,
}
