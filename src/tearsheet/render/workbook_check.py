"""Check the Excel backup by recalculation (M6 checklist): LibreOffice opens each workbook,
recomputes every formula from scratch (not the values saved in the file), and every metric
must equal the app's value. Same method as gate 1 (decision 0009).
"""

from __future__ import annotations

import csv
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

# LibreOffice profile setting: always recalculate Excel files when opening them.
PROFILE = """<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry"
 xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="OOXMLRecalcMode"
 oor:op="fuse"><value>0</value></prop></item>
</oor:items>
"""
# CSV export of every sheet, raw values (not as displayed), UTF-8.
CSV_FILTER = "csv:Text - txt - csv (StarCalc):44,34,UTF8,1,,0,false,true,false,false,false,-1"
TOLERANCE = Decimal("1e-9")  # relative; LibreOffice computes in binary floating point


def available() -> bool:
    return shutil.which("soffice") is not None


def recalculate(xlsx: Path) -> dict[str, list[list[str]]]:
    """Every sheet of the workbook after LibreOffice's recalculation, as rows of text."""
    with tempfile.TemporaryDirectory() as tmp:
        profile = Path(tmp) / "profile" / "user"
        profile.mkdir(parents=True)
        (profile / "registrymodifications.xcu").write_text(PROFILE)
        copy = Path(tmp) / "book.xlsx"
        shutil.copy(xlsx, copy)
        subprocess.run(
            ["soffice", f"-env:UserInstallation=file://{Path(tmp) / 'profile'}", "--headless",
             "--convert-to", CSV_FILTER, "--outdir", tmp, str(copy)],
            check=True, capture_output=True, timeout=180,
        )  # fmt: skip
        sheets = {}
        for path in Path(tmp).glob("book-*.csv"):
            name = path.stem.removeprefix("book-")
            sheets[name] = list(csv.reader(path.open(encoding="utf-8")))
        return sheets


@dataclass
class Result:
    checked: int
    mismatches: list[tuple[str, str, str, str]]  # metric, year, recalculated, app value
    medians_checked: int

    @property
    def ok(self) -> bool:
        return self.checked > 0 and not self.mismatches


def _num(text: str) -> Decimal | None:
    """A recalculated value as exported: LibreOffice keeps the % sign on percentages."""
    try:
        text = text.replace(",", "").strip()
        if text.endswith("%"):
            return Decimal(text[:-1]) / 100
        return Decimal(text)
    except (InvalidOperation, AttributeError):
        return None


def check(xlsx: Path) -> Result:
    sheets = recalculate(xlsx)
    mismatches, checked = [], 0
    for row in sheets["Metrics"][4:]:
        if len(row) < 4 or not row[3]:
            continue
        got, want = _num(row[2]), _num(row[3])
        if want is None:
            mismatches.append((row[0], row[1], row[2], f"unreadable app value {row[3]!r}"))
            continue
        checked += 1
        if got is None or abs(got - want) > TOLERANCE * max(abs(want), Decimal(1)):
            mismatches.append((row[0], row[1], row[2], row[3]))
    medians = 0
    head = sheets["Peers"][3]
    col = head.index("Median (live formula)")
    for row in sheets["Peers"][4:]:
        if len(row) > col + 1 and row[col + 1]:
            medians += 1
            got, want = _num(row[col]), _num(row[col + 1])
            if got is None or abs(got - want) > TOLERANCE * max(abs(want), Decimal(1)):
                mismatches.append((f"median {row[0]}", "", row[col], row[col + 1]))
    return Result(checked, mismatches, medians)
