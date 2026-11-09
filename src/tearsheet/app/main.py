"""Airline Credit Tearsheet: the web app (M5).

Run it with `uv run tearsheet app` (or `uv run streamlit run src/tearsheet/app/main.py`).
Four pages: Tearsheet, Peers, Data and audit, Method. Demo mode needs no key and no database.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from tearsheet.app import state

HERE = Path(__file__).parent

st.set_page_config(page_title="Airline Credit Tearsheet", page_icon=":material/flight:",
                   layout="wide")  # fmt: skip

pages = [
    st.Page(
        str(HERE / "views" / "tearsheet_page.py"),
        title="Tearsheet",
        icon=":material/description:",
        default=True,
    ),  # fmt: skip
    st.Page(str(HERE / "views" / "peers_page.py"), title="Peers", icon=":material/groups:"),
    st.Page(
        str(HERE / "views" / "audit_page.py"), title="Data and audit", icon=":material/fact_check:"
    ),  # fmt: skip
    st.Page(str(HERE / "views" / "method_page.py"), title="Method", icon=":material/menu_book:"),
]
page = st.navigation(pages)

with st.sidebar:
    st.markdown("### Airline Credit Tearsheet")
    if state.live_possible():
        st.radio(
            "Mode",
            [state.DEMO, state.LIVE],
            key="mode",
            horizontal=True,
            help="Demo: pre-built tearsheets, nothing saved. Live: the facts database; your "
            "edits and reviews are saved.",
        )
    else:
        st.caption("Demo mode: pre-built tearsheets, no API key needed.")
    lib = state.base_library()
    options = state.choices()
    state.current()
    st.selectbox(
        "Company and year",
        options,
        key="pick",
        format_func=lambda p: state.label_pick(lib, p),
    )
    if state.mode() == state.DEMO:
        st.caption("Edits and reviews last for this session only.")

page.run()
