# 0020 · M6: the PDF, the Excel backup and the run manifest

Date: 2026-11-10 · Status: plan approved by Imane with every recommendation ("approved with
all recommendations, go ahead on m6-exports")

**Choices approved with the plan** (`docs/m6/plan.md`):

1. **Text steps down to fit two pages** (8.5, 8.0, 7.5 point); still too long is an error,
   never a silent cut. In the 18 tearsheets as drafted, 16 print at 8.5 point and two at 8.0
   (IAG FY2025, Wizz Air FY2026); with a full analyst view, four print at 8.0.
2. **The analyst view has a fixed box of eight lines** on page 2. A longer view is cut at a
   word with "… (continued in the app)", and the app warns before export.
3. **Flagged text prints with a marker**: † on a sentence the analyst edited with a figure not
   traced to a filing, ‡ on a section the verifier did not clear, each with a footnote.
4. **LibreOffice checks all 18 workbooks; Imane may open one in Microsoft Excel**
   (`docs/m6/afkl_FY2025.xlsx`).
5. **All 18 PDFs are kept for review** in `docs/m6/pdf/` (2.5 MB).

**Choices made while building:**

- **Formulas live in `catalog.yaml`** (`excel:`), next to each metric's definition, written on
  the inputs the code recorded for that company and year. Optional lines (`share_of_associates?`),
  either-or inputs (`finance_costs | interest_expense | interest_paid`), company-specific sums
  (`sum()` for total debt and cash-like investments) and the prior year (`passengers@prior`)
  are spelled out in the formula language at the top of the catalog. A formula that does not
  use every recorded input, or needs one that is missing, is an error.
- **Named cells**: every input and metric cell is named `<line>_FY<year>`, so a formula reads
  `=net_debt_FY2025/ebitda_FY2025` rather than `=Inputs!D47/Metrics!C12`.
- **The workbook covers every year of the company**, so growth rates have their prior year and a
  reviewer sees the history. The Metrics sheet is one row per metric and year, with the app's
  value and the difference next to the live formula.
- **Peer medians and ranks are live formulas** (`=MEDIAN`, `=RANK`) over the verified peer
  figures; a figure awaiting review or not meaningful is text, which both functions ignore.
- **The PDF also prints the operating performance and peer positioning commentary**, under
  the operating table and the peer table. The spec's page 2 lists the tables only; leaving out
  checked commentary that is on screen would make the PDF disagree with the app.
- **Definitions are split by page**: the key-figures metrics at the foot of page 1, the others
  in the page 2 footnotes. This balanced the pages enough for 8.5 point text.
- **Unit revenue and cost print as plain numbers in PDF tables, with the unit in the label**
  ("RASK (euro cents)": 4.33): "4.33 euro cents" in every cell pushed the operating table into
  the peer table.
- **Overflow is measured on the laid-out page**, not only by counting pages: a table wider than
  its column, or a clipped box hiding lines, counts as overflow and steps the text size down.
  The page count alone missed both problems on the first try (Wizz Air).
- **Statement lines get a definition from where they are reported** ("Revenue: as reported in
  the income statement (IFRS tag ifrs-full:Revenue)"), so every row of every PDF table is
  defined in the footnotes.
- **The manifest** lists every filing and report behind a figure on the tearsheet (peers
  included) with its SHA-256, the drafting, extraction and events models and prompt versions,
  the fact sheet fingerprint, the draft's tokens, the code version (git commit), the export time,
  and the analyst's edits, view and unsaved session reviews. It is a JSON file, the Manifest
  sheet, and one line in the PDF footnotes.
- **Filing links are full addresses.** The database stores them relative to filings.xbrl.org;
  the app's "Open the filing" button from M5 had the same flaw and is fixed with it.
- **Font**: Inter (SIL Open Font License, licence in `src/tearsheet/render/pdf/fonts/`), also
  used in the chart images, so the PDF is identical on any machine.
- **Exports are not committed** (`exports/` is ignored); `uv run tearsheet export` remakes them.
- **New software**: WeasyPrint 70 and vl-convert 1.9 (stack table); Jinja2 made explicit.
  WeasyPrint warns that a future version will need the HarfBuzz subsetting library: to list with
  Pango in the M7 deployment files.
