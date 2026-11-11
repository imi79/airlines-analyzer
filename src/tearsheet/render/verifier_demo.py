"""Watch the verifier work (M7, spec use case 4): the AI's rejected attempts, and a try-it box.

Two things for the app and the demo:

- `attempts`: what the AI handed in at each try for a tearsheet, and what the verifier rejected,
  read from the recorded drafts (docs/m4/drafts/<company>_FY<year>.json);
- `examples` and `check`: sentences to put through the verifier on any tearsheet's fact sheet,
  faulty ones (each caught by its rule) and a correct one (passes), plus any sentence typed by
  the visitor.

The verifier is the M4 code itself, unchanged: nothing here decides what passes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from tearsheet.config import ROOT
from tearsheet.narrative.factsheet import FactSheet
from tearsheet.narrative.render import PLACEHOLDER
from tearsheet.narrative.verifier import CLAIMS, Ref, Sentence, Verifier

DRAFTS = ROOT / "docs" / "m4" / "drafts"
ERROR = re.compile(
    r"\[rule (?P<rule>\w+)\] (?P<section>\w+)(?:, sentence (?P<n>\d+))?: (?P<msg>.*)"
)
PREFERRED = ["net_leverage", "ebitda_margin", "interest_coverage", "ebitda", "revenue"]
RULES = {
    "1": "A number written outside a blank: only code may write a figure",
    "2": "A figure that is not in the fact sheet, or not verified",
    "3": "A direction claimed that contradicts the one computed by code",
    "4": "A direction word in the sentence that the form does not back",
    "5": "The form and the sentence list different figures",
    "6": "An earlier year's figure used without saying which year",
    "form": "The section's shape (missing, or the wrong number of sentences)",
    "style": "A note on style (a figure repeated): sent back, never a rejection",
}


def fill(text: str, rendered: dict[str, str]) -> str:
    return PLACEHOLDER.sub(lambda m: rendered.get(m.group(1), f"[[{m.group(1)}?]]"), text)


def attempts(issuer: str, fiscal_year: int, rendered: dict[str, str],
             folder: Path = DRAFTS) -> list[dict]:  # fmt: skip
    """Each try: the sections asked for, the sentences rejected (as the AI wrote them, with the
    rule and the verifier's message) and the number of style notes."""
    path = folder / f"{issuer}_FY{fiscal_year}.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    out = []
    for a in data.get("attempts") or []:
        draft = a.get("draft") or {}
        rejections, notes = [], 0
        for raw in a.get("errors") or []:
            m = ERROR.match(raw)
            if not m:
                rejections.append({"rule": "?", "section": "", "sentence": None, "text": "",
                                   "message": raw})  # fmt: skip
                continue
            if m["rule"] == "style":
                notes += 1
                continue
            n = int(m["n"]) if m["n"] else None
            sentences = draft.get(m["section"]) or []
            text = sentences[n - 1]["text"] if n and n <= len(sentences) else ""
            rejections.append({"rule": m["rule"], "section": m["section"], "sentence": n,
                               "text": fill(text, rendered), "message": m["msg"]})  # fmt: skip
        out.append({"try": a.get("try"), "sections": a.get("sections") or [],
                    "rejections": rejections, "style_notes": notes,
                    "error": a.get("error")})  # fmt: skip
    return out


# --- Try the verifier ----------------------------------------------------------------------------


def honest_claims(sheet: FactSheet, fid: str) -> list[str]:
    """The claims the form would make if it told the truth: the direction computed by code."""
    item = sheet.items.get(fid)
    if item is None:
        return []
    claims = [c for c in (item.direction, item.assessment) if c in CLAIMS and c != "neutral"]
    return claims


def check(sheet: FactSheet, text: str, claims: dict[str, list[str]] | None = None) -> list[dict]:
    """The verifier's verdict on one sentence: an empty list means it would reach the page.
    Without `claims`, the form claims the true direction of each figure, so only what the
    sentence itself says can be wrong."""
    ids = list(dict.fromkeys(PLACEHOLDER.findall(text)))
    facts = tuple(
        Ref(fid, tuple((claims or {}).get(fid, honest_claims(sheet, fid)))) for fid in ids
    )
    errors = Verifier().check_sentence(sheet, Sentence(text, facts))
    return [{"rule": rule, "title": RULES.get(rule, rule), "message": msg} for rule, msg in errors]


def examples(sheet: FactSheet) -> list[dict]:
    """Sentences for this tearsheet: four faulty (each with the rule that must catch it) and
    one correct. Built on a metric whose change the fact sheet holds."""
    fy = f"FY{sheet.fiscal_year}"
    candidates = [
        i
        for i in sheet.items.values()
        if i.kind == "change" and i.direction in ("up", "down")
        and f"{i.metric}@{fy}" in sheet.items
    ]  # fmt: skip
    candidates.sort(key=lambda i: PREFERRED.index(i.metric) if i.metric in PREFERRED else 99)
    change = candidates[0] if candidates else None
    out = []
    if change is not None:
        label = sheet.labels.get(change.metric, change.metric)
        level = f"{change.metric}@{fy}"
        right = "rose" if change.direction == "up" else "fell"
        wrong = "fell" if change.direction == "up" else "rose"
        out += [
            {"name": "A number typed by the AI", "rule": "1",
             "text": f"{label} {right} to 12.5 this year."},
            {"name": "The wrong direction", "rule": "4",
             "text": f"{label} {wrong} by {{{{{change.id}}}}} to {{{{{level}}}}}."},
            {"name": "A figure that does not exist", "rule": "2",
             "text": f"{label} reached {{{{{change.metric}@FY2030}}}}."},
            {"name": "A correct sentence", "rule": None,
             "text": f"{label} {right} by {{{{{change.id}}}}} to {{{{{level}}}}}."},
        ]  # fmt: skip
    unverified = next(
        (fid for fid, why in sheet.unavailable.items() if "not verified" in why and "@" in fid),
        None,
    )
    if unverified:
        out.insert(3, {"name": "A figure awaiting review", "rule": "2",
                       "text": f"The figure stood at {{{{{unverified}}}}}."})  # fmt: skip
    return out
