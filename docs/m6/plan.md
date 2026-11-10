# M6 plan: the tearsheet as a two-page PDF and an Excel backup

Status: **approved by Imane** (2026-11-10) with every recommendation: 1. text steps down in
half points to a floor of 7.5 point; 2. a fixed analyst view box of about eight lines; 3. flagged
text printed with a marker and a footnote; 4. Imane opens one workbook in Microsoft Excel
(optional); 5. all 18 PDFs kept in `docs/m6/pdf/`. Built in the same session, on `m6-exports`.

## What M6 is for

M5 put the tearsheet on screen. M6 produces what an analyst sends or files: the **two-page PDF**
for the reader, and the **Excel backup** for the reviewer who wants to redo the sums. Both come
from the same figures the screen shows, so the three can never disagree. A third output, the
**run manifest**, is the audit stamp: which filings (with their fingerprints), which AI models
and which versions of the instructions produced this tearsheet.

Think of it as the printed credit note, its supporting model, and the cover sheet that says
which data room versions it was built from.

## The PDF: two A4 pages (spec)

**Page 1.** Header (company, type, fiscal year with its months, currency, peer group),
snapshot, the four-year KPI table, the two charts (leverage, liquidity), credit metrics
commentary.

**Page 2.** Operating metrics (four-year table: traffic and unit revenue for airlines, traffic
and revenue per passenger for airports), the peer table (company, peers, median, rank),
liquidity and funding, watch items, the analyst view, then footnotes: the definition of every
metric on the page, the filing links, a one-line manifest (prompt version, model, fact sheet
fingerprint, date), and the line "Draft prepared with AI assistance. Figures computed from
regulatory filings and checked automatically. Not investment advice."

**How it is made.** An HTML page laid out for print (Jinja2 template and print stylesheet),
turned into PDF by WeasyPrint; charts drawn by the same chart library as the app (Altair)
and saved as vector images (vl-convert), so they stay sharp when printed. All three are in the
spec's stack table. One open-licence font (Inter, SIL Open Font License) is stored in the
repository so the PDF looks identical on any machine, including the free hosting.

**What goes in.** The commentary as checked by the verifier, your edits and your analyst view
(from `notes/` in live mode, or from your session in demo mode). Figures awaiting review print
as "awaiting review", never as a number, exactly as on screen.

**Fitting two pages.** The commentary runs 2,500 to 3,400 characters per tearsheet (about 400
to 550 words), plus tables and charts. The layout is fixed, two columns where it helps, body
text about 8.5 point. If a tearsheet would run onto a third page, the text steps down in
half-point steps to a floor of 7.5 point (question 1). Any tearsheet that still overflows
fails the test, and I fix the layout, never the content.

## The Excel backup (spec)

One workbook per tearsheet, five sheets:

| Sheet | Contents |
| --- | --- |
| Inputs | Every figure from the filings, the reports and the hand entries, all years: value as stored (full units, full decimals), label, year, source type, filing or document, IFRS tag or page, status |
| Metrics | Every metric, every year, as a **live formula** on the Inputs, written with names a reader can follow: `=ebitda_FY2025/revenue_FY2025`, `=SUM(cash_FY2025, other_cash_like_FY2025)` |
| Peers | The peer table: each company's figure with its source, and the median and rank as live formulas (`=MEDIAN(...)`, `=RANK(...)`) |
| Extracted | Figures read from the report text: value, the quote, the page, the checks passed or failed, review status |
| Manifest | The run manifest (below) |

**How the formulas are written.** Each metric gets its spreadsheet formula in
`catalog.yaml`, next to its definition, so the definition, the code and the spreadsheet stay in
one place. Company-specific parts (which short-term investments count as cash-like, leases
inside or outside borrowings) follow the inputs actually recorded for each figure. A metric
the tool marks "not meaningful" (leverage on negative EBITDA) shows "n.m." with the reason,
not a formula that would print a misleading number.

**How we know it is right.** LibreOffice recalculates every workbook from scratch (as for gate
1, decision 0009) and every metric cell is compared with the app's stored value. The pass mark
is exact agreement to the stored precision (twelve decimals), since both apply the same
definition to the same inputs. Plus a fast unit test that runs every formula on its inputs in
code, so a broken formula shows up without LibreOffice.

## The run manifest

For each export, a small file (`<company>_FY<year>_manifest.json`), the Manifest sheet, and the
one-line summary in the PDF footnotes:

- every filing behind a figure on the tearsheet, with its SHA-256 fingerprint and link, and
  the fingerprint of any PDF you supplied (Air France-KLM, ADP FY2025);
- the drafting model and prompt version (`draft-v7`), the extraction model and prompt
  version behind the figures read from the reports (today all 230 are `extract-v4`), and the
  events prompt;
- the fact sheet fingerprint, the AI calls, tokens and cost of the draft;
- the code version (the commit), the date and time of the export, and whether your edits and
  analyst view are included.

## Where you get them

- **In the app:** "Download PDF" and "Download Excel" buttons on the Tearsheet page. In demo
  mode they include your session's edits and analyst view, and nothing is saved on the server.
- **From the command line:** `uv run tearsheet export --issuer afkl --year 2025`, or all 18
  at once, into `exports/` (not committed; regenerated any time).

## How we know it works (the M6 checklist)

- [ ] **PDF fits two pages for every v1 issuer, with no overflow.** All 18 tearsheets render to
      exactly two pages; a test also checks each section lands on its page (snapshot and credit
      metrics on page 1; watch items, analyst view and footnotes on page 2) and that no text box
      is cut off. With a long analyst view (the box takes a fixed space; see question 2).
- [ ] **Excel recalculates to the app's values.** All 18 workbooks recalculated by LibreOffice:
      every metric cell equals the app's value. You open one in Microsoft Excel as a human
      check (question 4).
- [ ] **Manifest lists filing hashes, model and prompt version.** A test checks every filing
      behind every figure on the tearsheet appears with its fingerprint, and the models and
      prompt versions match the recorded AI answers.

Other tests: no export ever prints an unverified figure as a number; demo-mode exports leave no
file on the server; the PDF footnotes define every metric on the page.

## Order of work

1. Formulas in `catalog.yaml` and the in-code check on every stored figure (no Excel yet).
2. The Excel writer and the LibreOffice recalculation check on the 18 workbooks.
3. The manifest, with its test.
4. The PDF: template, print styles, charts, font; the two-page and no-overflow checks.
5. Download buttons in the app and the `export` command.
6. All 18 PDFs and workbooks reviewed, walkthrough, decision note, checklist.

No AI tokens are needed: everything uses the recorded drafts.

## New software

WeasyPrint (PDF) and vl-convert (chart images), both in the stack table; Jinja2 (template) is in
the stack table and already installed with the app. XlsxWriter is already in use. One font file
(Inter, open licence) is added to the repository. LibreOffice is used for the check only, as in
gate 1, not by the app.

## Known difficulties

- **Overflow on page 2.** Page 2 carries the most: operating table, peer table, two commentary
  sections, the analyst view and footnotes. The font steps of question 1 and a fixed analyst
  view box (question 2) are the safety valves.
- **Formulas that differ by company.** Total debt and cash-like investments are built from
  different lines per company (decision 0008); the workbook formula is written from the inputs
  each figure actually used, so it can't drift from the code.
- **Hosting.** WeasyPrint needs system libraries (Pango) on the free hosting; they are declared
  in M7's deployment files. Locally and in this cloud environment they are already present.
- **Edited sentences with a typed figure** have no source to put in a footnote (question 3).

## Questions for Imane

1. **A tearsheet that runs long.** (a) Step the text size down in half points to a floor of 7.5
   point; or (b) keep one size and shorten the layout (fewer table rows) for every tearsheet.
   Recommendation: (a); every tearsheet keeps the same content, and the test reports which
   ones needed a smaller size.
2. **The analyst view on the PDF.** (a) A fixed box of about eight lines on page 2: a longer
   view is cut with "continued in the app" and a warning before export; or (b) the view takes
   the space it needs and the commentary text shrinks to make room. Recommendation: (a), so
   the two-page promise holds whatever you write.
3. **Flagged text in the PDF.** A sentence with a figure you typed, or a section the verifier
   flagged "needs manual editing": (a) print it with a small marker (†) and a footnote, "figure
   entered by the analyst, not traced to a filing" or "draft section not cleared by the
   verifier"; or (b) refuse the export until it is fixed. Recommendation: (a): the analyst
   decides, the reader is told.
4. **Human check of the Excel file.** LibreOffice checks all 18 automatically. Do you also want
   to open one in Microsoft Excel (I suggest Air France-KLM FY2025) and confirm a few ratios
   recalculate? Recommendation: yes, optional and about five minutes; it doesn't hold up the
   milestone.
5. **PDFs kept in the repository.** (a) All 18 PDFs in `docs/m6/pdf/` (about 3 to 4 MB) so you
   can flip through every one; or (b) three, the M7 samples. Recommendation: (a) for this
   milestone's review; M7 picks three for the portfolio.

Working rule reminder: one milestone per session. Once you approve, I'd build M6 in a fresh
session (or this one, if you prefer), on the branch `m6-exports`.
