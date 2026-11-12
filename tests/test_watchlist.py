"""The watchlist (M9): credit triggers checked against verified figures only.

Checklist items:
- every trigger evaluated for every company and year shown, from verified figures only;
  missing or unverified figures shown as "cannot assess" with the reason
- every fired trigger traces to the figure behind it on click (all 18 tearsheets)
- unit tests for each trigger kind, the edges (exactly at the threshold) and "cannot assess"
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from tearsheet import watchlist as w
from tearsheet.config import load_issuers
from tearsheet.metrics.engine import load_catalog
from tearsheet.narrative import render
from tearsheet.render import library, sources, tearsheet
from tearsheet.render.library import Library, key

UNITS = {"net_leverage": "x", "gross_leverage": "x", "interest_coverage": "x",
         "liquidity_to_revenue": "pct", "cash_liquidity_to_revenue": "pct",
         "ebitda_margin": "pct", "fcf_after_leases": "amount",
         "short_term_debt_cover": "x"}  # fmt: skip


def fig(issuer: str, concept: str, year: int, value: str, status: str = "verified") -> dict:
    unit = UNITS[concept]
    v = Decimal(value)
    return {
        "issuer": issuer, "concept": concept, "fiscal_year": year,
        "period_end": f"{year}-12-31", "label": concept, "unit": unit, "currency": "EUR",
        "value": str(v), "decimals": None, "rendered": render.value_text(v, unit, "EUR"),
        "source_type": "tagged", "status": status, "source": {}, "filing_id": None,
    }  # fmt: skip


def make_lib(*figures: dict, gaps: dict | None = None, kind: str = "airline") -> Library:
    return Library(
        issuers={"co": {"name": "Test Air", "type": kind, "currency": "EUR"}},
        filings={},
        figures={key(f["issuer"], f["concept"], f["fiscal_year"]): f for f in figures},
        gaps=gaps or {},
        unit=dict(UNITS),
        label={k: k.replace("_", " ").capitalize() for k in UNITS},
        definition={},
        higher_is_better={},
    )


def trig(tid: str) -> w.Trigger:
    return w.by_id()[tid]


# --- The triggers file -----------------------------------------------------------------------


def test_the_seven_triggers_load_with_their_owner_and_date():
    ts = w.load()
    assert [t.id for t in ts] == [
        "net_leverage_high", "interest_coverage_low", "short_term_cover_low",
        "fcf_after_leases_negative", "liquidity_low", "net_leverage_up", "ebitda_margin_down",
    ]  # fmt: skip
    catalog = load_catalog()
    for t in ts:
        assert t.metric in catalog
        assert t.set_by == "Imane" and t.set_on == "2026-11-12" and t.reason
    assert trig("liquidity_low").applies_to == "airline"  # plan question 2
    assert trig("liquidity_low").threshold == Decimal("0.20")
    assert trig("ebitda_margin_down").threshold == Decimal("0.03")
    assert trig("net_leverage_high").threshold == Decimal("3.0")
    assert trig("fcf_after_leases_negative").threshold == 0


@pytest.mark.parametrize(
    ("written", "kind", "unit", "expected"),
    [("3.0x", "level", "x", "3.0"), ("20%", "level", "pct", "0.20"), (0, "level", "amount", "0"),
     ("0.5x", "move", "x", "0.5"), ("3 points", "move", "pct", "0.03")],
)  # fmt: skip
def test_thresholds_are_read_as_written(written, kind, unit, expected):
    assert w.parse_threshold(written, kind, unit) == Decimal(expected)


@pytest.mark.parametrize(
    ("written", "kind", "unit"),
    [("20", "level", "pct"), ("3.0", "level", "x"), ("3%", "move", "pct"), ("0x", "move", "x"),
     ("1x", "move", "amount")],
)  # fmt: skip
def test_a_threshold_in_the_wrong_unit_is_refused(written, kind, unit):
    with pytest.raises(ValueError):
        w.parse_threshold(written, kind, unit)


def test_a_trigger_on_an_unknown_metric_is_refused(tmp_path):
    bad = tmp_path / "watchlist.yaml"
    bad.write_text("triggers:\n  x:\n    label: X\n    kind: level\n    metric: no_such\n"
                   "    condition: above\n    threshold: 1.0x\n    reason: r\n    set_by: I\n"
                   "    set_on: 2026-11-12\n")  # fmt: skip
    with pytest.raises(ValueError, match="catalog"):
        w.load(bad)


# --- Level triggers, and their edges ---------------------------------------------------------


@pytest.mark.parametrize(
    ("value", "status"), [("3.2", "fired"), ("3.0", "clear"), ("3.0001", "fired"), ("1.7", "clear"),
                          ("-0.4", "clear")],
)  # fmt: skip
def test_level_above(value, status):
    lib = make_lib(fig("co", "net_leverage", 2025, value))
    c = w.check(lib, trig("net_leverage_high"), "co", 2025)
    assert c.status == status
    assert c.keys == ("co:net_leverage@FY2025",)


@pytest.mark.parametrize(
    ("value", "status"), [("2.9", "fired"), ("3.0", "clear"), ("2.9999", "fired"), ("8", "clear")],
)  # fmt: skip
def test_level_below(value, status):
    lib = make_lib(fig("co", "interest_coverage", 2025, value),
                   fig("co", "gross_leverage", 2025, "3"))  # fmt: skip
    assert w.check(lib, trig("interest_coverage_low"), "co", 2025).status == status


@pytest.mark.parametrize(("value", "status"), [("-1", "fired"), ("0", "clear"), ("5e6", "clear")])
def test_cash_flow_after_leases_below_zero(value, status):
    lib = make_lib(fig("co", "fcf_after_leases", 2025, value))
    assert w.check(lib, trig("fcf_after_leases_negative"), "co", 2025).status == status


def test_a_figure_printed_as_the_threshold_shows_its_stored_value():
    """Aena FY2022: 3.0031x prints as 3.00x, and fires (above 3.0x)."""
    lib = make_lib(fig("co", "net_leverage", 2022, "3.003057455241"))
    c = w.check(lib, trig("net_leverage_high"), "co", 2022)
    assert c.status == "fired"
    assert "3.00x" in c.detail and "stored value 3.0031x" in c.detail


def test_an_approved_figure_counts_like_a_verified_one():
    lib = make_lib(fig("co", "net_leverage", 2025, "3.5", status="overridden"))
    assert w.check(lib, trig("net_leverage_high"), "co", 2025).status == "fired"


# --- Move triggers, and their edges ----------------------------------------------------------


@pytest.mark.parametrize(
    ("prior", "now", "status", "shown"),
    [("1.29", "1.88", "fired", "up 0.59x"), ("1.5", "2.0", "clear", "up 0.50x"),
     ("1.5", "2.0001", "fired", "up 0.50x"), ("3.9", "1.2", "clear", "down 2.70x"),
     ("2", "2", "clear", "unchanged")],
)  # fmt: skip
def test_move_up(prior, now, status, shown):
    lib = make_lib(fig("co", "net_leverage", 2024, prior), fig("co", "net_leverage", 2025, now))
    c = w.check(lib, trig("net_leverage_up"), "co", 2025)
    assert (c.status, c.shown) == (status, shown)
    assert c.keys == ("co:net_leverage@FY2024", "co:net_leverage@FY2025")


@pytest.mark.parametrize(
    ("prior", "now", "status"),
    [("0.180", "0.146", "fired"), ("0.18", "0.15", "clear"), ("0.18", "0.1499", "fired"),
     ("0.10", "0.20", "clear")],
)  # fmt: skip
def test_move_down_in_points(prior, now, status):
    lib = make_lib(fig("co", "ebitda_margin", 2024, prior), fig("co", "ebitda_margin", 2025, now))
    assert w.check(lib, trig("ebitda_margin_down"), "co", 2025).status == status


# --- Cannot assess: never counted as clear ---------------------------------------------------


def test_missing_figure_cannot_be_assessed_with_its_reason():
    gaps = {"co:net_leverage@FY2025": "n.m.: EBITDA is negative (-19.0)"}
    c = w.check(make_lib(gaps=gaps), trig("net_leverage_high"), "co", 2025)
    assert c.status == "cannot_assess"
    assert "EBITDA is negative" in c.detail
    assert c.keys == ()


def test_unverified_figure_cannot_be_assessed():
    lib = make_lib(fig("co", "net_leverage", 2025, "9.9", status="unverified"))
    c = w.check(lib, trig("net_leverage_high"), "co", 2025)
    assert c.status == "cannot_assess"
    assert "awaiting Imane's review" in c.detail
    assert c.keys == ("co:net_leverage@FY2025",)  # its card shows it awaiting review


def test_ratio_to_a_very_small_debt_cannot_be_assessed():
    lib = make_lib(fig("co", "interest_coverage", 2025, "200"),
                   fig("co", "gross_leverage", 2025, "0.14"))  # fmt: skip
    c = w.check(lib, trig("interest_coverage_low"), "co", 2025)
    assert c.status == "cannot_assess"
    assert "debt is very small" in c.detail


def test_move_without_last_year_cannot_be_assessed():
    lib = make_lib(fig("co", "net_leverage", 2025, "9"))
    c = w.check(lib, trig("net_leverage_up"), "co", 2025)
    assert c.status == "cannot_assess"
    assert "FY2024: no figure for this year" in c.detail


def test_move_with_last_year_awaiting_review_cannot_be_assessed():
    lib = make_lib(fig("co", "net_leverage", 2024, "1", status="unverified"),
                   fig("co", "net_leverage", 2025, "9"))  # fmt: skip
    assert w.check(lib, trig("net_leverage_up"), "co", 2025).status == "cannot_assess"


# --- The floor: cash liquidity can only be lower than liquidity ------------------------------


def test_floor_at_or_above_the_threshold_clears_the_trigger():
    lib = make_lib(fig("co", "liquidity_to_revenue", 2025, "0.28", status="unverified"),
                   fig("co", "cash_liquidity_to_revenue", 2025, "0.20"))  # fmt: skip
    c = w.check(lib, trig("liquidity_low"), "co", 2025)
    assert c.status == "clear"
    assert c.keys == ("co:cash_liquidity_to_revenue@FY2025",)
    assert "can only add" in c.detail


def test_floor_below_the_threshold_cannot_be_assessed():
    lib = make_lib(
        fig("co", "cash_liquidity_to_revenue", 2025, "0.15"),
        gaps={"co:liquidity_to_revenue@FY2025": "undrawn lines not available"},
    )
    c = w.check(lib, trig("liquidity_low"), "co", 2025)
    assert c.status == "cannot_assess"
    assert "undrawn lines not available" in c.detail and "decide" in c.detail


def test_the_floor_never_fires_and_never_overrides_a_verified_figure():
    lib = make_lib(fig("co", "liquidity_to_revenue", 2025, "0.19"),
                   fig("co", "cash_liquidity_to_revenue", 2025, "0.50"))  # fmt: skip
    c = w.check(lib, trig("liquidity_low"), "co", 2025)
    assert c.status == "fired" and c.keys == ("co:liquidity_to_revenue@FY2025",)


def test_liquidity_trigger_is_for_airlines_only():
    lib = make_lib(kind="airport")
    assert "liquidity_low" not in {c.trigger for c in w.checks_for(lib, "co", 2025)}
    assert len(w.checks_for(make_lib(), "co", 2025)) == 7


# --- The tearsheet line ----------------------------------------------------------------------


def test_summary_line():
    lib = make_lib(fig("co", "net_leverage", 2024, "1.29"), fig("co", "net_leverage", 2025, "3.2"),
                   fig("co", "fcf_after_leases", 2025, "-5"))  # fmt: skip
    line = w.summary(w.checks_for(lib, "co", 2025))
    assert line.startswith(
        "Watchlist: 3 triggers fired (net leverage above 3.0x; cash flow "
        "after leases negative; net leverage up more than 0.5x); 0 clear, "
    )
    assert line.endswith("4 cannot be assessed")
    assert w.summary([]) == "Watchlist: no trigger fired; 0 clear"


def test_short_label_keeps_capitals():
    assert trig("ebitda_margin_down").short == "EBITDA margin down more than 3 points"
    assert trig("net_leverage_high").short == "net leverage above 3.0x"


# --- On the real figures (samples/figures.json, demo mode) -------------------------------------


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library.read()


def test_every_trigger_evaluated_for_every_company_and_year(lib):
    """Every company and year in the library, every trigger that applies: a result, and a
    reason for each one that cannot be assessed; a result never rests on an unverified figure."""
    total = 0
    for issuer in lib.issuers:
        company_type = lib.issuers[issuer]["type"]
        expected = [t.id for t in w.triggers() if t.applies(company_type)]
        for year in lib.years(issuer):
            checks = w.checks_for(lib, issuer, year)
            assert [c.trigger for c in checks] == expected
            for c in checks:
                total += 1
                assert c.status in ("fired", "clear", "cannot_assess")
                assert c.detail
                if c.status != "cannot_assess":
                    assert c.keys and all(lib.usable(k) for k in c.keys), c
    assert total > 250


def test_every_peer_year_board_has_every_company(lib):
    order = [i.id for i in load_issuers()]
    for py in [y for y in library.peer_years(lib) if y >= 2022]:
        rows = w.board(lib, py, order)
        assert {r["issuer"] for r in rows} == set(order)
        for r in rows:
            for tid, before in r["new"].items():
                assert r["cells"][tid].status == "fired" and before != "fired"


TEARSHEETS = tearsheet.available()


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_every_fired_trigger_traces_to_its_figures(lib, issuer, year):
    """Checklist: a click on a fired trigger opens its card; following it down reaches the
    filing fact, quote or hand entry behind every figure (all 18 tearsheets)."""
    ts = tearsheet.read(issuer, year)
    refs = tearsheet.page_refs(lib, ts)
    for c in tearsheet.watch_checks(lib, ts):
        if c.status != "fired":
            continue
        assert c.ref in refs  # the tearsheet line's source button
        card = sources.card(lib, ts, c.ref)
        assert card["kind"] == "watch" and card["rendered"] == "Fired"
        assert [i["key"] for i in card["inputs"]] == list(c.keys)
        ends = sources.endpoints(lib, ts, c.ref)
        assert ends and all(sources.traced(e) for e in ends), [e["title"] for e in ends]


def test_some_triggers_fire_on_the_tearsheets(lib):
    """The check is not idle: the 18 tearsheets carry fired triggers (9 at M9)."""
    fired = [c for i, y in TEARSHEETS for c in tearsheet.watch_checks(lib, tearsheet.read(i, y))
             if c.status == "fired"]  # fmt: skip
    assert len(fired) >= 5


# --- The short-term cover floor (M9, at Imane's request) ----------------------------------------

UNITS["cash_short_term_debt_cover"] = "x"


def test_cash_only_cover_clears_the_short_term_trigger():
    lib = make_lib(
        fig("co", "cash_short_term_debt_cover", 2025, "1.08"),
        gaps={"co:short_term_debt_cover@FY2025": "undrawn lines not available"},
    )
    c = w.check(lib, trig("short_term_cover_low"), "co", 2025)
    assert c.status == "clear" and c.keys == ("co:cash_short_term_debt_cover@FY2025",)


@pytest.mark.parametrize(("value", "status"), [("1.0", "clear"), ("0.99", "cannot_assess")])
def test_cash_only_cover_at_the_edge(value, status):
    """Exactly 1.0x on cash alone: full cover is at least 1.0x, so not below it (clear)."""
    lib = make_lib(
        fig("co", "cash_short_term_debt_cover", 2025, value),
        gaps={"co:short_term_debt_cover@FY2025": "undrawn lines not available"},
    )
    assert w.check(lib, trig("short_term_cover_low"), "co", 2025).status == status


def test_without_the_floor_both_reasons_are_shown():
    gaps = {
        "co:short_term_debt_cover@FY2025": "undrawn lines not available",
        "co:cash_short_term_debt_cover@FY2025": "current borrowings not reported separately",
    }
    c = w.check(make_lib(gaps=gaps), trig("short_term_cover_low"), "co", 2025)
    assert c.status == "cannot_assess"
    assert "undrawn lines" in c.detail and "current borrowings" in c.detail


def test_the_floor_metric_is_kept_out_of_the_commentary():
    """The cash-only cover is for the watchlist: the drafted notes' fact sheet is unchanged."""
    from tearsheet.narrative.factsheet import load_specs

    assert "cash_short_term_debt_cover" not in load_specs()
    assert "short_term_debt_cover" in load_specs()
