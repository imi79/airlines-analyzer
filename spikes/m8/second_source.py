"""M8 second-source check of the cash flow after leases (the gate 1 method, decision 0009).

Inputs typed from the published statements Imane supplied (documents/), page by page, with
their own arithmetic below: no tool code is used to compute them. The tool's figures are
then read from the database and compared within the gate 1 tolerances (0.1 point on ratios;
amounts equal to the million).

    uv run python -m spikes.m8.second_source      writes docs/m8/cash_flow_check.md

Air France-KLM: consolidated financial statements as of December 31, 2025 (English PDF),
cash flow statement page 8, balance sheet page 6 (FY2024 = the comparative column).
ADP: comptes consolidés au 31 décembre 2025 (French PDF), tableau des flux page 7, bilan
page 6 (FY2024 = the comparative column). ADP counts lease liabilities inside borrowings.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "m8" / "cash_flow_check.md"
D = Decimal

# EUR millions, as printed. interest_in_financing: where "Interest paid" sits on the page.
INPUTS = {
    ("afkl", 2025): dict(cfo=5055, capex=4449, disposals=1391, leases=960, interest=670,
                         interest_in_financing=True,
                         debt=[7265, 5487, 1803, 958], current=[1803, 958]),
    ("afkl", 2024): dict(cfo=3496, capex=3728, disposals=678, leases=891, interest=664,
                         interest_in_financing=True,
                         debt=[7254, 4714, 1692, 982], current=[1692, 982]),
    ("adp", 2025): dict(cfo=1638, capex=1265 - 47, disposals=35, leases=30, interest=295,
                        interest_in_financing=True, debt=[8728, 1859], current=[1859]),
    ("adp", 2024): dict(cfo=1524, capex=1089 + 80, disposals=13, leases=28, interest=298,
                        interest_in_financing=True, debt=[8887, 1785], current=[1785]),
}  # fmt: skip
# ADP capex: purchases of PP&E, intangibles and investment property less the change in payables
# on asset acquisitions (+47 in FY2025, (80) in FY2024), as in the tool's ADP mapping (M1).


def expected(i: dict) -> dict[str, Decimal]:
    net_capex = D(i["capex"]) - D(i["disposals"])
    after = D(i["cfo"]) - net_capex - D(i["leases"])
    if i["interest_in_financing"]:
        after -= D(i["interest"])
    debt = sum(D(x) for x in i["debt"])
    return {
        "net_capex": net_capex,
        "fcf_after_leases": after,
        "fcf_after_leases_to_debt": after / debt,
        "debt_due_1y": sum(D(x) for x in i["current"]),
    }


def main() -> None:
    con = duckdb.connect(str(ROOT / "data" / "tearsheet.duckdb"), read_only=True)
    lines = [
        "# M8 second-source check: cash flow after leases",
        "",
        "Inputs typed from the published statements (pages in `spikes/m8/second_source.py`),",
        "computed with their own arithmetic, against the tool. Tolerance: 0.1 point on ratios,",
        "the million on amounts (gate 1).",
        "",
        "| Company | Year | Metric | Second source | Tool | Difference | |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    ok = total = 0
    for (issuer, year), inputs in INPUTS.items():
        for metric, value in expected(inputs).items():
            row = con.execute(
                "SELECT value FROM facts WHERE issuer=? AND fiscal_year=? AND concept=? "
                "AND is_primary",
                [issuer, year, metric],
            ).fetchone()
            tool = D(row[0]) if row else None
            if metric.endswith("_to_debt"):
                diff = None if tool is None else (tool - value) * 100
                good = diff is not None and abs(diff) <= D("0.1")
                show = (f"{value * 100:.2f}%", "missing" if tool is None else f"{tool * 100:.2f}%",
                        "" if diff is None else f"{diff:+.2f} pt")  # fmt: skip
            else:
                tool_m = None if tool is None else tool / D(1_000_000)
                diff = None if tool_m is None else tool_m - value
                good = diff is not None and abs(diff) < D("0.5")
                show = (f"{value:,.0f}", "missing" if tool_m is None else f"{tool_m:,.0f}",
                        "" if diff is None else f"{diff:+,.1f}")  # fmt: skip
            total += 1
            ok += good
            name = {"afkl": "Air France-KLM", "adp": "Groupe ADP"}[issuer]
            lines.append(f"| {name} | FY{year} | {metric} | {' | '.join(show)} | "
                         f"{'✓' if good else '✗'} |")  # fmt: skip
    con.close()
    lines += ["", f"**{ok} of {total} within tolerance.**", ""]
    OUT.write_text("\n".join(lines))
    print(f"{ok}/{total} within tolerance -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
