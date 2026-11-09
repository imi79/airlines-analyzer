"""The figure library: every figure the app shows, each with the record of where it came from.

One library serves both modes of the app (decision 0019):

    live   built from the facts database (data/tearsheet.duckdb)
    demo   read from samples/figures.json, written by `uv run tearsheet samples`

A figure is keyed `<company>:<concept>@FY<year>`, for example `afkl:net_leverage@FY2025`, and
carries its value as stored (with its decimals), the printed form, and its source: the filing
fact, the formula and its inputs, the quote from the report, or the hand entry. Nothing here
computes a financial figure: the values come from the database, built by M1 to M4.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from decimal import Decimal
from functools import cache
from pathlib import Path

import duckdb
import yaml

from tearsheet.config import CONFIG, ROOT, load_issuers
from tearsheet.metrics.engine import ITEMS, labels, load_catalog
from tearsheet.metrics.peers import fiscal_label, months_from_december, peer_year
from tearsheet.narrative import render
from tearsheet.normalize.mapper import CONCEPT_MAP

SAMPLES = ROOT / "samples"
FIGURES_FILE = SAMPLES / "figures.json"
PEERS = CONFIG / "peers.yaml"
FORMAT_VERSION = 1


def key(issuer: str, concept: str, fiscal_year: int) -> str:
    return f"{issuer}:{concept}@FY{fiscal_year}"


def split(figure_key: str) -> tuple[str, str, int]:
    issuer, rest = figure_key.split(":", 1)
    concept, year = rest.rsplit("@FY", 1)
    return issuer, concept, int(year)


def _dumps(data) -> str:
    return json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True, default=str) + "\n"


# --- What each concept is ---------------------------------------------------------------------


@dataclass(frozen=True)
class Concepts:
    """Label, unit and definition of every concept: catalog metrics, statement lines and the
    figures read from the report text."""

    label: dict[str, str]
    unit: dict[str, str]
    definition: dict[str, str]
    higher_is_better: dict[str, bool | None]

    @classmethod
    def load(cls) -> Concepts:
        catalog = _catalog()
        lines = yaml.safe_load(CONCEPT_MAP.read_text())["lines"]
        items = yaml.safe_load(ITEMS.read_text())["items"]
        unit = {k: "amount" for k in lines}
        unit |= {k: v["unit"] for k, v in items.items()}
        unit |= {k: v["unit"] for k, v in catalog.items()}
        definition = {k: " ".join(str(v.get("definition") or "").split()) for k, v in lines.items()}
        definition |= {
            k: " ".join(str(v.get("definition") or "").split()) for k, v in items.items()
        }
        definition |= {k: " ".join(str(v["definition"]).split()) for k, v in catalog.items()}
        better = {k: v.get("higher_is_better") for k, v in catalog.items()}
        return cls(labels(catalog), unit, definition, better)


# --- The library --------------------------------------------------------------------------------


@dataclass
class Library:
    issuers: dict[str, dict]  # id -> name, type, segment, currency, country
    filings: dict[str, dict]  # filing id -> origin, hash, links
    figures: dict[str, dict]  # figure key -> value, printed form, source
    gaps: dict[str, str] = field(default_factory=dict)  # figure key -> why there is no value
    unit: dict[str, str] = field(default_factory=dict)  # concept -> unit
    label: dict[str, str] = field(default_factory=dict)  # concept -> label
    definition: dict[str, str] = field(default_factory=dict)
    higher_is_better: dict[str, bool | None] = field(default_factory=dict)

    # -- reading
    def figure(self, figure_key: str) -> dict | None:
        return self.figures.get(figure_key)

    def _index(self) -> dict[tuple[str, int], str]:
        """(company, year) -> latest period end, built once (the figures don't change)."""
        stamp = id(self.figures), len(self.figures)
        if getattr(self, "_ends_stamp", None) != stamp:
            ends: dict[tuple[str, int], str] = {}
            for f in self.figures.values():
                k = (f["issuer"], f["fiscal_year"])
                ends[k] = max(ends.get(k, f["period_end"]), f["period_end"])
            self._ends, self._ends_stamp = ends, stamp
        return self._ends

    def years(self, issuer: str) -> list[int]:
        return sorted(y for i, y in self._index() if i == issuer)

    def period_end(self, issuer: str, fiscal_year: int) -> str | None:
        return self._index().get((issuer, fiscal_year))

    def period_label(self, issuer: str, fiscal_year: int) -> str:
        from datetime import date

        end = self.period_end(issuer, fiscal_year)
        return fiscal_label(fiscal_year, date.fromisoformat(end)) if end else f"FY{fiscal_year}"

    def why_missing(self, figure_key: str) -> str:
        if figure_key in self.gaps:
            return self.gaps[figure_key]
        return "no figure for this year"

    def usable(self, figure_key: str) -> bool:
        """On the tearsheet: verified, or approved by Imane (overridden)."""
        f = self.figures.get(figure_key)
        return f is not None and f["status"] in ("verified", "overridden")

    # -- saving and loading
    def to_dict(self) -> dict:
        return {
            "format_version": FORMAT_VERSION,
            "issuers": self.issuers,
            "filings": self.filings,
            "figures": self.figures,
            "gaps": self.gaps,
            "concepts": {
                "unit": self.unit,
                "label": self.label,
                "definition": self.definition,
                "higher_is_better": self.higher_is_better,
            },
        }

    def write(self, path: Path = FIGURES_FILE) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_dumps(self.to_dict()))

    @classmethod
    def read(cls, path: Path = FIGURES_FILE) -> Library:
        data = json.loads(path.read_text())
        if data.get("format_version") != FORMAT_VERSION:
            raise ValueError(
                f"{path}: format {data.get('format_version')}, expected {FORMAT_VERSION}"
            )
        c = data["concepts"]
        return cls(
            data["issuers"],
            data["filings"],
            data["figures"],
            data["gaps"],
            c["unit"],
            c["label"],
            c["definition"],
            c["higher_is_better"],
        )


# --- Building the library from the facts database ------------------------------------------


def from_database(db_path: Path) -> Library:
    concepts = Concepts.load()
    issuers = {
        i.id: {
            "name": i.name,
            "type": i.type,
            "segment": i.segment,
            "currency": i.currency,
            "country": i.country,
            "fiscal_year_end": i.fiscal_year_end,
        }
        for i in load_issuers()
    }
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        filings = _filings(con)
        figures = _figures(con, issuers, concepts)
        gaps = {
            key(i, c, int(y)): reason
            for i, y, c, reason in con.execute(
                "SELECT issuer, fiscal_year, concept, reason FROM gaps ORDER BY 1, 2, 3"
            ).fetchall()
            if i in issuers
        }
    finally:
        con.close()
    _link_inputs(figures)
    return Library(
        issuers,
        filings,
        figures,
        {k: v for k, v in gaps.items() if k not in figures},
        concepts.unit,
        concepts.label,
        concepts.definition,
        concepts.higher_is_better,
    )


def _filings(con) -> dict[str, dict]:
    cols = [
        "filing_id", "issuer", "fiscal_year", "period_end", "origin", "sha256", "json_url",
        "viewer_url", "report_url", "package_url", "date_added", "language", "choice_reason",
    ]  # fmt: skip
    rows = con.execute(f"SELECT {', '.join(cols)} FROM filings ORDER BY filing_id").fetchall()
    out = {}
    for row in rows:
        rec = dict(zip(cols, row, strict=True))
        rec["period_end"] = str(rec["period_end"])
        out[rec.pop("filing_id")] = rec
    return out


def _figures(con, issuers: dict, concepts: Concepts) -> dict[str, dict]:
    cols = [
        "issuer", "fiscal_year", "period_end", "concept", "value", "value_tagged", "decimals",
        "currency", "source_type", "source_ref", "status", "restated", "comparative",
        "filing_id", "note", "footnote", "warnings",
    ]  # fmt: skip
    rows = con.execute(
        f"SELECT {', '.join(cols)} FROM facts WHERE is_primary "
        "ORDER BY issuer, fiscal_year, concept, source_type"
    ).fetchall()
    out: dict[str, dict] = {}
    for row in rows:
        r = dict(zip(cols, row, strict=True))
        if r["issuer"] not in issuers:
            continue
        concept = r["concept"]
        k = key(r["issuer"], concept, int(r["fiscal_year"]))
        if k in out and r["source_type"] == "computed":
            # a metric with the same id as the line it repeats (passengers): the line has the
            # source, the metric only copies it
            continue
        currency = issuers[r["issuer"]]["currency"]
        unit = concepts.unit.get(concept, "amount")
        value = Decimal(str(r["value"]))
        out[k] = {
            "issuer": r["issuer"],
            "concept": concept,
            "fiscal_year": int(r["fiscal_year"]),
            "period_end": str(r["period_end"]),
            "label": concepts.label.get(concept, concept),
            "unit": unit,
            "currency": currency,
            "value": str(value),
            "decimals": r["decimals"],
            "rendered": render.value_text(value, unit, currency),
            "source_type": r["source_type"],
            "status": r["status"],
            "restated": bool(r["restated"]),
            "comparative": bool(r["comparative"]),
            "filing_id": r["filing_id"] or None,
            "value_tagged": str(Decimal(str(r["value_tagged"]))),
            "note": r["note"] or None,
            "footnote": r["footnote"] or None,
            "warnings": json.loads(r["warnings"]) if r["warnings"] else [],
            "source": json.loads(r["source_ref"]) if r["source_ref"] else {},
        }
    return out


def _link_inputs(figures: dict[str, dict]) -> None:
    """Each input of a computed figure gets the key of the figure it was read from: the same
    year, or the year before for growth rates (matched on the value used)."""
    for f in figures.values():
        if f["source_type"] != "computed":
            continue
        links = []
        for inp in f["source"].get("inputs", []):
            value = Decimal(inp["value"])
            found = None
            for year in (f["fiscal_year"], f["fiscal_year"] - 1):
                candidate = figures.get(key(f["issuer"], inp["name"], year))
                if candidate is not None and _same(Decimal(candidate["value"]), value):
                    found = key(f["issuer"], inp["name"], year)
                    break
            links.append(found)
        f["input_keys"] = links


def _same(stored: Decimal, used: Decimal) -> bool:
    """The database keeps 12 decimals (DECIMAL(38, 12)); a formula may have used more."""
    step = Decimal("1e-12")
    return stored.quantize(step) == used.quantize(step) or abs(stored - used) <= step


@cache
def _catalog() -> dict:
    return load_catalog()


@cache
def _small_debt_rule() -> dict:
    from tearsheet.narrative.factsheet import load_narrative

    return load_narrative().get("small_debt") or {}


def small_debt(lib: Library, issuer: str, metric: str, fiscal_year: int) -> str | None:
    """Why a ratio to debt is not meaningful (debt is very small), as in the M4 fact sheets
    (config/narrative.yaml, small_debt), or None."""
    rule = _small_debt_rule()
    if metric not in (rule.get("metrics") or ()):
        return None
    gross = lib.figures.get(key(issuer, "gross_leverage", fiscal_year))
    if gross is None or Decimal(gross["value"]) >= Decimal(str(rule["gross_leverage_below"])):
        return None
    return (
        f"n.m.: debt is very small (gross leverage {gross['rendered']}), so ratios to debt "
        "say little"
    )


# --- Peer tables ----------------------------------------------------------------------------


def peer_groups() -> dict:
    return yaml.safe_load(PEERS.read_text())


@cache
def _peer_groups() -> dict:
    return peer_groups()


def peer_years(lib: Library) -> list[int]:
    from datetime import date

    return sorted({peer_year(date.fromisoformat(end)) for end in lib._index().values()})


def members_year(lib: Library, issuer: str, year: int) -> int | None:
    """The company's fiscal year that falls in peer year `year` (decision 0008)."""
    from datetime import date

    for fy in lib.years(issuer):
        end = lib.period_end(issuer, fy)
        if end and peer_year(date.fromisoformat(end)) == year:
            return fy
    return None


def peer_table(lib: Library, group: str, year: int, groups: dict | None = None) -> dict:
    """The peer view for one group and peer year: per metric, each member's value (verified
    only), the median and the ranks; unverified or missing values are shown with the reason.
    The median and ranks use the same rule as the M2 peer tables and the M4 fact sheets."""
    from datetime import date
    from statistics import median

    groups = groups or _peer_groups()
    spec = groups["groups"][group]
    members = list(spec["members"])
    years = {m: members_year(lib, m, year) for m in members}
    offsets = {}  # months from 31 December, for companies whose year ends elsewhere
    for m, fy in years.items():
        if fy is not None:
            months = months_from_december(date.fromisoformat(lib.period_end(m, fy)))
            if months:
                offsets[m] = months
    catalog = _catalog()
    rows = []
    for metric in groups["metrics"]:
        types = catalog.get(metric, {}).get("applies_to")
        if types and any(lib.issuers[m]["type"] not in types for m in members):
            continue
        cells, values = {}, {}
        for m in members:
            fy = years[m]
            if fy is None:
                cells[m] = {"key": None, "reason": "no fiscal year in this peer year"}
                continue
            k = key(m, metric, fy)
            tiny = small_debt(lib, m, metric, fy) if k in lib.figures else None
            if tiny:
                cells[m] = {"key": k, "reason": tiny, "nm": True}
            elif lib.usable(k):
                values[m] = Decimal(lib.figures[k]["value"])
                cells[m] = {"key": k, "rendered": lib.figures[k]["rendered"]}
            elif k in lib.figures:
                cells[m] = {"key": k, "reason": "not verified yet: waiting for Imane's review"}
            else:
                cells[m] = {"key": None, "reason": lib.why_missing(k)}
        better = lib.higher_is_better.get(metric)
        mid = median(values.values()) if values else None
        ranks = {}
        if better is not None and values:
            ordered = sorted(values, key=lambda i: values[i], reverse=bool(better))
            ranks = {m: n for n, m in enumerate(ordered, start=1)}
        for m, n in ranks.items():
            cells[m]["rank"] = n
            cells[m]["rank_of"] = len(values)
        unit = lib.unit.get(metric, "pct")
        rows.append(
            {
                "metric": metric,
                "label": lib.label.get(metric, metric),
                "unit": unit,
                "higher_is_better": better,
                "median": str(mid) if mid is not None else None,
                "median_rendered": render.value_text(mid, unit, "") if mid is not None else None,
                "count": len(values),
                "cells": cells,
            }
        )
    return {
        "group": group,
        "label": spec["label"],
        "peer_year": year,
        "members": members,
        "fiscal_years": {
            m: (lib.period_label(m, fy) if fy is not None else None) for m, fy in years.items()
        },
        "year_end_offsets": offsets,
        "rows": rows,
    }
