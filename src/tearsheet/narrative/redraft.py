"""M8 redraft (decision 0022): "Liquidity and funding" and "Watch items" with prompt draft-v8.

The fact sheet now holds the M8 figures (cash flow after leases, debt due within one and two
years, ratings where reviewed). Only the two sections that use them are redrafted; the other
four keep the draft-v7 text Imane accepted in M4. Every section of the merged note, kept or
new, is checked again by the verifier against the new fact sheet before it reaches the page.

    docs/m8/factsheets/<company>_FY<year>.md / .json   the new fact sheet
    docs/m8/drafts/<company>_FY<year>.md               the merged note, section by section
    docs/m8/drafts.md                                  summary and the ten-in-a-row check
"""

from __future__ import annotations

import copy
from pathlib import Path

import duckdb

from tearsheet.config import DB_PATH, ROOT, load_issuers
from tearsheet.llm import LLM
from tearsheet.narrative.drafting import (
    Outcome,
    draft_commentary,
    remove_failing_sentences,
    rendered_text,
)
from tearsheet.narrative.factsheet import (
    FactSheet,
    add_ratings,
    as_text,
    build,
    load_figures,
    load_narrative,
    load_specs,
)
from tearsheet.narrative.verifier import Draft, Verifier

OUT = ROOT / "docs" / "m8"


def narrative_v8(narrative: dict | None = None) -> dict:
    """The narrative with the M8 purposes and figure lists of the redrafted sections."""
    narrative = copy.deepcopy(narrative or load_narrative())
    m8 = narrative["m8_redraft"]
    for name in m8["sections"]:
        for key in ("purpose", "uses"):
            if key in m8.get(name, {}):
                narrative["sections"][name][key] = m8[name][key]
    return narrative


def vocabulary_v8(narrative: dict) -> dict:
    """The verifier's vocabulary with the phrases the M8 figures' names need."""
    import yaml

    from tearsheet.narrative.verifier import VOCABULARY

    vocabulary = yaml.safe_load(VOCABULARY.read_text())
    vocabulary["allowed_phrases"] += narrative["m8_redraft"].get("allowed_phrases", [])
    return vocabulary


def sheet_v8(issuer_id: str, year: int, figures, specs, narrative, events, ratings) -> FactSheet:
    """The fact sheet a tearsheet is drafted and checked against from M8 on: every catalog
    metric, the year's checked events, the ratings. The app builds the same one (live mode)."""
    issuer = {i.id: i for i in load_issuers()}[issuer_id]
    sheet = build(issuer, year, figures, specs, narrative)
    for item in events:
        sheet.items[item.id] = item
    add_ratings(sheet, ratings)
    return sheet


def run(
    llm: LLM,
    drafted: list[Outcome],
    db_path: Path = DB_PATH,
    out: Path = OUT,
    only: set[str] | None = None,
) -> list[Outcome]:
    """Redraft the two sections of each draft-v7 note (or replay the recorded answers)."""
    from tearsheet.ratings import checked_entries

    narrative = narrative_v8()
    m8 = narrative["m8_redraft"]
    verifier = Verifier(narrative, vocabulary_v8(narrative))
    specs = load_specs(narrative)
    con = duckdb.connect(str(db_path), read_only=True)
    figures = load_figures(con, set(specs))
    con.close()
    ratings = checked_entries(db_path)
    recorded = LLM(offline=True)
    outcomes = []
    for old in drafted:
        if not old.drafted:
            outcomes.append(old)
            continue
        events = [i for i in old.sheet.items.values() if i.kind == "event"]
        sheet = sheet_v8(old.sheet.issuer, old.sheet.fiscal_year, figures, specs, narrative,
                         events, ratings)  # fmt: skip
        kept = {k: v for k, v in old.sections.items() if k not in m8["sections"]}
        use = llm if not only or sheet.issuer in only else recorded
        new = draft_commentary(use, sheet, verifier, narrative, sections=m8["sections"],
                               kept=kept, prompt_version=m8["prompt_version"])  # fmt: skip
        new.previous = old  # the draft-v7 outcome, for tokens and the record
        if new.drafted:
            recheck(new, kept, verifier, old)
            remove_failing_sentences(new, verifier, narrative)  # decision 0018, kept sections too
        outcomes.append(new)
    write(outcomes, narrative, out)
    write_db(outcomes, db_path, m8)
    LAST[:] = outcomes
    return outcomes


def recheck(new: Outcome, kept: dict, verifier: Verifier, old: Outcome) -> None:
    """The kept draft-v7 sections against the new fact sheet: a sentence that now breaks a
    rule (a figure no longer available, a direction that changed) flags its section."""
    others = {k: v for k, v in new.sections.items() if k not in kept}
    report = verifier.check(new.sheet, Draft(kept), list(kept), others=others)
    for name in kept:
        errors = report.for_section(name)
        if any(e.blocking for e in errors):
            new.status[name] = "needs_manual_editing"
            new.errors[name] = errors
        else:
            new.errors[name] = old.errors.get(name, [])
            new.status[name] = old.status.get(name, "passed")


def prompt_of(name: str, m8: dict) -> str:
    return m8["prompt_version"] if name in m8["sections"] else "draft-v7"


# --- Records ----------------------------------------------------------------------------------


def gate(outcomes: list[Outcome]) -> tuple[int, set[str]]:
    """The longest run of consecutive notes (in drafting order) with no number outside a blank
    in the final text, and the companies it covers."""
    best, run_, companies, best_companies = 0, 0, [], set()
    for o in outcomes:
        clean = o.drafted and o.numbers_outside_blanks == 0
        run_ = run_ + 1 if clean else 0
        companies = companies + [o.sheet.issuer] if clean else []
        if run_ > best:
            best, best_companies = run_, set(companies)
    return best, best_companies


def tokens(o: Outcome) -> tuple[int, int]:
    results = [a.result for a in o.attempts if a.result is not None]
    return sum(r.usage.input_tokens for r in results), sum(r.usage.output_tokens for r in results)


def write(outcomes: list[Outcome], narrative: dict, out: Path) -> None:
    m8 = narrative["m8_redraft"]
    (out / "drafts").mkdir(parents=True, exist_ok=True)
    (out / "factsheets").mkdir(parents=True, exist_ok=True)
    rows = []
    for o in outcomes:
        if not o.drafted:
            rows.append(f"| {o.sheet.key} | not drafted | | | |")
            continue
        s = o.sheet
        (out / "factsheets" / f"{s.key}.json").write_text(s.to_json())
        (out / "factsheets" / f"{s.key}.md").write_text(as_text(s, narrative))
        md = [f"# {s.name}, {s.period_label}", "",
              f"Fact sheet `{o.input_hash()[:12]}`. Sections marked **{m8['prompt_version']}** "
              "were redrafted in M8; the others keep their draft-v7 text (M4).", ""]  # fmt: skip
        for name, sentences in o.sections.items():
            title = narrative["sections"][name]["title"]
            md += [f"## {title} ({prompt_of(name, m8)}, {o.status.get(name)})", ""]
            md += [f"{n}. {rendered_text(x.text, s.rendered())}" for n, x in
                   enumerate(sentences, start=1)]  # fmt: skip
            for text, why in o.removed.get(name, []):
                md.append(f"- removed by the verifier: “{text}” ({'; '.join(why)})")
            for e in o.errors.get(name, []):
                md.append(f"- {'error' if e.blocking else 'note'}: {e}")
            md.append("")
        (out / "drafts" / f"{s.key}.md").write_text("\n".join(md))
        i, t = tokens(o)
        first = o.attempts[0].report.ok if o.attempts and o.attempts[0].report else False
        rows.append(
            f"| {s.key} | {'passed' if o.passed else 'needs editing'} | "
            f"{'yes' if first else 'no'} | {o.numbers_outside_blanks} | {i:,} / {t:,} |"
        )
    length, companies = gate(outcomes)
    drafted = [o for o in outcomes if o.drafted]
    summary = [
        f"# M8 redraft: liquidity and funding, watch items (prompt `{m8['prompt_version']}`)",
        "",
        f"{len(drafted)} of {len(outcomes)} notes redrafted; {sum(o.passed for o in drafted)} "
        "pass the verifier in full (all six sections, the kept draft-v7 sections checked "
        "again against the new fact sheet).",
        f"Longest run of notes with no number outside a blank: **{length}**, over "
        f"{len(companies)} companies (the M8 checklist asks for ten in a row).",
        "",
        "| Note | Verifier | First try | Numbers outside blanks | Tokens (in / out) |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
    ]
    (out / "drafts.md").write_text("\n".join(summary))


def write_db(outcomes: list[Outcome], db_path: Path, m8: dict) -> None:
    """The merged notes replace the draft-v7 ones in the database (what the app shows)."""
    from tearsheet.narrative.run import write_db as write_v7

    write_v7(outcomes, db_path)
    con = duckdb.connect(str(db_path))
    redrafted = list(m8["sections"])
    con.execute(
        f"UPDATE drafts SET prompt_version = 'draft-v7' WHERE section NOT IN "
        f"({', '.join('?' * len(redrafted))})",
        redrafted,
    )
    con.execute(
        f"UPDATE drafts SET prompt_version = ? WHERE section IN "
        f"({', '.join('?' * len(redrafted))})",
        [m8["prompt_version"], *redrafted],
    )
    label = f"draft-v7 + {m8['prompt_version']} ({', '.join(redrafted)})"
    for o in outcomes:
        if not o.drafted:
            continue
        old = getattr(o, "previous", None)
        i, t = tokens(old) if old is not None else (0, 0)
        con.execute(
            "UPDATE runs SET prompt_version = ?, input_tokens = input_tokens + ?, "
            "output_tokens = output_tokens + ? WHERE issuer = ? AND fiscal_year = ?",
            [label, i, t, o.sheet.issuer, o.sheet.fiscal_year],
        )
    con.close()


def summary_line(outcomes: list[Outcome]) -> str:
    drafted = [o for o in outcomes if o.drafted]
    length, companies = gate(outcomes)
    return (
        f"M8 redraft: {len(drafted)}/{len(outcomes)} redrafted, "
        f"{sum(o.passed for o in drafted)} pass in full; run of {length} over "
        f"{len(companies)} companies with no number outside a blank (docs/m8/drafts.md)"
    )


LAST: list[Outcome] = []  # the latest redraft, for the command line summary
