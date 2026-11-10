"""M6: every metric's spreadsheet formula (catalog.yaml, `excel:`) gives the stored figure."""

from __future__ import annotations

from decimal import Decimal

import pytest

from tearsheet.metrics.engine import load_catalog
from tearsheet.render import sheet_formulas as sf
from tearsheet.render.library import Library


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library.read()


def test_every_metric_has_a_formula():
    assert all(spec.get("excel") for spec in load_catalog().values())


def test_every_computed_figure_is_reproduced_by_its_formula(lib):
    computed = [k for k, f in lib.figures.items() if f["source_type"] == "computed"]
    assert len(computed) > 800
    for k in computed:
        resolved = sf.resolve(lib, k)  # raises if an input is unused or missing
        stored = Decimal(lib.figures[k]["value"])
        got = sf.evaluate(lib, resolved)
        assert abs(got - stored) <= Decimal("1e-9") * max(abs(stored), Decimal(1)), k


def test_company_specific_formulas(lib):
    # ADP reports a share of associates inside operating profit; Air France-KLM does not
    adp = sf.to_excel(sf.resolve(lib, "adp:ebitda@FY2025"))
    afkl = sf.to_excel(sf.resolve(lib, "afkl:ebitda@FY2025"))
    assert "share_of_associates_FY2025" in adp
    assert afkl == "=operating_profit_FY2025+dda_FY2025"
    # growth uses the year before
    growth = sf.to_excel(sf.resolve(lib, "aena:traffic_growth@FY2025"))
    assert growth == "=passengers_FY2025/passengers_FY2024-1"


def test_formula_that_does_not_fit_its_inputs_is_refused(lib, monkeypatch):
    monkeypatch.setitem(sf.templates(), "ebitda_margin", "ebitda / passengers")
    with pytest.raises(sf.FormulaError):
        sf.resolve(lib, "afkl:ebitda_margin@FY2025")
