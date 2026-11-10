"""Command line: `uv run tearsheet <command>`.

    load         download (or read from cache) every v1 filing and rebuild the facts database
    report       write the reports: docs/m1 (figures), docs/m2 (metrics, peers, reconciliation)
                 and docs/m3 (figures read from the report text, answer key score)
    all          load, then report
    extract      ask the AI to read operating figures from each report not read before
                 (costs tokens; answers are recorded, so `load` replays them for free).
                 --issuer afkl,easyjet limits the AI calls to those companies
    draft        ask the AI to draft the commentary of each company's latest two years (M4),
                 check every sentence and write docs/m4 (costs tokens; answers are recorded,
                 so `all` and `report` replay them for free). --issuer limits the AI calls
    samples      write the pre-built tearsheets the app's demo mode reads (samples/), from the
                 database: every figure with its source, and the 18 drafted tearsheets
    export       the two-page PDF, the Excel backup and the run manifest of each pre-built
                 tearsheet, into exports/ (--issuer, --year to pick one; --check recalculates
                 every workbook with LibreOffice and compares it with the app's values)
    app          open the web app (demo mode by default; live mode needs the database)
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
        "command",
        choices=[
            "load",
            "report",
            "all",
            "extract",
            "draft",
            "samples",
            "export",
            "app",
            "llm-check",
            "add-package",
        ],  # fmt: skip
    )
    parser.add_argument("package", nargs="?", type=Path, help="add-package: the .zip file")
    parser.add_argument("--offline", action="store_true", help="use the local cache only")
    parser.add_argument("--issuer", help="issuer id(s), e.g. afkl or afkl,easyjet")
    parser.add_argument("--origin", help="add-package: where the package came from")
    parser.add_argument("--url", help="add-package: the page or link it was downloaded from")
    parser.add_argument("--year", type=int, help="export: the fiscal year")
    parser.add_argument("--out", type=Path, help="export: folder (default exports/)")
    parser.add_argument("--only", choices=["pdf", "excel"], help="export: one kind of file")
    parser.add_argument("--check", action="store_true", help="export: recalculate workbooks")
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

    if args.command == "samples":
        from tearsheet.render.samples import write_samples

        lib, written = write_samples()
        print(f"samples: {len(lib.figures)} figures, {len(written)} tearsheets (samples/)")
        return

    if args.command == "export":
        from tearsheet.render import export

        rows = export.run(args.issuer, args.year, args.out or export.EXPORTS, args.only,
                          args.check)  # fmt: skip
        failed = 0
        for r in rows:
            line = f"{r['tearsheet']:16} PDF at {r['font_size']}pt"
            if r["view_truncated"]:
                line += " (analyst view cut: continued in the app)"
            if "mismatches" in r:
                ok = not r["mismatches"] and r["metrics_checked"]
                failed += not ok
                line += (f"  Excel: {r['metrics_checked']} metrics and {r['medians_checked']} "
                         f"medians recalculated, {'all equal' if ok else 'MISMATCH'}")  # fmt: skip
            print(line)
        print(f"{len(rows)} exported to {args.out or export.EXPORTS}")
        raise SystemExit(1 if failed else 0)

    if args.command == "app":
        import subprocess
        import sys

        app = Path(__file__).parent / "app" / "main.py"
        raise SystemExit(subprocess.call([sys.executable, "-m", "streamlit", "run", str(app)]))

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
            a, h, b, f = scored["all"], scored["holdout"], scored["blind"], scored["fourth"]
            print(
                f"answer key: {a.counts['verified_correct']}/{a.total} verified and correct "
                f"({a.share_verified:.0%}; held-out {h.counts['verified_correct']}/{h.total}, "
                f"blind {b.counts['verified_correct']}/{b.total}, "
                f"fourth {f.counts['verified_correct']}/{f.total}), "
                f"{a.counts['verified_wrong']} verified but wrong (docs/m3/answer_key_score.md)"
            )
    if args.command in ("report", "all", "extract", "draft"):
        from tearsheet.llm import LLM
        from tearsheet.narrative import run as drafting

        live = args.command == "draft"
        only = set(args.issuer.split(",")) if live and args.issuer else None
        outcomes = drafting.run(LLM(offline=not live), only=only)
        done = [o for o in outcomes if o.drafted]
        length, companies, ok = drafting.gate2(outcomes)
        print(
            f"drafts: {len(done)}/{len(outcomes)} drafted, {sum(o.passed for o in done)} passed "
            f"the verifier, {sum(o.first_try_passed for o in done)} at the first try; gate 2: "
            f"run of {length} over {len(companies)} companies, "
            f"{'passed' if ok else 'not passed'} (docs/m4/drafts.md)"
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
