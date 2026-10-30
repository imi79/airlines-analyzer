"""Add an ESEF report package downloaded by hand (decision 0004, choice 4b).

The package (.zip) is converted to xBRL-JSON with Arelle, the open-source XBRL processor that
filings.xbrl.org also uses, so the result has the same shape as a database filing. The
conversion was checked on ADP's FY2024 package: the same 343 numeric facts as the database's
own xBRL-JSON (decision 0006).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date
from importlib.metadata import version
from pathlib import Path

import yaml

from tearsheet.config import MANUAL_FILINGS, Issuer
from tearsheet.ingest import manual
from tearsheet.ingest.xbrl_json import parse_period

HTTPS_PLUGIN = Path(__file__).with_name("arelle_https.py")


class PackageError(Exception):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def convert(package: Path, out_json: Path) -> int:
    """Run Arelle on the package; returns the number of errors it logged."""
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "arelle.log"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "arelle.CntlrCmdLine",
                "--file",
                str(package),
                "--plugins",
                f"saveLoadableOIM|{HTTPS_PLUGIN}",
                "--saveLoadableOIM",
                str(out_json),
                "--internetConnectivity",
                "online",
                "--logFile",
                str(log),
            ],
            check=True,
            capture_output=True,
        )
        errors = [line for line in log.read_text().splitlines() if line.startswith("[error]")]
    if not out_json.exists():
        raise PackageError("Arelle produced no output:\n" + "\n".join(errors))
    return len(errors)


def identify(document: dict) -> tuple[str, date]:
    """The reporting entity's LEI and the fiscal year end (most common annual period end)."""
    entities, ends = Counter(), Counter()
    for fact in document.get("facts", {}).values():
        dims = fact.get("dimensions", {})
        if dims.get("entity"):
            entities[dims["entity"].split(":")[-1]] += 1
        if dims.get("period") and "/" in dims["period"]:
            start, end = parse_period(dims["period"])
            if 300 <= (end - start).days + 1 <= 400:
                ends[end] += 1
    if not entities or not ends:
        raise PackageError("No entity or annual period found in the report.")
    return entities.most_common(1)[0][0], max(ends)


def register(entry: dict, register_path: Path | None = None) -> None:
    """Add or replace the entry for this filing in filings/manual.yaml."""
    register_path = register_path or manual.REGISTER
    data = yaml.safe_load(register_path.read_text()) if register_path.exists() else {}
    filings = [f for f in (data.get("filings") or []) if f["filing_id"] != entry["filing_id"]]
    filings.append(entry)
    filings.sort(key=lambda f: (f["issuer"], str(f["period_end"])))
    header = (
        "# ESEF report packages loaded by hand (decision 0004, choice 4b).\n"
        "# Written by `tearsheet add-package`; one entry per package.\n"
    )
    register_path.parent.mkdir(parents=True, exist_ok=True)
    register_path.write_text(
        header + yaml.safe_dump({"filings": filings}, sort_keys=False, allow_unicode=True)
    )


def add_package(
    package: Path,
    issuer: Issuer,
    origin: str,
    source_url: str | None,
    downloaded_on: date,
    folder: Path = MANUAL_FILINGS,
    register_path: Path | None = None,
) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        out_json = Path(tmp) / "report.json"
        errors = convert(package, out_json)
        document = json.loads(out_json.read_text())
    lei, period_end = identify(document)
    if lei != issuer.lei:
        raise PackageError(f"Package is for LEI {lei}, not {issuer.name} ({issuer.lei}).")
    if period_end.strftime("%m-%d") != issuer.fiscal_year_end:
        raise PackageError(f"Year ends {period_end}, not on {issuer.name}'s year-end date.")

    filing_id = f"{lei}-{period_end.isoformat()}-ESEF-manual"
    target = folder / issuer.id / f"{filing_id}.json.gz"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(gzip.compress(json.dumps(document, sort_keys=True).encode(), mtime=0))
    entry = {
        "filing_id": filing_id,
        "issuer": issuer.id,
        "period_end": period_end.isoformat(),
        "origin": origin,
        "source_url": source_url,
        "package_file": package.name,
        "package_sha256": sha256(package),
        "downloaded_on": downloaded_on.isoformat(),
        "converted_with": f"Arelle {version('arelle-release')}",
        "error_count": errors,
        "xbrl_json": str(target.relative_to(folder)),
    }
    register(entry, register_path)
    return entry
