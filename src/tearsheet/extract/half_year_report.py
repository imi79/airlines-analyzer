"""The M10 records: docs/m10/half_year.md (every half-year and LTM figure, with the control that
confirmed it or the reason it waits), half_year.csv, and the answer key score."""

from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path

import duckdb

from tearsheet.config import DB_PATH, ROOT, load_issuers
from tearsheet.extract import half_year
from tearsheet.metrics.engine import labels, load_catalog

OUT = ROOT / "docs" / "m10"
KEY = OUT / "answer_key.csv"
MILLION = Decimal(1_000_000)
READ_BY = {
    "ai": "the AI, checked by code",
    "hand": "hand entry (the PDF gives no text for its figures)",
}
SHOWN = [
    "ebitda",
    "ebitda_margin",
    "total_debt",
    "net_debt",
    "net_leverage",
    "gross_leverage",
    "interest_coverage",
    "ffo_to_debt",
    "fcf",
    "fcf_after_leases",
    "cash_liquidity",
    "cash_short_term_debt_cover",
]


def _fmt(value, unit: str = "amount") -> str:
    if value is None:
        return ""
    value = Decimal(str(value))
    if unit == "x":
        return f"{value:.2f}x"
    if unit == "pct":
        return f"{value * 100:.1f}%"
    return f"{value / MILLION:,.1f}"


def score(con, key_path: Path = KEY) -> dict:
    """Each line of the answer key against what was loaded: verified and correct, verified but
    wrong (must be zero), flagged and correct, flagged and wrong, or not read."""
    facts = {
        (i, p, c): (v, s)
        for i, p, c, v, s in con.execute(
            "SELECT issuer, period, concept, value, status FROM interim_facts"
        ).fetchall()
    }
    counts = {
        k: 0
        for k in (
            "verified_correct",
            "verified_wrong",
            "flagged_correct",
            "flagged_wrong",
            "not_read",
        )
    }
    rows = []
    with key_path.open() as handle:
        for r in csv.DictReader(handle):
            wanted = [("H1", r["current"])] + ([("H1_prior", r["prior"])] if r["prior"] else [])
            got = [facts.get((r["issuer"], p, r["line"])) for p, _ in wanted]
            if any(g is None for g in got):
                outcome = "not_read"
            else:
                right = all(
                    Decimal(str(g[0])) == Decimal(w) * MILLION
                    for g, (_, w) in zip(got, wanted, strict=True)
                )
                verified = all(g[1] in ("verified", "overridden") for g in got)
                outcome = (
                    f"{'verified' if verified else 'flagged'}_{'correct' if right else 'wrong'}"
                )
            counts[outcome] += 1
            rows.append((r["issuer"], r["line"], outcome))
    return {"counts": counts, "rows": rows, "total": len(rows)}


def write_all(db_path: Path = DB_PATH, out: Path = OUT) -> dict:
    con = duckdb.connect(str(db_path), read_only=True)
    names = labels(load_catalog())
    units = {k: v["unit"] for k, v in load_catalog().items()}
    issuers = {i.id: i for i in load_issuers()}
    reports = con.execute(
        "SELECT issuer, report_id, period_end, base_fiscal_year, h1_label, ltm_label, document, "
        "read_by, input_tokens, output_tokens, error, columns FROM interim_reports"
    ).fetchall()
    facts = con.execute(
        "SELECT issuer, period, period_end, concept, value, currency, source_type, status, "
        "source_ref, note FROM interim_facts ORDER BY issuer, concept, period"
    ).fetchall()
    gaps = con.execute("SELECT issuer, period, concept, reason FROM interim_gaps").fetchall()
    out.mkdir(parents=True, exist_ok=True)
    with (out / "half_year.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "issuer",
                "period",
                "period_end",
                "concept",
                "label",
                "value",
                "currency",
                "source",
                "status",
                "control_or_reason",
            ]
        )
        for i, p, end, c, v, cur, st, status, ref, note in facts:
            ref = json.loads(ref)
            why = ref.get("control") or "; ".join(ref.get("checks_failed") or []) or note or ""
            writer.writerow(
                [i, p, end, c, names.get(c, c), f"{Decimal(str(v)):f}", cur, st, status, why]
            )
    statements = {k: v["statement"] for k, v in half_year.load_settings()["lines"].items()}
    total = {"verified": 0, "flagged": 0, "loaded": 0}
    text = [
        "# Half-year and last-twelve-months figures (M10)",
        "",
        "Written by `uv run tearsheet all`. One section per company: the lines read from its "
        "half-year report, the control that confirmed each one or the reason it waits for "
        "review, and the credit metrics at LTM. Amounts in millions of the reporting currency. "
        "All half-year figures are **unaudited**.",
        "",
    ]
    for issuer_id, issuer in issuers.items():
        rep = next((r for r in reports if r[0] == issuer_id), None)
        if rep is None:
            continue
        _, rid, end, base, h1_label, ltm_label, document, read_by, tin, tout, error, cols = rep
        mine = [f for f in facts if f[0] == issuer_id]
        text += [
            f"## {issuer.name}: {ltm_label}",
            "",
            f"Report: {document}. Half year to {end}; last full year in the database: "
            f"FY{base}. Read by: {READ_BY[read_by]}"
            + (f" ({tin + tout:,} tokens)." if tin else "."),
            "",
        ]
        if error:
            text += [f"**Not loaded:** {error}", ""]
            continue
        total["loaded"] += 1
        for kind, c in json.loads(cols).items():
            how = "; ".join(c["how"] + c["failures"])
            text.append(f"- {kind.replace('_', ' ')} columns: {how}")
        text += [
            "",
            f"| Line | {h1_label} | Same half a year before | {ltm_label} | Status | "
            "Control, or why it waits |",
            "| --- | ---: | ---: | ---: | --- | --- |",
        ]
        lines = sorted(
            {f[3] for f in mine if f[3] in statements}, key=lambda x: list(statements).index(x)
        )
        for line in lines:
            by = {f[1]: f for f in mine if f[3] == line}
            h1 = by.get("H1")
            ref = json.loads(h1[8]) if h1 else {}
            status = h1[7] if h1 else ""
            flagged = status == "unverified"
            total["flagged" if flagged else "verified"] += 1
            why = ref.get("control") or "; ".join(ref.get("checks_failed") or [])
            cells = [_fmt(by[p][4]) if p in by else "" for p in ("H1", "H1_prior", "LTM")]
            text.append(
                f"| {names.get(line, line)} | {cells[0]} | {cells[1]} | {cells[2]} "
                f"| {'**awaiting review**' if flagged else status} | {why} |"
            )
        missing = [(c, r) for i, p, c, r in gaps if i == issuer_id and p == "H1"]
        if missing:
            text += [
                "",
                "Not in the half-year statements: "
                + "; ".join(f"{names.get(c, c)} ({r})" for c, r in missing)
                + ".",
            ]
        text += [
            "",
            f"| Metric at {ltm_label} | Value | Status | How, or why missing |",
            "| --- | ---: | --- | --- |",
        ]
        for metric in SHOWN:
            fact = next((f for f in mine if f[1] == "LTM" and f[3] == metric), None)
            if fact:
                status = "awaiting review" if fact[7] == "unverified" else fact[7]
                text.append(
                    f"| {names[metric]} | {_fmt(fact[4], units[metric])} | {status} | "
                    f"{fact[9] or ''} |"
                )
            else:
                why = next(
                    (r for i, p, c, r in gaps if (i, p, c) == (issuer_id, "LTM", metric)), None
                )
                if why:
                    text.append(f"| {names[metric]} | missing | | {why} |")
        text.append("")
    (out / "half_year.md").write_text("\n".join(text))
    result = {"reports": len(reports), **total, "score": None}
    if KEY.exists():
        s = score(con)
        result["score"] = s
        c = s["counts"]
        flagged = [
            f"- {i}, {names.get(x, x)}: {o.replace('_', ' and ')}"
            for i, x, o in s["rows"]
            if o != "verified_correct"
        ]
        (out / "answer_key_score.md").write_text(
            "\n".join(
                [
                    "# M10 answer key score",
                    "",
                    "The answer key (`answer_key.csv`, three companies, written before the AI read "
                    "anything) against the figures loaded. Written by `uv run tearsheet all`.",
                    "",
                    "| Outcome | Lines |",
                    "| --- | ---: |",
                    f"| Verified and correct | {c['verified_correct']} |",
                    f"| **Verified but wrong** (must be zero) | **{c['verified_wrong']}** |",
                    f"| Flagged for review, figure correct | {c['flagged_correct']} |",
                    f"| Flagged for review, figure wrong | {c['flagged_wrong']} |",
                    f"| Not read | {c['not_read']} |",
                    f"| Total | {s['total']} |",
                    "",
                    "Lines not verified automatically:",
                    "",
                    *(flagged or ["- none"]),
                    "",
                ]
            )
        )
    con.close()
    return result
