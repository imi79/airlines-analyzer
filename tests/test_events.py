"""Events of the year (decision 0018, fix D): code checks each quote and keeps numbers out of
the summary; the drafting verifier lets a sentence cite an event by id, never as a blank."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from tearsheet.config import load_issuers
from tearsheet.extract import events as ev
from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import DocumentIndex
from tearsheet.llm import LLM, ProviderSettings
from tearsheet.narrative.factsheet import FactSheet, add_events, as_text
from tearsheet.narrative.verifier import Ref, Sentence, Verifier

FIXTURES = Path(__file__).parent / "fixtures" / "narrative"
V = Verifier()
FINNAIR = next(i for i in load_issuers() if i.id == "finnair")
PAGES = (
    "Review of the year. The prolonged industrial action during the first half of the year "
    "had an immediate negative impact of approximately 68 million euros on the comparable "
    "operating result.",
    "Finnair signed a new revolving credit facility with a group of banks in June.",
)
STRIKE = {
    "topic": "labour",
    "title": "Prolonged industrial action in the first half",
    "summary": "Strikes in the first half cut the comparable operating result.",
    "quote": "The prolonged industrial action during the first half of the year had an "
    "immediate negative impact of approximately 68 million euros on the comparable operating "
    "result.",
}


def doc() -> Document:
    return Document("rep-2025", "finnair", 2025, "en", "test", "test", None, PAGES, "page")


def test_quote_found_and_summary_without_numbers_is_checked():
    location, failures = ev.check_event(STRIKE, DocumentIndex(doc()), V.numbers)
    assert failures == [] and location == "page 1"


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        ({"quote": "Strikes cost the company dearly in the spring."}, "not found word for word"),
        ({"summary": "Strikes cut the operating result by 68 million euros."}, "summary"),
        ({"title": "A record strike"}, "title"),
        ({"summary": "Strikes cut the result by about a third."}, "summary"),
        ({"quote": "x" * 700}, "longer than"),
        ({"title": ""}, "missing"),
    ],
)
def test_bad_event_is_not_checked(change, reason):
    _, failures = ev.check_event(STRIKE | change, DocumentIndex(doc()), V.numbers)
    assert any(reason in f for f in failures), failures


def answer(events: list[dict]) -> dict:
    call = {"function": {"name": "record_events", "arguments": json.dumps({"events": events})}}
    return {
        "model": "model-x",
        "choices": [{"message": {"tool_calls": [call]}}],
        "usage": {"prompt_tokens": 5000, "completion_tokens": 400},
    }


@pytest.fixture
def make_llm(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_LLM_KEY", "k")
    settings = ProviderSettings(
        "test", "openai_compatible", "https://llm.example", "TEST_LLM_KEY",
        {"extraction": "model-x"}, None,
    )  # fmt: skip

    def make(events: list[dict] | None = None, offline: bool = False) -> LLM:
        http = None
        if events is not None:
            reply = httpx.Response(200, json=answer(events))
            http = httpx.Client(transport=httpx.MockTransport(lambda request: reply))
        return LLM(settings, records=tmp_path / "records", offline=offline, http=http)

    return make


def test_read_events_checks_and_names_each_event(make_llm):
    funding = {
        "topic": "funding_and_rating",
        "title": "New revolving credit facility",
        "summary": "A new committed bank line supports liquidity.",
        "quote": "Finnair signed a new revolving credit facility with a group of banks in June.",
    }
    made_up = STRIKE | {"topic": "labour", "quote": "Pilots walked out for months."}
    run = ev.read_events(make_llm([STRIKE, funding, made_up]), FINNAIR, doc(), "FY2025", V.numbers)
    assert [e.id for e in run.events] == ["event:labour", "event:funding_and_rating",
                                          "event:labour-2"]  # fmt: skip
    assert [e.verified for e in run.events] == [True, True, False]
    replay = ev.read_events(make_llm(offline=True), FINNAIR, doc(), "FY2025", V.numbers)
    assert [e.id for e in replay.events] == [e.id for e in run.events]
    assert replay.result.cached


def test_not_read_offline_without_record(make_llm):
    run = ev.read_events(make_llm(offline=True), FINNAIR, doc(), "FY2025", V.numbers)
    assert run.error == ev.NOT_RUN and run.events == []


def test_passages_start_with_the_opening_and_find_event_words():
    text = ev.passages(doc(), ev.load_events_config())
    assert text.startswith("=== page 1 ===") and "revolving credit facility" in text


@pytest.fixture
def sheet_with_event() -> FactSheet:
    sheet = FactSheet.from_json(FIXTURES / "afkl_FY2025.json")
    event = ev.Event("event:labour", "afkl", 2025, "labour", STRIKE["title"], STRIKE["summary"],
                     STRIKE["quote"], "page 1", "rep-2025")  # fmt: skip
    rejected = ev.Event("event:other", "afkl", 2025, "other", "x", "y", "z", None, "rep", ["no"])
    add_events(sheet, [event, rejected])
    return sheet


def test_only_checked_events_reach_the_fact_sheet(sheet_with_event):
    assert "event:labour" in sheet_with_event.items
    assert "event:other" not in sheet_with_event.items
    assert "Events of the year" in as_text(sheet_with_event)


def check(sheet, text, *refs):
    facts = tuple(Ref(i, tuple(c)) for i, *c in refs)
    return V.check_sentence(sheet, Sentence(text, facts))


def test_a_sentence_may_cite_an_event_by_id(sheet_with_event):
    assert not check(
        sheet_with_event,
        "Strikes in the first half weighed on the operating result of {{operating_profit@FY2025}}.",
        ("event:labour",),
        ("operating_profit@FY2025",),
    )


def test_an_event_is_never_a_blank_and_carries_no_claim(sheet_with_event):
    blank = check(sheet_with_event, "Strikes: {{event:labour}}.", ("event:labour",))
    assert any(rule == "5" for rule, _ in blank)
    claim = check(sheet_with_event, "Strikes worsened.", ("event:labour", "worse"))
    assert any(rule == "3" for rule, _ in claim)


def test_unchecked_event_cannot_be_cited(sheet_with_event):
    found = check(sheet_with_event, "Something happened.", ("event:other",))
    assert any(rule == "2" for rule, _ in found)


def test_event_rejected_on_wording_is_retried_once(tmp_path, monkeypatch):
    monkeypatch.setenv("TEST_LLM_KEY", "k")
    settings = ProviderSettings(
        "test", "openai_compatible", "https://llm.example", "TEST_LLM_KEY",
        {"extraction": "model-x"}, None,
    )  # fmt: skip
    with_number = STRIKE | {"summary": "Strikes cut the result by 68 million euros."}
    replies = [answer([with_number]), answer([STRIKE])]
    seen = []

    def server(request):
        seen.append(json.loads(request.content))
        return httpx.Response(200, json=replies.pop(0))

    llm = LLM(settings, records=tmp_path, http=httpx.Client(transport=httpx.MockTransport(server)))
    run = ev.read_events(llm, FINNAIR, doc(), "FY2025", V.numbers)
    assert len(seen) == 2 and "Some events were rejected" in seen[1]["messages"][1]["content"]
    assert [e.verified for e in run.events] == [True]
    assert run.events[0].summary == STRIKE["summary"]
