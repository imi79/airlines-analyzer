"""Airline Credit Tearsheet: the web app (M5).

Run it with `uv run tearsheet app` (or `uv run streamlit run src/tearsheet/app/main.py`).
Five pages: Tearsheet, Peers, Watchlist (M9), Data and audit, Method. Demo mode needs no key
and no database.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import streamlit as st

HERE = Path(__file__).parent


def fresh_code() -> bool:
    """Make sure the code in memory is the code on disk; True if it had to be loaded again.

    The hosting service updates a running app without restarting it: this file and the page
    files are read again on every visit, but the modules they import stay in memory as they
    were. A new page then meets an old module (the M9 deploy: "module ... has no attribute
    'watch_checks'"). So before anything is imported, the app's source and config files are
    compared with what was there when the code in memory was loaded; if a file changed, was
    added or removed, the app's modules and Streamlit's caches are dropped and everything is
    loaded again from the files. Nothing here touches a figure."""
    root = HERE.parents[2]
    files = [*HERE.parent.rglob("*.py"), *HERE.parent.rglob("*.yaml"),
             *(root / "config").glob("*.yaml")]  # fmt: skip
    stamp = (len(files), max(f.stat().st_mtime_ns for f in files))
    # kept outside the app's own modules, so it survives the reload
    loaded = sys.modules.setdefault("_tearsheet_loaded", types.SimpleNamespace(stamp=stamp))
    if loaded.stamp == stamp:
        return False
    loaded.stamp = stamp
    for name in [n for n in sys.modules if n == "tearsheet" or n.startswith("tearsheet.")]:
        del sys.modules[name]
    st.cache_resource.clear()
    st.cache_data.clear()
    return True


fresh_code()

from tearsheet.app import state  # noqa: E402  (after fresh_code, so it is never an old copy)

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
        str(HERE / "views" / "watchlist_page.py"),
        title="Watchlist",
        icon=":material/flag:",
        url_path="watchlist",
    ),
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
