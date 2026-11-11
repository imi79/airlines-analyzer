"""M8 answer key for the debt maturity wall, read by code without AI (the method of decision
0012), written before the AI read any maturity table.

Kept apart from the tool on purpose:
- No AI, and none of the extraction code: the report text is rebuilt with the M3 key's own
  tag stripper (spikes/m3), the numbers are read here, and the columns are given their time
  spans by hand, by reading each table (not by the tool's label reader).
- Each value is anchored on the row it is printed in: the row's words and numbers in order,
  with any spacing between them. An anchor must match exactly once in the report, so a wrong
  or ambiguous reading stops the build instead of guessing.
- Where the table prints a total, the key checks its own reading: the columns must add up.

    uv run python -m spikes.m8.maturity_key           build docs/m8/maturity_key.csv
    uv run python -m spikes.m8.maturity_key score     compare the tool's walls with the key

Eight company-years, latest reports. A layer is "borrowings" as the company's balance sheet
defines it (lease liabilities included where it counts them inside borrowings) or "leases".
Some companies print several tables for a layer: each is in the key with its basis.
"""

from __future__ import annotations

import csv
import re
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "m8" / "maturity_key.csv"
SCORE = ROOT / "docs" / "m8" / "maturity_score.md"
BOUNDS = [Decimal(0), Decimal(1), Decimal(2), Decimal(5), None]
DASH = {"-", "–", "—"}
OPEN = None
D = Decimal


@dataclass
class Cell:
    span: tuple  # (start, end) in years from the year end; end None = open
    tokens: list[str]  # the printed row, in order: words and numbers
    pick: int  # which token is this cell's value


@dataclass
class Table:
    issuer: str
    fiscal_year: int
    layer: str
    basis: str
    scale: int
    language: str
    note: str
    cells: list[Cell] = field(default_factory=list)
    totals: list[tuple[list[str], int]] = field(default_factory=list)  # one per row, if printed


def rows(spans, row_specs, prefix_len=1) -> tuple[list[Cell], list]:
    """A table with one row per item and one column per span (then the total, if printed).
    row_specs: (tokens, has_total); tokens = label words + optional leading figures, then the
    values in span order, then the total."""
    cells, totals = [], []
    for tokens, lead, has_total in row_specs:
        start = prefix_len + lead
        for i, span in enumerate(spans):
            cells.append(Cell(span, tokens, start + i))
        if has_total:
            totals.append((tokens, start + len(spans)))
    return cells, totals


Y = [(D(i), D(i + 1)) for i in range(5)] + [(D(5), OPEN)]  # 1-year columns, then 5+ years

KEY: list[Table] = []


def add(t: Table, built: tuple[list[Cell], list]) -> None:
    t.cells, t.totals = built
    KEY.append(t)


# Finnair FY2025: "Maturity dates of interest-bearing financial liabilities 31 Dec 2025, EUR
# mill.", columns 2026...2030, Later, Total (principal: "the total ... differs from the book
# value by the amortised costs"). Leases apart from borrowings on Finnair's balance sheet.
add(
    Table("finnair", 2025, "borrowings", "principal", 10**6, "en", "JOLCO loans and bonds"),
    rows(Y, [
        (["JOLCO loans and other, fixed interest", "9.9", "-", "-", "-", "-", "-", "9.9"], 0, True),
        (["JOLCO loans and other, variable interest", "41.6", "21.0", "21.1", "21.3", "21.4",
          "87.2", "213.7"], 0, True),
        (["Bonds, fixed interest", "-", "-", "-", "500.0", "300.0", "-", "800.0", "Lease"],
         0, True),
    ]),
)  # fmt: skip
add(
    Table("finnair", 2025, "leases", "principal", 10**6, "en", "lease liabilities"),
    rows(Y, [
        (["Lease liabilities, fixed interest", "92.2", "85.4", "65.3", "63.2", "65.7", "178.5",
          "550.5"], 0, True),
        (["Lease liabilities, variable interest", "38.2", "40.0", "37.5", "21.2", "12.9", "62.3",
          "212.2"], 0, True),
    ]),
)  # fmt: skip
# Finnair FY2024: the same table at 31 Dec 2024, columns 2025...2029, Later, Total.
add(
    Table("finnair", 2024, "borrowings", "principal", 10**6, "en", "JOLCO loans and bonds"),
    rows(Y, [
        (["JOLCO loans and other, fixed interest", "22.5", "11.2", "-", "-", "-", "-", "33.7"],
         0, True),
        (["JOLCO loans and other, variable interest", "103.0", "45.5", "22.2", "22.4", "22.5",
          "112.2", "327.9"], 0, True),
        (["Bonds, fixed interest", "-", "-", "-", "-", "500.0", "-", "500.0"], 0, True),
    ]),
)  # fmt: skip
add(
    Table("finnair", 2024, "leases", "principal", 10**6, "en", "lease liabilities"),
    rows(Y, [
        (["Lease liabilities, fixed interest", "124.6", "105.6", "96.5", "73.8", "73.7", "276.3",
          "750.5"], 0, True),
        (["Lease liabilities, variable interest", "40.0", "39.5", "41.5", "38.9", "20.4", "73.7",
          "253.9"], 0, True),
    ]),
)  # fmt: skip

# Air France-KLM FY2024 (French URD), note 31.5 "Analyse par échéance": contractual cash flows
# of financial liabilities (without lease debt), principal 8,946 + interest 1,591. One row per
# year (N+1...N+5, beyond 5 years), columns 2024 and 2023: the FY2024 value is the first.
afkl = Table("afkl", 2024, "borrowings", "contractual_cash_flows", 10**6, "fr",
             "financial debt without lease debt")  # fmt: skip
afkl.cells = [
    Cell(Y[0], ["Échéances en", "N+1", "2 065", "2 089"], 2),
    Cell(Y[1], ["N+2", "1 848", "1 866"], 1),
    Cell(Y[2], ["N+3", "823", "2 013"], 1),
    Cell(Y[3], ["N+4", "1 132", "755"], 1),
    Cell(Y[4], ["N+5", "1 481", "1 082"], 1),
    Cell(Y[5], ["Au delà de 5 ans", "3 188", "3 263"], 1),
]
afkl.totals = [(["TOTAL", "10 537", "11 068", "Dont"], 1)]
KEY.append(afkl)

# ADP FY2024 (French URD), note 9.4.3: bonds and bank loans by maturity at their carrying
# amount (lease liabilities, inside ADP's borrowings, are not in this table).
A3 = [(D(0), D(1)), (D(1), D(5)), (D(5), OPEN)]
add(
    Table("adp", 2024, "borrowings", "carrying_amount", 10**6, "fr",
          "bonds and bank loans only (no lease liabilities)"),
    rows(A3, [(["TOTAL", "1 125", "3 742", "4 752", "9 619", "10 055"], 0, True)]),
)  # fmt: skip
# ADP FY2024, liquidity table: "Emprunts et dettes financières hors dérivés", contractual
# cash flows with interest; carrying amount 10,142 and contractual total 11,689 come first.
add(
    Table("adp", 2024, "borrowings", "contractual_cash_flows", 10**6, "fr",
          "all borrowings and financial debt, with interest"),
    rows(A3, [(["Emprunts et dettes financières", "hors dérivés", "10 142", "11 689", "1 456",
                "4 917", "5 316"], 0, False)], prefix_len=4),
)  # fmt: skip
KEY[-1].totals = [(KEY[-1].cells[0].tokens, 3)]  # the contractual total is printed first

# IAG FY2025, liquidity table: contractual cash flows with interest, columns within 6 months,
# 6-12 months, 1-2 years, 2-5 years, more than 5 years, total. Interest-bearing borrowings are
# four rows with no subtotal; IAG counts lease liabilities inside borrowings.
I5 = [(D(0), D("0.5")), (D("0.5"), D(1)), (D(1), D(2)), (D(2), D(5)), (D(5), OPEN)]
add(
    Table("iag", 2025, "borrowings", "contractual_cash_flows", 10**6, "en",
          "interest-bearing loans and borrowings, four rows"),
    rows(I5, [
        (["Asset financing liabilities", "(239)", "(239)", "(481)", "(1,737)", "(3,525)",
          "(6,221)", "Lease liabilities"], 0, True),
        (["Lease liabilities", "(775)", "(707)", "(1,342)", "(2,759)", "(4,329)", "(9,912)"],
         0, True),
        (["Fixed rate borrowings", "(17)", "(25)", "(220)", "(1,383)", "–", "(1,645)"], 0, True),
        (["Floating rate borrowings", "(13)", "(13)", "(16)", "–", "–", "(42)"], 0, True),
    ]),
)  # fmt: skip

# Norwegian FY2025, liquidity table "At 31 December 2025": borrowings (interest on a separate
# row, so the row is principal), columns less than 1 year, 1-2, 2-3, 3-5, over 5 years; no
# total printed.
N5 = [(D(0), D(1)), (D(1), D(2)), (D(2), D(3)), (D(3), D(5)), (D(5), OPEN)]
add(
    Table("norwegian", 2025, "borrowings", "principal", 10**6, "en", "borrowings, no total"),
    rows(N5, [(["At 31 December 2025", "Borrowings", "2,293", "531", "467", "1,044", "1,513",
                "Trade"], 0, False)], prefix_len=2),
)  # fmt: skip

# easyJet FY2025, lease liabilities: contractual undiscounted cash flows, one row per period,
# columns 2025 and 2024 (FY2025 first). No borrowings maturity table by period.
ej = Table("easyjet", 2025, "leases", "contractual_cash_flows", 10**6, "en", "lease liabilities")
ej.cells = [
    Cell((D(0), D(1)), ["Less than one year", "(299)", "(269)"], 1),
    Cell((D(1), D(5)), ["One to five years", "(727)", "(852)"], 1),
    Cell((D(5), OPEN), ["More than five years", "(186)", "(226)", "(1,212)"], 1),
]
ej.totals = [(["(186)", "(226)", "(1,212)", "(1,347)"], 2)]
KEY.append(ej)

# Aena FY2025, liquidity note (thousands of euros): carrying amount, then 2026...2030,
# following years, total. Aena counts lease liabilities inside its financial debt: the layer is
# every loan, bond, lease and accrued-interest row of the financial debt (other financial
# liabilities, payables and the estimated future interest are left out).
AENA_ROWS = [
    ("Préstamo con ENAIRE", "20", "1.949.147",
     ["376.402", "345.492", "318.887", "248.405", "184.357", "475.604"], "1.949.147"),
    ("Intereses devengados pdtes. de pago por préstamos con ENAIRE", "20", "5.738",
     ["5.738", "-", "-", "-", "-", "-"], "5.738"),
    ("Préstamos con entidades de crédito - Aena", "20.2", "3.306.662",
     ["304.128", "546.708", "26.724", "347.391", "127.307", "1.954.404"], "3.306.662"),
    ("AENA", "20.2", "22.723", ["22.723", "-", "-", "-", "-", "-"], "22.723"),
    ("Préstamos con entidades de crédito - LLAH III", "20.2", "356.571",
     ["41.729", "94.832", "67.866", "138.219", "10.681", "3.244"], "356.571"),
    ("Préstamos con entidades de crédito - ANB", "20.2", "223.868",
     ["7.463", "5.496", "4.785", "4.990", "5.306", "195.828"], "223.868"),
    ("Préstamos con entidades de crédito - BOAB", "20.2", "14.821",
     ["166", "-", "388", "776", "776", "12.715"], "14.821"),
    ("Pasivos por arrendamiento - Aena", "20", "24.754",
     ["10.062", "8.328", "4.791", "1.032", "430", "111"], "24.754"),
    ("Pasivos por arrendamiento - LLAH III", "20", "25.311",
     ["4.384", "4.634", "3.756", "3.492", "3.631", "5.414"], "25.311"),
    ("Pasivos por arrendamiento - ANB", "20", "350", ["121", "74", "74", "67", "14", "-"], "350"),
    ("Pasivos por arrendamiento - BOAB", "20", "22", ["22", "-", "-", "-", "-", "-"], "22"),
    ("Préstamos con accionistas - LLAH III", "20.2", "53.156",
     ["-", "-", "-", "-", "-", "53.156"], "53.156"),
    ("Intereses devengados Préstamo accionistas LLAH III", "20", "510",
     ["510", "-", "-", "-", "-", "-"], "510"),
    ("Obligaciones y otros valores negociables - Aena", "20", "502.313",
     ["4.653", "-", "-", "-", "497.660", "0"], "502.313"),
    ("Obligaciones y otros valores negociables - BOAB", None, "795.326",
     ["6.860", "-", "12.289", "20.482", "24.578", "731.117"], "795.326"),
]  # fmt: skip
aena = Table("aena", 2025, "borrowings", "carrying_amount", 10**3, "es",
             "financial debt: loans, bonds, leases and accrued interest, 15 rows")  # fmt: skip
for label, note, book, values, total in AENA_ROWS:
    tokens = [label] + ([note] if note else []) + [book] + values + [total]
    first = len(tokens) - len(values) - 1
    aena.cells += [Cell(span, tokens, first + i) for i, span in enumerate(Y)]
    aena.totals.append((tokens, len(tokens) - 1))
KEY.append(aena)


# --- Reading -----------------------------------------------------------------------------------


def number(printed: str, language: str) -> Decimal:
    s = printed.strip().strip("()")
    if s in DASH:
        return D(0)
    if language == "en":
        s = s.replace(",", "")
    else:
        s = s.replace(" ", "").replace(" ", "").replace(".", "").replace(",", ".")
    if not re.fullmatch(r"\d+(?:\.\d+)?", s):
        raise ValueError(f"not a number: {printed!r}")
    return D(s)


def pattern(tokens: list[str]) -> str:
    from spikes.m3.answer_key import loose

    return r"\s*".join(loose(t) for t in tokens)


def buckets(cells: list[tuple[tuple, Decimal]]) -> dict[str, Decimal]:
    """Standard buckets (0-1, 1-2, 2-5, 5+); a column straddling a boundary merges buckets."""
    std = list(zip(BOUNDS, BOUNDS[1:], strict=False))
    owner = list(range(len(std)))

    def where(x, end=False):
        for i, (_, hi) in enumerate(std):
            if hi is None or (x <= hi if end else x < hi):
                return i
        return len(std) - 1

    for (a, b), _ in cells:
        first, last = where(a), (len(std) - 1 if b is None else where(b, end=True))
        for i in range(first + 1, last + 1):
            owner = [owner[first] if o == owner[i] else o for o in owner]
    out: dict[str, Decimal] = {}
    for (a, _b), v in cells:
        g = owner[where(a)]
        members = [i for i, o in enumerate(owner) if o == g]
        lo, hi = std[members[0]][0], std[members[-1]][1]
        name = f"{int(lo)}_plus" if hi is None else f"{int(lo)}_{int(hi)}"
        out[name] = out.get(name, D(0)) + v
    return out


def build(out: Path = OUT) -> list[dict]:
    from spikes.m3.answer_key import documents, html_pages

    docs = documents()
    texts: dict[str, list[str]] = {}
    lines = []
    for t in KEY:
        doc_id, path, kind, _end = docs[(t.issuer, f"report FY{t.fiscal_year}")]
        if doc_id not in texts:
            texts[doc_id] = html_pages(path.read_text())
        pages = texts[doc_id]
        found, where = [], set()
        for c in t.cells:
            hits = [(i, m) for i, p in enumerate(pages) for m in re.finditer(pattern(c.tokens), p)]
            if len(hits) != 1:
                raise LookupError(f"{t.issuer} FY{t.fiscal_year}: {c.tokens} matches {len(hits)}x")
            where.add(hits[0][0] + 1)
            found.append((c.span, number(c.tokens[c.pick], t.language) * t.scale))
        total = None
        for tokens, pick in t.totals:
            hits = [m for p in pages for m in re.finditer(pattern(tokens), p)]
            if len(hits) != 1:
                raise LookupError(f"{t.issuer} FY{t.fiscal_year}: total {tokens} {len(hits)}x")
            total = (total or D(0)) + number(tokens[pick], t.language) * t.scale
        summed = sum((v for _, v in found), D(0))
        if total is not None and abs(summed - total) > len(found) * t.scale:
            raise ValueError(f"{t.issuer} FY{t.fiscal_year}: columns {summed} != total {total}")
        for name, value in buckets(found).items():
            lines.append({
                "issuer": t.issuer, "fiscal_year": t.fiscal_year, "layer": t.layer,
                "basis": t.basis, "bucket": name, "value": f"{value:f}",
                "total_printed": "" if total is None else f"{total:f}",
                "document": doc_id, "pages": ", ".join(str(p) for p in sorted(where)),
                "note": t.note,
            })  # fmt: skip
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lines[0]))
        w.writeheader()
        w.writerows(lines)
    return lines


# --- Scoring the tool --------------------------------------------------------------------------


def score(key_path: Path = OUT, out: Path = SCORE) -> dict:
    """Each wall the tool marked verified, against the key's table on the same layer and basis:
    every bucket must equal the key within rounding (one unit of the printed scale per column).
    A verified wall on a basis the key does not hold is listed for a check by hand."""
    import json

    import duckdb

    key: dict[tuple, dict[str, Decimal]] = {}
    for r in csv.DictReader(key_path.open()):
        k = (r["issuer"], int(r["fiscal_year"]), r["layer"], r["basis"])
        key.setdefault(k, {})[r["bucket"]] = D(r["value"])
    con = duckdb.connect(str(ROOT / "data" / "tearsheet.duckdb"), read_only=True)
    rows = con.execute(
        "SELECT issuer, fiscal_year, concept, value, status, source_ref FROM facts "
        "WHERE concept LIKE 'maturity_%' AND is_primary"
    ).fetchall()
    con.close()
    walls: dict[tuple, dict] = {}
    for issuer, year, concept, value, status, ref in rows:
        layer = "borrowings" if concept.startswith("maturity_borrowings_") else "leases"
        bucket = concept.removeprefix(f"maturity_{layer}_")
        basis = json.loads(ref).get("basis")
        w = walls.setdefault((issuer, int(year), layer, basis), {"status": status, "b": {}})
        if bucket != "total":
            w["b"][bucket] = D(value)
    counts = {"verified_correct": 0, "verified_wrong": 0, "verified_not_in_key": 0,
              "unverified": 0, "key_tables_without_a_verified_wall": 0}  # fmt: skip
    lines = ["# M8 maturity wall against the answer key", "",
             "| Company | Year | Layer | Basis | Tool | Key | Result |",
             "| --- | --- | --- | --- | --- | --- | --- |"]  # fmt: skip
    for k, w in sorted(walls.items()):
        shown = ", ".join(f"{b} {v / 10**6:,.1f}" for b, v in w["b"].items())
        if w["status"] not in ("verified", "overridden"):
            counts["unverified"] += 1
            result = "unverified (flagged)"
        elif k not in key:
            counts["verified_not_in_key"] += 1
            result = "verified, not in the key: check by hand"
        else:
            scale = D(10**3) if k[0] == "aena" else D(10**6)
            ok = set(w["b"]) == set(key[k]) and all(
                abs(w["b"][b] - key[k][b]) <= 8 * scale for b in key[k]
            )
            counts["verified_correct" if ok else "verified_wrong"] += 1
            result = "verified, correct" if ok else "**verified, WRONG**"
        expected = ", ".join(f"{b} {v / 10**6:,.1f}" for b, v in key.get(k, {}).items())
        lines.append(f"| {k[0]} | FY{k[1]} | {k[2]} | {k[3]} | {shown} | {expected} | {result} |")
    verified = {k for k, w in walls.items() if w["status"] in ("verified", "overridden")}
    for k in sorted(key):
        if k not in verified:
            counts["key_tables_without_a_verified_wall"] += 1
    lines += ["", "| Count | |", "| --- | --- |"] + [f"| {k} | {v} |" for k, v in counts.items()]
    out.write_text("\n".join(lines) + "\n")
    return counts


def main() -> None:
    if sys.argv[1:] == ["score"]:
        counts = score()
        print(counts, file=sys.stderr)
        return
    lines = build()
    tables = {(r["issuer"], r["fiscal_year"], r["layer"], r["basis"]) for r in lines}
    print(f"maturity key: {len(tables)} tables, {len(lines)} buckets -> "
          f"{OUT.relative_to(ROOT)}", file=sys.stderr)  # fmt: skip


if __name__ == "__main__":
    main()
