"""Reading printed statement lines for the gate 1 second-source model."""

import re

from spikes.m2.hand_model import FOOTNOTE, NUMBER, number


def numbers_after(label: str, line: str) -> list[float]:
    hit = re.match(r"\s*" + label + FOOTNOTE, line)
    return [number(t) for t in NUMBER.findall(line[hit.end() :]) if t != ","]


def test_brackets_are_negative_and_dashes_are_zero():
    assert numbers_after("Interest paid", "Interest paid   (295)   (298)") == [-295, -298]
    assert numbers_after("Restricted", "Restricted   125   –   138") == [125, 0, 138]


def test_thousands_separators_and_note_references():
    line = "Revenues from ordinary activities   6.1   33,007   31,459"
    assert numbers_after("Revenues from ordinary activities", line)[-2:] == [33007, 31459]


def test_footnote_marker_after_the_label_is_not_a_number():
    line = "Restricted bank balances(4)   138   138   118   –   118"
    assert numbers_after("Restricted bank balances", line)[0] == 138
    line = "Restricted bank balances⁽⁴⁾   125   125   138   –   138"
    assert numbers_after("Restricted bank balances", line)[0] == 125
