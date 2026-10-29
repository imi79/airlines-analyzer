"""M0 data feasibility spike.

Usage (from the repo root):
    uv run python -m spikes.m0.coverage discover   # find each issuer and list its filings
    uv run python -m spikes.m0.coverage matrix     # download filings, build the coverage matrix
    uv run python -m spikes.m0.coverage text       # search airline report text for traffic terms
    uv run python -m spikes.m0.coverage ecb        # confirm the ECB exchange-rate series
    uv run python -m spikes.m0.coverage all        # all of the above
Add --offline to rerun from the local cache only.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

from spikes.m0 import xbrl
from spikes.m0.api import Client

ROOT = Path(__file__).resolve().parents[2]
ISSUERS = ROOT / "config" / "issuers.yaml"
CONCEPTS = Path(__file__).with_name("concepts.yaml")
OUT = ROOT / "docs" / "m0"
FILINGS_CSV = OUT / "filings.csv"


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


# --- discover --------------------------------------------------------------------------------


def search_entities(client: Client, fragment: str) -> list[dict]:
    flt = json.dumps([{"name": "name", "op": "ilike", "val": f"%{fragment}%"}])
    return client.get_all("/api/entities", {"filter": flt})


def entity_filings(client: Client, entity: dict) -> list[dict]:
    related = entity.get("relationships", {}).get("filings", {}).get("links", {}).get("related")
    return client.get_all(related or f"/api/entities/{entity['id']}/filings")


def fiscal_year(period_end: str) -> int:
    return date.fromisoformat(period_end[:10]).year


def discover(client: Client, issuers: list[dict], first_fy: int) -> list[dict]:
    rows = []
    for issuer in issuers:
        entities = search_entities(client, issuer["search"])
        if issuer.get("lei"):
            entities = [e for e in entities if e["attributes"].get("identifier") == issuer["lei"]]
        print(f"{issuer['name']}: {len(entities)} matching entities")
        for entity in entities:
            attrs = entity["attributes"]
            print(f"    {attrs.get('identifier')}  {attrs.get('name')}")
            for filing in entity_filings(client, entity):
                f = filing["attributes"]
                if not f.get("period_end") or fiscal_year(f["period_end"]) < first_fy:
                    continue
                rows.append(
                    {
                        "issuer": issuer["id"],
                        "entity_name": attrs.get("name"),
                        "lei": attrs.get("identifier"),
                        "fiscal_year": fiscal_year(f["period_end"]),
                        "period_end": f["period_end"][:10],
                        "country": f.get("country"),
                        "fxo_id": f.get("fxo_id"),
                        "date_added": f.get("date_added"),
                        "error_count": f.get("error_count"),
                        "warning_count": f.get("warning_count"),
                        "json_url": f.get("json_url"),
                        "report_url": f.get("report_url"),
                        "viewer_url": f.get("viewer_url"),
                        "package_url": f.get("package_url"),
                        "chosen": "",
                        "choice_reason": "",
                        "language": "",
                    }
                )
    return rows


# --- choose one filing per issuer and year ----------------------------------------------------


def choose_filings(client: Client, rows: list[dict]) -> list[dict]:
    """English if available, then fewest validation errors, then most recently added."""
    groups: dict[tuple[str, int], list[dict]] = {}
    for row in rows:
        if row["json_url"]:
            groups.setdefault((row["issuer"], row["fiscal_year"]), []).append(row)
    for group in groups.values():
        for row in group:
            if len(group) > 1:
                row["language"] = xbrl.main_language(load_filing(client, row)) or ""

        # Stable sorts: newest first, then fewest errors, then English first.
        ordered = sorted(group, key=lambda r: r["date_added"] or "", reverse=True)
        ordered = sorted(ordered, key=lambda r: r["error_count"] or 0)
        ordered = sorted(ordered, key=lambda r: len(group) > 1 and r["language"] != "en")
        best = ordered[0]
        best["chosen"] = "yes"
        if len(group) == 1:
            best["choice_reason"] = "only filing"
        else:
            best["choice_reason"] = (
                f"{len(group)} filings: language={best['language'] or '?'}, "
                f"errors={best['error_count']}, added={best['date_added']}"
            )
    return rows


def load_filing(client: Client, row: dict) -> list[xbrl.Fact]:
    path = client.download(row["json_url"], "xbrl-json")
    return xbrl.load_facts(json.loads(path.read_text()))


# --- coverage matrix ---------------------------------------------------------------------------


def build_matrix(client: Client, rows: list[dict], spec: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    lines, blocks = spec["lines"], spec["text_blocks"]
    wide, long = [], []
    for row in (r for r in rows if r["chosen"] == "yes"):
        facts = load_filing(client, row)
        fy_end = date.fromisoformat(row["period_end"])
        statuses = {}
        for line_id, line_spec in lines.items():
            result = xbrl.classify_line(line_id, line_spec, facts, fy_end)
            statuses[line_id] = result.status
            long.append(
                {
                    "issuer": row["issuer"],
                    "fiscal_year": row["fiscal_year"],
                    "line": line_id,
                    "status": result.status,
                    "concept": result.concept or "",
                    "value": result.value or "",
                    "decimals": "" if result.decimals is None else result.decimals,
                    "unit": result.unit or "",
                    "extension_candidates": " ".join(result.candidates),
                }
            )
        for block_id, block_spec in blocks.items():
            concept = xbrl.has_text_block(block_spec["concepts"], facts)
            statuses[block_id] = "found" if concept else "missing"
            long.append(
                {
                    "issuer": row["issuer"],
                    "fiscal_year": row["fiscal_year"],
                    "line": block_id,
                    "status": statuses[block_id],
                    "concept": concept or "",
                    "value": "",
                    "decimals": "",
                    "unit": "",
                    "extension_candidates": "",
                }
            )
        failed = xbrl.critical_met(statuses, spec["critical"])
        extension_concepts = sorted({f.concept for f in facts if not f.standard})
        wide.append(
            {
                "issuer": row["issuer"],
                "fiscal_year": row["fiscal_year"],
                "period_end": row["period_end"],
                "usable": "yes" if not failed else "no",
                "critical_gaps": " ".join(failed),
                "facts": len(facts),
                "extension_concepts_in_filing": len(extension_concepts),
                **statuses,
            }
        )
    return pd.DataFrame(wide), pd.DataFrame(long)


def go_no_go(wide: pd.DataFrame, issuers: list[dict], min_years: int) -> pd.DataFrame:
    rows = []
    for issuer in issuers:
        sub = wide[wide["issuer"] == issuer["id"]] if not wide.empty else wide
        usable = sorted(sub[sub["usable"] == "yes"]["fiscal_year"].tolist()) if len(sub) else []
        years = sorted(sub["fiscal_year"].tolist()) if len(sub) else []
        rows.append(
            {
                "issuer": issuer["id"],
                "name": issuer["name"],
                "years_filed": " ".join(map(str, years)),
                "usable_years": " ".join(map(str, usable)),
                "decision": "go" if len(usable) >= min_years else "no-go",
            }
        )
    return pd.DataFrame(rows)


# --- airline report text -----------------------------------------------------------------------


def report_text(client: Client, rows: list[dict], issuers: list[dict], spec: dict) -> pd.DataFrame:
    airlines = {i["id"] for i in issuers if i["type"] == "airline"}
    latest: dict[str, dict] = {}
    for row in rows:
        if row["chosen"] == "yes" and row["issuer"] in airlines and row["report_url"]:
            if row["fiscal_year"] > latest.get(row["issuer"], {}).get("fiscal_year", 0):
                latest[row["issuer"]] = row
    out = []
    for issuer_id, row in sorted(latest.items()):
        path = client.download(row["report_url"], "report")
        text = xbrl.html_to_text(path.read_text(errors="replace"))
        for term_id, terms in spec["report_text_terms"].items():
            hits, snippet = xbrl.find_terms(text, terms)
            out.append(
                {
                    "issuer": issuer_id,
                    "fiscal_year": row["fiscal_year"],
                    "item": term_id,
                    "hits": hits,
                    "snippet": snippet or "",
                }
            )
    return pd.DataFrame(out)


# --- ECB ---------------------------------------------------------------------------------------

ECB_SERIES = {
    "monthly_average": "M.GBP.EUR.SP00.A",
    "monthly_end_of_period": "M.GBP.EUR.SP00.E",
}


def ecb(client: Client) -> pd.DataFrame:
    rows = []
    for name, key in ECB_SERIES.items():
        text = client.ecb_series("EXR", key, "2020-01")
        records = list(csv.DictReader(text.splitlines()))
        rows.append(
            {
                "series": name,
                "key": f"EXR/{key}",
                "observations": len(records),
                "first_period": records[0]["TIME_PERIOD"] if records else "",
                "last_period": records[-1]["TIME_PERIOD"] if records else "",
                "last_value": records[-1]["OBS_VALUE"] if records else "",
            }
        )
    return pd.DataFrame(rows)


# --- summary -----------------------------------------------------------------------------------


def markdown_table(df: pd.DataFrame) -> str:
    header = "| " + " | ".join(map(str, df.columns)) + " |"
    rule = "| " + " | ".join("---" for _ in df.columns) + " |"
    body = ["| " + " | ".join(str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([header, rule, *body])


def write_summary(
    wide: pd.DataFrame, long: pd.DataFrame, decisions: pd.DataFrame, spec: dict
) -> None:
    lines = [
        "# M0 coverage summary",
        "",
        "Generated by `spikes/m0/coverage.py`. Status per line: **found** (standard IFRS tag), "
        "**extension** (company-specific tag, to review by hand), **missing**.",
        "",
        "## Go / no-go",
        "",
        markdown_table(decisions) if not decisions.empty else "_no data_",
        "",
        "## Coverage matrix",
        "",
    ]
    if not wide.empty:
        columns = ["issuer", "fiscal_year", "usable", "critical_gaps", *spec["lines"]]
        columns += list(spec["text_blocks"])
        legend = {"found": "✓", "extension": "ext", "missing": "–"}
        table = wide[columns].replace(legend)
        lines += [markdown_table(table), ""]
    lines += ["## Extension candidates to review", ""]
    ext = long[long["status"] == "extension"] if not long.empty else long
    if ext.empty:
        lines.append("_none_")
    else:
        lines.append(markdown_table(ext[["issuer", "fiscal_year", "line", "extension_candidates"]]))
    (OUT / "coverage.md").write_text("\n".join(lines) + "\n")


# --- main --------------------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("step", choices=["discover", "matrix", "text", "ecb", "all"])
    parser.add_argument("--offline", action="store_true", help="use the local cache only")
    args = parser.parse_args()

    client = Client(offline=args.offline)
    issuers = load_yaml(ISSUERS)["issuers"]
    spec = load_yaml(CONCEPTS)
    OUT.mkdir(parents=True, exist_ok=True)

    if args.step in ("discover", "all"):
        rows = choose_filings(client, discover(client, issuers, spec["first_fiscal_year"]))
        pd.DataFrame(rows).to_csv(FILINGS_CSV, index=False)
        print(f"wrote {FILINGS_CSV} ({len(rows)} filings)")

    rows = pd.read_csv(FILINGS_CSV, dtype=str, keep_default_na=False).to_dict("records")
    for row in rows:
        row["fiscal_year"] = int(row["fiscal_year"])

    if args.step in ("matrix", "all"):
        wide, long = build_matrix(client, rows, spec)
        decisions = go_no_go(wide, issuers, spec["min_years_for_go"])
        wide.to_csv(OUT / "coverage_matrix.csv", index=False)
        long.to_csv(OUT / "coverage_detail.csv", index=False)
        decisions.to_csv(OUT / "go_no_go.csv", index=False)
        write_summary(wide, long, decisions, spec)
        print(decisions.to_string(index=False))

    if args.step in ("text", "all"):
        text = report_text(client, rows, issuers, spec)
        text.to_csv(OUT / "report_text.csv", index=False)
        print(text[["issuer", "fiscal_year", "item", "hits"]].to_string(index=False))

    if args.step in ("ecb", "all"):
        rates = ecb(client)
        rates.to_csv(OUT / "ecb_series.csv", index=False)
        print(rates.to_string(index=False))


if __name__ == "__main__":
    main()
