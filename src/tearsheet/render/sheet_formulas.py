"""Metric formulas for the Excel backup (M6): from `excel:` in catalog.yaml to a live formula.

Each computed figure records the inputs the code used (names, values and the figure each was
read from). The catalog formula is written on those names; here each name becomes the input
it stands for, so the spreadsheet formula uses exactly what the code used, company by company:

    catalog:      operating_profit - share_of_associates? + dda
    Air France:   =operating_profit_FY2025+dda_FY2025         (no associates line)
    Aena:         =operating_profit_FY2025-share_of_associates_FY2025+dda_FY2025

The same parsed formula is also evaluated in code, so a unit test can check every stored
figure without a spreadsheet program; LibreOffice does the full recalculation check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from functools import cache

from tearsheet.metrics.engine import load_catalog
from tearsheet.render.library import Library, split

TOKEN = re.compile(
    r"\s*(?:(?P<sum>sum\(\))"
    r"|(?P<name>[a-z_][a-z0-9_]*(?:@prior)?\??(?:\s*\|\s*[a-z_][a-z0-9_]*)*)"
    r"|(?P<op>[-+*/()])|(?P<num>\d+(?:\.\d+)?))"
)


class FormulaError(ValueError):
    """The catalog formula does not fit the inputs the code recorded."""


@cache
def templates() -> dict[str, str]:
    return {k: v["excel"] for k, v in load_catalog().items()}


def excel_name(figure_key: str) -> str:
    """The workbook name of a figure: net_leverage_FY2025 (the company is the workbook's)."""
    _, concept, year = split(figure_key)
    return f"{concept}_FY{year}"


@dataclass(frozen=True)
class Resolved:
    """A formula as a list of tokens: operators, numbers, and figure keys (or a SUM group)."""

    tokens: tuple  # str operator | Decimal | ("key", figure_key) | ("sum", (keys...))

    def keys(self) -> list[str]:
        out = []
        for t in self.tokens:
            if isinstance(t, tuple):
                out += [t[1]] if t[0] == "key" else list(t[1])
        return out


def resolve(lib: Library, figure_key: str) -> Resolved:
    f = lib.figures[figure_key]
    if f["source_type"] != "computed":
        raise FormulaError(f"{figure_key} is not computed")
    issuer, metric, year = split(figure_key)
    template = templates()[metric]
    inputs = [k for k in f.get("input_keys") or [] if k]
    if len(inputs) != len(f["source"].get("inputs") or []):
        raise FormulaError(f"{figure_key}: an input is not linked")

    def find(name: str, prior: bool) -> str | None:
        want = year - 1 if prior else year
        for k in inputs:
            _, concept, y = split(k)
            if concept == name and y == want:
                return k
        return None

    tokens: list = []
    pos = 0
    while pos < len(template):
        m = TOKEN.match(template, pos)
        if not m or m.end() == pos:
            raise FormulaError(f"{metric}: cannot read the formula at '{template[pos:]}'")
        pos = m.end()
        if m.group("sum"):
            tokens.append(("sum", tuple(inputs)))
        elif m.group("op"):
            tokens.append(m.group("op"))
        elif m.group("num"):
            tokens.append(Decimal(m.group("num")))
        else:
            raw = m.group("name").replace(" ", "")
            optional = raw.endswith("?")
            raw = raw.rstrip("?")
            prior = raw.endswith("@prior")
            names = raw.removesuffix("@prior").split("|")
            found = next((k for k in (find(n, prior) for n in names) if k), None)
            if found:
                tokens.append(("key", found))
            elif optional:
                if tokens and tokens[-1] in ("+", "-"):
                    tokens.pop()  # drop "- share_of_associates" with its sign
            else:
                raise FormulaError(f"{figure_key}: no input for {raw} in {template!r}")
    resolved = Resolved(tuple(tokens))
    unused = set(inputs) - set(resolved.keys())
    if unused:
        raise FormulaError(f"{figure_key}: inputs not used by the formula: {sorted(unused)}")
    return resolved


def to_excel(resolved: Resolved) -> str:
    parts = []
    for t in resolved.tokens:
        if isinstance(t, tuple):
            if t[0] == "key":
                parts.append(excel_name(t[1]))
            else:
                parts.append("SUM(" + ",".join(excel_name(k) for k in t[1]) + ")")
        else:
            parts.append(str(t))
    return "=" + "".join(parts)


def evaluate(lib: Library, resolved: Resolved) -> Decimal:
    """The formula computed in code on the stored values (for the unit test)."""
    expr = []
    values: dict[str, Decimal] = {}
    for t in resolved.tokens:
        if isinstance(t, tuple):
            keys = [t[1]] if t[0] == "key" else list(t[1])
            terms = []
            for k in keys:
                var = f"v{len(values)}"
                values[var] = Decimal(lib.figures[k]["value"])
                terms.append(var)
            expr.append("(" + "+".join(terms) + ")")
        elif isinstance(t, Decimal):
            var = f"v{len(values)}"
            values[var] = t
            expr.append(var)
        else:
            expr.append(t)
    return eval("".join(expr), {"__builtins__": {}}, values)  # noqa: S307 (our own tokens)
