"""Drafting loop with a stand-in AI: retries only the rejected sections, at most two times,
records every answer, and replays it offline. No network."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import yaml

from tearsheet.llm import LLM, ProviderSettings
from tearsheet.narrative.drafting import (
    MAX_RETRIES,
    draft_commentary,
    rendered_text,
    retry_message,
    tool,
    user_message,
)
from tearsheet.narrative.factsheet import FactSheet, load_narrative
from tearsheet.narrative.verifier import Verifier, parse_sections

FIXTURES = Path(__file__).parent / "fixtures" / "narrative"
SHEET = FactSheet.from_json(FIXTURES / "afkl_FY2025.json")
CORRECT = yaml.safe_load((FIXTURES / "afkl_FY2025_correct.yaml").read_text())
NARRATIVE = load_narrative()
BAD = {"text": "Net leverage stood at 1.71x.", "facts": []}


def answer(sections: dict) -> dict:
    return {
        "model": "model-x",
        "choices": [
            {
                "message": {
                    "tool_calls": [
                        {
                            "function": {
                                "name": "record_commentary",
                                "arguments": json.dumps({"sections": sections}),
                            }
                        }
                    ]
                }
            }
        ],
        "usage": {"prompt_tokens": 9000, "completion_tokens": 1500},
    }


class Server:
    """Answers each request with the next canned form; keeps the requests."""

    def __init__(self, forms: list[dict]):
        self.forms, self.requests = list(forms), []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(json.loads(request.content))
        return httpx.Response(200, json=answer(self.forms.pop(0)))


@pytest.fixture
def make_llm(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_LLM_KEY", "k")
    settings = ProviderSettings(
        "test", "openai_compatible", "https://llm.example", "TEST_LLM_KEY",
        {"drafting": "model-x"}, None,
    )  # fmt: skip

    def make(server: Server | None = None, offline: bool = False) -> LLM:
        http = httpx.Client(transport=httpx.MockTransport(server)) if server else None
        return LLM(settings, records=tmp_path / "records", offline=offline, http=http)

    return make


def with_bad(section: str) -> dict:
    sections = json.loads(json.dumps(CORRECT))
    sections[section][0] = BAD
    return sections


def test_first_try_passes(make_llm):
    server = Server([CORRECT])
    outcome = draft_commentary(make_llm(server), SHEET)
    assert outcome.passed and outcome.first_try_passed
    assert len(outcome.attempts) == 1 and len(server.requests) == 1


def test_retry_asks_only_for_the_rejected_section(make_llm):
    fixed = {"credit_metrics": CORRECT["credit_metrics"]}
    server = Server([with_bad("credit_metrics"), fixed])
    outcome = draft_commentary(make_llm(server), SHEET)
    assert outcome.passed and not outcome.first_try_passed
    second = server.requests[1]
    schema = second["tools"][0]["function"]["parameters"]["properties"]["sections"]
    assert list(schema["properties"]) == ["credit_metrics"]
    assert "number written outside a blank: '1.71x'" in second["messages"][1]["content"]
    assert outcome.sections["snapshot"] == parse_sections(CORRECT)[0].sections["snapshot"]


def test_flagged_after_two_retries(make_llm):
    bad = {"credit_metrics": with_bad("credit_metrics")["credit_metrics"]}
    server = Server([with_bad("credit_metrics"), bad, bad])
    outcome = draft_commentary(make_llm(server), SHEET)
    assert len(outcome.attempts) == 1 + MAX_RETRIES
    assert outcome.status["credit_metrics"] == "needs_manual_editing"
    assert outcome.status["snapshot"] == "passed"
    assert not outcome.passed and outcome.numbers_outside_blanks == 1


def test_records_replay_offline(make_llm):
    draft_commentary(make_llm(Server([with_bad("snapshot"), {"snapshot": CORRECT["snapshot"]}])),
                     SHEET)  # fmt: skip
    replay = draft_commentary(make_llm(offline=True), SHEET)
    assert replay.passed and len(replay.attempts) == 2
    assert all(a.result.cached for a in replay.attempts)


def test_not_drafted_offline_without_record(make_llm):
    outcome = draft_commentary(make_llm(offline=True), SHEET)
    assert not outcome.drafted and not outcome.passed


def test_request_holds_the_fact_sheet_and_sections():
    message = user_message(SHEET, list(NARRATIVE["sections"]), NARRATIVE)
    assert "| net_leverage@FY2025 | Net leverage, FY2025 | 1.71x |" in message
    assert "liquidity@FY2025: not verified yet" in message
    assert "`snapshot` (Snapshot, exactly 3 sentences)" in message
    spec = tool(["snapshot"], NARRATIVE)
    snapshot = spec.schema["properties"]["sections"]["properties"]["snapshot"]
    assert (snapshot["minItems"], snapshot["maxItems"]) == (3, 3)


def test_retry_message_lists_errors_and_previous_text():
    draft, _ = parse_sections(with_bad("snapshot"))
    report = Verifier().check(SHEET, draft, ["snapshot"])
    text = retry_message(SHEET, ["snapshot"], NARRATIVE, draft, report.errors)
    assert "[rule 1] snapshot, sentence 1" in text and "Net leverage stood at 1.71x." in text


def test_rendered_text_keeps_unknown_blanks_visible():
    assert rendered_text("At {{nope@FY2025}}.", SHEET.rendered()) == "At [[nope@FY2025?]]."


def test_score_sheet(make_llm, tmp_path):
    import zipfile

    from tearsheet.narrative import score_sheet

    outcome = draft_commentary(make_llm(Server([CORRECT])), SHEET)
    path = tmp_path / "score.xlsx"
    assert score_sheet.write([outcome] * 10, path)
    names = zipfile.ZipFile(path).namelist()
    assert sum(n.startswith("xl/worksheets/sheet") for n in names) == 11
    assert not score_sheet.has_scores(path)


def test_a_section_left_out_of_a_retry_keeps_its_previous_version(make_llm):
    first = with_bad("credit_metrics")
    first["snapshot"][0] = BAD
    server = Server([first, {"snapshot": CORRECT["snapshot"]}, {}])
    outcome = draft_commentary(make_llm(server), SHEET)
    assert outcome.status["snapshot"] == "passed"
    assert outcome.status["credit_metrics"] == "needs_manual_editing"
    assert outcome.sections["credit_metrics"][0].text == BAD["text"]
    assert any(e.message == "section missing" for e in outcome.errors["credit_metrics"])


def test_review_scores_count_only_for_the_draft_scored(make_llm, tmp_path):
    from tearsheet.narrative import score_sheet

    outcome = draft_commentary(make_llm(Server([CORRECT])), SHEET)
    entry = {"accuracy": 4, "relevance": 3, "concision": 3, "credit_insight": 2, "comment": "x"}
    right = {
        "scored_by": "test",
        "drafts": {SHEET.key: entry | {"draft": SHEET.fingerprint()[:12]}},
    }
    wrong = {"scored_by": "test", "drafts": {SHEET.key: entry | {"draft": "000000000000"}}}
    assert score_sheet.summary([outcome], right) == (1, 3.0)
    assert score_sheet.summary([outcome], wrong) == (0, None)
