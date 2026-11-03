"""The commentary score sheet (M4 checklist): Imane scores ten drafts from 1 to 5.

Four criteria from the spec: accuracy, relevance, concision, credit insight. The sheet
averages them per draft and over the ten; the pass mark is 4. The drafts are the first ten
of the drafting order (the latest year of all nine companies, then Air France-KLM's year
before), each printed in full on its own sheet so the file can be read on its own.

Written only when the file does not exist yet, or holds no score: a rerun never erases
Imane's scores.
"""

from __future__ import annotations

import re
import zipfile
from datetime import datetime
from pathlib import Path

import xlsxwriter

from tearsheet.config import ROOT
from tearsheet.narrative.drafting import Outcome, rendered_text
from tearsheet.narrative.factsheet import load_narrative

PATH = ROOT / "docs" / "m4" / "score_sheet.xlsx"
CRITERIA = [
    ("Accuracy", "Every statement is true and fairly put; nothing misleading."),
    ("Relevance", "The points a credit analyst would pick for this company and year."),
    ("Concision", "No padding or repetition; reads like a tearsheet, not a report."),
    ("Credit insight", "Links figures to credit quality: leverage, cash, liquidity, peers."),
]
DRAFTS = 10
CREATED = datetime(2026, 11, 3)
PASS_MARK = 4


def has_scores(path: Path) -> bool:
    """True if Imane has typed any score (the file is then left alone)."""
    if not path.exists():
        return False
    with zipfile.ZipFile(path) as z:
        sheet = z.read("xl/worksheets/sheet1.xml").decode()
    # Score cells are C5 to F14; xlsxwriter writes blank styled cells without <v>.
    return bool(re.search(r'<c r="[C-F](?:[5-9]|1[0-4])"[^>]*>(?:<f>[^<]*</f>)?<v>', sheet))


def write(outcomes: list[Outcome], path: Path = PATH) -> bool:
    """Write the score sheet; returns False (and writes nothing) if scores are already in."""
    if has_scores(path):
        return False
    narrative = load_narrative()
    chosen = [o for o in outcomes if o.drafted][:DRAFTS]
    path.parent.mkdir(parents=True, exist_ok=True)
    book = xlsxwriter.Workbook(str(path))
    book.set_properties({"created": CREATED})  # a fixed date: reruns give the same file
    bold = book.add_format({"bold": True})
    wrap = book.add_format({"text_wrap": True, "valign": "top"})
    head = book.add_format(
        {"bold": True, "text_wrap": True, "valign": "top", "bg_color": "#DDEBF7"}
    )
    score = book.add_format({"bg_color": "#FFF2CC", "align": "center", "border": 1})
    avg = book.add_format({"num_format": "0.0", "align": "center"})
    big = book.add_format({"num_format": "0.00", "bold": True, "font_size": 12})

    ws = book.add_worksheet("Scores")
    ws.write(0, 0, "M4 commentary score: give each draft a score from 1 (poor) to 5 "
                   "(publishable as is) on each criterion, in the yellow cells.", bold)  # fmt: skip
    ws.write(1, 0, "Pass mark: an average of 4 or more over the ten drafts. Each draft is "
                   "printed in full on its own sheet (tabs below).")  # fmt: skip
    ws.write(3, 0, "#", head)
    ws.write(3, 1, "Draft", head)
    for c, (name, hint) in enumerate(CRITERIA, start=2):
        ws.write(3, c, f"{name}\n{hint}", head)
    ws.write(3, 6, "Average", head)
    ws.write(3, 7, "Comments", head)
    ws.set_row(3, 75)
    ws.set_column(0, 0, 4)
    ws.set_column(1, 1, 38)
    ws.set_column(2, 5, 18)
    ws.set_column(6, 6, 10)
    ws.set_column(7, 7, 60)
    for n, o in enumerate(chosen, start=1):
        row = 3 + n
        ws.write(row, 0, n)
        ws.write_url(row, 1, f"internal:'{n}'!A1", string=f"{o.sheet.name} {o.sheet.period_label}")
        for c in range(2, 6):
            ws.write_blank(row, c, None, score)
        cells = f"C{row + 1}:F{row + 1}"
        ws.write_formula(row, 6, f'=IF(COUNT({cells})=0,"",AVERAGE({cells}))', avg)
        ws.write_blank(row, 7, None, wrap)
    last = 3 + len(chosen) + 1
    ws.write(last + 1, 1, "Average over the drafts scored", bold)
    ws.write_formula(last + 1, 6, f'=IF(COUNT(G5:G{last})=0,"",AVERAGE(G5:G{last}))', big)
    ws.write(last + 2, 1, "Pass (4 or more)?", bold)
    ws.write_formula(
        last + 2, 6, f'=IF(G{last + 2}="","",IF(G{last + 2}>={PASS_MARK},"yes","no"))', bold
    )

    for n, o in enumerate(chosen, start=1):
        page = book.add_worksheet(str(n))
        page.set_column(0, 0, 110, wrap)
        page.write(0, 0, f"{o.sheet.name}, {o.sheet.period_label}", bold)
        status = "passed the verifier" if o.passed else "needs manual editing"
        page.write(1, 0, f"Draft status: {status}. Figures written by code; words by the AI.")
        row = 3
        rendered = o.sheet.rendered()
        for name, sentences in o.sections.items():
            page.write(row, 0, narrative["sections"][name]["title"], bold)
            row += 1
            bullet = "• " if name == "watch_items" else ""
            for s in sentences:
                page.write(row, 0, bullet + rendered_text(s.text, rendered))
                row += 1
            row += 1
        page.write(row, 0, "Analyst view: left for the analyst (never drafted).", bold)
    book.close()
    return True
