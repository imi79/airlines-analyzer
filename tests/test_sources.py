"""M5 checklist: every figure the app shows has a source card that leads down to a filing fact,
a quote from the report or a hand entry. Runs on the committed demo files (samples/), so it
needs no database and no network."""

from __future__ import annotations

from decimal import Decimal
from statistics import median

import pytest

from tearsheet.render import library, sources, tearsheet
from tearsheet.render.library import Library, key

TEARSHEETS = tearsheet.available()


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library.read()


def _assert_traced(lib, ts, ref) -> None:
    ends = sources.endpoints(lib, ts, ref)
    assert ends, f"{ref}: no source"
    for c in ends:
        assert sources.traced(c), f"{ref} leads to an untraced card: {c['title']} {c['lines']}"


def test_eighteen_tearsheets_in_the_demo():
    assert len(TEARSHEETS) == 18  # nine companies, latest two years (plan question 2)
    assert {i for i, _ in TEARSHEETS} == {
        "afkl", "iag", "finnair", "easyjet", "norwegian", "wizz", "adp", "aena", "vie",
    }  # fmt: skip


def test_every_stored_figure_leads_to_its_source(lib):
    """The audit page lists every figure: each one, followed down, ends at a filing fact
    (with its filing), a quote (with its document) or a hand entry (with its page)."""
    for k in lib.figures:
        _assert_traced(lib, None, {"key": k})


def test_every_computed_input_is_linked(lib):
    for k, f in lib.figures.items():
        if f["source_type"] == "computed":
            assert None not in f["input_keys"], f"{k}: an input is not linked to its figure"


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_every_figure_on_the_tearsheet_page_has_a_source(lib, issuer, year):
    ts = tearsheet.read(issuer, year)
    refs = []
    for kpi in tearsheet.kpi_cards(lib, ts):
        if kpi["cell"].key:
            refs.append({"key": kpi["cell"].key})
        if kpi["change_id"]:
            refs.append({"fid": kpi["change_id"]})
    for row in tearsheet.kpi_table(lib, ts)["rows"]:
        refs += [{"key": c.key} for c in row["cells"] if c.key]
    for chart in ("leverage", "liquidity"):
        refs += [{"key": p["key"]} for p in tearsheet.chart_series(lib, ts, chart)]
    refs += [{"fid": fid} for fid in tearsheet.commentary_ids(ts)]
    assert len(refs) > 40
    for ref in refs:
        _assert_traced(lib, ts, ref)


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_commentary_matches_the_figures(issuer, year):
    """The draft was written from exactly these figures (same fact sheet fingerprint)."""
    ts = tearsheet.read(issuer, year)
    assert ts["run"]["matches_figures"]
    for section in ts["commentary"].values():
        for s in section["sentences"]:
            for fid in [f["id"] for f in s["facts"]]:
                assert fid in ts["factsheet"]["items"], f"{fid} not in the fact sheet"


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_peer_median_card_shows_the_figures_behind_the_median(lib, issuer, year):
    ts = tearsheet.read(issuer, year)
    for fid, item in ts["factsheet"]["items"].items():
        if item["kind"] != "peer_median":
            continue
        used, _ = sources.peer_members(lib, ts, item["metric"])
        assert median(Decimal(lib.figures[k]["value"]) for k in used) == Decimal(item["value"]), fid


def test_every_figure_on_the_peers_page_has_a_source(lib):
    groups = library.peer_groups()
    for group in groups["groups"]:
        for year in (2021, 2022, 2023, 2024, 2025):
            table = library.peer_table(lib, group, year, groups)
            for row in table["rows"]:
                for cell in row["cells"].values():
                    if cell.get("rendered"):
                        _assert_traced(lib, None, {"key": cell["key"]})
                if row["median"] is not None:
                    ref = sources.ref_of_peer_median(group, year, row["metric"])
                    card = sources.card(lib, None, ref)
                    assert card["rendered"] == row["median_rendered"]
                    _assert_traced(lib, None, ref)


def test_peer_table_matches_the_m2_peer_report(lib):
    """Network airlines, peer year 2025 (docs/m2/peers.md): margins, ranks and median."""
    table = library.peer_table(lib, "network", 2025)
    row = next(r for r in table["rows"] if r["metric"] == "ebitda_margin")
    assert [row["cells"][m]["rendered"] for m in ("afkl", "iag", "finnair")] == [
        "15.3%", "23.0%", "13.1%",
    ]  # fmt: skip
    assert [row["cells"][m]["rank"] for m in ("afkl", "iag", "finnair")] == [2, 1, 3]
    assert row["median_rendered"] == "15.3%"


def test_unverified_figures_never_print_as_numbers(lib):
    unverified = [k for k, f in lib.figures.items() if f["status"] == "unverified"]
    assert unverified
    for k in unverified:
        assert tearsheet.cell(lib, k).rendered == "awaiting review"
        issuer, concept, year = library.split(k)
        assert key(issuer, concept, year) == k


def test_year_end_offsets_shown_for_easyjet_and_wizz(lib):
    table = library.peer_table(lib, "low_cost", 2025)
    assert table["year_end_offsets"] == {"easyjet": -3, "wizz": 3}


def test_demo_files_match_the_database_when_it_exists(tmp_path):
    """The committed demo files are what `tearsheet samples` writes from today's database."""
    from tearsheet.config import DB_PATH
    from tearsheet.render.samples import write_samples

    if not DB_PATH.exists():
        pytest.skip("no database here (built by `uv run tearsheet all`)")
    figures = tmp_path / "figures.json"
    write_samples(DB_PATH, figures, tmp_path / "tearsheets")
    assert figures.read_text() == library.FIGURES_FILE.read_text()
    for path in (tmp_path / "tearsheets").glob("*.json"):
        assert path.read_text() == (tearsheet.TEARSHEETS / path.name).read_text(), path.name


def test_ratios_to_a_very_small_debt_are_not_meaningful(lib):
    """Vienna's debt is tiny: FFO to debt is shown as n.m. and left out of the peer median,
    as in the M4 fact sheets (config/narrative.yaml, small_debt)."""
    k = "vie:ffo_to_debt@FY2025"
    assert Decimal(lib.figures[k]["value"]) > 1  # over 100%: meaningless as a credit ratio
    assert tearsheet.cell(lib, k).rendered == "n.m."
    table = library.peer_table(lib, "airports", 2025)
    row = next(r for r in table["rows"] if r["metric"] == "ffo_to_debt")
    assert row["cells"]["vie"]["nm"] and "rank" not in row["cells"]["vie"]
    assert row["count"] == 2
    card = sources.figure_card(lib, k)
    assert any("very small" in line for line in card["lines"])


def test_filing_links_are_full_addresses(lib):
    """Every link to a filing opens on its own (the database stores them relative to the site)."""
    links = [rec[u] for rec in lib.filings.values() for u in ("viewer_url", "report_url") if rec[u]]
    assert links and all(link.startswith("https://filings.xbrl.org/") for link in links)
