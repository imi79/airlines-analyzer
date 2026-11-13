# 0025 · M10: half-year and last-twelve-months figures

Date: 2026-11-13 · Status: plan approved by Imane with every recommendation (recorded in
`docs/m10/plan.md` and `docs/progress.md`); built on `m10-half-year-ltm`; waiting for her
go-ahead to merge into `main`

**Choices approved with the plan** (`docs/m10/plan.md`):

1. **Scope A**: half-year and LTM credit figures for the nine companies, seven loaded as the
   pass mark. Result: nine loaded (coverage in `docs/m10/coverage.md`).
2. **The AI reads, code checks every figure**; hand entry as the fallback (used for
   Flughafen Wien, whose PDF gives no text for its figures).
3. **Public reports fetched by the assistant**, each registered with its address and
   fingerprint (`config/half_year_reports.yaml`, files in `documents/half-year/`). No PDF was
   needed from Imane: Air France-KLM's and ADP's sites served their half-year reports.
4. **LTM on the tearsheet's key figures table and the watchlist**, not the PDF.
5. **Labelled "unaudited"** on the column, the watchlist rows and every source card.

**How the reading works: the AI points, code reads.** The plan said the AI would read the
statements and code would check every figure. Built more strictly than that: the AI's form
(prompt `halfyear-v1`) asks only *which row* of the statements holds each line, with the row
copied as a quote. It never gives an amount in a field of its own. Code then:

- finds the three statements in the laid-out text of the PDF (`pdftotext -layout`, already in
  use for the FY2025 PDFs), by their titles and their rows of amounts; where a title appears
  twice (a summary in the management report), the three pages closest together win;
- finds the row on the page from the quote (spaces ignored), and reads the amounts **from the
  page**, never from the AI's copy;
- names the columns itself: for the income statement and the cash flow, from the header's
  years and words ("Q1-Q2 2026", "H1 2026", "Six months to 30 June", "Full Year 2025"; a
  quarter column is never taken for a half); for the balance sheet, **the year-end column is
  the one whose figures equal the database's, line by line** (6 to 9 lines per company);
- checks the row against the database: the year-end column (balance sheet) or the report's
  own full-year column (income statement and cash flow, where printed: Finnair, Norwegian)
  must equal the figure the database holds. Where the report prints no full year (seven of
  the nine), the row's label must be the one under which the last annual report prints the
  database's figure, the figure standing right after the label. This third control was added
  after the coverage check showed that most reports print two halves only;
- checks that the statements add up: total assets = total equity and liabilities (the second
  total is itself confirmed against the database at year end); opening cash + movements =
  closing cash.

A line that fails a check is stored "unverified" with every reason, and stays off the page
until Imane approves or corrects it in `config/half_year_reviews.yaml`. Amounts keep the
sign printed for results (a loss is negative); costs, cash outflows and debt are stored
positive, like the annual figures.

**Answer key, written and committed before the AI ran** (`docs/m10/answer_key.csv`, 58 lines
for Finnair, IAG and ADP, as in M8): **56 verified and correct, 0 verified but wrong**; ADP
capex flagged (the AI took the purchases row alone; the annual figure also includes the change
in payables on asset purchases, so the control caught it); ADP lease payments flagged although
right (the label control did not find the annual row).

**Rules found while building** (each covered by a unit test in `tests/test_half_year.py`):

- *A label must match whole.* "Amortization" in a half-year report is not "Amortization,
  depreciation and provisions" in the annual one: words between the label and the amount mean
  a longer label. Found on Air France-KLM; it moved 5 lines from verified to awaiting review.
- *Loss and profit, period and year.* A half year's "Operating loss" or "Loss for the period"
  is compared with the annual "Operating profit" or "Profit for the year".
- *A row printed twice with the same amounts* (a reconciliation under the cash flow) is the
  same row. *The statement of comprehensive income* repeats the profit row and is cut off the
  income statement.
- *Borrowings and leases printed as one row.* Norwegian's condensed balance sheet prints
  "Current debt" and "Non-current debt" with lease liabilities inside, where its annual one
  splits them. The two rows fail line by line; together they equal the database's borrowings
  plus lease liabilities at year end, so they are kept as debt including leases.
- *Half-year rows the full year holds but the half year does not give* (other cash-like
  items in a company's own net debt definition, undrawn credit lines, maturity tables,
  disposal proceeds printed net) make the LTM metric **missing, with the reason**, never zero.
  A formula's "not reported, counted as zero" rule is switched off for LTM.

**LTM.** `metrics/ltm.py`: for an income or cash flow line, LTM = last full fiscal year + this
first half − the same half a year before; for a balance sheet line, the figure at the
half-year date. The catalog's formulas then run unchanged; no catalog metric was added, so the
golden metric files and the AI's fact sheets are untouched. An LTM figure is verified only if
its three parts are.

**Kept apart from the fiscal years.** Half-year and LTM figures sit in tables of their own
(`interim_reports`, `interim_facts`, `interim_gaps`) and, for demo mode, in
`samples/interim.json`. The fiscal-year library, the 18 tearsheet records and docs/m1 to m8
rebuild byte for byte; the three sample PDFs are not touched. On screen, the LTM figures are laid over a copy of
the library as one extra column per company after its last fiscal year
(`render/interim.py`), so the key figures table, the watchlist and the source cards reuse
their code: an LTM figure opens on its three parts, and each part on its row and page of the
half-year report or on the annual filing (all 335 LTM figures traced, test).

**Watchlist at "Latest (LTM)".** Each company at its own half-year date; moves compared with its
last fiscal year. M9's cash-only floors decide liquidity and short-term cover where the
half-year report gives no undrawn lines.

**Flughafen Wien by hand.** Its PDF draws the tables' digits with a font that carries no text
(English and German versions alike). 17 lines typed from the page images into
`config/half_year_entries.yaml`, with the 31 December column as a control: all five balance
sheet lines equal the database. Unverified until Imane reviews them.

**Cost.** About 60,000 AI tokens (eight reports; the recorded answers hold 54,000; one answer
came back malformed and was asked again, one was replaced after the statement finder
improved), against 200,000 to 400,000 planned. No drafting tokens. No new software.

**Not in M10** (as planned): the commentary, the PDF, traffic figures for the half year, the
companies' own LTM figures.

**Open for later (M11 candidates).** Air France-KLM adopted IFRS 18 in 2026 and restated its
first half of 2025: its income and cash flow lines fail the label control and wait for review,
because FY2025 (old format) + H1 2026 − H1 2025 (new format) would mix two definitions; the
restated FY2025 in its note 4 could serve as the LTM base. And at 30 June airlines hold peak
cash from summer bookings, so net debt at the half-year date is seasonally low; a seasonal
comparison (June against June) would help read the LTM column.
