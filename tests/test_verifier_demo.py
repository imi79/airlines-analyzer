"""M7: watch the verifier work. The examples are caught by their rule on every tearsheet,
the correct one passes, and the AI's recorded rejections are shown."""

from __future__ import annotations

import pytest

from tearsheet.narrative.factsheet import FactSheet
from tearsheet.render import tearsheet, verifier_demo

TEARSHEETS = tearsheet.available()


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_examples_are_caught_by_their_rule(issuer, year):
    sheet = FactSheet.from_dict(tearsheet.read(issuer, year)["factsheet"])
    examples = verifier_demo.examples(sheet)
    assert len(examples) >= 4
    for e in examples:
        rules = {v["rule"] for v in verifier_demo.check(sheet, e["text"])}
        if e["rule"] is None:
            assert not rules, f"{e['name']}: {rules}"
        else:
            assert e["rule"] in rules, f"{e['name']}: {rules}"


def test_a_typed_sentence_is_checked_with_the_true_direction():
    sheet = FactSheet.from_dict(tearsheet.read("afkl", 2025)["factsheet"])
    # net leverage fell from 1.88x to 1.71x: "rose" is caught, "fell" passes
    assert verifier_demo.check(sheet, "Net leverage fell to {{net_leverage@FY2025}}.") == []
    caught = verifier_demo.check(sheet, "Net leverage rose to {{net_leverage@FY2025}}.")
    assert {v["rule"] for v in caught} == {"4"}


def test_the_ai_rejections_are_on_record():
    ts = tearsheet.read("easyjet", 2025)
    first = ts["attempts"][0]
    assert first["try"] == 1 and first["rejections"]
    r = next(r for r in first["rejections"] if r["rule"] == "3")
    assert r["section"] == "snapshot" and r["sentence"] == 3
    assert "{{" not in r["text"] and "worse" in r["message"]
    assert all(len(ts["attempts"]) >= 1 for ts in map(lambda p: tearsheet.read(*p), TEARSHEETS))
