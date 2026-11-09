"""Editing the commentary and writing the analyst view (saved in live mode only)."""

from __future__ import annotations

import streamlit as st

from tearsheet.app import state
from tearsheet.narrative.verifier import Verifier
from tearsheet.render import notes, tearsheet


@st.cache_resource(show_spinner=False)
def _verifier() -> Verifier:
    return Verifier()


def get_note(ts: dict) -> dict:
    """The analyst's note for this tearsheet: from the session, else from notes/ (live)."""
    store = st.session_state.setdefault("notes", {})
    k = f"{ts['issuer']}_FY{ts['fiscal_year']}"
    if k not in store:
        store[k] = (
            notes.load(ts["issuer"], ts["fiscal_year"])
            if state.mode() == state.LIVE
            else notes.empty(ts["issuer"], ts["fiscal_year"])
        )
    return store[k]


def _persist(note: dict) -> None:
    if state.mode() == state.LIVE:
        path = notes.save(note, tearsheet.load_app_config()["analyst"])
        st.toast(f"Saved to {path.relative_to(path.parents[1])}")
    else:
        st.toast("Kept for this session (demo mode saves nothing)")


def edited_sentence(ts: dict, section: str, n: int, sentence: dict) -> tuple[str, str, bool]:
    """(text with blanks, flag text or "", edited?) for one sentence."""
    edit = get_note(ts)["edits"].get(section, {}).get(n)
    if edit is None:
        return sentence["text_blanks"], "", False
    flag = notes.UNTRACED if edit.get("untraced") else ""
    return edit["text"], flag, True


def edit_section(lib, ts: dict, name: str, section: dict, rendered: dict[str, str]) -> None:
    note = get_note(ts)
    with st.form(f"edit-{ts['issuer']}-{ts['fiscal_year']}-{name}", border=False):
        texts = []
        for n, sentence in enumerate(section["sentences"], start=1):
            current, _, _ = edited_sentence(ts, name, n, sentence)
            texts.append(st.text_area(f"Sentence {n}", notes.fill(current, rendered),
                                      key=f"ta-{ts['issuer']}-{ts['fiscal_year']}-{name}-{n}",
                                      height=90))  # fmt: skip
        saved = st.form_submit_button("Save this section")
    if not saved:
        return
    known = set(ts["factsheet"]["items"])
    changed = note["edits"].setdefault(name, {})
    flagged = []
    for n, (sentence, text) in enumerate(zip(section["sentences"], texts, strict=True), start=1):
        ids = [f["id"] for f in sentence["facts"]]
        if text.strip() == notes.fill(sentence["text_blanks"], rendered).strip():
            changed.pop(n, None)  # back to the AI's text
            continue
        blanks = notes.to_blanks(text.strip(), ids, rendered)
        problems = notes.untraced(blanks, known, _verifier())
        changed[n] = {"text": blanks, "untraced": problems}
        if problems:
            flagged.append((n, problems))
    if not changed:
        note["edits"].pop(name, None)
    _persist(note)
    for n, problems in flagged:
        st.warning(f"Sentence {n} {notes.UNTRACED}: " + "; ".join(problems))


def analyst_view(ts: dict) -> None:
    note = get_note(ts)
    st.subheader("Analyst view")
    st.caption("Written by the analyst only: never drafted by the AI.")
    with st.form(f"view-{ts['issuer']}-{ts['fiscal_year']}", border=False):
        text = st.text_area("Your view", note.get("analyst_view") or "", height=160,
                            label_visibility="collapsed",
                            placeholder="Your credit view on this issuer.")  # fmt: skip
        if st.form_submit_button("Save the analyst view"):
            note["analyst_view"] = text
            _persist(note)
