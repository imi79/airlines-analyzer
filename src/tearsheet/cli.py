"""Command line: `uv run tearsheet <command>`.

    load         download (or read from cache) every v1 filing and rebuild the facts database
    report       write the reports: docs/m1 (figures), docs/m2 (metrics, peers, reconciliation)
                 and docs/m3 (figures read from the report text, answer key score)
    all          load, then report
    extract      ask the AI to read operating figures from each report not read before
                 (costs tokens; answers are recorded, so `load` replays them for free).
                 --issuer afkl,easyjet limits the AI calls to those companies
    llm-check    send one tiny request to confirm config/models.yaml and the API key work
    add-package  convert and register an ESEF package (.zip) downloaded by hand:
                 add-package <zip> --issuer afkl --origin "Air France-KLM website" [--url ...]

Add --offline to use only the local cache (no network). `load` and `report` never call the AI.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from tearsheet import reports
from tearsheet.config import load_issuers
from tearsheet.extract import report as extraction_reports
from tearsheet.ingest.client import Client
from tearsheet.metrics import reports as metric_reports
from tearsheet.pipeline import load_all

CHECK_ISSUERS = ["afkl", "adp"]  # decision 0004: the M1 spot check
CHECK_YEARS = [2023, 2024]


def main() -> None:
    parser = argparse.ArgumentParser(prog="tearsheet", description=__doc__.splitlines()[0])
    parser.add_argument(
        "command", choices=["load", "report", "all", "extract", "llm-check", "add-package"]
    )
    parser.add_argument("package", nargs="?", type=Path, help="add-package: the .zip file")
    parser.add_argument("--offline", action="store_true", help="use the local cache only")
    parser.add_argument("--issuer", help="issuer id(s), e.g. afkl or afkl,easyjet")
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

    if args.command == "llm-check":
        from tearsheet.llm import LLM

        print(LLM().check())
        return

    if args.command in ("load", "all", "extract"):
        llm, only = None, None
        if args.command == "extract":
            from tearsheet.llm import LLM

            llm = LLM()
            only = set(args.issuer.split(",")) if args.issuer else None
        results = load_all(Client(offline=args.offline), llm=llm, only=only)
        for r in results:
            years = sorted({f.fiscal_year for f in r.facts})
            missing = sum(g.counts_as_missing for g in r.gaps)
            print(
                f"{r.issuer.name:28} FY{years[0]}-FY{years[-1]}  "
                f"{sum(f.primary for f in r.facts):4} figures  {missing} missing"
                + _extraction_summary(r.extraction)
            )
    if args.command in ("report", "all", "extract"):
        reports.export_csv()
        totals = reports.coverage_report()
        path = reports.check_sheet(CHECK_ISSUERS, CHECK_YEARS)
        matched, checked = reports.manual_entries_report()
        metric_reports.write_all()
        print(f"coverage: {totals}; check sheet: {path}")
        print(f"figures entered by hand: prior-year control {matched}/{checked} match")
        read, scored = extraction_reports.write_all()
        print(
            f"read from report text: {read['verified']} verified, {read['unverified']} "
            f"unverified, from {read['reports']} reports (docs/m3/extractions.md)"
        )
        if scored is not None:
            print(
                f"answer key: {scored.counts['verified_correct']}/{scored.total} verified and "
                f"correct ({scored.share_verified:.0%}), {scored.counts['verified_wrong']} "
                "verified but wrong (docs/m3/answer_key_score.md)"
            )


def _extraction_summary(extraction) -> str:
    if extraction is None:
        return ""
    primary = [c for c in extraction.candidates if c.primary]
    verified = sum(c.status in ("verified", "overridden") for c in primary)
    not_run = sum(1 for run in extraction.runs if run.error) + len(extraction.skipped)
    tokens = sum(
        run.result.usage.input_tokens + run.result.usage.output_tokens
        for run in extraction.runs
        if run.result is not None and not run.result.cached
    )
    text = f"  | read from text: {verified}/{len(primary)} verified"
    if not_run:
        text += f", {not_run} report(s) not read"
    if tokens:
        text += f", {tokens:,} new tokens"
    return text


if __name__ == "__main__":
    main()
