"""M6 checklist: the Excel backup recalculates to the app's values (LibreOffice, as gate 1)."""

from __future__ import annotations

import copy
import re
import zipfile
from decimal import Decimal

import pytest

from tearsheet.render import manifest, tearsheet, workbook
from tearsheet.render import workbook_check as wc
from tearsheet.render.library import Library

needs_libreoffice = pytest.mark.skipif(not wc.available(), reason="LibreOffice not installed")


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library.read()


def _book(lib, issuer, year, path, **kw):
    ts = tearsheet.read(issuer, year)
    workbook.write(lib, ts, manifest.build(lib, ts), path, **kw)
    return path


def test_five_sheets_and_named_inputs(lib, tmp_path):
    path = _book(lib, "aena", 2025, tmp_path / "aena.xlsx")
    xml = zipfile.ZipFile(path).read("xl/workbook.xml").decode()
    assert re.findall(r'<sheet name="([^"]+)"', xml) == [
        "Inputs", "Metrics", "Peers", "Extracted", "Manifest",
    ]  # fmt: skip
    for name in ("revenue_FY2025", "ebitda_FY2025", "net_leverage_FY2025", "passengers_FY2025"):
        assert f'name="{name}"' in xml
    sheet = zipfile.ZipFile(path).read("xl/worksheets/sheet2.xml").decode()
    assert "<f>ebitda_FY2025/revenue_FY2025</f>" in sheet  # a live formula on named inputs


def test_workbook_from_memory(lib):
    ts = tearsheet.read("vie", 2025)
    data = workbook.write(lib, ts, manifest.build(lib, ts))
    assert data[:2] == b"PK" and len(data) > 10_000


@needs_libreoffice
def test_recalculates_to_the_app_values(lib, tmp_path):
    result = wc.check(_book(lib, "afkl", 2025, tmp_path / "afkl.xlsx"))
    assert result.ok, result.mismatches
    assert result.checked > 60 and result.medians_checked > 5


@needs_libreoffice
def test_values_come_from_the_recalculation_not_the_file(lib, tmp_path):
    """Saved without results, the formulas can only match if LibreOffice computes them."""
    result = wc.check(_book(lib, "easyjet", 2025, tmp_path / "e.xlsx", cached_results=False))
    assert result.ok, result.mismatches


@needs_libreoffice
def test_the_check_catches_a_wrong_input(lib, tmp_path):
    bad = copy.copy(lib)
    bad.figures = dict(lib.figures)
    k = "iag:revenue@FY2025"
    bad.figures[k] = dict(lib.figures[k], value=str(Decimal(lib.figures[k]["value"]) * 2))
    result = wc.check(_book(bad, "iag", 2025, tmp_path / "bad.xlsx"))
    assert not result.ok
    assert any(m[0] == "EBITDA margin" and m[1] == "2025" for m in result.mismatches)
