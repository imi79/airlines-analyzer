"""Rebuild the recorded fixtures and golden files from the local cache.

    uv run python -m tests.fixtures.build

Each fixture is a trimmed copy of a real filing: only the facts the mappings use (no
breakdowns, no text). The golden files are the mapped statement lines per issuer. Rebuild
them only on purpose (for example after adding an override) and review the diff.
"""

from __future__ import annotations

import csv
import gzip
import json
from dataclasses import asdict
from pathlib import Path

from tearsheet.config import load_issuers
from tearsheet.ingest.client import Client
from tearsheet.ingest.filings import choose, list_filings
from tearsheet.ingest.manual import manual_filings
from tearsheet.ingest.manual_figures import manual_figures
from tearsheet.ingest.xbrl_json import canonical_concept, parse_report
from tearsheet.metrics.engine import compute
from tearsheet.normalize.mapper import consolidate, load_mapping, map_report

HERE = Path(__file__).parent
FIXTURES = HERE / "filings"
GOLDEN = HERE.parent / "golden"
GOLDEN_COLUMNS = ["fiscal_year", "line", "value", "concepts", "rule", "comparative", "restated"]
METRIC_COLUMNS = ["fiscal_year", "metric", "kind", "value", "reason"]


def _mapped_concepts(mapping) -> set[str]:
    concepts = set()
    for line in mapping.lines.values():
        for rule in line.rules:
            concepts.update(rule.concepts + rule.add_if_tagged + rule.subtract)
    return concepts


def trim(document: dict, keep: set[str]) -> dict:
    namespaces = document.get("documentInfo", {}).get("namespaces", {})
    facts = {}
    for fact_id, raw in document.get("facts", {}).items():
        dims = raw.get("dimensions", {})
        concept = dims.get("concept", "")
        extra = set(dims) - {"concept", "entity", "period", "unit", "language", "noteId"}
        if not extra and dims.get("unit") and canonical_concept(concept, namespaces) in keep:
            facts[fact_id] = raw
    return {"documentInfo": {"namespaces": namespaces}, "facts": facts}


def plain(value) -> str:
    """Decimal as plain text without trailing zeros: 3728000000, 55527.6."""
    text = f"{value:f}"
    return text.rstrip("0").rstrip(".") if "." in text else text


def golden_rows(facts) -> list[dict]:
    return [
        {
            "fiscal_year": f.fiscal_year,
            "line": f.line,
            "value": plain(f.value),
            "concepts": " + ".join(f.concepts),
            "rule": f.rule_source,
            "comparative": f.comparative,
            "restated": f.restated,
        }
        for f in facts
        if f.primary
    ]


def metric_rows(issuer, mapped, filings, mapping) -> list[dict]:
    """Metrics from the tagged facts plus the figures entered by hand (config/manual_figures)."""
    hand_filings, hand_facts, _ = manual_figures(issuer)
    facts, _ = consolidate(issuer, mapped + hand_facts, filings + hand_filings, mapping)
    return [
        {
            "fiscal_year": r.fiscal_year,
            "metric": r.metric,
            "kind": r.kind,
            "value": "" if r.value is None else f"{r.value:.6f}",
            "reason": r.reason or "",
        }
        for r in compute(issuer, facts)
    ]


def main() -> None:
    client = Client(offline=True)
    GOLDEN.mkdir(parents=True, exist_ok=True)
    for issuer in load_issuers():
        mapping = load_mapping(issuer.id)
        keep = _mapped_concepts(mapping)
        filings = choose(client, list_filings(client, issuer) + manual_filings(issuer))
        folder = FIXTURES / issuer.id
        folder.mkdir(parents=True, exist_ok=True)
        register = []
        mapped = []
        for filing in filings:
            if filing.local_json:
                raw = json.loads(gzip.decompress(Path(filing.local_json).read_bytes()))
            else:
                raw = json.loads(client.download(filing.json_url, "xbrl-json").read_text())
            trimmed = trim(raw, keep)
            name = f"{filing.filing_id}.json.gz"
            (folder / name).write_bytes(
                gzip.compress(json.dumps(trimmed, sort_keys=True).encode(), mtime=0)
            )
            record = asdict(filing)
            record["period_end"] = filing.period_end.isoformat()
            record["local_json"] = name
            register.append(record)
            mapped.extend(map_report(issuer, filing, parse_report(trimmed), mapping))
        (folder / "filings.json").write_text(json.dumps(register, indent=1, sort_keys=True) + "\n")
        facts, _ = consolidate(issuer, mapped, filings, mapping)
        with (GOLDEN / f"{issuer.id}.csv").open("w", newline="") as out:
            writer = csv.DictWriter(out, GOLDEN_COLUMNS)
            writer.writeheader()
            writer.writerows(golden_rows(facts))
        (GOLDEN / "metrics").mkdir(exist_ok=True)
        rows = metric_rows(issuer, mapped, filings, mapping)
        with (GOLDEN / "metrics" / f"{issuer.id}.csv").open("w", newline="") as out:
            writer = csv.DictWriter(out, METRIC_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        print(
            f"{issuer.id}: {len(filings)} filings, {len(golden_rows(facts))} golden lines, "
            f"{len(rows)} metric results"
        )


if __name__ == "__main__":
    main()
