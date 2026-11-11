"""M6 checklist: the PDF fits two pages for every v1 issuer, with no overflow.

Each of the 18 tearsheets is rendered in the worst case: an analyst view longer than its box
and an edited sentence with a typed figure. The layout check measures the rendered boxes: a
table wider than its column, or a clipped box that hides lines, counts as overflow.
"""

from __future__ import annotations

import re

import pytest

from tearsheet.render import manifest, notes, pdf, tearsheet
from tearsheet.render.library import Library
from tearsheet.render.tearsheet import load_app_config

TEARSHEETS = tearsheet.available()
PAGE1 = {"page1", "snapshot", "kpi", "credit", "definitions1"}
PAGE2 = {"page2", "operating", "peers", "liquidity", "watch", "view", "footnotes", "end"}
LONG_VIEW = "\n".join(
    ["We see the credit as stable: leverage is moderate for the sector and liquidity is ample, "
     "with refinancing needs well covered by cash and committed lines."] * 10
)  # fmt: skip


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library.read()


def worst_case(ts: dict) -> dict:
    first = ts["commentary"]["credit_metrics"]["sentences"][0]
    edit = {"text": first["text_blanks"] + " We expect about 0.3x less next year.",
            "untraced": ["number written outside a blank: '0.3x'"]}  # fmt: skip
    return notes.empty(ts["issuer"], ts["fiscal_year"]) | {
        "analyst_view": LONG_VIEW, "edits": {"credit_metrics": {1: edit}},
    }  # fmt: skip


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_two_pages_every_section_in_place(lib, issuer, year):
    ts = tearsheet.read(issuer, year)
    note = worst_case(ts)
    r = pdf.render(lib, ts, note, manifest.build(lib, ts, note))  # raises on any overflow
    assert r.pages == 2
    assert r.pdf.startswith(b"%PDF")
    assert {a for a, page in r.anchors.items() if page == 1} == PAGE1
    assert {a for a, page in r.anchors.items() if page == 2} == PAGE2
    assert r.font_size >= 7.5
    assert r.view_truncated  # the long view was cut, with the note visible in the box
    assert r.fonts == ("Tearsheet Inter",)  # the bundled font, never a fallback


@pytest.mark.parametrize(("issuer", "year"), [("easyjet", 2025), ("adp", 2025)])
def test_page_content(lib, issuer, year):
    ts = tearsheet.read(issuer, year)
    note = worst_case(ts)
    ctx = pdf.context(lib, ts, note, manifest.build(lib, ts, note), 8.5)
    page = pdf.html_page(ctx)
    assert "{{" not in page and "[[" not in page  # every blank filled by code
    assert "Not investment advice." in page
    assert "prompt draft-v7" in page
    assert "(continued in the app)" in page
    assert "†" in page and "not traced to a filing" in page
    defined = {label for label, _ in ctx["definitions_p1"] + ctx["definitions"]}
    for table in (ctx["kpi"], ctx["operating_table"], ctx["peers"]["table"]):
        for row in table["rows"]:
            assert row["label"].split(" (")[0] in defined or row["label"] in defined


def test_unverified_figures_never_print_as_numbers(lib):
    ts = tearsheet.read("afkl", 2025)  # undrawn facilities, hence liquidity, await review
    ctx = pdf.context(lib, ts, None, manifest.build(lib, ts), 8.5)
    row = next(r for r in ctx["kpi"]["rows"] if r["label"] == "Liquidity")
    assert row["cells"][-1]["text"] == "pending"
    assert not re.search(r"\d", row["cells"][-1]["text"])


def test_too_long_is_an_error_not_a_cut(lib):
    ts = tearsheet.read("iag", 2025)
    config = load_app_config()
    config = config | {"pdf": config["pdf"] | {"font_sizes": [14]}}
    with pytest.raises(pdf.Overflow):
        pdf.render(lib, ts, None, manifest.build(lib, ts), config)


def test_view_fits():
    assert pdf.view_fits({"analyst_view": "Stable outlook."})
    assert not pdf.view_fits({"analyst_view": LONG_VIEW})
