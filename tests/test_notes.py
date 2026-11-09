"""The analyst's edits and reviews (M5): figures left unchanged stay traced, typed figures are
flagged, a review needs a reason and a valid value, and the reviews file keeps its notes."""

from __future__ import annotations

import shutil
from datetime import date

import yaml

from tearsheet.narrative.verifier import Verifier
from tearsheet.render import notes

RENDERED = {
    "net_leverage@FY2025": "1.71x",
    "net_leverage.change@FY2025": "0.17x",
    "revenue@FY2025": "EUR 33.0bn",
}


def test_unchanged_figures_go_back_into_their_blanks():
    edited = "Leverage eased by 0.17x to 1.71x on revenue of EUR 33.0bn."
    out = notes.to_blanks(edited, list(RENDERED), RENDERED)
    assert out == (
        "Leverage eased by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} on "
        "revenue of {{revenue@FY2025}}."
    )
    assert notes.untraced(out, set(RENDERED), Verifier()) == []


def test_typed_figure_is_flagged_not_refused():
    edited = "Leverage eased to 1.71x, and we expect 1.5x next year."
    out = notes.to_blanks(edited, list(RENDERED), RENDERED)
    assert "{{net_leverage@FY2025}}" in out
    problems = notes.untraced(out, set(RENDERED), Verifier())
    assert problems and "1.5x" in problems[0]


def test_unknown_blank_is_flagged():
    problems = notes.untraced("Leverage {{made_up@FY2025}}.", set(RENDERED), Verifier())
    assert problems == ["unknown figure {{made_up@FY2025}}"]


def test_note_saved_and_read_back(tmp_path):
    note = notes.empty("afkl", 2025)
    note["analyst_view"] = "Stable outlook; liquidity is the watch point."
    note["edits"] = {"snapshot": {2: {"text": "Edited {{net_leverage@FY2025}}.", "untraced": []}}}
    notes.save(note, "Imane", tmp_path, today=date(2026, 11, 9))
    back = notes.load("afkl", 2025, tmp_path)
    assert back["analyst_view"] == note["analyst_view"]
    assert back["edits"]["snapshot"][2]["text"] == "Edited {{net_leverage@FY2025}}."
    assert back["updated_by"] == "Imane" and back["updated_on"] == "2026-11-09"


def test_review_checks():
    ok = {"action": "approve", "reason": "Page 32", "by": "Imane"}
    assert notes.check_review(ok, "pct") == []
    assert "give a reason" in notes.check_review(ok | {"reason": " "}, "pct")[0]
    wrong = ok | {"action": "correct", "value": "85.6"}
    assert "fraction" in notes.check_review(wrong, "pct")[0]
    assert notes.check_review(ok | {"action": "correct", "value": "0.856"}, "pct") == []
    assert "not a number" in notes.check_review(ok | {"action": "correct", "value": "x"},
                                                "amount")[0]  # fmt: skip


def test_review_appended_to_the_file_with_its_explanations(tmp_path):
    path = tmp_path / "extraction_reviews.yaml"
    shutil.copy(notes.REVIEWS, path)
    before = path.read_text()
    review = {"issuer": "iag", "fiscal_year": 2025, "item": "load_factor", "action": "correct",
              "value": "0.856", "reason": "Page 32, total network", "by": "Imane",
              "on": "2026-11-09"}  # fmt: skip
    notes.add_review(review, path)
    text = path.read_text()
    assert text.startswith(before.split("reviews:")[0])  # the explanations are kept
    saved = yaml.safe_load(text)["reviews"]
    assert saved == [{"issuer": "iag", "fiscal_year": 2025, "item": "load_factor",
                      "action": "correct", "value": 0.856, "by": "Imane", "on": "2026-11-09",
                      "reason": "Page 32, total network"}]  # fmt: skip
    notes.add_review(review | {"item": "passengers", "action": "approve"}, path)
    assert len(yaml.safe_load(path.read_text())["reviews"]) == 2
    try:
        notes.add_review(review, path)
    except ValueError as exc:
        assert "already reviewed" in str(exc)
    else:
        raise AssertionError("a second review of the same figure was accepted")
