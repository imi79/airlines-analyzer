"""`uv run tearsheet samples`: the pre-built tearsheets the app's demo mode reads.

    samples/figures.json                    every figure of the nine companies, with its source
    samples/tearsheets/<company>_FY<y>.json one per drafted tearsheet (latest two years)

Built from the facts database, so `uv run tearsheet all` must have run first. The files are
text (JSON) and committed: any change to a figure shows in the history.
"""

from __future__ import annotations

from pathlib import Path

from tearsheet.config import DB_PATH
from tearsheet.render import library, tearsheet
from tearsheet.render.library import Library


def write_samples(
    db_path: Path = DB_PATH,
    figures_file: Path = library.FIGURES_FILE,
    folder: Path = tearsheet.TEARSHEETS,
) -> tuple[Library, list[Path]]:
    from tearsheet.narrative.run import build_sheets

    if not db_path.exists():
        raise SystemExit(f"no database at {db_path}: run `uv run tearsheet all` first")
    lib = library.from_database(db_path)
    lib.write(figures_file)
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.json"):
        old.unlink()
    written = [
        tearsheet.write(tearsheet.from_database(db_path, sheet), folder)
        for sheet in build_sheets(db_path).drafted
    ]
    return lib, written
