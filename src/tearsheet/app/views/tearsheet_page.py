"""Tearsheet page: header, KPI cards, four-year table, two charts, commentary, analyst view."""

from __future__ import annotations

import json

import altair as alt
import pandas as pd
import streamlit as st

from tearsheet.app import state
from tearsheet.app.cards import safe, selection_opens, sources_button
from tearsheet.app.notes_ui import analyst_view, edit_section, edited_sentence, get_note
from tearsheet.narrative.factsheet import load_narrative
from tearsheet.narrative.render import PLACEHOLDER
from tearsheet.ratings import header_text
from tearsheet.render import export, notes, pdf, tearsheet
from tearsheet.render.library import key, small_debt
from tearsheet.render.sources import ref_of_id, ref_of_key

TYPE_WORDS = {"airline": "Airline", "airport": "Airport"}
SEGMENT_WORDS = {"network": "network airline", "low_cost": "low-cost airline"}

lib = state.get_library()
issuer, year = state.current()
ts = state.get_tearsheet(issuer, year)
st.session_state["card_tearsheet"] = ts
config = tearsheet.load_app_config()
rendered = {k: v["rendered"] for k, v in ts["factsheet"]["items"].items()}
order = [n for n in load_narrative()["sections"] if n in ts["commentary"]]  # snapshot first


def show_section(name: str) -> None:
    section = ts["commentary"][name]
    st.subheader(section["title"])
    if section["status"] == "not_drafted":
        st.info("Not drafted for this year: the AI drafts each company's latest two years.")
        return
    edits = (get_note(ts).get("edits") or {}).get(name, {})
    if section["status"] != "passed" and notes.cleared(section, name, edits):
        st.caption("The sentences the verifier rejected have been edited by the analyst.")
    elif section["status"] != "passed":
        st.warning("This section failed the verifier after two retries: edit it before use.")
    if editing:
        edit_section(lib, ts, name, section, rendered)
        return
    bullets = name == "watch_items"
    for n, sentence in enumerate(section["sentences"], start=1):
        text_blanks, flags, edited = edited_sentence(ts, name, n, sentence)
        shown = PLACEHOLDER.sub(
            lambda m: f"**{rendered.get(m.group(1), m.group(0))}**", text_blanks
        )
        ids = list(dict.fromkeys(PLACEHOLDER.findall(text_blanks)))
        ids += [f["id"] for f in sentence["facts"] if f["id"].startswith("event:")]
        text_col, button_col = st.columns([24, 1])
        with text_col:
            prefix = "- " if bullets else ""
            mark = " :gray-badge[edited by the analyst]" if edited else ""
            if flags:
                mark += f" :red-badge[{safe(flags)}]"
            st.markdown(prefix + safe(shown) + mark)
        with button_col:
            sources_button(
                [ref_of_id(i) for i in ids],
                f"{section['title']}, sentence {n}",
                key=f"s-{name}-{n}",
            )


# --- Header -------------------------------------------------------------------------------------
info = lib.issuers[issuer]
kind = SEGMENT_WORDS.get(info.get("segment") or "", TYPE_WORDS.get(info["type"], info["type"]))
st.title(ts["name"])
st.markdown(
    f"**{safe(ts['period_label'])}** · {kind[0].upper() + kind[1:]} · reporting currency "
    f"{ts['currency']} · peer group: {ts['peer_group']}"
)
rating_line = header_text(ts.get("rating"))
if rating_line:
    st.caption(safe(rating_line))  # M8: the ratings box, from the company's own report
run = ts.get("run")
if run is not None and run.get("matches_figures") is False:
    st.warning(
        "The figures have changed since this commentary was drafted (for example after a "
        "review). Redraft it from the Data and audit page before relying on it."
    )

editing = st.toggle("Edit the commentary", key=f"editing-{issuer}-{year}")
show_section(order[0])

# --- KPI cards ----------------------------------------------------------------------------------
cards = tearsheet.kpi_cards(lib, ts, config)
cols = st.columns(len(cards))
for col, kpi in zip(cols, cards, strict=True):
    with col:
        c = kpi["cell"]
        change = kpi["change"]
        delta, colour = None, "off"
        if change and c.status in ("verified", "overridden"):
            sign = {"up": "+", "down": "-"}.get(change["direction"], "")
            delta = f"{sign}{change['rendered']}" if sign else f"stable ({change['rendered']})"
            better = lib.higher_is_better.get(kpi["metric"])
            if change["direction"] != "flat" and better is not None:
                colour = "normal" if better else "inverse"
        why = None
        if c.status == "missing":
            why = lib.why_missing(key(issuer, kpi["metric"], year))
        elif c.status == "not_meaningful":
            why = small_debt(lib, issuer, kpi["metric"], year)
        elif c.status == "unverified":
            why = "Read from the report but not verified yet: see the Data and audit page."
        st.metric(kpi["label"], c.rendered, delta=delta, delta_color=colour, border=True,
                  help=why)  # fmt: skip
        if why:
            st.caption(safe(why))
        refs = [ref_of_key(c.key)] if c.key else []
        if kpi["change_id"] and delta:
            refs.append(ref_of_id(kpi["change_id"]))
        sources_button(refs, f"{kpi['label']}, FY{year}", key=f"kpi-{kpi['metric']}",
                       label="Source")  # fmt: skip

# --- Four-year table ------------------------------------------------------------------------------
table = tearsheet.kpi_table(lib, ts, config)
st.subheader("Key figures")
frame = pd.DataFrame(
    [[r["label"]] + [c.rendered for c in r["cells"]] for r in table["rows"]],
    columns=["Metric"] + table["labels"],
)
st.dataframe(frame, hide_index=True, on_select="rerun", selection_mode="single-row",
             height=36 * (len(frame) + 1) + 4,
             key="kpi_table", width="stretch")  # fmt: skip
st.caption("Click a row to see where its figures come from. \"Awaiting review\": a figure read "
           "from the report that has not passed every check, kept off the tearsheet. \"n.m.\": "
           "not meaningful, for example a ratio to a very small debt.")  # fmt: skip


def _row_refs(selection) -> list[dict]:
    rows = selection.get("rows") or []
    if not rows:
        return []
    r = table["rows"][rows[0]]
    return [ref_of_key(c.key) for c in r["cells"] if c.key]


def _row_title(selection) -> str:
    return table["rows"][selection["rows"][0]]["label"]


selection_opens("kpi_table", _row_refs, _row_title)

# --- Charts ------------------------------------------------------------------------------------
left, right = st.columns(2)
for col, chart_id in ((left, "leverage"), (right, "liquidity")):
    with col:
        spec = config["charts"][chart_id]
        points = tearsheet.chart_series(lib, ts, chart_id, config)
        st.markdown(f"**{spec['title']}**")
        if not points:
            st.caption("No verified figures to chart.")
            continue
        data = pd.DataFrame(points)
        pick = alt.selection_point(name="pick", fields=["key"])
        base = alt.Chart(data)
        if chart_id == "liquidity":
            unit = ts["currency"]
            data["millions"] = data["value"] / 1e6
            mark = (
                alt.Chart(data)
                .mark_bar()
                .encode(
                    x=alt.X("year:N", title=None, sort=None),  # liquidity, then maturities
                    y=alt.Y("millions:Q", title=f"{unit} m", stack="zero"),
                    color=alt.Color("metric:N", title=None, legend=alt.Legend(orient="bottom")),
                    tooltip=["year", "metric", "rendered"],
                    opacity=alt.condition(pick, alt.value(1), alt.value(0.6)),
                )
            )
        else:
            mark = base.mark_line(point=alt.OverlayMarkDef(size=90)).encode(
                x=alt.X("year:N", title=None),
                y=alt.Y("value:Q", title="x EBITDA"),
                color=alt.Color("metric:N", title=None, legend=alt.Legend(orient="bottom")),
                tooltip=["year", "metric", "rendered"],
            )
        chart = mark.add_params(pick).properties(height=260)
        st.altair_chart(chart, width="stretch", on_select="rerun",
                        key=f"chart-{chart_id}")  # fmt: skip
        st.caption("Click a point or bar to see its source.")

        def _point_refs(selection, _points=points) -> list[dict]:
            picked = (selection.get("pick") or []) if isinstance(selection, dict) else []
            keys = [p.get("key") for p in picked if p.get("key")]
            return [ref_of_key(k) for k in keys]

        selection_opens(f"chart-{chart_id}", _point_refs, lambda s, t=spec["title"]: t)

# --- The rest of the commentary ----------------------------------------------------------------
st.divider()
for name in order[1:]:
    show_section(name)

st.divider()
analyst_view(ts)
st.caption("Draft prepared with AI assistance. Figures computed from regulatory filings and "
           "checked automatically. Not investment advice.")  # fmt: skip

# --- Export: the two-page PDF, the Excel backup and the manifest (M6) ----------------------------
st.divider()
st.subheader("Export")
note = get_note(ts)
if not pdf.view_fits(note):
    st.warning("The analyst view is longer than the PDF's box (about eight lines): the PDF "
               "shows the start, marked \"continued in the app\".")  # fmt: skip
untraced = sum(1 for v in (note.get("edits") or {}).values() for e in v.values()
               if e.get("untraced"))  # fmt: skip
if untraced:
    st.info(f"{untraced} edited sentence(s) contain a figure not traced to a source: the PDF "
            "marks them with † and a footnote.")  # fmt: skip
ready_key = f"export-{issuer}-{year}"
if st.button("Prepare the PDF and the Excel backup", key=f"prepare-{issuer}-{year}",
             icon=":material/picture_as_pdf:"):  # fmt: skip
    session = st.session_state.get("demo_reviews") or {}
    reviews = [k for k in session if k.startswith(f"{issuer}:")]
    with st.spinner("Laying out the two pages and writing the workbook..."):
        st.session_state[ready_key] = export.build(
            lib, ts, note, mode=state.mode().lower(), session_reviews=len(reviews)
        )
done = st.session_state.get(ready_key)
if done is not None:
    left, mid, right = st.columns(3)
    left.download_button("Download PDF", done.pdf, f"{done.name}.pdf", "application/pdf",
                         key=f"dl-pdf-{issuer}-{year}", icon=":material/download:")  # fmt: skip
    mid.download_button(
        "Download Excel", done.xlsx, f"{done.name}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"dl-xlsx-{issuer}-{year}", icon=":material/download:",
    )  # fmt: skip
    right.download_button(
        "Download manifest", json.dumps(done.manifest, indent=1, ensure_ascii=False),
        f"{done.name}_manifest.json", "application/json", key=f"dl-json-{issuer}-{year}",
        icon=":material/download:",
    )  # fmt: skip
    st.caption(f"Prepared at {done.manifest['exported_at'][:16].replace('T', ' ')} UTC, text at "
               f"{done.font_size} point. Includes your edits and analyst view as they were "
               "then; prepare again after a change.")  # fmt: skip
