"""The analyst's own work on a tearsheet: commentary edits, the analyst view, figure reviews.

    notes/<company>_FY<year>.yaml     edits to the drafted sentences and the analyst view
    config/extraction_reviews.yaml    approvals and corrections of unverified figures (M3)

Saved only in live mode; in demo mode they last for the visitor's session (decision 0019).

An edited sentence keeps its links to the figures it already had: wherever the printed figure
("1.71x") is left unchanged, it is turned back into its blank ({{net_leverage@FY2025}}), so
it stays traced. A figure typed by hand has no source: the verifier's number finder flags it,
and the sentence is marked "contains a figure not traced to a source" (approved plan, question
3: warn and mark, do not refuse).
"""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml

from tearsheet.config import CONFIG, ROOT
from tearsheet.narrative.render import PLACEHOLDER

NOTES = ROOT / "notes"
REVIEWS = CONFIG / "extraction_reviews.yaml"
UNTRACED = "contains a figure not traced to a source"


def path_for(issuer: str, fiscal_year: int, folder: Path = NOTES) -> Path:
    return folder / f"{issuer}_FY{fiscal_year}.yaml"


def empty(issuer: str, fiscal_year: int) -> dict:
    return {"issuer": issuer, "fiscal_year": fiscal_year, "analyst_view": "", "edits": {}}


def load(issuer: str, fiscal_year: int, folder: Path = NOTES) -> dict:
    path = path_for(issuer, fiscal_year, folder)
    if not path.exists():
        return empty(issuer, fiscal_year)
    data = yaml.safe_load(path.read_text()) or {}
    out = empty(issuer, fiscal_year) | data
    out["edits"] = {
        section: {int(n): v for n, v in (sentences or {}).items()}
        for section, sentences in (out.get("edits") or {}).items()
    }
    return out


def save(note: dict, by: str, folder: Path = NOTES, today: date | None = None) -> Path:
    note = dict(note)
    note["updated_by"] = by
    note["updated_on"] = str(today or date.today())
    folder.mkdir(parents=True, exist_ok=True)
    path = path_for(note["issuer"], note["fiscal_year"], folder)
    header = (
        "# The analyst's edits and view for this tearsheet, saved by the app (live mode).\n"
        "# Figures in {{blanks}} are filled and traced by code; any other figure is flagged.\n"
    )
    path.write_text(header + yaml.safe_dump(note, sort_keys=False, allow_unicode=True))
    return path


# --- Edited sentences --------------------------------------------------------------------------


def to_blanks(edited: str, ids: list[str], rendered: dict[str, str]) -> str:
    """Turn each printed figure of the original sentence, left unchanged, back into its blank.
    Longest printed forms first, so "EUR 1.2bn" is matched before "1.2"."""
    text = edited
    found = []
    for fid in sorted(ids, key=lambda i: -len(rendered.get(i, ""))):
        printed = rendered.get(fid)
        if not printed:
            continue
        pattern = re.compile(rf"(?<![\w.]){re.escape(printed)}(?![\w])")
        if pattern.search(text):
            marker = f"\x00{len(found)}\x00"
            text = pattern.sub(marker, text, count=1)
            found.append(fid)
    for n, fid in enumerate(found):
        text = text.replace(f"\x00{n}\x00", "{{" + fid + "}}")
    return text


def untraced(text_blanks: str, known: set[str], verifier) -> list[str]:
    """Why a sentence is flagged: figures typed outside a blank, or a blank the fact sheet
    doesn't know. Empty when every figure is traced."""
    problems = [f"unknown figure {{{{{m}}}}}" for m in PLACEHOLDER.findall(text_blanks)
                if m not in known]  # fmt: skip
    problems += verifier.numbers(PLACEHOLDER.sub(" ", text_blanks))
    return problems


def cleared(section: dict, name: str, edits: dict) -> bool:
    """A section the verifier did not clear counts as cleared once the analyst has edited every
    sentence it rejected, with every figure traced (M8). An error about the section as a whole
    (no sentence number) keeps it flagged."""
    if section.get("status") == "passed":
        return True
    failing = set()
    for message in section.get("notes") or []:
        if not re.match(r"\[rule \w+\]", message) or message.startswith("[rule style]"):
            continue  # a style note (repetition) rejects nothing
        m = re.search(rf"{re.escape(name)}, sentence (\d+)", message)
        if m is None:
            return False
        failing.add(int(m.group(1)))
    if not failing:
        return False
    return all(n in edits and not edits[n].get("untraced") for n in failing)


def fill(text_blanks: str, rendered: dict[str, str]) -> str:
    return PLACEHOLDER.sub(lambda m: rendered.get(m.group(1), m.group(0)), text_blanks)


# --- Figure reviews ------------------------------------------------------------------------------


def check_review(review: dict, unit: str) -> list[str]:
    """What is wrong with an approval or correction before it is saved (empty when fine)."""
    problems = []
    if review.get("action") not in ("approve", "correct"):
        problems.append("choose approve or correct")
    if not str(review.get("reason") or "").strip():
        problems.append("give a reason (for example the page you checked)")
    if not str(review.get("by") or "").strip():
        problems.append("give your name")
    if review.get("action") == "correct":
        try:
            value = Decimal(str(review.get("value")).replace(",", ""))
        except (InvalidOperation, ValueError):
            problems.append("the corrected value is not a number")
        else:
            if unit == "pct" and not Decimal(0) <= value <= Decimal(1):
                problems.append("a percentage is entered as a fraction: 0.856 for 85.6%")
            if value < 0:
                problems.append("the corrected value is negative")
    return problems


def add_review(review: dict, path: Path = REVIEWS) -> None:
    """Append a review to config/extraction_reviews.yaml, keeping the file's explanations."""
    entry = {
        "issuer": review["issuer"],
        "fiscal_year": int(review["fiscal_year"]),
        "item": review["item"],
        "action": review["action"],
    }
    if review["action"] == "correct":
        value = Decimal(str(review["value"]).replace(",", ""))
        entry["value"] = int(value) if value == value.to_integral() else float(value)
    entry |= {"by": review["by"], "on": str(review.get("on") or date.today()),
              "reason": review["reason"].strip()}  # fmt: skip
    text = path.read_text()
    current = yaml.safe_load(text).get("reviews") or []
    for r in current:
        if (r["issuer"], int(r["fiscal_year"]), r["item"]) == (
            entry["issuer"], entry["fiscal_year"], entry["item"]
        ):  # fmt: skip
            raise ValueError(f"{entry['issuer']} {entry['fiscal_year']} {entry['item']} "
                             "is already reviewed in config/extraction_reviews.yaml")  # fmt: skip
    block = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True)
    block = "".join("  " + line if line.strip() else line for line in block.splitlines(True))
    if re.search(r"^reviews:\s*\[\]\s*$", text, flags=re.M):
        text = re.sub(r"^reviews:\s*\[\]\s*$", "reviews:\n" + block.rstrip("\n"), text,
                      flags=re.M)  # fmt: skip
        text = text.rstrip("\n") + "\n"
    else:
        text = text.rstrip("\n") + "\n" + block
    path.write_text(text)
