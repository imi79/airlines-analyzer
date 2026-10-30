"""Registering a hand-downloaded ESEF package (the Arelle conversion itself is replaced by a
small synthetic report; it was checked against the database on ADP FY2024, decision 0006)."""

import json
from datetime import date

import pytest

from tearsheet.config import Issuer
from tearsheet.ingest import package
from tearsheet.ingest.manual import manual_filings

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


def fake_convert(lei):
    def convert(_package, out_json):
        fact = {
            "value": "1000000",
            "decimals": -6,
            "dimensions": {
                "concept": "ifrs-full:Revenue",
                "entity": f"scheme:{lei}",
                "period": "2025-01-01T00:00:00/2026-01-01T00:00:00",
                "unit": "iso4217:EUR",
            },
        }
        ns = {"ifrs-full": "https://xbrl.ifrs.org/taxonomy/2024-03-27/ifrs-full"}
        out_json.write_text(json.dumps({"documentInfo": {"namespaces": ns}, "facts": {"f1": fact}}))
        return 0

    return convert


def test_package_is_converted_identified_and_registered(tmp_path, monkeypatch):
    monkeypatch.setattr(package, "convert", fake_convert(ISSUER.lei))
    zip_file = tmp_path / "abc-2025.zip"
    zip_file.write_bytes(b"package bytes")
    register = tmp_path / "manual.yaml"
    entry = package.add_package(
        zip_file,
        ISSUER,
        "company website",
        "https://example.com",
        date(2026, 10, 30),
        folder=tmp_path,
        register_path=register,
    )
    assert entry["filing_id"] == f"{ISSUER.lei}-2025-12-31-ESEF-manual"
    assert entry["package_sha256"] == package.sha256(zip_file)

    (filing,) = manual_filings(ISSUER, register=register, folder=tmp_path)
    assert filing.fiscal_year == 2025 and filing.origin == "company website"
    assert [f.concept for f in filing.report(None).facts] == ["ifrs-full:Revenue"]


def test_package_for_another_company_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(package, "convert", fake_convert("529900SOMEONEELSE000"))
    zip_file = tmp_path / "x.zip"
    zip_file.write_bytes(b"x")
    with pytest.raises(package.PackageError, match="not Example Air"):
        package.add_package(
            zip_file,
            ISSUER,
            "x",
            None,
            date(2026, 10, 30),
            folder=tmp_path,
            register_path=tmp_path / "manual.yaml",
        )
