"""The source card window: click a figure, see where it came from, follow it down.

The window keeps a trail (like breadcrumbs): opening an input pushes its card, "Back" returns.
"""

from __future__ import annotations

import streamlit as st

from tearsheet.render import sources
from tearsheet.render.library import Library

KIND_BADGE = {
    "tagged": ":blue-badge[Filing fact]",
    "computed": ":violet-badge[Computed]",
    "extracted": ":orange-badge[Read from the report]",
    "manual": ":gray-badge[Entered by hand]",
    "change": ":violet-badge[Change]",
    "peer_median": ":violet-badge[Peer median]",
    "peer_rank": ":violet-badge[Peer rank]",
    "event": ":orange-badge[Event of the year]",
    "derived": ":violet-badge[Computed]",
    "missing": ":red-badge[Not available]",
    "watch": ":orange-badge[Watchlist trigger]",
}
STATUS_BADGE = {
    "verified": ":green-badge[Verified]",
    "overridden": ":green-badge[Approved by the analyst]",
    "unverified": ":red-badge[Awaiting review]",
}


def safe(text: str) -> str:
    """Markdown-safe: a $ would start a formula in Streamlit."""
    return str(text).replace("$", "\\$")


def open_sources(refs: list[dict], title: str) -> None:
    """Call from a button handler: opens the window on these figures."""
    st.session_state["card_trail"] = [{"refs": refs, "title": title}]
    source_window()


def _ref_label(ref: dict) -> str:
    if "peer" in ref:
        return f"{ref['peer']}-{ref['year']}-{ref['metric']}"
    if "watch" in ref:
        return f"{ref['watch']}-{ref['issuer']}-{ref['year']}"
    return ref.get("key") or ref.get("fid") or "?"


@st.dialog("Where the figures come from", width="large")
def source_window() -> None:
    from tearsheet.app.state import get_library

    lib: Library = get_library()
    ts = st.session_state.get("card_tearsheet")
    trail = st.session_state.get("card_trail") or []
    if not trail:
        st.write("Nothing selected.")
        return
    view = trail[-1]
    if len(trail) > 1:
        path = " › ".join(v["title"] for v in trail)
        st.caption(safe(path))
        if st.button("← Back", key=f"back-{len(trail)}"):
            st.session_state["card_trail"] = trail[:-1]
            st.rerun(scope="fragment")
    else:
        st.caption(safe(view["title"]))
    for n, ref in enumerate(view["refs"]):
        show_card(lib, ts, ref, f"{len(trail)}-{n}")


def show_card(lib: Library, ts: dict | None, ref: dict, slot: str) -> None:
    card = sources.card(lib, ts, ref)
    with st.container(border=True):
        badges = KIND_BADGE.get(card["kind"], "")
        if card.get("status"):
            badges += " " + STATUS_BADGE.get(card["status"], "")
        st.markdown(f"**{safe(card['title'])}** &nbsp; {badges}")
        if card.get("rendered"):
            st.markdown(f"### {safe(card['rendered'])}")
        if card.get("how"):
            st.markdown(f"*{safe(card['how'])}*")
        if card.get("definition"):
            st.markdown(f"Definition: {safe(card['definition'])}")
        for line in card["lines"]:
            st.markdown(f"- {safe(line)}")
        if card.get("link"):
            st.link_button("Open the filing", card["link"])
        if card["inputs"]:
            st.markdown("**Built from** (click to follow)")
            for m, inp in enumerate(card["inputs"]):
                sub = sources.card(lib, ts, inp)
                label = f"{sub['title']}: {sub.get('rendered') or 'n.a.'}"
                if st.button(label, key=f"in-{slot}-{m}-{_ref_label(inp)}"):
                    trail = st.session_state.get("card_trail") or []
                    trail = trail + [{"refs": [inp], "title": sub["title"]}]
                    st.session_state["card_trail"] = trail
                    st.rerun(scope="fragment")


def sources_button(refs: list[dict], title: str, key: str, label: str = "") -> None:
    """A small button that opens the source window on these figures."""
    if not refs:
        return
    if st.button(label or "", key=key, icon=":material/info:", help="Where these figures come from",
                 type="tertiary"):  # fmt: skip
        open_sources(refs, title)


def selection_opens(widget_key: str, refs_for, title_for) -> None:
    """Open the window when a table row or chart point is newly selected. `refs_for(selection)`
    gives the figures, `title_for(selection)` the window's title."""
    state = st.session_state.get(widget_key)
    if not state:
        return
    selection = (
        state.get("selection") if isinstance(state, dict) else getattr(state, "selection", None)
    )
    if not selection:
        return
    marker = repr(selection)
    if st.session_state.get(f"{widget_key}-handled") == marker:
        return
    st.session_state[f"{widget_key}-handled"] = marker
    refs = refs_for(selection)
    if refs:
        open_sources(refs, title_for(selection))
