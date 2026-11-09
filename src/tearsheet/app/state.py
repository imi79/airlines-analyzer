"""What the app is looking at: the mode, the company and year, and the figures behind them.

Demo mode reads the pre-built files in samples/ and saves nothing. Live mode reads the facts
database and saves the analyst's work (decision 0019). The public link is demo only (approved
plan, question 4): live mode is offered only where the database exists, and never when
TEARSHEET_DEMO_ONLY is set.
"""

from __future__ import annotations

import copy
import os
from decimal import Decimal

import streamlit as st

from tearsheet.config import DB_PATH, load_issuers
from tearsheet.narrative import render
from tearsheet.render import library, tearsheet
from tearsheet.render.library import Library

DEMO, LIVE = "Demo", "Live"


def live_possible() -> bool:
    return DB_PATH.exists() and os.environ.get("TEARSHEET_DEMO_ONLY", "") not in ("1", "true")


def mode() -> str:
    m = st.session_state.get("mode", DEMO)
    return m if m == DEMO or live_possible() else DEMO


# --- Loading (cached: a pre-built tearsheet opens in well under ten seconds) ------------------


def _mtime(path) -> float:
    return path.stat().st_mtime if path.exists() else 0.0


@st.cache_resource(show_spinner=False)
def _demo_library(stamp: float) -> Library:
    return Library.read(library.FIGURES_FILE)


@st.cache_resource(show_spinner=False)
def _live_library(stamp: float) -> Library:
    return library.from_database(DB_PATH)


@st.cache_data(show_spinner=False)
def _demo_tearsheet(issuer: str, year: int, stamp: float) -> dict:
    return tearsheet.read(issuer, year)


@st.cache_data(show_spinner=False)
def _live_tearsheet(issuer: str, year: int, stamp: float) -> dict:
    return tearsheet.live_record(DB_PATH, issuer, year)


def base_library() -> Library:
    if mode() == LIVE:
        return _live_library(_mtime(DB_PATH))
    return _demo_library(_mtime(library.FIGURES_FILE))


def get_library() -> Library:
    """The library, with this session's demo reviews applied (never saved)."""
    lib = base_library()
    reviews = st.session_state.get("demo_reviews") or {}
    if mode() == DEMO and reviews:
        return with_session_reviews(lib, reviews)
    return lib


def get_tearsheet(issuer: str, year: int) -> dict:
    if mode() == LIVE:
        return _live_tearsheet(issuer, year, _mtime(DB_PATH))
    return _demo_tearsheet(
        issuer, year, _mtime(tearsheet.TEARSHEETS / tearsheet.file_name(issuer, year))
    )


def choices() -> list[tuple[str, int]]:
    """(company, year) pairs the picker offers."""
    if mode() == LIVE:
        lib = base_library()
        order = [i.id for i in load_issuers()]
        return [(i, y) for i in order for y in reversed(lib.years(i))]
    return tearsheet.available()


def current() -> tuple[str, int]:
    """The company and year on screen. A link can name them: ?company=wizz&year=2026."""
    options = choices()
    picked = st.session_state.get("pick")
    if picked is None:
        try:
            asked = (st.query_params.get("company"), int(st.query_params.get("year", "0")))
        except ValueError:
            asked = None
        picked = asked if asked in options else None
    if picked not in options:
        picked = options[0]
    if st.session_state.get("pick") != picked:  # set before the picker is drawn
        st.session_state["pick"] = picked
    if (st.query_params.get("company"), st.query_params.get("year")) != (
        picked[0],
        str(picked[1]),
    ):
        st.query_params.update(company=picked[0], year=str(picked[1]))
    return picked


# --- Demo reviews: kept in the session only ---------------------------------------------------


def with_session_reviews(lib: Library, reviews: dict[str, dict]) -> Library:
    """A copy of the library with the session's approvals and corrections. An approval also
    clears the figures computed from it, if all their other inputs are verified; a correction
    changes only the figure itself (ratios are recomputed in live mode)."""
    lib = copy.copy(lib)
    lib.figures = dict(lib.figures)
    for k, review in reviews.items():
        f = lib.figures.get(k)
        if f is None:
            continue
        f = dict(f)
        f["status"] = "overridden"
        f["session_review"] = review
        if review["action"] == "correct":
            value = Decimal(str(review["value"]).replace(",", ""))
            f["value"] = str(value)
            f["rendered"] = render.value_text(value, f["unit"], f["currency"])
        lib.figures[k] = f
    approved = {k for k, r in reviews.items() if r["action"] == "approve"}
    changed = True
    while changed:  # follow approvals up through the figures computed from them
        changed = False
        for k, f in lib.figures.items():
            links = f.get("input_keys") or []
            if f["status"] != "unverified" or not links or not any(x in approved for x in links):
                continue
            if all(x and lib.usable(x) for x in links):
                f = dict(f)
                f["status"] = "verified"
                lib.figures[k] = f
                approved.add(k)
                changed = True
    return lib


def name_of(lib: Library, issuer: str) -> str:
    return lib.issuers.get(issuer, {}).get("name", issuer)


def label_pick(lib: Library, pick: tuple[str, int]) -> str:
    issuer, year = pick
    return f"{name_of(lib, issuer)} · {lib.period_label(issuer, year)}"
