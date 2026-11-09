"""Verifier rules on a small fact sheet (the full adversarial suite is test_adversarial.py)."""

from __future__ import annotations

import pytest

from tearsheet.narrative.factsheet import build
from tearsheet.narrative.verifier import Draft, Ref, Sentence, Verifier, parse_sections
from tests.test_factsheet import ISSUERS, universe

V = Verifier()


@pytest.fixture(scope="module")
def sheet():
    return build(ISSUERS["afkl"], 2025, universe())


def errors(sheet, text, *refs):
    facts = tuple(Ref(i, tuple(c)) for i, *c in refs)
    return V.check_sentence(sheet, Sentence(text, facts))


def rules(found):
    return sorted({rule for rule, _ in found})


def test_clean_sentence_passes(sheet):
    assert not errors(
        sheet,
        "Net leverage fell to {{net_leverage@FY2025}} in FY2025, down"
        " {{net_leverage.change@FY2025}} from {{net_leverage@FY2024}}.",
        ("net_leverage@FY2025", "down"),
        ("net_leverage.change@FY2025", "down", "better"),
        ("net_leverage@FY2024",),
    )


def test_allowed_names_and_years(sheet):
    assert not errors(
        sheet,
        "Under IFRS 16, leases count as debt; the A321neo and A220 deliveries run to 2027, and"
        " the margin reached {{ebitda_margin@FY2025}} in FY2025.",
        ("ebitda_margin@FY2025",),
    )


@pytest.mark.parametrize(
    "text",
    [
        "Net leverage was 1.7x at {{net_leverage@FY2025}}.",
        "Revenue grew 5% to {{revenue@FY2025}}.",
        "Liquidity of EUR {{revenue@FY2025}} bn.",
        "Leverage roughly halved to {{net_leverage@FY2025}}.",
        "About a third of revenue, at {{revenue@FY2025}}.",
        "A record {{revenue@FY2025}} of revenue.",
        "Revenue reached {{revenue@FY2025}}, up two points.",
        "Revenue of {{revenue@FY2025}} (€).",
    ],
)
def test_rule_1_numbers(sheet, text):
    assert "1" in rules(errors(sheet, text, ("revenue@FY2025",), ("net_leverage@FY2025",)))


def test_rule_2_unknown_and_unavailable(sheet):
    found = errors(sheet, "Liquidity was {{liquidity@FY2025}}.", ("liquidity@FY2025",))
    assert any("not available" in m for _, m in found)
    found = errors(sheet, "Leverage was {{leverage@FY2025}}.", ("leverage@FY2025",))
    assert any("not in the fact sheet" in m for _, m in found)
    found = errors(sheet, "Leverage was {net_leverage@FY2025}.")
    assert any("malformed" in m for _, m in found)


@pytest.mark.parametrize(
    ("claim", "rule_found"),
    [("up", True), ("flat", True), ("worse", True), ("down", False), ("better", False)],
)
def test_rule_3_claims(sheet, claim, rule_found):
    found = errors(
        sheet,
        "Net leverage moved by {{net_leverage.change@FY2025}}.",
        ("net_leverage.change@FY2025", claim),
    )
    assert ("3" in rules(found)) is rule_found


def test_rule_3_claim_on_prior_year_has_no_direction(sheet):
    found = errors(sheet, "Leverage was {{net_leverage@FY2024}}.", ("net_leverage@FY2024", "up"))
    assert "3" in rules(found)


def test_rule_3_superlative_needs_rank_one(sheet):
    found = errors(
        sheet,
        "Net leverage ranks {{net_leverage.peer_rank@FY2025}}, the strongest in the group.",
        ("net_leverage.peer_rank@FY2025", "best_in_group"),
    )
    assert "3" in rules(found)  # the rank is 2nd of 3


def test_rule_4_verb_contradicts_claim(sheet):
    found = errors(
        sheet,
        "Net leverage rose to {{net_leverage@FY2025}}.",
        ("net_leverage@FY2025", "down"),
    )
    assert rules(found) == ["4"]


def test_rule_4_direction_word_without_claim(sheet):
    found = errors(sheet, "Net leverage improved to {{net_leverage@FY2025}}.",
                   ("net_leverage@FY2025",))  # fmt: skip
    assert rules(found) == ["4"]


def test_rule_4_reads_clauses_separately(sheet):
    good = errors(
        sheet,
        "Net leverage fell to {{net_leverage@FY2025}}, while the EBITDA margin rose to"
        " {{ebitda_margin@FY2025}}.",
        ("net_leverage@FY2025", "down"),
        ("ebitda_margin@FY2025", "up"),
    )
    assert not good
    swapped = errors(
        sheet,
        "Net leverage rose to {{net_leverage@FY2025}}, while the EBITDA margin fell to"
        " {{ebitda_margin@FY2025}}.",
        ("net_leverage@FY2025", "down"),
        ("ebitda_margin@FY2025", "up"),
    )
    assert rules(swapped) == ["4"]


def test_rule_4_lowest_follows_higher_is_better():
    figures = universe()
    figures = [f for f in figures if not (f.concept == "net_leverage" and f.issuer == "afkl")]
    from tests.test_factsheet import fig

    figures += [fig("afkl", "net_leverage", 2025, "0.5")]
    sheet = build(ISSUERS["afkl"], 2025, figures)
    ok = errors(sheet, "Net leverage is the lowest in the group, ranking"
                " {{net_leverage.peer_rank@FY2025}}.",
                ("net_leverage.peer_rank@FY2025", "best_in_group"))  # fmt: skip
    assert not ok
    wrong = errors(sheet, "Net leverage is the highest in the group, ranking"
                   " {{net_leverage.peer_rank@FY2025}}.",
                   ("net_leverage.peer_rank@FY2025", "best_in_group"))  # fmt: skip
    assert rules(wrong) == ["4"]


def test_rule_5_listed_and_used_ids(sheet):
    found = errors(sheet, "Net leverage was {{net_leverage@FY2025}}.", ("revenue@FY2025",))
    assert rules(found) == ["5"]
    assert len(found) == 2


def test_form_counts_and_missing_sections(sheet):
    one = Sentence("Net leverage was {{net_leverage@FY2025}}.", (Ref("net_leverage@FY2025"),))
    draft = Draft({"snapshot": [one, one], "analyst_view": [one]})
    report = V.check(sheet, draft)
    messages = [str(e) for e in report.errors if e.rule == "form"]
    assert any("snapshot: 2 sentences; needs exactly 3" in m for m in messages)
    assert any("analyst_view: not a drafted section" in m for m in messages)
    assert any("credit_metrics: section missing" in m for m in messages)
    assert set(report.sections_failed()) >= {"snapshot", "credit_metrics", "analyst_view"}


def test_parse_sections_reports_malformed_lines():
    draft, errs = parse_sections({"snapshot": [{"text": "x", "facts": [{"claims": []}]}, "y"]})
    assert len(draft.sections["snapshot"]) == 1
    assert {e.rule for e in errs} == {"form"} and len(errs) == 2
