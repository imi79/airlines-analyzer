"""The two example notes shown to the AI pass the verifier on their own fact sheets."""

from __future__ import annotations

from pathlib import Path

import pytest

from tearsheet.narrative.drafting import examples_text, load_examples, system_prompt
from tearsheet.narrative.factsheet import FactSheet, load_narrative
from tearsheet.narrative.render import fill
from tearsheet.narrative.verifier import Verifier, parse_sections

FIXTURES = Path(__file__).parent / "fixtures" / "narrative"
EXAMPLES = {f"{e['issuer']}_FY{e['fiscal_year']}": e for e in load_examples()}


@pytest.mark.parametrize("key", sorted(EXAMPLES))
def test_example_passes_the_verifier(key):
    sheet = FactSheet.from_json(FIXTURES / f"{key}.json")
    draft, form_errors = parse_sections(EXAMPLES[key]["sections"])
    report = Verifier().check(sheet, draft)
    assert not form_errors
    assert report.ok, "\n".join(str(e) for e in report.errors)
    for sentences in draft.sections.values():
        for s in sentences:
            assert "{{" not in fill(s.text, sheet.rendered())


def test_examples_are_in_the_prompt_and_not_drafted_years():
    text = system_prompt()
    assert "{examples}" not in text
    assert examples_text(load_examples(), load_narrative()) in text
    assert {e["fiscal_year"] for e in EXAMPLES.values()} == {2023}  # drafts are FY2024 onwards
