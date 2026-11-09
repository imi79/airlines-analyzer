"""Draft every company's latest two years, and write what Imane reads (docs/m4/).

Order of work: the latest year of all nine companies, then the year before. Any ten drafts in
a row therefore cover all nine companies, which is what gate 2 asks.

    docs/m4/factsheets/<company>_FY<year>.md / .json   what the AI was allowed to use
    docs/m4/drafts/<company>_FY<year>.md               the draft as printed, with its checks
    docs/m4/drafts/<company>_FY<year>.json             the form as the AI filled it, per try
    docs/m4/drafts.md                                  summary and gate 2
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import duckdb

from tearsheet.config import DB_PATH, ROOT, Issuer, load_issuers
from tearsheet.extract import events as ev
from tearsheet.extract.documents import Document, from_report, supplied_documents
from tearsheet.ingest.client import Client
from tearsheet.llm import LLM
from tearsheet.narrative import score_sheet
from tearsheet.narrative.drafting import (
    MAX_RETRIES,
    PROMPT_VERSION,
    Outcome,
    draft_commentary,
    load_examples,
    rendered_text,
)
from tearsheet.narrative.factsheet import (
    FactSheet,
    add_events,
    as_text,
    build,
    load_figures,
    load_narrative,
    load_specs,
)
from tearsheet.narrative.verifier import Verifier
from tearsheet.store import db

OUT = ROOT / "docs" / "m4"
YEARS_DRAFTED = 2
GATE_RUN = 10  # gate 2: ten consecutive drafts across companies


@dataclass
class Sheets:
    drafted: list[FactSheet]  # in drafting order
    examples: list[FactSheet]  # the years the two example notes are written on


def build_sheets(db_path: Path = DB_PATH, years: int = YEARS_DRAFTED) -> Sheets:
    narrative = load_narrative()
    specs = load_specs(narrative)
    con = duckdb.connect(str(db_path), read_only=True)
    figures = load_figures(con, set(specs))
    con.close()
    issuers = load_issuers()
    latest = {
        i.id: max(f.fiscal_year for f in figures if f.issuer == i.id and f.value is not None)
        for i in issuers
    }
    drafted = [
        build(i, latest[i.id] - back, figures, specs, narrative)
        for back in range(years)
        for i in issuers
    ]
    by_id: dict[str, Issuer] = {i.id: i for i in issuers}
    examples = [
        build(by_id[ex["issuer"]], ex["fiscal_year"], figures, specs, narrative)
        for ex in load_examples()
    ]
    return Sheets(drafted, examples)


def run(
    llm: LLM,
    db_path: Path = DB_PATH,
    out: Path = OUT,
    only: set[str] | None = None,
) -> list[Outcome]:
    """Draft (or replay) every tearsheet; `only` limits live AI calls to some companies."""
    narrative = load_narrative()
    verifier = Verifier(narrative)
    sheets = build_sheets(db_path)
    recorded = LLM(offline=True)
    issuers = {i.id: i for i in load_issuers()}
    event_runs = []
    for sheet in sheets.drafted:
        use = llm if not only or sheet.issuer in only else recorded
        event_run = events_for(use, issuers[sheet.issuer], sheet, db_path, verifier)
        add_events(sheet, event_run.events)
        event_runs.append(event_run)
    write_events(event_runs, out)
    for sheet in sheets.drafted + sheets.examples:
        write_factsheet(sheet, narrative, out)
    write_examples(sheets.examples, narrative, out)
    outcomes = []
    for sheet in sheets.drafted:
        use = llm if not only or sheet.issuer in only else recorded
        outcome = draft_commentary(use, sheet, verifier, narrative)
        outcomes.append(outcome)
        write_draft(outcome, narrative, out)
    write_summary(outcomes, out)
    write_db(outcomes, db_path)
    write_events_db(event_runs, db_path)
    if out == OUT and sum(o.drafted for o in outcomes) >= score_sheet.DRAFTS:
        score_sheet.write(outcomes)
    return outcomes


# --- Events of the year (fix D) ------------------------------------------------------------


def report_document(issuer: Issuer, year: int, db_path: Path) -> Document | None:
    """The year's own annual report: the filing's report, else a PDF supplied by Imane."""
    con = duckdb.connect(str(db_path), read_only=True)
    row = con.execute(
        "SELECT filing_id, language, report_url, sha256 FROM filings "
        "WHERE issuer = ? AND fiscal_year = ? AND report_url IS NOT NULL",
        [issuer.id, year],
    ).fetchone()
    con.close()
    if row:
        filing_id, language, url, sha = row
        try:
            path = Client(offline=True).download(url, "report")
        except FileNotFoundError:
            return None
        return from_report(filing_id, issuer.id, year, language, path, url, sha)
    supplied = [d for d in supplied_documents(issuer.id) if d.fiscal_year == year]
    return supplied[0] if supplied else None


def events_for(llm: LLM, issuer: Issuer, sheet: FactSheet, db_path: Path, verifier):
    doc = report_document(issuer, sheet.fiscal_year, db_path)
    if doc is None:
        run = ev.EventsRun(issuer.id, sheet.fiscal_year, "-")
        run.error = "no report for this year in the local cache"
        return run
    return ev.read_events(llm, issuer, doc, sheet.period_label, verifier.numbers)


def write_events(runs: list, out: Path) -> None:
    md = [
        "# Events of the year, read from the reports",
        "",
        "Read by the AI (prompt `"
        + ev.PROMPT_VERSION
        + "`) and checked by code (decision 0018, fix D): the quote "
        "is in the report word for word, and the title and summary hold no number. Only checked "
        "events reach the fact sheets. Code cannot check that the English summary is a fair "
        "reading of the quote: please read the quotes.",
        "",
    ]
    for run in runs:
        md += [f"## {run.issuer} FY{run.fiscal_year} (`{run.document}`)", ""]
        if run.error:
            md += [f"_{run.error}_", ""]
            continue
        if not run.events:
            md += ["_No event recorded._", ""]
        for e in run.events:
            mark = "" if e.verified else " \\* (not checked: " + "; ".join(e.failures) + ")"
            md += [f"- **{e.title}** ({e.topic}, `{e.id}`){mark}. {e.summary}",
                   f"  > {e.quote} ({e.location or 'not found'})"]  # fmt: skip
        md.append("")
    (out / "events.md").write_text("\n".join(md))


def write_events_db(runs: list, db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    db.ensure_draft_tables(con)
    con.execute("DELETE FROM events")
    for run in runs:
        r = run.result
        for e in run.events:
            con.execute(
                "INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [e.issuer, e.fiscal_year, e.id, e.topic, e.title, e.summary, e.quote, e.location,
                 e.document, "verified" if e.verified else "unverified",
                 json.dumps(e.failures, ensure_ascii=False), r.model if r else None,
                 r.prompt_version if r else None, r.request_hash if r else None],
            )  # fmt: skip
    con.close()


# --- Pages ---------------------------------------------------------------------------------


def write_factsheet(sheet: FactSheet, narrative: dict, out: Path) -> None:
    folder = out / "factsheets"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{sheet.key}.json").write_text(sheet.to_json())
    (folder / f"{sheet.key}.md").write_text(as_text(sheet, narrative))


def write_examples(sheets: list[FactSheet], narrative: dict, out: Path) -> None:
    """The two example notes as printed, for Imane to rewrite in her own words."""
    md = [
        "# The two example notes, as printed",
        "",
        "These teach the AI the house style (decision 0016). I drafted them from the fact "
        "sheets; please rewrite them in your own words, as you would write a sell-side credit "
        "note. Plain text is fine: edit the sentences below, keep each figure where it is, and "
        "I will turn your text back into blanks. Files: `src/tearsheet/narrative/examples/`.",
        "",
    ]
    for sheet, example in zip(sheets, load_examples(), strict=True):
        md += [f"## {sheet.name}, {sheet.period_label}", ""]
        rendered = sheet.rendered()
        for name, sentences in example["sections"].items():
            md += [f"**{narrative['sections'][name]['title']}**", ""]
            bullet = "- " if name == "watch_items" else ""
            md += [bullet + rendered_text(" ".join(x["text"].split()), rendered)
                   for x in sentences]  # fmt: skip
            md.append("")
    (out / "example_notes.md").write_text("\n".join(md))


def _tokens(outcome: Outcome) -> tuple[int, int]:
    results = [a.result for a in outcome.attempts if a.result is not None]
    return sum(r.usage.input_tokens for r in results), sum(r.usage.output_tokens for r in results)


def write_draft(outcome: Outcome, narrative: dict, out: Path) -> None:
    sheet = outcome.sheet
    folder = out / "drafts"
    folder.mkdir(parents=True, exist_ok=True)
    md = [f"# {sheet.name}, {sheet.period_label}: draft commentary", ""]
    if not outcome.drafted:
        md += [f"**{outcome.not_run}**", ""]
        (folder / f"{sheet.key}.md").write_text("\n".join(md))
        return
    first = outcome.attempts[0].result
    tokens_in, tokens_out = _tokens(outcome)
    verdict = (
        "passed the verifier"
        if outcome.passed
        else "**needs manual editing** (some sections still rejected after two retries)"
    )
    md += [
        f"Status: {verdict}. First try: {'passed' if outcome.first_try_passed else 'rejected'}; "
        f"tries: {len(outcome.attempts)}. Model {first.model if first else '-'}, prompt "
        f"`{PROMPT_VERSION}`, fact sheet `{outcome.input_hash()[:12]}` "
        f"([fact sheet](../factsheets/{sheet.key}.md)). Tokens: {tokens_in:,} in, "
        f"{tokens_out:,} out.",
        "",
        "Every figure below was written by code from the fact sheet; the AI wrote the words.",
        "",
    ]
    rendered = sheet.rendered()
    for name, sentences in outcome.sections.items():
        title = narrative["sections"][name]["title"]
        flag = "" if outcome.status.get(name) == "passed" else " (needs manual editing)"
        md += [f"## {title}{flag}", ""]
        bullet = "- " if name == "watch_items" else ""
        md += [bullet + rendered_text(s.text, rendered) for s in sentences]
        cited = [r.id for s in sentences for r in s.facts if r.id in sheet.items
                 and sheet.items[r.id].kind == "event"]  # fmt: skip
        for eid in dict.fromkeys(cited):
            md.append(f"\n> Event `{eid}`: {sheet.items[eid].note}")
        for e in outcome.errors.get(name, []):
            md.append(f"\n> verifier: {e}")
        for text, why in outcome.removed.get(name, []):
            md.append(f"\n> removed by the verifier (still broke a rule after two retries): "
                      f"\"{text}\" ({'; '.join(why)})")  # fmt: skip
        md.append("")
    md += ["## Analyst view", "", "_Left for the analyst: never drafted._", ""]
    md += ["## How each try went", "", "| Try | Sections asked | Verifier | Tokens |",
           "| --- | --- | --- | --- |"]  # fmt: skip
    for a in outcome.attempts:
        n_err = len(a.report.errors) if a.report else 0
        verdict = a.error or ("passed" if a.report and a.report.ok else f"{n_err} errors")
        tokens = (
            f"{a.result.usage.input_tokens:,} / {a.result.usage.output_tokens:,}"
            if a.result
            else "-"
        )
        md.append(f"| {a.number} | {', '.join(a.sections)} | {verdict} | {tokens} |")
    md += ["", "### Errors found, by try", ""]
    for a in outcome.attempts:
        if a.report and a.report.errors:
            md += [f"Try {a.number}:", ""] + [f"- {e}" for e in a.report.errors] + [""]
    md += ["### Text with blanks (as the AI wrote it)", ""]
    for name, sentences in outcome.sections.items():
        md += [f"`{name}`", ""] + [f"- {s.text}" for s in sentences] + [""]
    (folder / f"{sheet.key}.md").write_text("\n".join(md))
    record = {
        "issuer": sheet.issuer,
        "fiscal_year": sheet.fiscal_year,
        "prompt_version": PROMPT_VERSION,
        "input_hash": outcome.input_hash(),
        "status": outcome.status,
        "removed": outcome.removed,
        "attempts": [
            {
                "try": a.number,
                "sections": a.sections,
                "request_hash": a.result.request_hash if a.result else None,
                "model": a.result.model if a.result else None,
                "draft": _in_order(a.draft.to_dict(), narrative) if a.draft else None,
                "errors": [str(e) for e in a.report.errors] if a.report else [],
                "error": a.error,
            }
            for a in outcome.attempts
        ],
    }
    (folder / f"{sheet.key}.json").write_text(
        json.dumps(record, indent=1, ensure_ascii=False) + "\n"
    )


def _in_order(sections: dict, narrative: dict) -> dict:
    """Sections in tearsheet order: a live answer and its replay give the same file."""
    order = list(narrative["sections"])
    return dict(sorted(sections.items(), key=lambda kv: order.index(kv[0]) if kv[0] in order
                       else len(order)))  # fmt: skip


def gate2(outcomes: list[Outcome]) -> tuple[int, set[str], bool]:
    """Longest run of consecutive passing drafts, the companies it covers, and the verdict."""
    best: list[Outcome] = []
    current: list[Outcome] = []
    for o in outcomes:
        current = current + [o] if o.passed and o.numbers_outside_blanks == 0 else []
        if len(current) > len(best):
            best = current
    companies = {o.sheet.issuer for o in best}
    all_companies = {o.sheet.issuer for o in outcomes}
    return len(best), companies, len(best) >= GATE_RUN and companies == all_companies


def write_summary(outcomes: list[Outcome], out: Path) -> None:
    drafted = [o for o in outcomes if o.drafted]
    run, companies, ok = gate2(outcomes)
    first = sum(o.first_try_passed for o in drafted)
    passed = sum(o.passed for o in drafted)
    tokens = [_tokens(o) for o in drafted]
    md = [
        "# M4 drafts: summary and gate 2",
        "",
        "Generated by `tearsheet draft` (or replayed by `tearsheet all`). Drafting order: the "
        "latest year of every company, then the year before, so any ten drafts in a row cover "
        f"all nine companies. Prompt `{PROMPT_VERSION}`; up to {MAX_RETRIES} retries per draft.",
        "",
        f"- **Drafts:** {len(drafted)} of {len(outcomes)} drafted; {passed} passed the verifier "
        f"(after retries), {first} at the first try "
        f"({first / len(drafted):.0%})."
        if drafted
        else "- **Drafts:** none yet.",
        f"- **Gate 2** (ten consecutive drafts across companies with zero unreferenced numbers): "
        f"longest run {run}, covering {len(companies)} companies: "
        f"**{'passed' if ok else 'not passed'}**.",
        f"- **Tokens:** {sum(t[0] for t in tokens):,} in, {sum(t[1] for t in tokens):,} out.",
        "",
        "| # | Company and year | Verifier | First try | Tries | Sentences removed | "
        "Numbers outside blanks | Page |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n, o in enumerate(outcomes, start=1):
        s = o.sheet
        if not o.drafted:
            md.append(f"| {n} | {s.name} {s.period_label} | not drafted | | | | | |")
            continue
        verdict = "passed" if o.passed else "needs manual editing"
        md.append(
            f"| {n} | {s.name} {s.period_label} | {verdict} | "
            f"{'yes' if o.first_try_passed else 'no'} | {len(o.attempts)} | "
            f"{o.sentences_removed} | {o.numbers_outside_blanks} | [draft](drafts/{s.key}.md) |"
        )
    md.append("")
    (out / "drafts.md").write_text("\n".join(md))


# --- Database ------------------------------------------------------------------------------


def write_db(outcomes: list[Outcome], db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    db.ensure_draft_tables(con)
    con.execute("DELETE FROM drafts")
    con.execute("DELETE FROM runs")
    hashes = con.execute("SELECT issuer, fiscal_year, filing_id, sha256 FROM filings").fetchall()
    for o in outcomes:
        if not o.drafted:
            continue
        s = o.sheet
        results = [a.result for a in o.attempts if a.result is not None]
        last = results[-1] if results else None
        for name, sentences in o.sections.items():
            report = json.dumps([str(e) for e in o.errors.get(name, [])], ensure_ascii=False)
            for n, sentence in enumerate(sentences, start=1):
                facts = [{"id": r.id, "claims": list(r.claims)} for r in sentence.facts]
                con.execute(
                    "INSERT INTO drafts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [
                        s.issuer,
                        s.fiscal_year,
                        name,
                        n,
                        sentence.text,
                        rendered_text(sentence.text, s.rendered()),
                        json.dumps(facts, ensure_ascii=False),
                        o.status.get(name),
                        last.model if last else None,
                        PROMPT_VERSION,
                        o.input_hash(),
                        report,
                        len(o.attempts),
                    ],
                )
        used = {
            fid: sha
            for issuer, year, fid, sha in hashes
            if issuer == s.issuer and year in (s.fiscal_year, s.fiscal_year - 1)
        }
        costs = [r.cost_usd for r in results if r.cost_usd is not None]
        con.execute(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                s.issuer,
                s.fiscal_year,
                json.dumps(dict(sorted(used.items()))),
                last.provider if last else None,
                last.model if last else None,
                PROMPT_VERSION,
                o.input_hash(),
                len(results),
                sum(r.usage.input_tokens for r in results),
                sum(r.usage.output_tokens for r in results),
                sum(costs) if costs else None,
                o.first_try_passed,
                o.passed,
                max((r.extra.get("recorded_at") or "" for r in results), default=None),
            ],
        )
    con.close()
