"""Events of the year, read from the annual report by the AI and checked by code (decision
0018, fix D).

The fact sheet holds figures only; the year's story (strikes, grounded aircraft, a buyback, an
acquisition) is not a figure. The AI reads the opening pages of the report and the passages
around event words, and records up to six events: a topic, a short title, a one-sentence
summary with no numbers, and the exact quote. Code then checks, as for the figures of M3:

  1. the quote is in the report word for word (spaces ignored); its location is found by code;
  2. the quote is not overlong;
  3. title and summary contain no number of any kind (the verifier's rule 1);
  4. title and summary are present, the title is short.

Only events that pass reach the fact sheet. Code cannot check that an English summary is a
fair reading of a French or German quote: the quote is kept with the event and printed with
the draft, so the analyst can.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from tearsheet.config import Issuer
from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import DocumentIndex
from tearsheet.extract.locator import Window, _merge_and_cap, find_terms
from tearsheet.extract.numbers import year_marks
from tearsheet.llm import LLM, LLMError, NotRecorded, ToolResult, ToolSpec

HERE = Path(__file__).parent
EVENTS = HERE / "events.yaml"
PROMPT_VERSION = "events-v2"  # bump with every change to the prompt, the form or the request
OPENING_CHARS = 15_000  # the start of the report: letters to shareholders, highlights
MAX_CHARS = 45_000
WINDOWS = 14
BEFORE, AFTER = 500, 700
MAX_EVENTS = 6
MAX_QUOTE = 600
MAX_TITLE_WORDS = 12
NOT_RUN = "events not read yet: no recorded AI answer (run `tearsheet draft`)"


def load_events_config(path: Path = EVENTS) -> dict:
    return yaml.safe_load(path.read_text())


def tool(topics: list[str]) -> ToolSpec:
    event = {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "enum": topics},
            "title": {"type": "string", "description": "At most ten words, no numbers."},
            "summary": {"type": "string", "description": "One sentence, no numbers."},
            "quote": {"type": "string", "description": "One or two sentences, verbatim."},
            "location": {"type": "string"},
        },
        "required": ["topic", "title", "summary", "quote"],
    }
    return ToolSpec(
        name="record_events",
        description="Record the main events of the fiscal year, each with its exact quote.",
        schema={
            "type": "object",
            "properties": {"events": {"type": "array", "maxItems": MAX_EVENTS, "items": event}},
            "required": ["events"],
        },
    )


def system_prompt(version: str = PROMPT_VERSION) -> str:
    return (HERE / "prompts" / f"{version.replace('-', '_')}.md").read_text()


def passages(doc: Document, config: dict) -> str:
    """The opening of the report, then the best windows around event words."""
    terms = list(config["terms"].get(doc.language or "en", []))
    terms += [t for t in config["terms"]["en"] if t not in terms]
    size, first = 0, []
    for p, page in enumerate(doc.pages):
        if size >= OPENING_CHARS:
            break
        take = page[: OPENING_CHARS - size]
        first.append(Window(p, 0, len(take), 100.0, {"opening"}))
        size += len(take)
    candidates = []
    for p, page in enumerate(doc.pages):
        for pos, _ in find_terms(page, terms):
            start = page.rfind("\n", 0, max(0, pos - BEFORE)) + 1
            end = page.find("\n", min(len(page), pos + AFTER))
            end = len(page) if end < 0 else end
            text = page[start:end]
            distinct = len({t for _, t in find_terms(text, terms)})
            score = 2 * distinct + (3 if doc.fiscal_year in {m.year for m in year_marks(text)}
                                    else 0)  # fmt: skip
            candidates.append(Window(p, start, end, score, {"events"}))
    candidates.sort(key=lambda w: -w.score)
    kept: list[Window] = []
    for w in candidates:
        if len(kept) == WINDOWS:
            break
        overlaps = any(
            k.page == w.page and k.start < w.end and w.start < k.end for k in kept + first
        )
        if not overlaps:
            kept.append(w)
    windows = _merge_and_cap(first + kept)
    total, chosen = 0, []
    for w in sorted(windows, key=lambda w: -w.score):  # the opening first, then the best
        if total + (w.end - w.start) > MAX_CHARS:
            continue
        chosen.append(w)
        total += w.end - w.start
    chosen.sort(key=lambda w: (w.page, w.start))
    return "\n\n".join(
        f"=== {doc.location(w.page)} ===\n{doc.pages[w.page][w.start : w.end].strip()}"
        for w in chosen
    )


def user_message(issuer: Issuer, doc: Document, fiscal_label: str, topics: list[str], text: str):
    return "\n".join(
        [
            f"Company: {issuer.name} ({issuer.type}). Report: annual report for {fiscal_label}, "
            f"language: {doc.language or 'en'}.",
            f"Topics: {', '.join(topics)}.",
            "",
            "Passages from the report:",
            "",
            text,
        ]
    )


@dataclass
class Event:
    id: str  # event:labour, event:funding_and_rating-2
    issuer: str
    fiscal_year: int
    topic: str
    title: str
    summary: str
    quote: str
    location: str | None
    document: str
    failures: list[str] = field(default_factory=list)

    @property
    def verified(self) -> bool:
        return not self.failures


@dataclass
class EventsRun:
    issuer: str
    fiscal_year: int
    document: str
    events: list[Event] = field(default_factory=list)
    result: ToolResult | None = None
    error: str | None = None
    retry: ToolResult | None = None
    retry_error: str | None = None


def check_event(raw: dict, index: DocumentIndex, numbers) -> tuple[str | None, list[str]]:
    """(location found by code, reasons it fails). `numbers` is the verifier's rule 1."""
    failures = []
    quote = (raw.get("quote") or "").strip()
    title = (raw.get("title") or "").strip()
    summary = (raw.get("summary") or "").strip()
    location = index.find(quote) if quote else None
    if not quote:
        failures.append("no quote")
    elif location is None:
        failures.append("quote not found word for word in the report")
    if len(quote) > MAX_QUOTE:
        failures.append(f"quote longer than {MAX_QUOTE} characters")
    if not title or not summary:
        failures.append("title or summary missing")
    if len(title.split()) > MAX_TITLE_WORDS:
        failures.append(f"title longer than {MAX_TITLE_WORDS} words")
    for part, text in (("title", title), ("summary", summary)):
        failures += [f"{part}: {m}" for m in numbers(text)]
    return location, failures


def read_events(
    llm: LLM, issuer: Issuer, doc: Document, fiscal_label: str, numbers, config: dict | None = None
) -> EventsRun:
    config = config or load_events_config()
    topics = list(config["topics"])
    run = EventsRun(issuer.id, doc.fiscal_year, doc.doc_id)
    message = user_message(issuer, doc, fiscal_label, topics, passages(doc, config))
    try:
        run.result = llm.call_tool(
            "extraction",
            system_prompt(),
            message,
            tool(topics),
            PROMPT_VERSION,
            label=f"{issuer.id} FY{doc.fiscal_year} events {doc.doc_id}",
        )
    except NotRecorded:
        run.error = NOT_RUN
        return run
    except LLMError as exc:
        run.error = str(exc)
        return run
    index = DocumentIndex(doc)
    raws = list((run.result.arguments.get("events") or [])[:MAX_EVENTS])
    rejected = [
        (n, raw, failures)
        for n, raw in enumerate(raws)
        if isinstance(raw, dict)
        for location, failures in [check_event(raw, index, numbers)]
        if failures and location is not None  # a real quote: only the wording can be fixed
    ]
    if rejected:  # one retry, as for the drafts: rewrite the wording, keep the quote
        lines = [message, "", "# Some events were rejected", "",
                 "Rewrite only the title and summary of each event below so they hold no number "
                 "of any kind. Keep its topic and quote exactly as they are.", ""]  # fmt: skip
        for _, raw, failures in rejected:
            lines.append(json.dumps({k: raw.get(k) for k in ("topic", "title", "summary", "quote")},
                                    ensure_ascii=False))  # fmt: skip
            lines += [f"- {f}" for f in failures]
        try:
            retry = llm.call_tool(
                "extraction",
                system_prompt(),
                "\n".join(lines),
                tool(topics),
                PROMPT_VERSION,
                label=f"{issuer.id} FY{doc.fiscal_year} events retry {doc.doc_id}",
            )
            run.retry = retry
            fixed = {
                " ".join((r.get("quote") or "").split()): r
                for r in retry.arguments.get("events") or []
                if isinstance(r, dict)
            }
            for n, raw, _ in rejected:
                again = fixed.get(" ".join((raw.get("quote") or "").split()))
                if again:
                    raws[n] = raw | {"title": again.get("title"), "summary": again.get("summary")}
        except LLMError as exc:  # NotRecorded included: keep the first answer
            run.retry_error = str(exc)
    seen, counts = set(), {}
    for raw in raws:
        if not isinstance(raw, dict):
            continue
        topic = raw.get("topic") if raw.get("topic") in topics else "other"
        quote = (raw.get("quote") or "").strip()
        if quote in seen:
            continue
        seen.add(quote)
        counts[topic] = counts.get(topic, 0) + 1
        event_id = f"event:{topic}" + (f"-{counts[topic]}" if counts[topic] > 1 else "")
        location, failures = check_event(raw, index, numbers)
        run.events.append(
            Event(
                event_id,
                issuer.id,
                doc.fiscal_year,
                topic,
                " ".join((raw.get("title") or "").split()),
                " ".join((raw.get("summary") or "").split()),
                " ".join(quote.split()),
                location,
                doc.doc_id,
                failures,
            )
        )
    return run
