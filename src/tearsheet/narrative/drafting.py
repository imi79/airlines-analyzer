"""Drafting: the AI fills a form of sentences with blanks; the verifier reads every sentence.

One request per company and year, answered through the form `record_commentary`. Sections the
verifier rejects go back to the AI with the list of errors, up to two more times; a section
still rejected after that is kept, flagged "needs manual editing", and never shown as a
finished draft. Every answer is recorded (records/llm/), so a rerun replays it for free.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from tearsheet.llm import LLM, LLMError, NotRecorded, ToolResult, ToolSpec
from tearsheet.narrative.factsheet import FactSheet, as_text, load_narrative
from tearsheet.narrative.render import PLACEHOLDER
from tearsheet.narrative.verifier import CLAIMS, Draft, Error, Report, Verifier, parse_sections

HERE = Path(__file__).parent
PROMPTS = HERE / "prompts"
EXAMPLES = HERE / "examples"
PROMPT_VERSION = "draft-v6"  # bump with every change to the prompt, examples, form or request
MAX_RETRIES = 2  # spec: up to two retries with the error list fed back
NOT_RUN = "not drafted yet: no recorded AI answer (run `tearsheet draft`)"


# --- The request ---------------------------------------------------------------------------


def load_examples(folder: Path = EXAMPLES) -> list[dict]:
    return [yaml.safe_load(p.read_text()) for p in sorted(folder.glob("*.yaml"))]


def examples_text(examples: list[dict], narrative: dict) -> str:
    out = []
    for ex in examples:
        out.append(f"## Example: {ex['issuer']} FY{ex['fiscal_year']}")
        for name, sentences in ex["sections"].items():
            out += ["", f"### {narrative['sections'][name]['title']} (`{name}`)"]
            for s in sentences:
                facts = [{"id": f["id"], "claims": f.get("claims") or []} for f in s["facts"]]
                line = {"text": " ".join(s["text"].split()), "facts": facts}
                out.append(json.dumps(line, ensure_ascii=False))
        out.append("")
    return "\n".join(out)


def system_prompt(version: str = PROMPT_VERSION, narrative: dict | None = None) -> str:
    narrative = narrative or load_narrative()
    template = (PROMPTS / f"{version.replace('-', '_')}.md").read_text()
    return template.replace("{examples}", examples_text(load_examples(), narrative))


def tool(sections: list[str], narrative: dict) -> ToolSpec:
    sentence = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "One sentence, figures as {{id}} blanks."},
            "facts": {
                "type": "array",
                "description": "Every id used in the text, once, with the claims made on it.",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "claims": {"type": "array", "items": {"type": "string", "enum": CLAIMS}},
                    },
                    "required": ["id", "claims"],
                },
            },
        },
        "required": ["text", "facts"],
    }
    props = {}
    for name in sections:
        low, high = narrative["sections"][name]["sentences"]
        props[name] = {
            "type": "array",
            "minItems": low,
            "maxItems": high,
            "description": narrative["sections"][name]["title"],
            "items": sentence,
        }
    return ToolSpec(
        name="record_commentary",
        description="Record the tearsheet commentary, section by section, with blanks for figures.",
        schema={
            "type": "object",
            "properties": {
                "sections": {"type": "object", "properties": props, "required": list(sections)}
            },
            "required": ["sections"],
        },
    )


def user_message(sheet: FactSheet, sections: list[str], narrative: dict) -> str:
    lines = [
        f"Company: {sheet.name} ({sheet.type}). Fiscal year: {sheet.period_label}. "
        f"Reporting currency: {sheet.currency}.",
        "",
        "Sections to draft:",
    ]
    for name in sections:
        s = narrative["sections"][name]
        low, high = s["sentences"]
        count = f"exactly {low}" if low == high else f"{low} to {high}"
        lines.append(f"- `{name}` ({s['title']}, {count} sentences): {s['purpose'].strip()}")
    lines += ["", as_text(sheet, narrative)]
    return "\n".join(lines)


def retry_message(
    sheet: FactSheet,
    sections: list[str],
    narrative: dict,
    previous: Draft,
    errors: list[Error],
    accepted: dict[str, list] | None = None,
) -> str:
    lines = [
        user_message(sheet, sections, narrative),
        "# Your previous draft of these sections was rejected",
        "",
        "Return the sections below in full. Rewrite only the sentences named in the errors and "
        "keep every other sentence word for word; a sentence that breaks a rule is never "
        "accepted. The verifier's errors:",
        "",
    ]
    lines += [f"- {e}" for e in errors]
    lines += ["", "Your previous draft:", ""]
    for name in sections:
        lines.append(f"`{name}`:")
        for s in previous.sections.get(name, []):
            facts = [{"id": r.id, "claims": list(r.claims)} for r in s.facts]
            lines.append(json.dumps({"text": s.text, "facts": facts}, ensure_ascii=False))
        lines.append("")
    if accepted:
        lines += [
            "The sections already accepted, for reference only (do not rewrite them; a figure "
            "they give in a body section must not be given again in another body section):",
            "",
        ]
        for name, sentences in accepted.items():
            lines.append(f"`{name}`: " + " ".join(s.text for s in sentences))
        lines.append("")
    return "\n".join(lines)


# --- Drafting with retries -----------------------------------------------------------------


@dataclass
class Attempt:
    number: int  # 1 = first try
    sections: list[str]
    result: ToolResult | None = None
    draft: Draft | None = None
    report: Report | None = None
    error: str | None = None


@dataclass
class Outcome:
    sheet: FactSheet
    attempts: list[Attempt] = field(default_factory=list)
    sections: dict[str, list] = field(default_factory=dict)  # final sentences per section
    status: dict[str, str] = field(default_factory=dict)  # passed | needs_manual_editing
    errors: dict[str, list[Error]] = field(default_factory=dict)  # remaining, per section
    not_run: str | None = None
    removed: dict[str, list[tuple[str, list[str]]]] = field(default_factory=dict)  # text, why

    @property
    def drafted(self) -> bool:
        return self.not_run is None

    @property
    def sentences_removed(self) -> int:
        return sum(len(v) for v in self.removed.values())

    @property
    def passed(self) -> bool:
        return self.drafted and all(v == "passed" for v in self.status.values())

    @property
    def first_try_passed(self) -> bool:
        first = self.attempts[0] if self.attempts else None
        return bool(first and first.report and first.report.ok)

    @property
    def numbers_outside_blanks(self) -> int:
        """Rule 1 errors left in the final draft (gate 2 counts drafts where this is zero)."""
        return sum(e.rule == "1" for errs in self.errors.values() for e in errs)

    def draft(self) -> Draft:
        return Draft(self.sections)

    def input_hash(self) -> str:
        return self.sheet.fingerprint()


def draft_commentary(
    llm: LLM,
    sheet: FactSheet,
    verifier: Verifier | None = None,
    narrative: dict | None = None,
    retries: int = MAX_RETRIES,
) -> Outcome:
    narrative = narrative or load_narrative()
    verifier = verifier or Verifier(narrative)
    system = system_prompt(narrative=narrative)
    outcome = Outcome(sheet)
    ask = list(narrative["sections"])
    previous: Draft | None = None
    previous_errors: list[Error] = []
    for number in range(1, retries + 2):
        attempt = Attempt(number, list(ask))
        outcome.attempts.append(attempt)
        if number == 1:
            message = user_message(sheet, ask, narrative)
        else:
            accepted = {k: v for k, v in outcome.sections.items() if k not in ask}
            message = retry_message(sheet, ask, narrative, previous, previous_errors, accepted)
        try:
            attempt.result = llm.call_tool(
                "drafting",
                system,
                message,
                tool(ask, narrative),
                PROMPT_VERSION,
                label=f"{sheet.key} attempt {number}",
            )
        except NotRecorded:
            if number == 1:
                outcome.not_run = NOT_RUN
                outcome.attempts.clear()
                return outcome
            attempt.error = NOT_RUN
            break
        except LLMError as exc:
            attempt.error = str(exc)
            attempt.report = Report([Error(s, None, "form", f"no answer: {exc}") for s in ask])
            previous, previous_errors = Draft({}), attempt.report.errors
            for s in ask:
                outcome.status.setdefault(s, "needs_manual_editing")
                outcome.sections.setdefault(s, [])
                outcome.errors[s] = attempt.report.for_section(s)
            continue
        draft, form_errors = parse_sections(attempt.result.arguments.get("sections") or {})
        accepted = {k: v for k, v in outcome.sections.items() if k not in ask}
        report = verifier.check(sheet, draft, ask, others=accepted)
        if number > 1 and keep_good_sentences(draft, report, outcome, ask):
            report = verifier.check(sheet, draft, ask, others=accepted)  # the merged sections
        report.errors = form_errors + report.errors
        attempt.draft, attempt.report = draft, report
        blocked = set(report.sections_failed())  # safety errors
        noted = [s for s in ask if report.for_section(s)]  # safety errors or style notes
        for s in ask:
            if s in blocked and outcome.status.get(s) == "passed":
                continue  # a rewrite asked for style broke a rule: keep the safe version
            if s in draft.sections or s not in outcome.sections:
                outcome.sections[s] = draft.sections.get(s, [])
            # else: the AI left the section out of a retry; keep its previous version
            outcome.status[s] = "needs_manual_editing" if s in blocked else "passed"
            outcome.errors[s] = report.for_section(s)
        if not noted:
            break
        ask, previous, previous_errors = noted, draft, report.errors
    outcome.sections = {s: outcome.sections.get(s, []) for s in narrative["sections"]}
    remove_failing_sentences(outcome, verifier, narrative)
    return outcome


def remove_failing_sentences(outcome: Outcome, verifier: Verifier, narrative: dict) -> None:
    """After the retries, a sentence that still breaks a rule is removed when its section
    keeps at least its minimum number of sentences (decision 0018); the removal is recorded
    and shown with the draft. Otherwise the section stays flagged for manual editing. Either
    way, no sentence that broke a rule reaches the page as finished text."""
    for name, status in list(outcome.status.items()):
        if status == "passed":
            continue
        errors = [e for e in outcome.errors.get(name, []) if e.blocking]
        if any(e.sentence is None for e in errors):
            continue  # the section as a whole is wrong (missing, wrong count)
        bad = sorted({e.sentence for e in errors})
        sentences = outcome.sections.get(name, [])
        low = narrative["sections"][name]["sentences"][0]
        if len(sentences) - len(bad) < low:
            continue
        kept = [x for i, x in enumerate(sentences, start=1) if i not in bad]
        others = {k: v for k, v in outcome.sections.items() if k != name}
        report = verifier.check(outcome.sheet, Draft({name: kept}), [name], others=others)
        if not report.ok:
            continue
        outcome.removed[name] = [
            (sentences[i - 1].text, [e.message for e in errors if e.sentence == i]) for i in bad
        ]
        outcome.sections[name] = kept
        outcome.status[name] = "passed"
        outcome.errors[name] = report.for_section(name)


def keep_good_sentences(draft: Draft, report: Report, outcome: Outcome, ask: list[str]) -> bool:
    """After a retry, a sentence that passed before and breaks a rule now is put back as it
    was: a retry can only fix sentences, never break good ones. Same sentence count only."""
    changed = False
    for name in ask:
        new, old = draft.sections.get(name), outcome.sections.get(name)
        if not new or not old or len(new) != len(old):
            continue
        new_bad = {e.sentence for e in report.for_section(name) if e.blocking and e.sentence}
        old_bad = {e.sentence for e in outcome.errors.get(name, []) if e.blocking and e.sentence}
        for i in range(len(new)):
            if i + 1 in new_bad and i + 1 not in old_bad:
                new[i] = old[i]
                changed = True
    return changed


def rendered_text(text: str, rendered: dict[str, str]) -> str:
    """Fill the blanks; a blank the fact sheet doesn't know stays visible as [[id?]]."""
    return PLACEHOLDER.sub(lambda m: rendered.get(m.group(1), f"[[{m.group(1)}?]]"), text)
