"""DuckDB schema and writes.

The database is rebuilt from scratch on every load, in a fixed order, so the same filings
always give the same database.
"""

from __future__ import annotations

import json
from pathlib import Path

import duckdb

from tearsheet.ingest.filings import Filing
from tearsheet.ingest.xbrl_json import Fact
from tearsheet.normalize.mapper import Gap, MappedFact

SCHEMA = """
CREATE TABLE filings (
    filing_id     VARCHAR PRIMARY KEY,
    issuer        VARCHAR NOT NULL,
    fiscal_year   INTEGER NOT NULL,
    period_end    DATE NOT NULL,
    origin        VARCHAR NOT NULL,   -- filings.xbrl.org, or company website (loaded by hand)
    sha256        VARCHAR,
    json_url      VARCHAR,
    viewer_url    VARCHAR,
    report_url    VARCHAR,
    package_url   VARCHAR,
    error_count   INTEGER,
    date_added    VARCHAR,
    language      VARCHAR,
    choice_reason VARCHAR
);

-- Every number tagged in the filings used, exactly as tagged.
CREATE TABLE raw_facts (
    filing_id      VARCHAR NOT NULL,
    fact_id        VARCHAR NOT NULL,
    concept        VARCHAR NOT NULL,  -- ifrs-full:... or ext:... (company concept)
    tagged_concept VARCHAR NOT NULL,
    value          DECIMAL(38, 6) NOT NULL,
    decimals       INTEGER,           -- NULL means exact
    unit           VARCHAR,
    period_start   DATE,              -- NULL for balance-sheet (instant) facts
    period_end     DATE NOT NULL,
    dimensions     VARCHAR            -- JSON; empty for facts without breakdown
);

-- Canonical statement lines, with provenance.
CREATE TABLE facts (
    issuer       VARCHAR NOT NULL,
    fiscal_year  INTEGER NOT NULL,
    period_end   DATE NOT NULL,
    concept      VARCHAR NOT NULL,    -- canonical line id, or metric id for computed metrics
    value        DECIMAL(38, 12) NOT NULL, -- canonical sign: costs and outflows positive
    value_tagged DECIMAL(38, 12) NOT NULL, -- as tagged (sum of parts if several)
    decimals     INTEGER,
    currency     VARCHAR NOT NULL,    -- reporting currency; "x" or "pct" for ratios
    source_type  VARCHAR NOT NULL,    -- tagged | computed | extracted | manual
    source_ref   VARCHAR NOT NULL,    -- JSON: filing, hash, concepts, fact ids, rule
    status       VARCHAR NOT NULL,    -- verified | unverified | overridden
    is_primary   BOOLEAN NOT NULL,    -- the value the tearsheet uses (latest restated)
    restated     BOOLEAN NOT NULL,    -- another filing gives a different value for the year
    comparative  BOOLEAN NOT NULL,    -- read from the prior-year column of a later filing
    filing_id    VARCHAR NOT NULL,
    note         VARCHAR,
    footnote     VARCHAR,
    warnings     VARCHAR              -- JSON list
);

-- Lines with no value for a year, and why.
CREATE TABLE gaps (
    issuer            VARCHAR NOT NULL,
    fiscal_year       INTEGER NOT NULL,
    concept           VARCHAR NOT NULL,
    reason            VARCHAR NOT NULL,
    counts_as_missing BOOLEAN NOT NULL
);
"""


def create(path: Path) -> duckdb.DuckDBPyConnection:
    path.parent.mkdir(parents=True, exist_ok=True)
    for stale in (path, path.with_suffix(path.suffix + ".wal")):
        stale.unlink(missing_ok=True)
    con = duckdb.connect(str(path))
    con.execute(SCHEMA)
    return con


def write_filings(con, filings: list[Filing]) -> None:
    con.executemany(
        "INSERT INTO filings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                f.filing_id,
                f.issuer,
                f.fiscal_year,
                f.period_end,
                f.origin,
                f.sha256,
                f.json_url,
                f.viewer_url,
                f.report_url,
                f.package_url,
                f.error_count,
                f.date_added,
                f.language,
                f.choice_reason,
            )
            for f in filings
        ],
    )


def write_raw_facts(con, filing_id: str, facts: list[Fact]) -> None:
    con.executemany(
        "INSERT INTO raw_facts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                filing_id,
                f.fact_id,
                f.concept,
                f.tagged_concept,
                f.value,
                f.decimals,
                f.unit,
                f.start,
                f.end,
                json.dumps(dict(f.dimensions)) if f.dimensions else "",
            )
            for f in sorted(facts, key=lambda f: f.fact_id)
        ],
    )


def source_ref(fact: MappedFact, sha256: str | None) -> str:
    return json.dumps(
        {
            "filing_id": fact.filing_id,
            "sha256": sha256,
            "concepts": list(fact.concepts),
            "fact_ids": list(fact.fact_ids),
            "rule": fact.rule_source,
            "sign": fact.sign,
        },
        ensure_ascii=False,
    )


def write_facts(con, facts: list[MappedFact], hashes: dict[str, str | None]) -> None:
    con.executemany(
        "INSERT INTO facts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                f.issuer,
                f.fiscal_year,
                f.period_end,
                f.line,
                f.value,
                f.value_tagged,
                f.decimals,
                f.currency,
                f.source_type,
                source_ref(f, hashes.get(f.filing_id)),
                f.status,
                f.primary,
                f.restated,
                f.comparative,
                f.filing_id,
                f.note,
                f.footnote,
                json.dumps(list(f.warnings), ensure_ascii=False) if f.warnings else None,
            )
            for f in facts
        ],
    )


def write_metrics(con, results, currency: str, units: dict[str, str]) -> None:
    """Computed metrics go to `facts` (values) and `gaps` (missing, n.m. or awaiting M3)."""
    rows, gaps = [], []
    for r in results:
        if r.value is None:
            gaps.append((r.issuer, r.fiscal_year, r.metric, r.reason, r.kind == "missing"))
            continue
        ref = json.dumps(
            {
                "formula": r.metric,
                "inputs": [
                    {"name": i.name, "value": str(i.value), "source": i.source} for i in r.inputs
                ],
            },
            ensure_ascii=False,
        )
        unit_currency = currency if units[r.metric] == "amount" else units[r.metric]
        rows.append(
            (
                r.issuer,
                r.fiscal_year,
                r.period_end,
                r.metric,
                r.value,
                r.value,
                None,
                unit_currency,
                "computed",
                ref,
                r.status,
                True,
                False,
                False,
                "",
                r.note,
                None,
                None,
            )
        )
    con.executemany(
        "INSERT INTO facts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows
    )
    con.executemany("INSERT INTO gaps VALUES (?, ?, ?, ?, ?)", gaps)


def write_gaps(con, gaps: list[Gap]) -> None:
    con.executemany(
        "INSERT INTO gaps VALUES (?, ?, ?, ?, ?)",
        [(g.issuer, g.fiscal_year, g.line, g.reason, g.counts_as_missing) for g in gaps],
    )
