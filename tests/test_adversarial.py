"""The adversarial suite (M4 checklist): every faulty draft is rejected, for the right rule;
every correct draft passes, so the verifier is not simply rejecting everything."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tearsheet.narrative.factsheet import FactSheet
from tearsheet.narrative.verifier import Draft, Verifier, parse_sections

FIXTURES = Path(__file__).parent / "fixtures" / "narrative"
SHEET = FactSheet.from_json(FIXTURES / "afkl_FY2025.json")
CORRECT = yaml.safe_load((FIXTURES / "afkl_FY2025_correct.yaml").read_text())
SUITE = yaml.safe_load((FIXTURES / "adversarial.yaml").read_text())
V = Verifier()


def base() -> Draft:
    draft, errors = parse_sections(CORRECT)
    assert not errors
    return draft


def with_sentence(case: dict) -> Draft:
    draft = base()
    sentence = parse_sections({"x": [{"text": case["text"], "facts": case["facts"]}]})[0]
    new = sentence.sections["x"][0]
    if "add" in case:
        draft.sections.setdefault(case["add"], []).append(new)
        return draft
    section, number = case.get("replace", ["credit_metrics", 4])
    draft.sections[section][number - 1] = new
    return draft


def test_the_correct_draft_passes():
    report = V.check(SHEET, base())
    assert report.ok, "\n".join(str(e) for e in report.errors)


def test_suite_size():
    assert len(SUITE["faulty"]) >= 30
    assert {c["rule"] for c in SUITE["faulty"]} == {"1", "2", "3", "4", "5", "6", "form"}


@pytest.mark.parametrize("case", SUITE["faulty"], ids=[c["name"] for c in SUITE["faulty"]])
def test_faulty_draft_is_rejected_for_its_rule(case):
    report = V.check(SHEET, with_sentence(case))
    assert not report.ok
    assert case["rule"] in {e.rule for e in report.errors}, "\n".join(map(str, report.errors))


@pytest.mark.parametrize("case", SUITE["correct"], ids=range(len(SUITE["correct"])))
def test_correct_sentence_passes(case):
    report = V.check(SHEET, with_sentence(case))
    assert report.ok, "\n".join(str(e) for e in report.errors)
