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
PROMPT_VERSION = "draft-v3"  # bump with every change to the prompt, examples, form or request
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
) -> str:
    lines = [
        user_message(sheet, sections, narrative),
        "# Your previous draft of these sections was rejected",
        "",
        "Rewrite only the sections below, each in full, and fix every error. The verifier's "
        "errors:",
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

    @property
    def drafted(self) -> bool:
        return self.not_run is None

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
            message = retry_message(sheet, ask, narrative, previous, previous_errors)
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
        report = verifier.check(sheet, draft, ask)
        report.errors = form_errors + report.errors
        attempt.draft, attempt.report = draft, report
        failed = [s for s in ask if report.for_section(s)]
        for s in ask:
            if s in draft.sections or s not in outcome.sections:
                outcome.sections[s] = draft.sections.get(s, [])
            # else: the AI left the section out of a retry; keep its previous version
            outcome.status[s] = "needs_manual_editing" if s in failed else "passed"
            outcome.errors[s] = report.for_section(s)
        if not failed:
            break
        ask, previous, previous_errors = failed, draft, report.errors
    outcome.sections = {s: outcome.sections.get(s, []) for s in narrative["sections"]}
    return outcome


def rendered_text(text: str, rendered: dict[str, str]) -> str:
    """Fill the blanks; a blank the fact sheet doesn't know stays visible as [[id?]]."""
    return PLACEHOLDER.sub(lambda m: rendered.get(m.group(1), f"[[{m.group(1)}?]]"), text)
