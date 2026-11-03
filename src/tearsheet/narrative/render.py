"""Turn stored values into the text printed on the tearsheet, the same way everywhere.

Values are stored as reported, with their decimals; rounding happens only here. Changes are
printed without a sign ("0.09x", "1.2 points", "4.5%"): the direction is carried by the AI's
own word ("fell by"), which the verifier checks against the computed direction.
"""

from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal

PLACEHOLDER = re.compile(r"\{\{\s*([^{}]*?)\s*\}\}")
SMALL_UNITS = {"EUR": "euro cents", "GBP": "pence", "NOK": "øre", "USD": "US cents"}
ORDINAL = {1: "st", 2: "nd", 3: "rd"}


def _round(value: Decimal, places: int) -> Decimal:
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def _num(value: Decimal, places: int) -> str:
    rounded = _round(value, places)
    return f"{abs(rounded) if rounded == 0 else rounded:,.{places}f}"  # never "-0.0"


def amount(value: Decimal, currency: str) -> str:
    """EUR 1.2bn, EUR 845m, EUR 45.3m, NOK 37.6bn."""
    v = Decimal(value)
    if abs(v) >= Decimal("1e9"):
        return f"{currency} {_num(v / Decimal('1e9'), 1)}bn"
    millions = v / Decimal("1e6")
    return f"{currency} {_num(millions, 0 if abs(millions) >= 100 else 1)}m"


def count(value: Decimal) -> str:
    """Passengers 98.5m, ASK 301.2bn, fleet 616."""
    v = Decimal(value)
    if abs(v) >= Decimal("1e9"):
        return f"{_num(v / Decimal('1e9'), 1)}bn"
    if abs(v) >= Decimal("1e6"):
        return f"{_num(v / Decimal('1e6'), 1)}m"
    return _num(v, 0)


def ordinal(n: int) -> str:
    suffix = "th" if 10 <= n % 100 <= 20 else ORDINAL.get(n % 10, "th")
    return f"{n}{suffix}"


def value_text(value: Decimal, unit: str, currency: str = "") -> str:
    """A level: 1.62x, 18.3%, EUR 1.2bn, 98.5m, 11.2 years, 8.45 euro cents, EUR 23.10."""
    v = Decimal(value)
    if unit == "x":
        return f"{_num(v, 2)}x"
    if unit == "pct":
        return f"{_num(v * 100, 1)}%"
    if unit == "amount":
        return amount(v, currency)
    if unit == "count":
        return count(v)
    if unit == "years":
        return f"{_num(v, 1)} years"
    if unit == "per_km":
        return f"{_num(v * 100, 2)} {SMALL_UNITS.get(currency, currency + ' cents')}"
    if unit == "per_passenger":
        return f"{currency} {_num(v, 2)}"
    raise ValueError(f"unknown unit {unit}")


def change_text(value: Decimal, unit: str) -> str:
    """A change, without its sign: 0.09x, 1.2 points, 4.5% (relative), 0.3 years."""
    v = abs(Decimal(value))
    if unit == "x":
        return f"{_num(v, 2)}x"
    if unit == "points":  # change in a percentage, stored as a fraction
        text = _num(v * 100, 1)
        return f"{text} point" if text == "1.0" else f"{text} points"
    if unit == "relative":  # share of the prior-year value
        return f"{_num(v * 100, 1)}%"
    if unit == "years":
        return f"{_num(v, 1)} years"
    raise ValueError(f"unknown change unit {unit}")


def change_between(prior: Decimal, current: Decimal, unit: str) -> str:
    """An absolute change, computed from the two levels as printed, so the page always adds
    up: 1.88x to 1.71x is "0.17x", even if the stored values differ by 0.1649."""
    places = {"x": 2, "points": 3, "years": 1}[unit]
    diff = _round(Decimal(current), places) - _round(Decimal(prior), places)
    return change_text(diff, unit)


def rank_text(rank: int, of: int) -> str:
    return f"{ordinal(rank)} of {of}"


def fill(text: str, rendered: dict[str, str]) -> str:
    """Replace every {{id}} with its rendered value. Unknown ids raise KeyError: the verifier
    runs first, so this only happens if it was skipped."""
    return PLACEHOLDER.sub(lambda m: rendered[m.group(1)], text)
