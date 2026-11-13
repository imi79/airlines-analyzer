"""The app's LTM layer (M10): the pre-built half-year file and the view laid over the library."""

from decimal import Decimal

from tearsheet import watchlist
from tearsheet.config import load_issuers
from tearsheet.render import interim, library, sources, tearsheet

LIB = library.Library.read()
INTERIM = interim.Interim.read()
VIEW = interim.ltm_view(LIB, INTERIM)


def test_nine_reports_loaded_at_least_seven_with_figures():
    assert len(INTERIM.reports) == 9
    loaded = [i for i, r in INTERIM.reports.items() if not r["error"]]
    assert len(loaded) >= 7
    assert all(r["audit"] == "unaudited" for r in INTERIM.reports.values())


def test_the_view_leaves_every_fiscal_year_figure_as_it_is():
    assert all(VIEW.figures[k] is f for k, f in LIB.figures.items())
    assert VIEW.gaps.items() >= LIB.gaps.items()
    assert library.Library.read().figures == LIB.figures  # the library itself is not altered


def test_each_company_gets_one_column_after_its_last_fiscal_year():
    for issuer, info in VIEW.ltm.items():
        assert info["year"] == max(LIB.years(issuer)) + 1
        assert VIEW.period_label(issuer, info["year"]).startswith("LTM ")
        assert VIEW.period_label(issuer, info["base"]) == LIB.period_label(issuer, info["base"])
    assert VIEW.ltm["easyjet"]["label"] == "LTM Mar 2026"
    assert VIEW.ltm["wizz"]["label"] == "LTM Sep 2026"


def test_ltm_revenue_is_the_sum_of_its_three_parts():
    for issuer, info in VIEW.ltm.items():
        f = VIEW.figure(library.key(issuer, "revenue", info["year"]))
        if f is None:
            continue
        full, half, before = (Decimal(VIEW.figures[k]["value"]) for k in f["input_keys"])
        assert Decimal(f["value"]) == full + half - before
        assert f["input_keys"][0] == library.key(issuer, "revenue", info["base"])


def test_every_ltm_figure_traces_to_a_filing_fact_a_report_row_or_a_hand_entry():
    checked = 0
    for issuer, info in VIEW.ltm.items():
        for k, f in VIEW.figures.items():
            if f["issuer"] != issuer or f["fiscal_year"] != info["year"]:
                continue
            ends = sources.endpoints(VIEW, None, {"key": k})
            assert ends and all(sources.traced(e) for e in ends), k
            checked += 1
    assert checked > 300


def test_a_half_year_card_shows_the_row_the_page_and_the_control():
    card = sources.card(VIEW, None, {"key": "finnair:revenue.h1@FY2026"})
    text = " ".join(card["lines"])
    assert "page 28" in text and "1,694.8" in text
    assert "Control passed" in text and "Unaudited" in text
    assert card["link"].startswith("https://")


def test_a_missing_ltm_metric_says_why():
    card = sources.card(VIEW, None, {"key": "adp:net_debt@FY2026"})
    assert card["kind"] == "missing" and "LTM Jun 2026" in card["title"]
    assert "half-year reports are condensed" in card["lines"][0]


def test_unverified_ltm_figures_are_not_printed():
    year = VIEW.ltm["afkl"]["year"]
    cell = tearsheet.cell(VIEW, library.key("afkl", "ebitda", year))
    assert cell.rendered == "awaiting review"


def test_watchlist_at_ltm_compares_with_the_last_fiscal_year():
    order = [i.id for i in load_issuers()]
    rows = watchlist.board(VIEW, None, order, {i: v["year"] for i, v in VIEW.ltm.items()})
    assert len(rows) == len(VIEW.ltm)
    wizz = next(r for r in rows if r["issuer"] == "wizz")
    assert wizz["period_label"] == "LTM Sep 2026 (unaudited)"
    assert wizz["cells"]["net_leverage_high"].status == watchlist.FIRED
    move = wizz["cells"]["net_leverage_up"]
    assert move.status == watchlist.CLEAR and library.key("wizz", "net_leverage", 2026) in move.keys
    # an unverified LTM figure is never counted as clear
    afkl = next(r for r in rows if r["issuer"] == "afkl")
    assert afkl["cells"]["net_leverage_high"].status == watchlist.CANNOT


def test_the_fiscal_year_watchlist_is_unchanged_by_the_view():
    order = [i.id for i in load_issuers()]
    assert watchlist.board(VIEW, 2025, order) == watchlist.board(LIB, 2025, order)
