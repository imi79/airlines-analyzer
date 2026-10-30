"""Command line: `uv run tearsheet <command>`.

    load         download (or read from cache) every v1 filing and rebuild the facts database
    report       write the reports: docs/m1 (figures) and docs/m2 (metrics, peers, reconciliation)
    all          load, then report
    add-package  convert and register an ESEF package (.zip) downloaded by hand:
                 add-package <zip> --issuer afkl --origin "Air France-KLM website" [--url ...]

Add --offline to use only the local cache (no network).
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from tearsheet import reports
from tearsheet.config import load_issuers
from tearsheet.ingest.client import Client
from tearsheet.metrics import reports as metric_reports
from tearsheet.pipeline import load_all

CHECK_ISSUERS = ["afkl", "adp"]  # decision 0004: the M1 spot check
CHECK_YEARS = [2023, 2024]


def main() -> None:
    parser = argparse.ArgumentParser(prog="tearsheet", description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["load", "report", "all", "add-package"])
    parser.add_argument("package", nargs="?", type=Path, help="add-package: the .zip file")
    parser.add_argument("--offline", action="store_true", help="use the local cache only")
    parser.add_argument("--issuer", help="add-package: issuer id, e.g. afkl")
    parser.add_argument("--origin", help="add-package: where the package came from")
    parser.add_argument("--url", help="add-package: the page or link it was downloaded from")
    parser.add_argument("--downloaded-on", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    if args.command == "add-package":
        from tearsheet.ingest.package import add_package

        if not (args.package and args.issuer and args.origin):
            parser.error("add-package needs the .zip file, --issuer and --origin")
        issuer = {i.id: i for i in load_issuers()}[args.issuer]
        entry = add_package(args.package, issuer, args.origin, args.url, args.downloaded_on)
        print(f"registered {entry['filing_id']} ({entry['error_count']} Arelle errors)")
        return

    if args.command in ("load", "all"):
        results = load_all(Client(offline=args.offline))
        for r in results:
            years = sorted({f.fiscal_year for f in r.facts})
            missing = sum(g.counts_as_missing for g in r.gaps)
            print(
                f"{r.issuer.name:28} FY{years[0]}-FY{years[-1]}  "
                f"{sum(f.primary for f in r.facts):4} figures  {missing} missing"
            )
    if args.command in ("report", "all"):
        reports.export_csv()
        totals = reports.coverage_report()
        path = reports.check_sheet(CHECK_ISSUERS, CHECK_YEARS)
        matched, checked = reports.manual_entries_report()
        metric_reports.write_all()
        print(f"coverage: {totals}; check sheet: {path}")
        print(f"figures entered by hand: prior-year control {matched}/{checked} match")


if __name__ == "__main__":
    main()
