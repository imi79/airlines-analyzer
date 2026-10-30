"""Gate 1 second-source model (decision 0009), built at Imane's request.

Kept apart from the tool on purpose:
- Inputs are read mechanically from the text of the published statements (PDF), not from
  the XBRL filings the tool uses, and not from the hand entries in config/manual_figures.yaml.
- Every metric is an Excel formula on those inputs, recalculated by LibreOffice, not by the
  tool's code. Only the definitions (the 'Definitions' sheet of the reconciliation) are shared.

    uv run python -m spikes.m2.hand_model <AF-KLM 2025 PDF> <ADP 2025 PDF>

Writes docs/m2/hand_model.xlsx (inputs with page and source text, model with formulas) and
docs/m2/hand_model_inputs.csv.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "m2"
NUMBER = re.compile(r"\(?-?[\d,]+(?:\.\d+)?\)?|–")
FOOTNOTE = r"(?:\s*\(\d\)|\s*⁽\d⁾)?"  # a footnote marker after the label is not a number

# name: (label regex at line start, anchor that must come before it, token picks [2025, 2024])
# Values are taken as printed: brackets mean negative. Picks index the numbers on the line,
# counted from the right (-2 = second from last) unless stated.
AFKL = {
    "revenue": (r"Revenues from ordinary activities", r"CONSOLIDATED INCOME STATEMENT", (-2, -1)),
    "dda": (
        r"Amortization, depreciation and provisions",
        r"CONSOLIDATED INCOME STATEMENT",
        (-2, -1),
    ),
    "operating_income": (
        r"Income from operating activities",
        r"CONSOLIDATED INCOME STATEMENT",
        (-2, -1),
    ),
    "interest_expense": (r"Interests expenses", r"CONSOLIDATED INCOME STATEMENT", (-2, -1)),
    "cash": (r"Cash and cash equivalents", r"CONSOLIDATED BALANCE SHEET", (-2, -1)),
    "borrowings_noncurrent": (
        r"Non-current financial liabilities",
        r"Consolidated balance sheet \(continuation\)",
        (-2, -1),
    ),
    "lease_noncurrent": (
        r"Non-current lease debt",
        r"Consolidated balance sheet \(continuation\)",
        (-2, -1),
    ),
    "borrowings_current": (
        r"Current financial liabilities",
        r"Consolidated balance sheet \(continuation\)",
        (-2, -1),
    ),
    "lease_current": (
        r"Current lease debt",
        r"Consolidated balance sheet \(continuation\)",
        (-2, -1),
    ),
    "advance_ticket_sales": (
        r"Deferred revenue on ticket sales",
        r"Consolidated balance sheet \(continuation\)",
        (-2, -1),
    ),
    "cfo": (
        r"CASH-FLOW FROM OPERATING ACTIVITIES",
        r"CONSOLIDATED STATEMENT OF CASH FLOWS",
        (-2, -1),
    ),
    "capex_printed": (
        r"Purchase of property plant and equipment and intangible assets",
        r"CONSOLIDATED STATEMENT OF CASH FLOWS",
        (-2, -1),
    ),
    "interest_paid": (r"Interest paid", r"CONSOLIDATED STATEMENT OF CASH FLOWS", (-2, -1)),
    "tax_paid": (
        r"Income tax \(paid\) / reimbursed",
        r"CONSOLIDATED STATEMENT OF CASH FLOWS",
        (-2, -1),
    ),
    "marketable_securities": (r"Marketable securities > 3 months", r"NOTE 32\s+NET DEBT", (-2, -1)),
    "bonds_held": (r"Bonds", r"NOTE 32\s+NET DEBT", (-2, -1)),
}
ADP = {
    "revenue": (r"Revenue\s", r"1\.1\.1\s+CONSOLIDATED INCOME STATEMENT", (-2, -1)),
    "associates": (
        r"Profit \(loss\) from equity-accounted companies",
        r"1\.1\.1\s+CONSOLIDATED INCOME STATEMENT",
        (-2, -1),
    ),
    "dda": (
        r"intangible assets, net of reversals",
        r"1\.1\.1\s+CONSOLIDATED INCOME STATEMENT",
        (-2, -1),
    ),
    "operating_income": (
        r"Operating income(?=\s+[\d(])",
        r"1\.1\.1\s+CONSOLIDATED INCOME STATEMENT",
        (-2, -1),
    ),
    "cash": (
        r"Cash and cash equivalents",
        r"1\.1\.3\s+CONSOLIDATED STATEMENT OF FINANCIAL POSITION",
        (-2, -1),
    ),
    "borrowings_noncurrent": (
        r"Non-current borrowings and debt",
        r"1\.1\.3\s+CONSOLIDATED STATEMENT OF FINANCIAL POSITION",
        (-2, -1),
    ),
    "borrowings_current": (
        r"Current borrowings and debt",
        r"1\.1\.3\s+CONSOLIDATED STATEMENT OF FINANCIAL POSITION",
        (-2, -1),
    ),
    "tax_paid": (r"Tax expenses", r"1\.1\.4\s+CONSOLIDATED CASH FLOW STATEMENT", (-2, -1)),
    "cfo": (
        r"Cash flows from operating activities",
        r"1\.1\.4\s+CONSOLIDATED CASH FLOW STATEMENT",
        (-2, -1),
    ),
    "capex_printed": (
        r"and investment property",
        r"1\.1\.4\s+CONSOLIDATED CASH FLOW STATEMENT",
        (-2, -1),
    ),
    "payables_change": (
        r"Change in payables and advances on asset acquisitions",
        r"1\.1\.4\s+CONSOLIDATED CASH FLOW STATEMENT",
        (-2, -1),
    ),
    "interest_paid": (r"Interest paid", r"1\.1\.4\s+CONSOLIDATED CASH FLOW STATEMENT", (-2, -1)),
    "restricted_bank_balances": (r"Restricted bank balances", r"9\.4\.2\s+Net debt", (0, 2)),
}

# Excel formulas per metric, with {input} placeholders resolved to cells for each year.
# Inputs are as printed (costs and outflows in brackets are negative), so the signs are
# handled here, in the open.
COMMON = {
    "total_debt": "{borrowings_noncurrent}+{borrowings_current}{leases}",
    "net_debt": "{total_debt}-{cash_like}",
    "net_leverage": "{net_debt}/{ebitda}",
    "gross_leverage": "{total_debt}/{ebitda}",
    "ffo": "{ebitda}+{interest_paid}+{tax_paid}",
    "ffo_to_debt": "{ffo}/{total_debt}",
    "fcf": "{cfo}-{capex}",
    "fcf_to_debt": "{fcf}/{total_debt}",
    "ebitda_margin": "{ebitda}/{revenue}",
    "capex_intensity": "{capex}/{revenue}",
    "cash_liquidity_to_revenue": "{cash_like}/{revenue}",
}
MODELS = {
    "afkl": {
        "name": "Air France-KLM",
        "inputs": AFKL,
        "metrics": {
            "ebitda": "{operating_income}-{dda}",
            "cash_like": "{cash}+{marketable_securities}+{bonds_held}",
            "interest_coverage": "{ebitda}/-{interest_expense}",
            "capex": "-{capex_printed}",
            "advance_ticket_cover": "{advance_ticket_sales}/{cash_like}",
            **COMMON,
        },
        "leases": "+{lease_noncurrent}+{lease_current}",
    },
    "adp": {
        "name": "Groupe ADP",
        "inputs": ADP,
        "metrics": {
            "ebitda": "{operating_income}-{associates}-{dda}",
            "cash_like": "{cash}+{restricted_bank_balances}",
            "interest_coverage": "{ebitda}/-{interest_paid}",
            "capex": "-({capex_printed}+{payables_change})",
            **COMMON,
        },
        "leases": "",  # included in borrowings (ADP note: "Dettes de location")
    },
}
ORDER = [
    "ebitda",
    "ebitda_margin",
    "total_debt",
    "cash_like",
    "net_debt",
    "net_leverage",
    "gross_leverage",
    "interest_coverage",
    "ffo",
    "ffo_to_debt",
    "capex",
    "fcf",
    "fcf_to_debt",
    "capex_intensity",
    "cash_liquidity_to_revenue",
    "advance_ticket_cover",
]


def number(token: str) -> float | None:
    if token == "–":
        return 0.0
    negative = token.startswith("(")
    value = float(token.strip("()").replace(",", ""))
    return -value if negative else value


def extract(pdf: Path, spec: dict) -> dict[str, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        txt = Path(tmp) / "out.txt"
        subprocess.run(
            ["pdftotext", "-layout", str(pdf), str(txt)], check=True, capture_output=True
        )
        pages = txt.read_text().split("\f")
    found = {}
    for name, (label, anchor, picks) in spec.items():
        seen_anchor = False
        for page_no, page in enumerate(pages, start=1):
            for line in page.splitlines():
                # The heading itself, not its table-of-contents entry (which ends in a page no.)
                if re.search(anchor + r"\s*$", line.strip()):
                    seen_anchor = True
                    continue
                hit = seen_anchor and re.match(r"\s*" + label + FOOTNOTE, line)
                if hit:
                    tokens = [t for t in NUMBER.findall(line[hit.end() :]) if t != ","]
                    values = [number(tokens[p]) for p in picks]
                    found[name] = {
                        "2025": values[0],
                        "2024": values[1],
                        "pdf_page": page_no,
                        "text": " ".join(line.split()),
                    }
                    break
            if name in found:
                break
        if name not in found:
            raise SystemExit(f"{pdf.name}: '{name}' not found after '{anchor}'")
    return found


def build(pdfs: dict[str, Path]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "hand_model.xlsx"
    book = xlsxwriter.Workbook(str(path))
    bold = book.add_format({"bold": True})
    head = book.add_format({"bold": True, "bg_color": "#DDE6F0", "border": 1})
    num = book.add_format({"num_format": "#,##0.00", "border": 1})
    txt = book.add_format({"border": 1})
    results = book.add_worksheet("Results")  # first sheet: what LibreOffice exports to CSV
    results.write_row(0, 0, ["issuer", "metric", "FY2025", "FY2024"], head)
    rows_out, out_row = [], 1
    for issuer, model in MODELS.items():
        data = extract(pdfs[issuer], model["inputs"])
        ws = book.add_worksheet(model["name"][:31])
        ws.write(0, 0, f"{model['name']}: inputs read from the published statements (EUR m)", bold)
        ws.write_row(2, 0, ["Input", "FY2025", "FY2024", "PDF page", "Line as printed"], head)
        ws.set_column(0, 0, 28)
        ws.set_column(4, 4, 110)
        cells = {}
        for r, (name, d) in enumerate(data.items(), start=3):
            ws.write(r, 0, name, txt)
            ws.write_number(r, 1, d["2025"], num)
            ws.write_number(r, 2, d["2024"], num)
            ws.write_number(r, 3, d["pdf_page"], txt)
            ws.write(r, 4, d["text"], txt)
            cells[name] = (r, 1, 2)
            rows_out.append(
                {
                    "issuer": issuer,
                    "input": name,
                    "fy2025": d["2025"],
                    "fy2024": d["2024"],
                    "pdf_page": d["pdf_page"],
                    "text": d["text"],
                }
            )
        start = len(data) + 5
        ws.write(start - 1, 0, "Model (Excel formulas on the inputs above)", bold)
        ws.write_row(start, 0, ["Metric", "FY2025", "FY2024", "", "Formula (FY2025 column)"], head)
        metrics = {k: v.replace("{leases}", model["leases"]) for k, v in model["metrics"].items()}
        order = [m for m in ORDER if m in metrics]
        rows = {m: start + 1 + i for i, m in enumerate(order)}
        for m in order:
            r = rows[m]
            ws.write(r, 0, m, txt)
            for col in (1, 2):
                refs = {k: xl_rowcol_to_cell(v[0], col) for k, v in cells.items()}
                refs |= {k: xl_rowcol_to_cell(rows[k], col) for k in rows}
                ws.write_formula(r, col, "=" + metrics[m].format(**refs), num)
            ws.write(r, 4, "=" + metrics[m], txt)
            sheet = model["name"][:31].replace("'", "''")
            results.write(out_row, 0, issuer)
            results.write(out_row, 1, m)
            results.write_formula(out_row, 2, f"='{sheet}'!{xl_rowcol_to_cell(r, 1)}")
            results.write_formula(out_row, 3, f"='{sheet}'!{xl_rowcol_to_cell(r, 2)}")
            out_row += 1
    book.close()
    with (OUT / "hand_model_inputs.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, ["issuer", "input", "fy2025", "fy2024", "pdf_page", "text"])
        writer.writeheader()
        writer.writerows(rows_out)
    return path


PROFILE = """<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry"
 xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="OOXMLRecalcMode"
 oor:op="fuse"><value>0</value></prop></item>
</oor:items>
"""


def recalculate(xlsx: Path) -> list[dict]:
    """Let LibreOffice compute the formulas (recalculate on load) and export the Results sheet."""
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp) / "profile" / "user"
        profile.mkdir(parents=True)
        (profile / "registrymodifications.xcu").write_text(PROFILE)
        subprocess.run(
            [
                "soffice",
                f"-env:UserInstallation=file://{Path(tmp) / 'profile'}",
                "--headless",
                "--convert-to",
                "csv",
                "--outdir",
                tmp,
                str(xlsx),
            ],
            check=True,
            capture_output=True,
        )
        return list(csv.DictReader((Path(tmp) / f"{xlsx.stem}.csv").open()))


def compare(
    model_rows: list[dict], db_path: Path = ROOT / "data" / "tearsheet.duckdb"
) -> list[dict]:
    """Second-source model vs the tool, with the gate 1 tolerances."""
    import duckdb
    import yaml

    units = {
        k: v["unit"]
        for k, v in yaml.safe_load((ROOT / "src/tearsheet/metrics/catalog.yaml").read_text())[
            "metrics"
        ].items()
    }
    units["capex"] = "amount"
    con = duckdb.connect(str(db_path), read_only=True)
    tool = {
        (r[0], r[1], str(r[2])): float(r[3])
        for r in con.execute(
            "SELECT issuer, concept, fiscal_year, value FROM facts "
            "WHERE (source_type = 'computed' OR concept = 'capex') AND is_primary"
        ).fetchall()
    }
    con.close()
    out = []
    for row in model_rows:
        for year in ("2025", "2024"):
            unit = units[row["metric"]]
            mine = float(row[f"FY{year}"])
            theirs = tool.get((row["issuer"], row["metric"], year))
            if theirs is not None and unit == "amount":
                theirs /= 1_000_000
            if theirs is None:
                ok, diff = False, None
            else:
                diff = mine - theirs
                tolerance = {"x": 0.05, "pct": 0.001}.get(unit, 0.5)  # amounts: rounding only
                ok = abs(diff) <= tolerance
            out.append(
                {
                    **row,
                    "year": year,
                    "unit": unit,
                    "model": mine,
                    "tool": theirs,
                    "diff": diff,
                    "ok": ok,
                }
            )
    return out


def write_report(rows: list[dict]) -> Path:
    def show(v, unit):
        if v is None:
            return "–"
        return {"x": f"{v:.2f}x", "pct": f"{v * 100:.1f}%"}.get(unit, f"{v:,.0f}")

    passed = sum(r["ok"] for r in rows)
    md = [
        "# Gate 1: second-source model vs the tool",
        "",
        "Built by the AI at Imane's request (decision 0009). Inputs are read mechanically from",
        "the published 2025 statements (PDF text, page and line recorded in",
        "`docs/m2/hand_model_inputs.csv`); every metric is an Excel formula recalculated by",
        "LibreOffice (`docs/m2/hand_model.xlsx`). Tolerances: leverage and coverage 0.05x,",
        "margins and ratios 0.1 point, amounts EUR 0.5m (rounding).",
        "",
        f"**Result: {passed} of {len(rows)} comparisons within tolerance.**",
        "",
        "| Company | Metric | Year | Model | Tool | Difference | Within tolerance |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        diff = (
            "–"
            if r["diff"] is None
            else (f"{r['diff']:+.4f}" if r["unit"] in ("x", "pct") else f"{r['diff']:+,.1f}")
        )
        md.append(
            f"| {r['issuer']} | {r['metric']} | FY{r['year']} | {show(r['model'], r['unit'])} "
            f"| {show(r['tool'], r['unit'])} | {diff} | {'✓' if r['ok'] else '✗'} |"
        )
    path = OUT / "gate1.md"
    path.write_text("\n".join(md) + "\n")
    return path


def main() -> None:
    workbook = build({"afkl": Path(sys.argv[1]), "adp": Path(sys.argv[2])})
    rows = compare(recalculate(workbook))
    path = write_report(rows)
    print(f"{sum(r['ok'] for r in rows)}/{len(rows)} within tolerance; report: {path}")
    for r in rows:
        if not r["ok"]:
            print("  ✗", r["issuer"], r["metric"], r["year"], r["model"], r["tool"])


if __name__ == "__main__":
    main()
