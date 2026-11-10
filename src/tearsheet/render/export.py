"""Export a tearsheet (M6): the two-page PDF, the Excel backup and the run manifest.

    uv run tearsheet export                          all 18 pre-built tearsheets, into exports/
    uv run tearsheet export --issuer afkl --year 2025
    uv run tearsheet export --check                  also recalculate every workbook (LibreOffice)

The analyst's saved work (notes/<company>_FY<year>.yaml) is included when it exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tearsheet.config import ROOT
from tearsheet.render import manifest, notes, pdf, tearsheet, workbook
from tearsheet.render.library import Library

EXPORTS = ROOT / "exports"


@dataclass
class Exported:
    name: str  # file stem: <company>_FY<year>
    pdf: bytes
    xlsx: bytes
    manifest: dict
    font_size: float
    view_truncated: bool


def build(
    lib: Library, ts: dict, note: dict | None, mode: str, session_reviews: int = 0
) -> Exported:
    m = manifest.build(lib, ts, note, mode=mode, session_reviews=session_reviews)
    rendered = pdf.render(lib, ts, note, m)
    xlsx = workbook.write(lib, ts, m)
    return Exported(f"{ts['issuer']}_FY{ts['fiscal_year']}", rendered.pdf, xlsx, m,
                    rendered.font_size, rendered.view_truncated)  # fmt: skip


def write(e: Exported, folder: Path, only: str | None = None) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)
    out = []
    if only in (None, "pdf"):
        out.append(folder / f"{e.name}.pdf")
        out[-1].write_bytes(e.pdf)
    if only in (None, "excel"):
        out.append(folder / f"{e.name}.xlsx")
        out[-1].write_bytes(e.xlsx)
    if only is None:
        out.append(manifest.write(e.manifest, folder))
    return out


def run(issuer: str | None = None, year: int | None = None, folder: Path = EXPORTS,
        only: str | None = None, check: bool = False) -> list[dict]:  # fmt: skip
    from tearsheet.render import workbook_check

    lib = Library.read()
    picks = [(i, y) for i, y in tearsheet.available()
             if (issuer is None or i == issuer) and (year is None or y == year)]  # fmt: skip
    if not picks:
        raise SystemExit(f"no pre-built tearsheet for {issuer} {year} (see samples/tearsheets)")
    results = []
    for i, y in picks:
        ts = tearsheet.read(i, y)
        note = notes.load(i, y) if notes.path_for(i, y).exists() else None
        e = build(lib, ts, note, mode="export")
        paths = write(e, folder, only)
        row = {"tearsheet": e.name, "font_size": e.font_size, "files": paths,
               "view_truncated": e.view_truncated}  # fmt: skip
        if check:
            xlsx = next((p for p in paths if p.suffix == ".xlsx"), None)
            if xlsx is None:
                xlsx = folder / f"{e.name}.xlsx"
                xlsx.write_bytes(e.xlsx)
            r = workbook_check.check(xlsx)
            row |= {"metrics_checked": r.checked, "medians_checked": r.medians_checked,
                    "mismatches": r.mismatches}  # fmt: skip
        results.append(row)
    return results
