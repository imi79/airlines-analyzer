"""Command line: `uv run tearsheet <command>`.

    load      download (or read from cache) every v1 filing and rebuild the facts database
    report    write the CSV exports, coverage report and check sheet to docs/m1/
    all       load, then report

Add --offline to use only the local cache (no network).
"""

from __future__ import annotations

import argparse

from tearsheet import reports
from tearsheet.ingest.client import Client
from tearsheet.pipeline import load_all

CHECK_ISSUERS = ["afkl", "adp"]  # decision 0004: the M1 spot check
CHECK_YEARS = [2023, 2024]


def main() -> None:
    parser = argparse.ArgumentParser(prog="tearsheet", description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["load", "report", "all"])
    parser.add_argument("--offline", action="store_true", help="use the local cache only")
    args = parser.parse_args()

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
        print(f"coverage: {totals}; check sheet: {path}")


if __name__ == "__main__":
    main()
