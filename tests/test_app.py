"""The web app (M5), run by Streamlit's page tester: no browser, no network.

Checklist item "Demo mode works without a key": every page opens with no API key, no
database and the network blocked, for every pre-built tearsheet.
"""

from __future__ import annotations

import socket
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from tearsheet.config import DB_PATH, ROOT
from tearsheet.llm.settings import load_settings
from tearsheet.render import tearsheet

APP = str(ROOT / "src" / "tearsheet" / "app" / "main.py")
PAGES = [
    "views/peers_page.py", "views/watchlist_page.py", "views/audit_page.py",
    "views/method_page.py",
]  # fmt: skip
TEARSHEETS = tearsheet.available()


@pytest.fixture
def demo(monkeypatch, tmp_path):
    """No key, no database, no network; the reviews file and notes/ cannot be written."""
    from tearsheet.app import state

    monkeypatch.delenv(load_settings().api_key_env, raising=False)
    monkeypatch.setattr(state, "DB_PATH", tmp_path / "no-database.duckdb")

    def refuse(*args, **kwargs):
        raise OSError("network blocked in tests")

    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket.socket, "connect", refuse)
    reviews = (ROOT / "config" / "extraction_reviews.yaml").read_text()
    saved_notes = _snapshot(ROOT / "notes")
    yield
    assert (ROOT / "config" / "extraction_reviews.yaml").read_text() == reviews
    assert _snapshot(ROOT / "notes") == saved_notes  # demo mode writes no note


def _snapshot(folder: Path) -> dict[str, str]:
    """Every file in the folder and its content (the saved analyst notes)."""
    if not folder.exists():
        return {}
    return {p.name: p.read_text() for p in sorted(folder.iterdir()) if p.is_file()}


def run(pick=None, page=None) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    if pick:
        at.session_state["pick"] = pick
    at.run()
    if page:
        at.switch_page(page)
        at.run()
    assert not at.exception, [e.value for e in at.exception]
    return at


@pytest.mark.parametrize("pick", TEARSHEETS)
def test_every_tearsheet_opens_in_demo_mode(demo, pick):
    at = run(pick)
    assert at.title[0].value
    assert [s.value for s in at.subheader][:1] == ["Snapshot"]
    assert len(at.metric) >= 4
    assert not at.error
    text = " ".join(m.value for m in at.markdown)
    assert "{{" not in text  # every blank was filled by code
    assert "Not investment advice" in " ".join(c.value for c in at.caption)


@pytest.mark.parametrize("page", PAGES)
def test_other_pages_open_in_demo_mode(demo, page):
    at = run(("easyjet", 2025), page)
    assert at.title[0].value in ("Peers", "Watchlist", "Data and audit", "Method")
    assert not at.error


def test_no_live_mode_without_the_database(demo):
    at = run()
    assert not [r for r in at.radio if r.label == "Mode"]


def test_source_button_opens_the_card(demo):
    at = run(("afkl", 2025))
    at.button(key="kpi-net_leverage").click().run()
    assert not at.exception
    text = " ".join(m.value for m in at.markdown)
    assert "Net debt" in text and "Built from" in text


def test_demo_review_lasts_for_the_session_only(demo):
    at = run(("afkl", 2025), "views/audit_page.py")
    form_inputs = [t for t in at.text_input if t.label == "Reason"]
    assert form_inputs, "no figure awaiting review for Air France-KLM"
    form_inputs[0].input("Checked on page 15 of the FY2025 statements")
    at.button[[b.label for b in at.button].index("Save the review")].click().run()
    assert not at.exception
    reviews = at.session_state["demo_reviews"]
    assert len(reviews) == 1
    assert next(iter(reviews.values()))["action"] == "approve"


def test_review_without_reason_is_refused(demo):
    at = run(("afkl", 2025), "views/audit_page.py")
    at.button[[b.label for b in at.button].index("Save the review")].click().run()
    assert any("give a reason" in e.value for e in at.error)
    assert "demo_reviews" not in at.session_state or not at.session_state["demo_reviews"]


def test_edited_sentence_with_a_typed_figure_is_flagged(demo):
    at = run(("afkl", 2025))
    at.toggle(key="editing-afkl-2025").set_value(True).run()
    area = at.text_area(key="ta-afkl-2025-snapshot-2")
    area.input(area.value + " We expect leverage near 1.5x next year.")
    labels = [b.label for b in at.button]
    at.button[labels.index("Save this section")].click().run()  # the snapshot's form
    assert not at.exception
    assert any("not traced to a source" in w.value for w in at.warning)
    note = at.session_state["notes"]["afkl_FY2025"]
    edit = note["edits"]["snapshot"][2]
    assert "{{net_leverage@FY2025}}" in edit["text"]  # the original figure stays traced
    assert edit["untraced"]


@pytest.mark.skipif(not Path(DB_PATH).exists(), reason="live mode needs the database")
def test_live_mode_opens_from_the_database(monkeypatch):
    monkeypatch.delenv("TEARSHEET_DEMO_ONLY", raising=False)
    at = AppTest.from_file(APP, default_timeout=120)
    at.session_state["mode"] = "Live"
    at.session_state["pick"] = ("vie", 2025)
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    assert at.title[0].value == "Flughafen Wien"
    assert not at.warning  # the drafts match the database's figures


def test_demo_approval_clears_the_ratios_built_on_the_figure():
    from tearsheet.app.state import with_session_reviews
    from tearsheet.render.library import Library

    lib = Library.read()
    k = "afkl:undrawn_facilities@FY2025"
    assert lib.figures[k]["status"] == "unverified"
    assert lib.figures["afkl:liquidity_to_revenue@FY2025"]["status"] == "unverified"
    review = {"action": "approve", "reason": "page 15", "by": "Imane"}
    after = with_session_reviews(lib, {k: review})
    assert after.figures[k]["status"] == "overridden"
    assert after.figures["afkl:liquidity@FY2025"]["status"] == "verified"
    assert after.figures["afkl:liquidity_to_revenue@FY2025"]["status"] == "verified"
    assert lib.figures[k]["status"] == "unverified"  # the shared library is untouched


def test_a_link_opens_the_named_tearsheet(demo):
    at = AppTest.from_file(APP, default_timeout=60)
    at.query_params["company"] = "wizz"
    at.query_params["year"] = "2026"
    at.run()
    assert not at.exception
    assert at.title[0].value == "Wizz Air Holdings"
    assert "Apr 2025 to Mar 2026" in at.markdown[0].value or any(
        "Apr 2025 to Mar 2026" in m.value for m in at.markdown
    )


def test_demo_shows_the_analysts_saved_edits_and_view(demo):
    """Demo mode starts from the analyst's committed notes (M8, at Imane's request)."""
    at = run(("finnair", 2025))
    assert not at.exception, [e.value for e in at.exception]
    sentence = [m.value for m in at.markdown if "liquidity covers them" in m.value]
    assert sentence and "edited by the analyst" in sentence[0]
    assert "17.39x" in sentence[0] and "times" not in sentence[0]
    at = run(("easyjet", 2025))
    note = at.session_state["notes"]["easyjet_FY2025"]
    assert note["analyst_view"].startswith("The strongest balance sheet")


def test_demo_export_includes_the_session_and_saves_nothing(demo):
    """Demo mode: the PDF and Excel carry the visitor's analyst view; no file is written."""
    from tearsheet.render.export import EXPORTS

    before = set(EXPORTS.glob("*")) if EXPORTS.exists() else set()
    at = run(("vie", 2025))
    form = [t for t in at.text_area if t.label == "Your view"][0]
    form.input("Stable credit; liquidity ample.")
    labels = [b.label for b in at.button]
    at.button[labels.index("Save the analyst view")].click().run()
    labels = [b.label for b in at.button]
    at.button[labels.index("Prepare the PDF and the Excel backup")].click().run()
    assert not at.exception, [e.value for e in at.exception]
    done = at.session_state["export-vie-2025"]
    assert done.pdf.startswith(b"%PDF") and done.xlsx[:2] == b"PK"
    assert done.manifest["mode"] == "demo" and done.manifest["analyst"]["analyst_view"]
    assert len(at.get("download_button")) == 3
    after = set(EXPORTS.glob("*")) if EXPORTS.exists() else set()
    assert after == before


def test_try_the_verifier_on_the_method_page(demo):
    at = run(("afkl", 2025), "views/method_page.py")
    at.selectbox(key="verifier-example-afkl-2025").set_value(1).run()  # the wrong direction
    at.button(key="verifier-check-afkl-2025").click().run()
    assert not at.exception
    assert at.error and "Rejected" in at.error[0].value
    assert any("Rule 4" in m.value for m in at.markdown)


def test_audit_page_shows_the_rejected_attempts(demo):
    at = run(("easyjet", 2025), "views/audit_page.py")
    assert any(e.label.startswith("Try 1:") and "rejected" in e.label for e in at.expander)


def test_the_flagged_snapshots_show_the_analysts_fixes(demo):
    """Finnair FY2024, Wizz Air FY2025, Aena FY2024: the rejected sentences were rewritten by
    Imane's edits (M8), so the snapshots no longer carry the verifier's warning."""
    for pick in (("finnair", 2024), ("wizz", 2025), ("aena", 2024)):
        at = run(pick)
        assert not any("failed the verifier" in w.value for w in at.warning), pick
        assert any("edited by the analyst" in m.value for m in at.markdown), pick


# --- The watchlist (M9) ----------------------------------------------------------------------


def test_tearsheet_shows_the_watchlist_line(demo):
    at = run(("adp", 2025))
    captions = [c.value for c in at.caption]
    assert any(c.startswith("Watchlist: 1 trigger fired (net leverage above 3.0x)")
               for c in captions), captions  # fmt: skip
    at.button(key="watch-line").click().run()
    assert not at.exception
    text = " ".join(m.value for m in at.markdown)
    assert "Watchlist trigger" in text and "Built from" in text and "3.68x" in text


def test_watchlist_page_lists_fired_triggers_with_their_sources(demo):
    at = run(("adp", 2025), "views/watchlist_page.py")
    assert at.title[0].value == "Watchlist"
    text = " ".join(m.value for m in at.markdown)
    assert "Groupe ADP FY2025** · Net leverage above 3.0x" in text
    at.button(key="watch-adp-net_leverage_high").click().run()
    assert not at.exception
    text = " ".join(m.value for m in at.markdown)
    assert "Why it matters" in text and "Built from" in text


def test_watchlist_page_filters_new_warnings(demo):
    at = run(("adp", 2025), "views/watchlist_page.py")
    at.radio(key="watch-filter").set_value("With a new warning").run()
    assert not at.exception
    text = " ".join(m.value for m in at.markdown)
    assert "new: clear the year before" in text  # Vienna FY2025, EBITDA margin
    assert "Groupe ADP" not in text  # fired in FY2024 too: not new


def test_demo_approval_reaches_the_watchlist():
    """Approving Air France-KLM's undrawn lines (session only) lets the liquidity trigger use
    liquidity itself instead of the cash floor."""
    from tearsheet import watchlist
    from tearsheet.app.state import with_session_reviews
    from tearsheet.render.library import Library

    lib = Library.read()
    t = watchlist.by_id()["liquidity_low"]
    before = watchlist.check(lib, t, "afkl", 2025)
    assert before.keys == ("afkl:cash_liquidity_to_revenue@FY2025",)
    review = {"action": "approve", "reason": "page 15", "by": "Imane"}
    after = with_session_reviews(lib, {"afkl:undrawn_facilities@FY2025": review})
    now = watchlist.check(after, t, "afkl", 2025)
    assert now.status == "clear" and now.keys == ("afkl:liquidity_to_revenue@FY2025",)


def test_a_hot_update_reloads_the_code_in_memory(demo):
    """The hosting service updates a running app without restarting it (the M9 deploy broke on
    an old module kept in memory). When the files no longer match what was loaded, the app
    drops its modules and loads them again before drawing the page."""
    import sys

    run(("adp", 2025))  # the app has run once: the loaded code is on record
    before = {
        n: m for n, m in sys.modules.items() if n == "tearsheet" or n.startswith("tearsheet.")
    }
    try:
        sys.modules["_tearsheet_loaded"].stamp = (0, 0)  # as if a file had changed since
        at = run(("adp", 2025))
        assert at.title[0].value == "Groupe ADP"
        assert sys.modules["tearsheet.render.tearsheet"] is not before["tearsheet.render.tearsheet"]
        assert sys.modules["tearsheet.app.state"] is not before["tearsheet.app.state"]
        assert sys.modules["_tearsheet_loaded"].stamp != (0, 0)
        again = sys.modules["tearsheet.render.tearsheet"]
        run(("adp", 2025))  # nothing changed since: no second reload
        assert sys.modules["tearsheet.render.tearsheet"] is again
    finally:  # the other tests keep the modules they imported
        for name in [n for n in sys.modules if n == "tearsheet" or n.startswith("tearsheet.")]:
            del sys.modules[name]
        sys.modules.update(before)
