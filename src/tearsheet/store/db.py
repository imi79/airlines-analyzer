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

-- Every line of every form the AI filled in (M3), with the outcome of the checks.
CREATE TABLE extraction_log (
    issuer        VARCHAR NOT NULL,
    document      VARCHAR NOT NULL,
    document_year INTEGER NOT NULL,
    fiscal_year   INTEGER,
    item          VARCHAR,
    outcome       VARCHAR NOT NULL,  -- verified unverified not_found invalid not_run error
    value         DECIMAL(38, 12),   -- full units, reporting currency (after conversion)
    printed       VARCHAR,
    scale         VARCHAR,
    currency      VARCHAR,
    quote         VARCHAR,
    table_header  VARCHAR,
    location      VARCHAR,           -- found by code in the report
    scope         VARCHAR,
    reasons       VARCHAR,           -- JSON list: checks failed, or why not found
    notes         VARCHAR            -- JSON list
);

-- Every AI request (M3), for the run manifest: model, prompt version, tokens, cost.
CREATE TABLE llm_calls (
    issuer         VARCHAR NOT NULL,
    document       VARCHAR NOT NULL,
    job            VARCHAR NOT NULL,
    provider       VARCHAR,
    model          VARCHAR,
    prompt_version VARCHAR,
    request_hash   VARCHAR,
    input_tokens   INTEGER,
    output_tokens  INTEGER,
    cost_usd       DECIMAL(18, 6),
    from_record    BOOLEAN,
    passage_chars  INTEGER,
    error          VARCHAR
);
"""

DRAFT_TABLES = """
-- The drafted commentary (M4): one row per sentence, as the AI wrote it (with blanks) and as
-- printed (blanks filled by code), with the verifier's verdict.
CREATE TABLE drafts (
    issuer          VARCHAR NOT NULL,
    fiscal_year     INTEGER NOT NULL,
    section         VARCHAR NOT NULL,
    sentence        INTEGER NOT NULL,
    text_blanks     VARCHAR NOT NULL,  -- with {{id}} blanks
    text_rendered   VARCHAR NOT NULL,
    facts           VARCHAR NOT NULL,  -- JSON: ids used and the claims made on each
    status          VARCHAR NOT NULL,  -- passed | needs_manual_editing (the whole section)
    model           VARCHAR,
    prompt_version  VARCHAR,
    input_hash      VARCHAR NOT NULL,  -- fingerprint of the fact sheet
    verifier_report VARCHAR NOT NULL,  -- JSON list of the section's remaining errors
    attempts        INTEGER NOT NULL
);

-- One manifest per drafted tearsheet (M4): filings, model, prompt version, tokens, cost.
CREATE TABLE runs (
    issuer          VARCHAR NOT NULL,
    fiscal_year     INTEGER NOT NULL,
    filing_hashes   VARCHAR NOT NULL,  -- JSON: filing id -> sha256, for the years used
    provider        VARCHAR,
    model           VARCHAR,
    prompt_version  VARCHAR,
    input_hash      VARCHAR NOT NULL,
    calls           INTEGER NOT NULL,
    input_tokens    INTEGER NOT NULL,
    output_tokens   INTEGER NOT NULL,
    cost_usd        DECIMAL(18, 6),
    first_try_ok    BOOLEAN,
    passed          BOOLEAN,
    recorded_at     VARCHAR            -- when the last AI answer was recorded
);

-- Events of the year read from the reports (M4, decision 0018, fix D).
CREATE TABLE events (
    issuer          VARCHAR NOT NULL,
    fiscal_year     INTEGER NOT NULL,
    event_id        VARCHAR NOT NULL,
    topic           VARCHAR NOT NULL,
    title           VARCHAR NOT NULL,
    summary         VARCHAR NOT NULL,
    quote           VARCHAR NOT NULL,
    location        VARCHAR,           -- found by code in the report
    document        VARCHAR NOT NULL,
    status          VARCHAR NOT NULL,  -- verified | unverified
    reasons         VARCHAR,           -- JSON list
    model           VARCHAR,
    prompt_version  VARCHAR,
    request_hash    VARCHAR
);
"""
SCHEMA += DRAFT_TABLES

# Half-year and last-twelve-months figures (M10, decision 0025). Kept in tables of their own:
# the fiscal-year figures, their keys and everything built from them stay exactly as they are.
INTERIM_TABLES = """
CREATE TABLE interim_reports (
    issuer           VARCHAR NOT NULL,
    report_id        VARCHAR NOT NULL,
    period_end       DATE NOT NULL,     -- the half-year date
    base_fiscal_year INTEGER NOT NULL,  -- the last full fiscal year LTM is built on
    h1_label         VARCHAR NOT NULL,
    ltm_label        VARCHAR NOT NULL,
    document         VARCHAR NOT NULL,
    file             VARCHAR NOT NULL,
    sha256           VARCHAR NOT NULL,
    url              VARCHAR,
    language         VARCHAR,
    audit            VARCHAR,           -- unaudited
    read_by          VARCHAR,           -- ai | hand
    provider         VARCHAR,
    model            VARCHAR,
    prompt_version   VARCHAR,
    request_hash     VARCHAR,
    input_tokens     INTEGER,
    output_tokens    INTEGER,
    from_record      BOOLEAN,
    error            VARCHAR,
    columns          VARCHAR            -- JSON: per statement, how the columns were named
);

CREATE TABLE interim_facts (
    issuer       VARCHAR NOT NULL,
    period       VARCHAR NOT NULL,     -- H1 | H1_prior | LTM
    period_end   DATE NOT NULL,
    concept      VARCHAR NOT NULL,     -- statement line, or metric id for LTM metrics
    value        DECIMAL(38, 12) NOT NULL,
    decimals     INTEGER,
    currency     VARCHAR NOT NULL,
    source_type  VARCHAR NOT NULL,     -- extracted | manual | computed
    source_ref   VARCHAR NOT NULL,     -- JSON: rows and checks, or the parts of the LTM sum
    status       VARCHAR NOT NULL,     -- verified | unverified | overridden
    note         VARCHAR,
    warnings     VARCHAR
);

-- Lines and metrics with no half-year or LTM value, and why.
CREATE TABLE interim_gaps (
    issuer   VARCHAR NOT NULL,
    period   VARCHAR NOT NULL,
    concept  VARCHAR NOT NULL,
    reason   VARCHAR NOT NULL
);
"""
SCHEMA += INTERIM_TABLES


def ensure_draft_tables(con) -> None:
    """The M4 tables, in a database built before they existed."""
    con.execute(DRAFT_TABLES.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS"))


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
    if fact.ref is not None:  # extracted: document, location, quote, model, checks
        return json.dumps(fact.ref, ensure_ascii=False, default=str)
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


def write_extraction(con, extraction) -> None:
    """The extraction log and the AI calls for one issuer (an IssuerExtraction)."""
    issuer = extraction.issuer.id
    rows, calls = [], []
    final = {
        (c.doc.doc_id, c.fiscal_year, c.item): c for c in extraction.candidates
    }  # after cross-checks and reviews
    for run in extraction.runs:
        doc = run.doc
        r = run.result
        calls.append(
            (
                issuer,
                doc.doc_id,
                "extraction",
                r.provider if r else None,
                r.model if r else None,
                r.prompt_version if r else None,
                r.request_hash if r else None,
                r.usage.input_tokens if r else None,
                r.usage.output_tokens if r else None,
                r.cost_usd if r else None,
                r.cached if r else None,
                run.passage_chars,
                run.error,
            )
        )
        if run.error:
            outcome = "not_run" if run.error.startswith("not extracted yet") else "error"
            rows.append(_short_row(issuer, doc.doc_id, doc.fiscal_year, outcome, run.error))
        for msg in run.invalid:
            rows.append(_short_row(issuer, doc.doc_id, doc.fiscal_year, "invalid", msg))
        for raw in run.not_found:
            rows.append(
                _short_row(
                    issuer,
                    doc.doc_id,
                    doc.fiscal_year,
                    "not_found",
                    raw.comment or "",
                    raw.fiscal_year,
                    raw.item,
                    raw.scope,
                )  # fmt: skip
            )
        for f in run.figures:
            c = final.get((doc.doc_id, f.fiscal_year, f.item))
            status = c.status if c else ("verified" if f.verified else "unverified")
            reasons = list(c.failures) if c else list(f.failures)
            notes = list(c.notes) if c else list(f.notes)
            value = c.value if c and len(c.figures) == 1 else f.value
            rows.append(
                (
                    issuer,
                    doc.doc_id,
                    doc.fiscal_year,
                    f.fiscal_year,
                    f.item,
                    "verified" if status in ("verified", "overridden") else "unverified",
                    value,
                    f.raw.printed_value,
                    f.raw.scale,
                    f.currency,
                    f.raw.quote,
                    f.raw.table_header,
                    f.location,
                    f.raw.scope,
                    json.dumps(reasons, ensure_ascii=False),
                    json.dumps(notes, ensure_ascii=False),
                )
            )
    for doc_id, year, reason in extraction.skipped:
        rows.append(_short_row(issuer, doc_id, year, "not_run", reason))
    if rows:
        con.executemany(f"INSERT INTO extraction_log VALUES ({', '.join('?' * 16)})", rows)
    if calls:
        con.executemany(f"INSERT INTO llm_calls VALUES ({', '.join('?' * 13)})", calls)


def _short_row(issuer, doc_id, doc_year, outcome, reason, year=None, item=None, scope=None):
    """An extraction log row without a value: not run, error, invalid line or not found."""
    no_value = (None,) * 7  # value, printed, scale, currency, quote, header, location
    reasons = json.dumps([reason], ensure_ascii=False)
    return (issuer, doc_id, doc_year, year, item, outcome, *no_value, scope, reasons, None)


def write_maturity(con, issuer: str, runs) -> None:
    """The AI calls that read the maturity tables (M8), for the run manifest."""
    calls = []
    for run in runs:
        r = run.result
        if r is None and run.error is None:
            continue  # entered by hand: no AI call
        calls.append(
            (
                issuer,
                run.doc.doc_id,
                "maturity",
                r.provider if r else None,
                r.model if r else None,
                r.prompt_version if r else None,
                r.request_hash if r else None,
                r.usage.input_tokens if r else None,
                r.usage.output_tokens if r else None,
                r.cost_usd if r else None,
                r.cached if r else None,
                None,
                run.error,
            )
        )
    if calls:
        con.executemany(
            "INSERT INTO llm_calls VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", calls
        )


def write_interim(con, load, currency: str, units: dict[str, str]) -> None:
    """One company's half-year report, its H1 lines, LTM lines and LTM metrics (an
    InterimLoad of metrics/ltm.py)."""
    report, run = load.report, load.run
    r = run.result
    columns = {
        kind: {"count": c.count, "labels": c.labels, "how": c.how, "failures": c.failures}
        for kind, c in run.columns.items()
    }
    con.execute(
        f"INSERT INTO interim_reports VALUES ({', '.join('?' * 22)})",
        (
            report.issuer, report.id, report.period_end, report.base_fiscal_year,
            report.h1_label, report.ltm_label, report.document, report.file, report.sha256,
            report.url, report.language, report.audit, report.read_by,
            r.provider if r else None, r.model if r else None,
            r.prompt_version if r else None, r.request_hash if r else None,
            r.usage.input_tokens if r else None, r.usage.output_tokens if r else None,
            r.cached if r else None, run.error, json.dumps(columns, ensure_ascii=False),
        ),
    )  # fmt: skip
    rows, gaps = [], []
    for f in load.h1 + load.ltm:
        rows.append(
            (
                f.issuer, f.rule_source, f.period_end, f.line, f.value, f.decimals, f.currency,
                f.source_type, json.dumps(f.ref, ensure_ascii=False, default=str), f.status,
                f.note, json.dumps(list(f.warnings), ensure_ascii=False) if f.warnings else None,
            )
        )  # fmt: skip
    for res in load.metrics:
        if res.value is None:
            gaps.append((res.issuer, "LTM", res.metric, res.reason))
            continue
        ref = json.dumps(
            {
                "formula": res.metric,
                "inputs": [
                    {"name": i.name, "value": str(i.value), "source": i.source} for i in res.inputs
                ],
            },
            ensure_ascii=False,
        )
        unit = currency if units[res.metric] == "amount" else units[res.metric]
        rows.append(
            (res.issuer, "LTM", res.period_end, res.metric, res.value, None, unit, "computed",
             ref, res.status, res.note, None)
        )  # fmt: skip
    for line, why in run.not_found.items():
        gaps.append((report.issuer, "H1", line, why))
    for line, why in load.gaps.items():
        gaps.append((report.issuer, "LTM", line, why))
    if rows:
        con.executemany(f"INSERT INTO interim_facts VALUES ({', '.join('?' * 12)})", rows)
    if gaps:
        con.executemany("INSERT INTO interim_gaps VALUES (?, ?, ?, ?)", gaps)
