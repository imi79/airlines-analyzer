"""AI extraction: one request per report, answered through a fixed form, then checked.

The request holds: the instructions (a versioned prompt file), the company and fiscal year,
the figures wanted with their definition and scope, and the passages chosen by the locator.
The model answers only by filling the form `record_figures`. Every line it records then goes
through the grounding checks; nothing is trusted on the model's word.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

import yaml
from pydantic import ValidationError

from tearsheet.config import CONFIG, Issuer
from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import Checked, DocumentIndex, RawFigure, check_figure
from tearsheet.extract.locator import items_for, locate, render
from tearsheet.llm import LLM, LLMError, ToolResult, ToolSpec

PROMPTS = Path(__file__).with_name("prompts")
PROMPT_VERSION = "extract-v1"  # bump with every change to the prompt, the form or the request
SCOPES = CONFIG / "extraction.yaml"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def tool(item_ids: list[str]) -> ToolSpec:
    line = {
        "type": "object",
        "properties": {
            "item": {"type": "string", "enum": item_ids},
            "fiscal_year": {"type": "integer"},
            "found": {"type": "boolean"},
            "printed_value": {"type": "string", "description": "Number exactly as printed."},
            "scale": {"type": "string", "enum": ["one", "thousand", "million", "billion"]},
            "currency": {"type": "string", "description": "ISO code, amounts only."},
            "quote": {"type": "string", "description": "Sentence or table row, verbatim."},
            "table_header": {"type": "string", "description": "Column header row, verbatim."},
            "location": {"type": "string"},
            "scope": {"type": "string", "description": "Perimeter the figure covers."},
            "component": {"type": "boolean"},
            "comment": {"type": "string"},
        },
        "required": ["item", "fiscal_year", "found"],
    }
    return ToolSpec(
        name="record_figures",
        description="Record each requested figure with its exact quote, or mark it not found.",
        schema={
            "type": "object",
            "properties": {"figures": {"type": "array", "items": line}},
            "required": ["figures"],
        },
    )


def system_prompt(version: str = PROMPT_VERSION) -> str:
    return (PROMPTS / f"{version.replace('-', '_')}.md").read_text()


def load_scopes(path: Path = SCOPES) -> dict[str, dict[str, str]]:
    return yaml.safe_load(path.read_text())["issuers"]


def fiscal_label(issuer: Issuer, year: int) -> str:
    month = int(issuer.fiscal_year_end[:2])
    if month == 12:
        return f"FY{year} (Jan to Dec {year})"
    start = MONTHS[month % 12]
    return f"FY{year} ({start} {year - 1} to {MONTHS[month - 1]} {year})"


def user_message(
    issuer: Issuer, doc: Document, items: dict[str, dict], scopes: dict, passages: str
) -> str:
    years = [doc.fiscal_year, doc.fiscal_year - 1]
    lines = [
        f"Company: {issuer.name} ({issuer.type}). Reporting currency: {issuer.currency}.",
        f"Report: annual report for {fiscal_label(issuer, doc.fiscal_year)}, "
        f"language: {doc.language or 'en'}.",
        "Fiscal years wanted: "
        + ", ".join(fiscal_label(issuer, y) for y in years)
        + " (the prior year as printed in this report).",
        "",
        "Figures wanted:",
    ]
    for item_id, item in items.items():
        scope = scopes.get(item_id)
        text = f"- {item_id}: {item['definition'].strip()}"
        if scope:
            text += f" Scope: {scope.strip()}"
        lines.append(text)
    lines += ["", "Passages from the report:", "", passages]
    return "\n".join(lines)


@dataclass
class DocumentRun:
    doc: Document
    figures: list[Checked] = field(default_factory=list)
    not_found: list[RawFigure] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)  # form lines that broke the form's rules
    result: ToolResult | None = None
    error: str | None = None
    passage_chars: int = 0


def extract_document(
    llm: LLM,
    issuer: Issuer,
    doc: Document,
    revenue: dict[int, Decimal],
    items: dict[str, dict] | None = None,
    scopes: dict | None = None,
) -> DocumentRun:
    items = items or items_for(issuer.type)
    scopes = scopes if scopes is not None else load_scopes().get(issuer.id, {})
    run = DocumentRun(doc)
    windows = locate(doc, items)
    passages = render(doc, windows)
    run.passage_chars = len(passages)
    message = user_message(issuer, doc, items, scopes, passages)
    try:
        run.result = llm.call_tool(
            "extraction",
            system_prompt(),
            message,
            tool(list(items)),
            PROMPT_VERSION,
            label=f"{issuer.id} FY{doc.fiscal_year} {doc.doc_id}",
        )
    except LLMError as exc:
        run.error = str(exc)
        return run
    index = DocumentIndex(doc)
    for n, line in enumerate(run.result.arguments.get("figures") or []):
        try:
            raw = RawFigure.model_validate(line)
        except ValidationError as exc:
            run.invalid.append(f"line {n + 1}: {exc.errors()[0]['msg']}")
            continue
        if raw.item not in items:
            run.invalid.append(f"line {n + 1}: unknown figure '{raw.item}'")
            continue
        if not raw.found:
            run.not_found.append(raw)
            continue
        checked = check_figure(
            raw, index, items[raw.item], issuer.currency, revenue.get(raw.fiscal_year)
        )
        run.figures.append(checked)
    return run
