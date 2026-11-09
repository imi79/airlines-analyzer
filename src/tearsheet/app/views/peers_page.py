"""Peers page: the peer table with median and rank, and net leverage against EBITDA margin."""

from __future__ import annotations

from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

from tearsheet.app import state
from tearsheet.app.cards import safe, selection_opens
from tearsheet.metrics.peers import peer_year
from tearsheet.render import library
from tearsheet.render.library import key
from tearsheet.render.sources import peer_median_card, ref_of_key, ref_of_peer_median

lib = state.get_library()
issuer, year = state.current()
st.session_state["card_tearsheet"] = None
groups = library.peer_groups()
end = lib.period_end(issuer, year)
own_year = peer_year(date.fromisoformat(end))
own_groups = [g for g, spec in groups["groups"].items() if issuer in spec["members"]]

st.title("Peers")
left, mid = st.columns([2, 1])
with left:
    group = st.selectbox(
        "Peer group",
        list(groups["groups"]),
        index=list(groups["groups"]).index(own_groups[0]),
        format_func=lambda g: groups["groups"][g]["label"],
        key=f"peer-group-{issuer}",
    )
with mid:
    years = [y for y in library.peer_years(lib) if y >= 2021]
    py = st.selectbox("Peer year", years, index=years.index(own_year), key=f"peer-year-{issuer}")

table = library.peer_table(lib, group, py, groups)
names = {m: state.name_of(lib, m) for m in table["members"]}
st.caption(
    "Each company's fiscal year whose 31 December falls within six months of its year end "
    "(decision 0008). Rank 1 is the strongest. Medians and ranks use verified figures only."
)
for m, months in table["year_end_offsets"].items():
    when = "after" if months > 0 else "before"
    st.caption(f"⚑ {names[m]}: {table['fiscal_years'][m]}, year end {abs(months)} months {when} "
               "31 December.")  # fmt: skip

# --- Table ---------------------------------------------------------------------------------------
sort_by = st.selectbox(
    "Sort companies by",
    ["(group order)"] + [r["metric"] for r in table["rows"]],
    format_func=lambda m: m if m.startswith("(") else lib.label.get(m, m),
    key=f"peer-sort-{group}",
)
order = list(table["members"])
if not sort_by.startswith("("):
    row = next(r for r in table["rows"] if r["metric"] == sort_by)
    order.sort(key=lambda m: row["cells"][m].get("rank", 99))


def _cell_text(c: dict) -> str:
    if c.get("rendered"):
        rank = f" ({c['rank']})" if c.get("rank") else ""
        return c["rendered"] + rank
    if c.get("nm"):
        return "n.m."
    return "awaiting review" if c.get("key") else "–"


frame = pd.DataFrame(
    [
        [r["label"]] + [_cell_text(r["cells"][m]) for m in order] + [r["median_rendered"] or "–"]
        for r in table["rows"]
    ],
    columns=["Metric"]
    + [f"{names[m]} {table['fiscal_years'][m] or ''}".strip() for m in order]
    + ["Median"],
)
if issuer in order:
    own = f"{names[issuer]} {table['fiscal_years'][issuer] or ''}".strip()
    styled = frame.style.set_properties(subset=[own], **{"font-weight": "bold"})
else:
    styled = frame
st.dataframe(styled, hide_index=True, on_select="rerun", selection_mode="single-row",
             height=36 * (len(frame) + 1) + 4,
             key=f"peer-table-{group}-{py}", width="stretch")  # fmt: skip
st.caption("Click a row to see the source of each company's figure and of the median.")


def _refs(selection) -> list[dict]:
    rows = selection.get("rows") or []
    if not rows:
        return []
    r = table["rows"][rows[0]]
    refs = [ref_of_key(r["cells"][m]["key"]) for m in order if r["cells"][m].get("key")]
    if r["median"] is not None:
        refs.append(ref_of_peer_median(group, py, r["metric"]))
    return refs


selection_opens(f"peer-table-{group}-{py}", _refs,
                lambda s: f"{table['rows'][s['rows'][0]]['label']}, {table['label']}")  # fmt: skip

with st.expander("How each median was computed"):
    for r in table["rows"]:
        card = peer_median_card(lib, table, r)
        st.markdown(f"**{safe(r['label'])}**: {safe(card['rendered'])}. {safe(card['lines'][0])}.")

# --- Scatter -------------------------------------------------------------------------------------
st.subheader("Net leverage against EBITDA margin")
points = []
for m in table["members"]:
    fy_label = table["fiscal_years"][m]
    fy = library.members_year(lib, m, py)
    if fy is None:
        continue
    lev, margin = key(m, "net_leverage", fy), key(m, "ebitda_margin", fy)
    if lib.usable(lev) and lib.usable(margin):
        points.append({
            "company": names[m],
            "net_leverage": float(lib.figures[lev]["value"]),
            "ebitda_margin": float(lib.figures[margin]["value"]) * 100,
            "label": f"{names[m]} {fy_label}: {lib.figures[lev]['rendered']}, "
                     f"{lib.figures[margin]['rendered']}",
            "key": lev,
            "key2": margin,
            "own": m == issuer,
        })  # fmt: skip
if points:
    data = pd.DataFrame(points)
    pick = alt.selection_point(name="pick", fields=["key", "key2"])
    base = alt.Chart(data).encode(
        x=alt.X("ebitda_margin:Q", title="EBITDA margin (%)", scale=alt.Scale(zero=False)),
        y=alt.Y("net_leverage:Q", title="Net leverage (x)"),
        tooltip=["label"],
    )
    dots = (
        base.mark_circle(size=160)
        .encode(color=alt.condition("datum.own", alt.value("#c0392b"), alt.value("#4a6fa5")))
        .add_params(pick)
    )
    text = base.mark_text(align="left", dx=9, dy=-6).encode(text="company")
    st.altair_chart((dots + text).properties(height=360), width="stretch",
                    on_select="rerun", key=f"peer-scatter-{group}-{py}")  # fmt: skip
    st.caption("Lower and to the right is stronger. Click a company to see both figures' sources.")

    def _point_refs(selection) -> list[dict]:
        picked = (selection.get("pick") or []) if isinstance(selection, dict) else []
        out = []
        for p in picked:
            out += [ref_of_key(p[k]) for k in ("key", "key2") if p.get(k)]
        return out

    selection_opens(f"peer-scatter-{group}-{py}", _point_refs, lambda s: "Peer scatter")
else:
    st.caption("No company in this group has both figures verified for this peer year.")
