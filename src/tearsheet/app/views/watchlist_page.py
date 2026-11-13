"""Watchlist page (M9): every company against the analyst's credit triggers, for one year.

Companies down the side, triggers across the top; each cell fired, clear or cannot assess.
A click on a row, or on a fired trigger below the table, opens the trigger's card: the figure
against the threshold, last year's value, and the figures behind it down to the filing.
Nothing is saved: the page reads the figures and config/watchlist.yaml.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from tearsheet import watchlist
from tearsheet.app import state
from tearsheet.app.cards import safe, selection_opens, sources_button
from tearsheet.config import load_issuers
from tearsheet.metrics.peers import peer_year
from tearsheet.render import library

LATEST = "Latest (LTM)"
lib = state.get_library()
issuer, year = state.current()
st.session_state["card_tearsheet"] = None
triggers = watchlist.triggers()
order = [i.id for i in load_issuers()]

st.title("Watchlist")
st.caption(
    "Credit triggers set by the analyst in config/watchlist.yaml, checked by code against "
    'verified figures only. A figure exactly at the threshold does not fire. "Cannot '
    'assess": the figure is missing, not meaningful or awaiting review; it is never counted '
    "as clear."
)

left, right = st.columns([1, 2])
with left:
    years = [y for y in library.peer_years(lib) if y >= 2021]
    own = peer_year(date.fromisoformat(lib.period_end(issuer, year)))
    view = state.get_ltm_library()
    options = years + ([LATEST] if view.ltm else [])
    py = st.selectbox("Year", options,
                      index=years.index(own) if own in years else len(years) - 1,
                      key="watch-year",
                      help="Each company's fiscal year whose 31 December falls within six "
                      "months of its year end (decision 0008). Latest (LTM): the last twelve "
                      "months to each company's latest half-year date, from its unaudited "
                      "half-year report; moves are measured against the last fiscal "
                      "year.")  # fmt: skip
ltm = py == LATEST
if ltm:
    lib = view
with right:
    show = st.radio(
        "Show",
        ["All companies", "With a trigger fired", "With a new warning"],
        horizontal=True,
        key="watch-filter",
        help="New warning: a trigger fired this year that did not fire the year before.",
    )

if ltm:
    rows = watchlist.board(lib, None, order, {i: v["year"] for i, v in view.ltm.items()})
    st.caption("Last twelve months, from unaudited half-year reports: each company at its own "
               "half-year date (shown beside its name). Undrawn credit lines and maturity tables "
               "are not in half-year reports: liquidity and short-term cover are decided on "
               "cash alone where cash already clears the threshold, else cannot be "
               "assessed.")  # fmt: skip
else:
    rows = watchlist.board(lib, py, order)
if show == "With a trigger fired":
    rows = [r for r in rows if any(c and c.status == watchlist.FIRED for c in r["cells"].values())]
elif show == "With a new warning":
    rows = [r for r in rows if r["new"]]

MARK = {watchlist.FIRED: "● fired", watchlist.CLEAR: "clear", watchlist.CANNOT: "cannot assess"}


def _text(row: dict, tid: str) -> str:
    c = row["cells"][tid]
    if c is None:
        return "–"
    text = MARK[c.status]
    if c.status == watchlist.FIRED and tid in row["new"]:
        text += " (new)"
    if c.status != watchlist.CANNOT:
        text += f" · {c.shown}"
    return text


fired_total = sum(1 for r in rows for c in r["cells"].values() if c and c.status == "fired")
st.markdown(f"**{fired_total} trigger{'s' if fired_total != 1 else ''} fired** across "
            f"{len(rows)} compan{'ies' if len(rows) != 1 else 'y'}.")  # fmt: skip

if not rows:
    st.info("No company matches this filter for this year.")
else:
    frame = pd.DataFrame(
        [[f"{state.name_of(lib, r['issuer'])} {r['period_label']}"]
         + [_text(r, t.id) for t in triggers] for r in rows],
        columns=["Company"] + [t.label for t in triggers],
    )  # fmt: skip
    st.dataframe(frame, hide_index=True, on_select="rerun", selection_mode="single-row",
                 height=36 * (len(frame) + 1) + 4, key="watch_table",
                 width="stretch")  # fmt: skip
    st.caption("Click a row to see every trigger's figures and sources. \"–\": the trigger "
               "does not apply (liquidity to revenue is for airlines only).")  # fmt: skip

    def _row_refs(selection) -> list[dict]:
        picked = selection.get("rows") or []
        if not picked:
            return []
        r = rows[picked[0]]
        return [c.ref for c in r["cells"].values() if c is not None]

    def _row_title(selection) -> str:
        r = rows[selection["rows"][0]]
        return f"Watchlist: {state.name_of(lib, r['issuer'])} {r['period_label']}"

    selection_opens("watch_table", _row_refs, _row_title, ltm=ltm)

# --- The fired triggers, one line each, then what could not be assessed -------------------------
st.subheader("Fired")
fired = [(r, t, r["cells"][t.id]) for r in rows for t in triggers
         if r["cells"][t.id] and r["cells"][t.id].status == watchlist.FIRED]  # fmt: skip
if not fired:
    st.caption("No trigger fired.")
for r, t, c in fired:
    text_col, button_col = st.columns([24, 1])
    with text_col:
        new = ""
        if t.id in r["new"]:
            before = watchlist.STATUS_WORDS[r["new"][t.id]]
            new = f" :orange-badge[new: {before} the year before]"
        st.markdown(f"**{safe(state.name_of(lib, r['issuer']))} {safe(r['period_label'])}** · "
                    f"{safe(t.label)}: {safe(c.detail)}{new}")  # fmt: skip
    with button_col:
        sources_button([c.ref], f"{t.label}, {state.name_of(lib, r['issuer'])}",
                       key=f"watch-{r['issuer']}-{t.id}", ltm=ltm)  # fmt: skip

cannot = [(r, t, r["cells"][t.id]) for r in rows for t in triggers
          if r["cells"][t.id] and r["cells"][t.id].status == watchlist.CANNOT]  # fmt: skip
with st.expander(f"Cannot assess ({len(cannot)}), with the reason"):
    for r, t, c in cannot:
        st.markdown(f"- **{safe(state.name_of(lib, r['issuer']))} {safe(r['period_label'])}** · "
                    f"{safe(t.label)}: {safe(c.detail)}")  # fmt: skip

with st.expander("The triggers"):
    for t in triggers:
        scope = {"all": "every company", "airline": "airlines", "airport": "airports"}
        st.markdown(f"- **{safe(t.label)}** ({scope[t.applies_to]}): {safe(t.reason)} "
                    f"Set by {safe(t.set_by)} on {safe(t.set_on)}.")  # fmt: skip
    st.caption("To change a threshold, edit config/watchlist.yaml (decision 0023).")
