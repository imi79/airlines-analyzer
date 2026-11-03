"""Cross-checks across figures (consolidate.py): agreement between reports, RPK ÷ ASK against
the printed load factor (or not, for seat-based load factors), year-on-year jumps, and the
choice of one value per year."""

from __future__ import annotations

from decimal import Decimal

from tearsheet.extract.consolidate import Candidate, cross_check
from tearsheet.extract.documents import Document
from tearsheet.extract.grounding import Checked, RawFigure
from tearsheet.extract.locator import load_items

ITEMS = load_items()


def doc(year: int) -> Document:
    return Document(f"report-{year}", "x", year, "en", "test", "test", None, ("",), "page")


def cand(item, year, value, printed, doc_year=None, decimals=None) -> Candidate:
    raw = RawFigure(item=item, fiscal_year=year, found=True, printed_value=printed)
    checked = Checked(raw, doc(doc_year or year), Decimal(value), decimals)
    return Candidate(item, year, Decimal(value), decimals, [checked], status="verified")


def traffic(lf_printed="90.8", lf="0.908"):
    return [
        cand("ask", 2025, "134451000000", "134,451", decimals=-6),
        cand("rpk", 2025, "122021000000", "122,021", decimals=-6),
        cand("load_factor", 2025, lf, lf_printed),
    ]


def test_rpk_over_ask_matching_the_printed_load_factor_is_kept():
    cs = traffic()
    cross_check(cs, ITEMS)
    assert all(c.status == "verified" for c in cs)
    assert any("matches the printed load factor" in n for n in cs[0].notes)


def test_rpk_over_ask_not_matching_the_printed_load_factor_is_rejected():
    cs = traffic("89.8", "0.898")
    cross_check(cs, ITEMS)
    assert cs[0].status == cs[1].status == "unverified"
    assert "RPK ÷ ASK = 90.8%" in cs[0].failures[0]


def test_seat_based_load_factor_skips_the_rpk_over_ask_check():
    # easyJet prints passengers ÷ seats (89.8%); RPK ÷ ASK is 90.8%. Both are right.
    cs = traffic("89.8", "0.898")
    cross_check(cs, ITEMS, load_factor_basis="seats")
    assert all(c.status == "verified" for c in cs)
    assert any("seats sold" in n for n in cs[0].notes)


def test_two_reports_that_disagree_are_both_unverified():
    own = cand("passengers", 2024, "89700000", "89.7", decimals=-5)
    later = cand("passengers", 2024, "91000000", "91.0", doc_year=2025, decimals=-5)
    cross_check([own, later], ITEMS)
    assert own.status == later.status == "unverified"
    assert "reports disagree" in own.failures[0]


def test_two_reports_that_agree_within_rounding_are_kept_and_own_report_is_used():
    own = cand("passengers", 2024, "89700000", "89.7", decimals=-5)
    later = cand("passengers", 2024, "89712000", "89,712", doc_year=2025, decimals=-3)
    cross_check([later, own], ITEMS)
    assert own.status == later.status == "verified"
    assert own.primary and not later.primary


def test_implausible_jump_is_rejected():
    before = cand("fleet_count", 2024, "347", "347")
    after = cand("fleet_count", 2025, "56", "56")  # halving beyond the item's limit (2x)
    cross_check([before, after], ITEMS)
    assert before.status == after.status == "unverified"
    assert "implausible jump" in after.failures[0]


def test_fleet_printed_in_parts_is_added_up():
    # Finnair FY2025: 55 aircraft on Finnair's certificate + 24 flown by Norra for Finnair.
    from datetime import date

    from tearsheet.config import load_issuers
    from tearsheet.extract.consolidate import build_candidates

    finnair = next(i for i in load_issuers() if i.id == "finnair")
    parts = []
    for printed in ("55", "24"):
        raw = RawFigure(
            item="fleet_count", fiscal_year=2025, found=True, printed_value=printed,
            component=True,
        )  # fmt: skip
        parts.append(Checked(raw, doc(2025), Decimal(printed), 0))
    (c,) = build_candidates(parts, finnair, ITEMS, {2025: date(2025, 12, 31)}, {}, None)
    assert c.value == Decimal(79) and c.status == "verified"
