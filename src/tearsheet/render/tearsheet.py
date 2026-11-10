"""One tearsheet: company, year, the fact sheet, the checked commentary and the run record.

Written by `uv run tearsheet samples` to samples/tearsheets/<company>_FY<year>.json for demo
mode, or built from the database in live mode. The layout helpers below (KPI cards, table,
charts) are used by the app and by the "every figure has a source" test, so the test checks
exactly what the page shows.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import duckdb
import yaml

from tearsheet.config import CONFIG, ROOT, load_issuers
from tearsheet.narrative.factsheet import FactSheet, add_events
from tearsheet.render.library import SAMPLES, Library, key, small_debt

TEARSHEETS = SAMPLES / "tearsheets"
APP_CONFIG = CONFIG / "app.yaml"
DRAFTS_DIR = ROOT / "docs" / "m4" / "drafts"
FORMAT_VERSION = 1


def load_app_config(path: Path = APP_CONFIG) -> dict:
    return yaml.safe_load(path.read_text())


def file_name(issuer: str, fiscal_year: int) -> str:
    return f"{issuer}_FY{fiscal_year}.json"


# --- Building from the database ----------------------------------------------------------------


def from_database(db_path: Path, sheet: FactSheet) -> dict:
    """The tearsheet record for a fact sheet (built by narrative.run.build_sheets). The year's
    checked events are added to the fact sheet as in M4, so its fingerprint can be compared
    with the one the draft was written from."""
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        commentary = _commentary(con, sheet)
        run = _run(con, sheet)
        event_rows = _events(con, sheet)
    finally:
        con.close()
    add_events(sheet, [_Event(sheet.fiscal_year, e) for e in event_rows])
    current = sheet.fingerprint()
    if run is not None:
        run["matches_figures"] = run["input_hash"] == current
    return {
        "format_version": FORMAT_VERSION,
        "issuer": sheet.issuer,
        "name": sheet.name,
        "type": sheet.type,
        "currency": sheet.currency,
        "fiscal_year": sheet.fiscal_year,
        "period_label": sheet.period_label,
        "peer_year": sheet.peer_year,
        "peer_group": sheet.peer_group,
        "peer_members": sheet.peer_members,
        "factsheet": sheet.to_dict(),
        "commentary": commentary,
        "events": event_rows,
        "run": run,
    }


@dataclass(frozen=True)
class _Event:
    """An events-table row, shaped as add_events reads it."""

    fiscal_year: int
    row: dict

    @property
    def verified(self) -> bool:
        return self.row["status"] == "verified"

    def __getattr__(self, name):
        names = {"id": "event_id", "title": "title", "summary": "summary",
                 "quote": "quote", "location": "location"}  # fmt: skip
        if name in names:
            return self.row[names[name]]
        raise AttributeError(name)


def _commentary(con, sheet: FactSheet) -> dict:
    from tearsheet.narrative.factsheet import load_narrative

    narrative = load_narrative()
    rows = con.execute(
        "SELECT section, sentence, text_blanks, text_rendered, facts, status, verifier_report "
        "FROM drafts WHERE issuer = ? AND fiscal_year = ? ORDER BY section, sentence",
        [sheet.issuer, sheet.fiscal_year],
    ).fetchall()
    removed = _removed(sheet.issuer, sheet.fiscal_year)
    out = {}
    for name, section in narrative["sections"].items():
        mine = [r for r in rows if r[0] == name]
        out[name] = {
            "title": section["title"],
            "status": mine[0][5] if mine else "not_drafted",
            "sentences": [
                {"text_blanks": r[2], "text": r[3], "facts": json.loads(r[4])} for r in mine
            ],
            "notes": json.loads(mine[0][6]) if mine else [],
            "removed": removed.get(name, []),
        }
    return out


def _removed(issuer: str, fiscal_year: int) -> dict[str, list[dict]]:
    """Sentences the verifier removed after two retries (decision 0018), from docs/m4."""
    path = DRAFTS_DIR / f"{issuer}_FY{fiscal_year}.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {
        name: [{"text": text, "why": why} for text, why in items]
        for name, items in (data.get("removed") or {}).items()
    }


def _run(con, sheet: FactSheet) -> dict | None:
    cols = [
        "filing_hashes", "provider", "model", "prompt_version", "input_hash", "calls",
        "input_tokens", "output_tokens", "cost_usd", "first_try_ok", "passed", "recorded_at",
    ]  # fmt: skip
    row = con.execute(
        f"SELECT {', '.join(cols)} FROM runs WHERE issuer = ? AND fiscal_year = ?",
        [sheet.issuer, sheet.fiscal_year],
    ).fetchone()
    if row is None:
        return None
    rec = dict(zip(cols, row, strict=True))
    rec["filing_hashes"] = json.loads(rec["filing_hashes"])
    rec["cost_usd"] = str(rec["cost_usd"]) if rec["cost_usd"] is not None else None
    return rec


def _events(con, sheet: FactSheet) -> list[dict]:
    cols = [
        "event_id", "topic", "title", "summary", "quote", "location", "document", "status",
        "model", "prompt_version",
    ]  # fmt: skip
    rows = con.execute(
        f"SELECT {', '.join(cols)} FROM events WHERE issuer = ? AND fiscal_year = ? "
        "ORDER BY event_id",
        [sheet.issuer, sheet.fiscal_year],
    ).fetchall()
    return [dict(zip(cols, r, strict=True)) for r in rows]


def write(record: dict, folder: Path = TEARSHEETS) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / file_name(record["issuer"], record["fiscal_year"])
    path.write_text(json.dumps(record, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def read(issuer: str, fiscal_year: int, folder: Path = TEARSHEETS) -> dict:
    data = json.loads((folder / file_name(issuer, fiscal_year)).read_text())
    if data.get("format_version") != FORMAT_VERSION:
        raise ValueError(f"{issuer} FY{fiscal_year}: tearsheet file in an old format")
    return data


def available(folder: Path = TEARSHEETS) -> list[tuple[str, int]]:
    """(company, year) of every pre-built tearsheet, in the order of config/issuers.yaml."""
    order = {i.id: n for n, i in enumerate(load_issuers())}
    found = []
    for p in folder.glob("*_FY*.json"):
        issuer, _, year = p.stem.rpartition("_FY")
        found.append((issuer, int(year)))
    return sorted(found, key=lambda t: (order.get(t[0], 99), -t[1]))


# --- Layout: what the tearsheet page shows ---------------------------------------------------


@dataclass(frozen=True)
class Cell:
    """One figure on the page: a library key (or None) and what to print instead if missing."""

    key: str | None
    rendered: str
    status: str  # verified | overridden | unverified | missing | not_meaningful


def cell(lib: Library, figure_key: str) -> Cell:
    f = lib.figure(figure_key)
    if f is None:
        return Cell(None, "n.a.", "missing")
    if small_debt(lib, f["issuer"], f["concept"], f["fiscal_year"]):
        return Cell(figure_key, "n.m.", "not_meaningful")
    if f["status"] not in ("verified", "overridden"):
        return Cell(figure_key, "awaiting review", "unverified")
    return Cell(figure_key, f["rendered"], f["status"])


def years_shown(lib: Library, ts: dict, config: dict | None = None) -> list[int]:
    config = config or load_app_config()
    have = [y for y in lib.years(ts["issuer"]) if y <= ts["fiscal_year"]]
    return have[-config["years_shown"] :]


def kpi_cards(lib: Library, ts: dict, config: dict | None = None) -> list[dict]:
    """The headline cards: metric, the year's figure and the fact sheet's change, if any."""
    config = config or load_app_config()
    cards = config["kpi_cards"]
    issuer, year = ts["issuer"], ts["fiscal_year"]
    out = []
    for metric in cards["all"] + cards.get(ts["type"], []):
        chosen = metric
        if not lib.usable(key(issuer, metric, year)) and metric in cards.get("fallback", {}):
            chosen = cards["fallback"][metric]
        c = cell(lib, key(issuer, chosen, year))
        change_id = f"{chosen}.change@FY{year}"
        change = ts["factsheet"]["items"].get(change_id)
        out.append(
            {
                "metric": chosen,
                "label": lib.label.get(chosen, chosen),
                "cell": c,
                "change_id": change_id if change else None,
                "change": change,
            }
        )
    return out


def kpi_table(lib: Library, ts: dict, config: dict | None = None, part: str = "both") -> dict:
    """The four-year table. `part`: "credit" (the rows for every company, PDF page 1),
    "operating" (the airline or airport rows, PDF page 2) or "both" (the app)."""
    config = config or load_app_config()
    years = years_shown(lib, ts, config)
    rows = []
    metrics = {
        "credit": config["kpi_table"]["all"],
        "operating": config["kpi_table"].get(ts["type"], []),
        "both": config["kpi_table"]["all"] + config["kpi_table"].get(ts["type"], []),
    }[part]
    for metric in metrics:
        cells = [cell(lib, key(ts["issuer"], metric, y)) for y in years]
        if all(c.status == "missing" for c in cells):
            continue
        rows.append({"metric": metric, "label": lib.label.get(metric, metric), "cells": cells})
    return {"years": years, "labels": [lib.period_label(ts["issuer"], y) for y in years],
            "rows": rows}  # fmt: skip


def chart_series(lib: Library, ts: dict, chart: str, config: dict | None = None) -> list[dict]:
    """Points of one chart: year, metric, value (only figures on the tearsheet), and the key."""
    config = config or load_app_config()
    points = []
    for metric in config["charts"][chart]["metrics"]:
        for y in years_shown(lib, ts, config):
            k = key(ts["issuer"], metric, y)
            if not lib.usable(k):
                continue
            f = lib.figures[k]
            points.append(
                {
                    "year": f"FY{y}",
                    "metric": lib.label.get(metric, metric),
                    "value": float(f["value"]),
                    "rendered": f["rendered"],
                    "key": k,
                }
            )
    return points


def commentary_ids(ts: dict) -> list[str]:
    """Every fact sheet id the commentary uses (figures and events)."""
    ids = []
    for section in ts["commentary"].values():
        for s in section["sentences"]:
            ids += [f["id"] for f in s["facts"]]
    return list(dict.fromkeys(ids))


def peer_table_for(lib: Library, ts: dict) -> dict:
    """The company's own peer group in its peer year (the tearsheet's peer table)."""
    from tearsheet.narrative.factsheet import load_narrative
    from tearsheet.render.library import peer_groups, peer_table

    groups = peer_groups()
    own = next(
        g for g in load_narrative()["peer_groups"] if ts["issuer"] in groups["groups"][g]["members"]
    )
    return peer_table(lib, own, ts["peer_year"], groups)


def page_refs(lib: Library, ts: dict, config: dict | None = None) -> list[dict]:
    """Every figure the tearsheet shows (app page and PDF), as references for source cards:
    {"key": library key} or {"fid": fact sheet id}."""
    config = config or load_app_config()
    refs: list[dict] = []
    for kpi in kpi_cards(lib, ts, config):
        if kpi["cell"].key:
            refs.append({"key": kpi["cell"].key})
        if kpi["change_id"]:
            refs.append({"fid": kpi["change_id"]})
    for row in kpi_table(lib, ts, config)["rows"]:
        refs += [{"key": c.key} for c in row["cells"] if c.key]
    for chart in config["charts"]:
        refs += [{"key": p["key"]} for p in chart_series(lib, ts, chart, config)]
    for row in peer_table_for(lib, ts)["rows"]:
        refs += [{"key": c["key"]} for c in row["cells"].values() if c.get("key")]
    refs += [{"fid": fid} for fid in commentary_ids(ts)]
    unique = {repr(sorted(r.items())): r for r in refs}
    return list(unique.values())


def live_record(db_path: Path, issuer_id: str, fiscal_year: int) -> dict:
    """The tearsheet record for any company and year, straight from the database (live mode)."""
    from tearsheet.narrative.factsheet import build, load_figures, load_narrative, load_specs

    narrative = load_narrative()
    specs = load_specs(narrative)
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        figures = load_figures(con, set(specs))
    finally:
        con.close()
    issuer = {i.id: i for i in load_issuers()}[issuer_id]
    sheet = build(issuer, fiscal_year, figures, specs, narrative)
    return from_database(db_path, sheet)
