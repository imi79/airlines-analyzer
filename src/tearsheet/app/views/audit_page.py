"""Data and audit page: every figure with its source and status, the figures awaiting review
(approve or correct, with a reason), the filings and the run record of the draft."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import date

import pandas as pd
import streamlit as st

from tearsheet.app import state
from tearsheet.app.cards import open_sources, safe, selection_opens
from tearsheet.config import ROOT
from tearsheet.llm.settings import load_settings
from tearsheet.render import notes, tearsheet, verifier_demo
from tearsheet.render.sources import SOURCE_WORDS, STATUS_WORDS, figure_card, ref_of_key

lib = state.get_library()
issuer, year = state.current()
ts = state.get_tearsheet(issuer, year)
st.session_state["card_tearsheet"] = ts
live = state.mode() == state.LIVE
analyst = tearsheet.load_app_config()["analyst"]

st.title("Data and audit")
st.markdown(f"**{safe(ts['name'])}**, {safe(ts['period_label'])}")

# --- Every figure for the year ----------------------------------------------------------------
st.subheader("Every figure for the year")
mine = sorted(
    (k for k, f in lib.figures.items() if f["issuer"] == issuer and f["fiscal_year"] == year),
    key=lambda k: (lib.figures[k]["source_type"] != "computed", lib.figures[k]["label"]),
)
kinds = st.multiselect(
    "Source", list(SOURCE_WORDS), default=list(SOURCE_WORDS),
    format_func=lambda s: SOURCE_WORDS[s].split(",")[0], key=f"audit-kinds-{issuer}-{year}",
)  # fmt: skip
shown = [k for k in mine if lib.figures[k]["source_type"] in kinds]
frame = pd.DataFrame(
    [
        {
            "Figure": lib.figures[k]["label"],
            "Value": lib.figures[k]["rendered"],
            "Source": SOURCE_WORDS[lib.figures[k]["source_type"]].split(",")[0],
            "Status": STATUS_WORDS[lib.figures[k]["status"]].split(":")[0],
        }
        for k in shown
    ]
)
st.dataframe(frame, hide_index=True, on_select="rerun", selection_mode="single-row",
             key=f"audit-table-{issuer}-{year}", width="stretch", height=380)  # fmt: skip
st.caption(f"{len(shown)} figures. Click a row for its source card.")
selection_opens(
    f"audit-table-{issuer}-{year}",
    lambda s: [ref_of_key(shown[s["rows"][0]])] if s.get("rows") else [],
    lambda s: lib.figures[shown[s["rows"][0]]]["label"],
)

# --- Awaiting review --------------------------------------------------------------------------
st.subheader("Figures awaiting your review")
waiting = sorted(
    (
        k
        for k, f in lib.figures.items()
        if f["issuer"] == issuer and f["source_type"] == "extracted" and f["status"] == "unverified"
    ),
    key=lambda k: (-lib.figures[k]["fiscal_year"], k),
)
if live:
    st.caption("Approvals and corrections are saved to config/extraction_reviews.yaml with your "
               "name, the date and the reason. Rebuild the figures to apply them.")  # fmt: skip
else:
    st.caption("Demo mode: a review lasts for this session only. In live mode it is saved.")
if not waiting:
    st.success("Nothing waiting for review for this company.")
for k in waiting:
    f = lib.figures[k]
    card = figure_card(lib, k)
    with st.expander(f"{f['label']}, FY{f['fiscal_year']}: {f['rendered']}"):
        for line in card["lines"]:
            st.markdown(f"- {safe(line)}")
        with st.form(f"review-{k}"):
            words = {"approve": "Approve: the value is right", "correct": "Correct the value"}
            action = st.radio("Decision", list(words), horizontal=True, format_func=words.get)
            hint = (
                "a fraction: 0.856 for 85.6%"
                if f["unit"] == "pct"
                else (f"full units, {f['currency']}" if f["unit"] == "amount" else "full units")
            )
            value = st.text_input(f"Corrected value ({hint})", "")
            reason = st.text_input("Reason", placeholder="Checked on page 32 of the report")
            by = st.text_input("Your name", analyst)
            if st.form_submit_button("Save the review"):
                review = {"issuer": issuer, "fiscal_year": f["fiscal_year"],
                          "item": f["concept"], "action": action, "value": value or None,
                          "reason": reason, "by": by, "on": str(date.today())}  # fmt: skip
                problems = notes.check_review(review, f["unit"])
                if problems:
                    st.error("Not saved: " + "; ".join(problems))
                elif live:
                    try:
                        notes.add_review(review)
                    except ValueError as exc:
                        st.error(str(exc))
                    else:
                        st.success("Saved. Rebuild the figures below to apply it.")
                else:
                    st.session_state.setdefault("demo_reviews", {})[k] = review
                    st.rerun()
reviewed = st.session_state.get("demo_reviews") or {}
mine_reviewed = [k for k in reviewed if k.startswith(f"{issuer}:")]
if not live and mine_reviewed:
    st.markdown("**Reviewed in this session (not saved)**")
    for k in mine_reviewed:
        r = reviewed[k]
        cols = st.columns([6, 1])
        cols[0].markdown(f"- {safe(lib.figures[k]['label'])} FY{lib.figures[k]['fiscal_year']}: "
                         f"{r['action']} ({safe(r['reason'])}), by {safe(r['by'])}")  # fmt: skip
        if cols[1].button("Undo", key=f"undo-{k}"):
            reviewed.pop(k)
            st.rerun()

# --- Filings ----------------------------------------------------------------------------------
st.subheader("Filings used")
filings = sorted(
    ((fid, rec) for fid, rec in lib.filings.items() if rec["issuer"] == issuer),
    key=lambda t: -t[1]["fiscal_year"],
)
for fid, rec in filings:
    link = rec.get("viewer_url") or rec.get("report_url")
    where = f"[open the filing]({link})" if link else safe(rec.get("choice_reason") or "")
    sha = f" · SHA-256 `{rec['sha256'][:16]}…`" if rec.get("sha256") else ""
    st.markdown(f"- FY{rec['fiscal_year']}: `{fid}` ({safe(rec['origin'])}) · {where}{sha}")

# --- The draft's run record -------------------------------------------------------------------
st.subheader("Commentary: run record")
run = ts.get("run")
if run is None:
    st.info("No commentary drafted for this year.")
else:
    tokens = (run["input_tokens"] or 0) + (run["output_tokens"] or 0)
    st.markdown(
        f"- Model: {safe(run['provider'] or '')} `{run['model']}`, "
        f"prompt `{run['prompt_version']}`\n"
        f"- AI calls: {run['calls']}, tokens: {tokens:,}"
        + (f", cost USD {run['cost_usd']}" if run.get("cost_usd") else "")
        + f"\n- Passed the verifier: {'yes' if run['passed'] else 'no'}"
        f" (first try: {'yes' if run['first_try_ok'] else 'no'})\n"
        f"- Fact sheet fingerprint: `{run['input_hash'][:12]}`"
        + ("" if run.get("matches_figures", True) else " (figures changed since)")
        + f"\n- Recorded: {run.get('recorded_at') or 'n.a.'}"
    )
    st.markdown("Filings behind the figures:")
    for fid, sha in run["filing_hashes"].items():
        st.markdown(f"  - `{fid}`: `{(sha or 'no hash')[:16]}`")
    notes_list = [n for s in ts["commentary"].values() for n in s["notes"]]
    removed = [(s["title"], r) for s in ts["commentary"].values() for r in s["removed"]]
    if notes_list or removed:
        with st.expander(f"Verifier notes ({len(notes_list)}) and sentences removed "
                         f"({len(removed)})"):  # fmt: skip
            for n in notes_list:
                st.markdown(f"- {safe(n)}")
            for title, r in removed:
                st.markdown(f"- Removed from {title}: “{safe(r['text'])}” "
                            f"({safe('; '.join(r['why']))})")  # fmt: skip
    if ts["events"]:
        with st.expander(f"Events of the year read from the report ({len(ts['events'])})"):
            for e in ts["events"]:
                if st.button(f"{e['title']} ({e['status']})", key=f"ev-{e['event_id']}"):
                    open_sources([{"fid": e["event_id"]}], e["title"])

# --- How the draft was checked: the AI's attempts and the verifier's verdicts (M7) ----------
st.subheader("How the AI's draft was checked")
tries = ts.get("attempts") or []
if not tries:
    st.info("No recorded draft for this year.")
else:
    rejected = sum(len(a["rejections"]) for a in tries)
    st.caption(
        f"The AI handed in {len(tries)} version(s). The verifier rejected {rejected} sentence(s) "
        "along the way; a rejected section goes back to the AI with the reasons, up to two "
        "times. Only what passed reaches the tearsheet."
    )
    for a in tries:
        n = len(a["rejections"])
        head = (
            f"Try {a['try']}: "
            + (f"{n} sentence(s) rejected" if n else "passed the verifier")
            + f" ({', '.join(a['sections'])})"
        )
        with st.expander(head, expanded=bool(n) and a["try"] == 1):
            if a.get("error"):
                st.warning(safe(a["error"]))
            for r in a["rejections"]:
                title = verifier_demo.RULES.get(r["rule"], r["rule"])
                where = f"{r['section'].replace('_', ' ')}, sentence {r['sentence']}" if (
                    r["sentence"]) else r["section"].replace("_", " ")  # fmt: skip
                st.markdown(f"**Rule {r['rule']}: {safe(title)}** · {safe(where)}")
                if r["text"]:
                    st.markdown(f"> {safe(r['text'])}")
                st.caption(safe(r["message"]))
            if a["style_notes"]:
                st.caption(f"Plus {a['style_notes']} note(s) on style, sent back but not rejected.")

# --- Live mode: rebuild and redraft -----------------------------------------------------------
if live:
    st.subheader("Live mode")
    settings = load_settings()
    st.caption(f"AI provider from config/models.yaml: {settings.name}, drafting model "
               f"`{settings.model('drafting')}`. The key is read from {settings.api_key_env}, or "
               "typed below for this session only (kept in memory, never saved).")  # fmt: skip
    typed = st.text_input("API key for this session", type="password", key="session_key")
    c1, c2 = st.columns(2)
    if c1.button("Rebuild the figures (offline, no AI)"):
        with st.spinner("Rebuilding the database and reports from the cached filings..."):
            done = subprocess.run([sys.executable, "-m", "tearsheet.cli", "all", "--offline"],
                                  cwd=ROOT, capture_output=True, text=True)  # fmt: skip
        if done.returncode == 0:
            st.cache_resource.clear()
            st.cache_data.clear()
            st.success("Rebuilt. Tearsheets whose figures changed need a redraft.")
        else:
            st.error(done.stderr[-2000:])
    if c2.button(f"Redraft {ts['name']} with the AI"):
        env = dict(os.environ)
        if typed:
            env[settings.api_key_env] = typed
        if not env.get(settings.api_key_env):
            st.error(f"No key: set {settings.api_key_env} or type one above.")
        else:
            with st.spinner("Drafting (recorded answers are replayed for free)..."):
                done = subprocess.run(
                    [sys.executable, "-m", "tearsheet.cli", "draft", "--issuer", issuer],
                    cwd=ROOT, capture_output=True, text=True, env=env,
                )  # fmt: skip
            if done.returncode == 0:
                st.cache_resource.clear()
                st.cache_data.clear()
                st.success(done.stdout.strip().splitlines()[-1] if done.stdout.strip() else "Done")
            else:
                st.error(done.stderr[-2000:])
