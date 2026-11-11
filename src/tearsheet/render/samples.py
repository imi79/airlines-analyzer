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
    import duckdb

    from tearsheet.config import load_issuers
    from tearsheet.narrative.factsheet import build, load_figures, load_narrative, load_specs
    from tearsheet.narrative.run import build_sheets

    if not db_path.exists():
        raise SystemExit(f"no database at {db_path}: run `uv run tearsheet all` first")
    lib = library.from_database(db_path)
    lib.write(figures_file)
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.glob("*.json"):
        old.unlink()
    # The drafted company-years, each with the fact sheet of M8: every metric (decision 0022).
    narrative = load_narrative()
    specs = load_specs(narrative)
    con = duckdb.connect(str(db_path), read_only=True)
    figures = load_figures(con, set(specs))
    con.close()
    issuers = {i.id: i for i in load_issuers()}
    written = [
        tearsheet.write(
            tearsheet.from_database(
                db_path, build(issuers[s.issuer], s.fiscal_year, figures, specs, narrative)
            ),
            folder,
        )
        for s in build_sheets(db_path).drafted
    ]
    return lib, written
