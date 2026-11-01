"""ECB month-end exchange rates (decision 0002), to convert an amount reported in another
currency (for example a credit facility in US dollars) into the reporting currency."""

from __future__ import annotations

import csv
from collections.abc import Callable
from datetime import date
from decimal import Decimal

from tearsheet.ingest.client import Client

Converter = Callable[[Decimal, str, str, date], tuple[Decimal, str]]


def ecb_month_end(client: Client) -> Converter:
    """A converter using ECB end-of-month reference rates (foreign currency per 1 EUR)."""
    cache: dict[str, dict[str, Decimal]] = {}

    def per_eur(currency: str, period_end: date) -> Decimal:
        if currency == "EUR":
            return Decimal(1)
        if currency not in cache:
            text = client.ecb_series("EXR", f"M.{currency}.EUR.SP00.E", "2020-01")
            cache[currency] = {
                row["TIME_PERIOD"]: Decimal(row["OBS_VALUE"])
                for row in csv.DictReader(text.splitlines())
                if row.get("OBS_VALUE")
            }
        month = f"{period_end.year}-{period_end.month:02d}"
        if month not in cache[currency]:
            raise KeyError(f"no ECB {currency} rate for {month}")
        return cache[currency][month]

    def convert(amount: Decimal, source: str, target: str, period_end: date):
        rate = per_eur(target, period_end) / per_eur(source, period_end)
        note = (
            f"converted from {source} at the ECB end-of-month rate for "
            f"{period_end:%b %Y} ({rate:.4f} {target} per {source})"
        )
        return amount * rate, note

    return convert
