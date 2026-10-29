"""Paths and issuer configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config"
DATA = ROOT / "data"
CACHE = DATA / "raw"
DB_PATH = DATA / "tearsheet.duckdb"
MANUAL_FILINGS = ROOT / "filings"
FIRST_FISCAL_YEAR = 2021


@dataclass(frozen=True)
class Issuer:
    id: str
    name: str
    type: str  # airline | airport
    lei: str
    currency: str
    fiscal_year_end: str  # "MM-DD"
    country: str
    status: str
    segment: str | None = None
    leases_in_borrowings: bool = False
    leases_evidence: str | None = None
    extra: dict = field(default_factory=dict, compare=False)


def load_issuers(path: Path = CONFIG / "issuers.yaml", status: str | None = "v1") -> list[Issuer]:
    known = set(Issuer.__dataclass_fields__) - {"extra"}
    issuers = []
    for raw in yaml.safe_load(path.read_text())["issuers"]:
        if status and raw.get("status") != status:
            continue
        values = {k: v for k, v in raw.items() if k in known}
        extra = {k: v for k, v in raw.items() if k not in known}
        issuers.append(Issuer(**values, extra=extra))
    return issuers
