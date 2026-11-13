"""Half-year and last-twelve-months figures for the app (M10, decision 0025).

The fiscal-year library (samples/figures.json) and the 18 tearsheet records are not touched.
The half-year figures live in a file of their own:

    live   read from the facts database (tables interim_reports, interim_facts, interim_gaps)
    demo   read from samples/interim.json, written by `uv run tearsheet samples`

For the pages, `ltm_view` lays the LTM figures over a copy of the library as one extra column
per company, after its last fiscal year, labelled with its date ("LTM Jun 2026, unaudited").
The tearsheet's key figures table and the watchlist read that view with the code they already
use, and every LTM figure opens on its parts: the full year (down to the filing), this first
half and last year's (down to the row and page of the half-year report).
Nothing here computes a financial figure: the values come from the database.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

import duckdb

from tearsheet.narrative import render
from tearsheet.render.library import SAMPLES, Library, _dumps, key

INTERIM_FILE = SAMPLES / "interim.json"
FORMAT_VERSION = 1
UNAUDITED = "Unaudited half-year figures"
PARTS = {"H1": "h1", "H1_prior": "h1_prior"}


def period_key(issuer: str, concept: str, period: str) -> str:
    return f"{issuer}:{concept}@{period}"


@dataclass
class Interim:
    reports: dict[str, dict] = field(default_factory=dict)  # issuer -> its half-year report
    figures: dict[str, dict] = field(default_factory=dict)  # issuer:concept@H1|H1_prior|LTM
    gaps: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"format_version": FORMAT_VERSION, "reports": self.reports,
                "figures": self.figures, "gaps": self.gaps}  # fmt: skip

    def write(self, path: Path = INTERIM_FILE) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_dumps(self.to_dict()))

    @classmethod
    def read(cls, path: Path = INTERIM_FILE) -> Interim:
        if not path.exists():
            return cls()
        data = json.loads(path.read_text())
        if data.get("format_version") != FORMAT_VERSION:
            raise ValueError(f"{path}: format {data.get('format_version')}")
        return cls(data["reports"], data["figures"], data["gaps"])


def from_database(db_path: Path) -> Interim:
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        tables = {r[0] for r in con.execute("SHOW TABLES").fetchall()}
        if "interim_facts" not in tables:
            return Interim()
        cols = ["issuer", "report_id", "period_end", "base_fiscal_year", "h1_label", "ltm_label",
                "document", "file", "sha256", "url", "language", "audit", "read_by", "provider",
                "model", "prompt_version", "error"]  # fmt: skip
        reports = {}
        for row in con.execute(
            f"SELECT {', '.join(cols)} FROM interim_reports ORDER BY issuer"
        ).fetchall():
            rec = dict(zip(cols, row, strict=True))
            rec["period_end"] = str(rec["period_end"])
            reports[rec.pop("issuer")] = rec
        figures = {}
        for i, p, end, c, v, d, cur, st, ref, status, note, warn in con.execute(
            "SELECT issuer, period, period_end, concept, value, decimals, currency, source_type, "
            "source_ref, status, note, warnings FROM interim_facts ORDER BY 1, 4, 2"
        ).fetchall():
            figures[period_key(i, c, p)] = {
                "issuer": i, "concept": c, "period": p, "period_end": str(end),
                "value": str(Decimal(str(v))), "decimals": d, "currency": cur,
                "source_type": st, "status": status, "note": note,
                "warnings": json.loads(warn) if warn else [],
                "source": json.loads(ref) if ref else {},
            }  # fmt: skip
        gaps = {
            period_key(i, c, p): reason
            for i, p, c, reason in con.execute(
                "SELECT issuer, period, concept, reason FROM interim_gaps ORDER BY 1, 3, 2"
            ).fetchall()
        }
    finally:
        con.close()
    return Interim(reports, figures, gaps)


# --- The LTM column: a view over the library --------------------------------------------------


@dataclass
class LtmLibrary(Library):
    """The library with one extra column per company: its LTM figures, stored under the year
    after its last full fiscal year and labelled with the half-year date."""

    ltm: dict[str, dict] = field(default_factory=dict)  # issuer -> {"year", "label", ...}

    def ltm_year(self, issuer: str) -> int | None:
        return self.ltm.get(issuer, {}).get("year")

    def period_label(self, issuer: str, fiscal_year: int) -> str:
        if self.ltm_year(issuer) == fiscal_year:
            return f"{self.ltm[issuer]['label']} (unaudited)"
        return super().period_label(issuer, fiscal_year)

    def why_missing(self, figure_key: str) -> str:
        return self.gaps.get(figure_key) or super().why_missing(figure_key)


def _figure(lib: Library, f: dict, concept: str, year: int, label: str, unit: str) -> dict:
    value = Decimal(f["value"])
    currency = lib.issuers[f["issuer"]]["currency"]
    return {
        "issuer": f["issuer"], "concept": concept, "fiscal_year": year,
        "period_end": f["period_end"], "label": label, "unit": unit, "currency": currency,
        "value": str(value), "decimals": f["decimals"],
        "rendered": render.value_text(value, unit, currency),
        "source_type": f["source_type"], "status": f["status"], "restated": False,
        "comparative": False, "filing_id": None, "value_tagged": str(value),
        "note": f["note"], "footnote": UNAUDITED, "warnings": f["warnings"],
        "source": f["source"],
    }  # fmt: skip


def ltm_view(lib: Library, interim: Interim) -> LtmLibrary:
    view = LtmLibrary(
        lib.issuers, dict(lib.filings), dict(lib.figures), dict(lib.gaps), dict(lib.unit),
        dict(lib.label), dict(lib.definition), dict(lib.higher_is_better),
    )  # fmt: skip
    for issuer, report in interim.reports.items():
        if issuer not in lib.issuers or report.get("error"):
            continue
        base = int(report["base_fiscal_year"])
        year = base + 1
        if year in lib.years(issuer):
            continue  # the full year has been loaded since: the annual figures take over
        view.ltm[issuer] = {
            "year": year, "label": report["ltm_label"], "base": base,
            "h1_label": report["h1_label"], "period_end": report["period_end"],
        }  # fmt: skip
        view.filings[report["report_id"]] = {
            "issuer": issuer, "fiscal_year": year, "period_end": report["period_end"],
            "origin": "half-year report (PDF), unaudited", "sha256": report["sha256"],
            "report_url": report["url"], "viewer_url": None, "json_url": None,
            "package_url": report["file"], "date_added": None, "language": report["language"],
            "choice_reason": report["document"],
        }  # fmt: skip
        mine = {k: f for k, f in interim.figures.items() if f["issuer"] == issuer}
        prior_end = _prior_end(report["period_end"])
        for f in mine.values():
            concept, period = f["concept"], f["period"]
            name = lib.label.get(concept, concept)
            unit = lib.unit.get(concept, "amount")
            if period == "LTM":
                fig = _figure(lib, f, concept, year, name, unit)
                src = f["source"]
                if src.get("formula") == "ltm":
                    links, inputs = [], []
                    for part in src["parts"]:
                        if part["period"] in PARTS:
                            links.append(key(issuer, f"{concept}.{PARTS[part['period']]}", year))
                        else:
                            links.append(key(issuer, concept, base))
                        inputs.append({"name": part["line"], "value": part["value"]})
                    fig["source"] = {"formula": "ltm", "inputs": inputs}
                    fig["input_keys"] = links
                else:
                    fig["input_keys"] = [
                        key(issuer, i["name"], year) if period_key(issuer, i["name"], "LTM")
                        in mine else None
                        for i in src.get("inputs", [])
                    ]  # fmt: skip
                view.figures[key(issuer, concept, year)] = fig
            else:
                part = f"{concept}.{PARTS[period]}"
                end = report["period_end"] if period == "H1" else prior_end
                flow = period == "H1_prior" or period_key(issuer, concept, "H1_prior") in mine
                label = f"{name}, {'six months to' if flow else 'at'} {end}"
                fig = _figure(lib, f, part, year, label, unit)
                fig["filing_id"] = report["report_id"]
                fig["footnote"] = None  # its card already says the figures are unaudited
                src = dict(f["source"])
                quotes = src.get("quotes") or []
                src["locations"] = (src.get("locations") or [""]) * max(1, len(quotes))
                src["document"] = report["document"]
                src["concepts"] = [r["label"] for r in src.get("rows") or []]
                src["fact_ids"] = [x for x in f["source"].get("locations") or [] if x]
                fig["source"] = src
                view.figures[key(issuer, part, year)] = fig
                view.label[part], view.unit[part] = label, unit
                where = "income statement or cash flow statement" if flow else "balance sheet"
                view.definition[part] = (
                    f"Read from the {where} of the half-year report and checked by code "
                    "against the last annual figures (M10)."
                )
        for k, reason in interim.gaps.items():
            i, rest = k.split(":", 1)
            concept, period = rest.rsplit("@", 1)
            if i == issuer and period == "LTM":
                view.gaps.setdefault(key(issuer, concept, year), reason)
    return view


def _prior_end(period_end: str) -> str:
    return f"{int(period_end[:4]) - 1}{period_end[4:]}"
