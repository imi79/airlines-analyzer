"""Figures entered by hand from published statements (decision 0007)."""

from decimal import Decimal

from tearsheet.config import Issuer
from tearsheet.ingest.manual_figures import manual_figures

ISSUER = Issuer(
    id="abc",
    name="Example Air",
    type="airline",
    lei="969500EXAMPLE0000000",
    currency="EUR",
    fiscal_year_end="12-31",
    country="FR",
    status="v1",
)

DOC = """
documents:
  - issuer: abc
    fiscal_year: 2025
    period_end: 2025-12-31
    document: Example statements 2025 (PDF)
    file: example.pdf
    sha256: deadbeef
    entered_by: test
    entered_on: 2026-10-30
    reviewed_by: {reviewed}
    scale: 1000000
    lines:
      revenue: [33007, 31459, 3, "Revenues"]
      capex: [4449, 3728, 8, "Purchase of PP&E"]
    footnotes:
      revenue: A footnote.
  - issuer: someone_else
    fiscal_year: 2025
    period_end: 2025-12-31
    document: x
    file: x.pdf
    sha256: x
    entered_by: test
    entered_on: 2026-10-30
    scale: 1000000
    lines:
      revenue: [1, 1, 1, "x"]
"""


def load(tmp_path, reviewed="null"):
    path = tmp_path / "manual_figures.yaml"
    path.write_text(DOC.format(reviewed=reviewed))
    return manual_figures(ISSUER, path)


def test_entries_become_manual_facts_in_full_units(tmp_path):
    filings, facts, _ = load(tmp_path)
    assert [f.fiscal_year for f in filings] == [2025]
    revenue = next(f for f in facts if f.line == "revenue")
    assert revenue.value == Decimal("33007000000")
    assert revenue.decimals == -6
    assert revenue.source_type == "manual"
    assert revenue.fact_ids == ("page 3",)
    assert revenue.footnote == "A footnote."


def test_entries_stay_unverified_until_reviewed(tmp_path):
    assert {f.status for f in load(tmp_path)[1]} == {"unverified"}
    assert {f.status for f in load(tmp_path, reviewed="Imane")[1]} == {"verified"}


def test_prior_year_column_is_kept_as_a_control_not_a_fact(tmp_path):
    _, facts, controls = load(tmp_path)
    assert {f.fiscal_year for f in facts} == {2025}
    capex = next(c for c in controls if c.line == "capex")
    assert (capex.fiscal_year, capex.printed, capex.page) == (2024, Decimal("3728000000"), 8)
