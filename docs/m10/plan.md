# M10 plan: half-year and last-twelve-months figures

Status: **waiting for Imane's approval** (written 2026-11-12, after M9). Nothing is built yet.
Branch: `m10-half-year-ltm`.

## What M10 is for

Today the tool knows each company once a year. For a December year end, that means that in
November 2026 the freshest leverage on the tearsheet and the watchlist is eleven months old.
A credit analyst works on the latest half-year instead: **where does the name stand at 30 June,
on the last twelve months of earnings?**

M10 reads each company's half-year report and adds two things beside the fiscal years:

- **H1**: the first-half figures (income statement and cash flow for the six months, balance
  sheet at the half-year date);
- **LTM** (last twelve months): for earnings and cash flows, *last full year + this first half −
  last year's first half*; for debt, cash and liquidity, the half-year balance sheet. Net
  leverage at LTM is then net debt at 30 June ÷ EBITDA of the last twelve months.

Why LTM and not "first half × 2": airlines earn most of their profit in the summer, which falls
in the second half. Finnair's operating result was −34.2m in H1 2025 and +64.2m for the full
year. Doubling a first half would badly misstate the year; LTM always contains one full summer
and one full winter, like a covenant tested on trailing twelve months.

The spec lists this under v2 ("half-year reports ... LTM figures"); the M9 plan named it as the
natural M10.

## What I checked before writing this

Half-year reports are not in the structured filings database (it holds annual reports only), so
they have to be read from PDFs. That was the open risk, so I tried it on two companies:

| Check | Result |
| --- | --- |
| Can the reports be fetched automatically? | Yes for both tried: Finnair's half-year report 1 January to 30 June 2026 (41 pages) and IAG's (50 pages), from the news-wire and stock-exchange document services. Air France-KLM's and ADP's own sites refused automated downloads in M1, so some will come from you, as then |
| Do the statements read cleanly from the PDF? | Yes, with the tool the app already uses for your two FY2025 PDFs (no new software). Income statement, balance sheet and cash flow come out as clean rows and columns |
| Is everything for LTM in one document? | Yes. Finnair prints H1 2026, H1 2025 and full-year 2025 side by side: LTM revenue = 3,106.2 + 1,694.8 − 1,481.9 = 3,319.1; LTM operating result = 64.2 + 90.2 − (−34.2) = 188.6 (my arithmetic, to illustrate: in M10 code computes it) |
| Is there a control against what we already hold? | Yes, and it is strong. The half-year balance sheet prints the 31 December 2025 column again. On every line I compared, it equals the figure in our database from the tagged annual filing (cash 529.6, other financial assets 531.4, lease liabilities 130.4 and 632.3; revenue 3,106.2 and operating result 64.2 in the full-year column). A misread column or a wrong unit would break that match |
| Are the notes as rich as the annual report's? | No. Half-year statements are condensed and **unaudited** (Finnair says so; IAG's are "unaudited condensed"). IAG still states its undrawn facilities (2,698m); maturity tables are usually absent. Some figures will be missing at the half-year, with the reason |

Not checked yet: the other seven reports. easyJet's half year ends in March and Wizz Air's in
September (its report is due about now), so their LTM dates differ, as their fiscal years do.

## What gets built

1. **A coverage check first** (as M0 did for the annual filings): for each of the nine
   companies, the half-year report found or not, its language, whether the three statements
   are there, and whether I could fetch it or you need to supply it. Go or no-go per company,
   recorded before anything else is built.
2. **Reading the statements.** The AI reads the three condensed statements from the PDF (the
   same lines the annual load carries, about 20 per company, for three columns). Code then
   checks every figure before it counts:
   - the number is on the page, in the quoted row (as in M3);
   - **the year-end column equals our database**, line by line (the control above);
   - **the full-year column equals our database** for the income statement and cash flow, where
     the report prints it;
   - the statements add up: assets = equity + liabilities; opening cash + movements = closing
     cash.
   A figure that fails a check is "awaiting review" and stays off the page until you approve or
   correct it, exactly as today. An answer key for three companies is written before the AI
   runs, as in M8: the target is **no wrong figure marked verified**.
3. **A period beside the fiscal year.** Today a figure is "company, line, fiscal year". M10
   adds first-half and LTM figures *beside* the annual ones, under their own names. The annual
   figures, their keys and the 18 tearsheets stay exactly as they are (I will prove it the way
   M9 did: the tearsheet records rebuild byte for byte).
4. **LTM metrics by the same formulas.** The catalog's formulas (EBITDA, net debt, leverage,
   coverage, cash flow after leases, liquidity) run on the LTM figures unchanged. Where the
   half-year report lacks an input (undrawn lines, lease payments shown apart), the metric is
   missing with the reason; M9's cash-only floors already cover the watchlist in that case.
5. **Where you see it.**
   - Tearsheet, key figures table: an **LTM column** after the last fiscal year, headed with
     its date ("LTM Jun 2026"), marked unaudited.
   - Watchlist: the year picker gains **"Latest (LTM)"**, so the page answers "which names
     cross a trigger on the half-year figures?", with the move triggers comparing LTM with the
     last fiscal year.
   - Source cards: an LTM figure opens on its three parts (full year, this H1, last H1), each
     followed down to the page of the report or the filing.
6. **Tests and records**: unit tests for the LTM arithmetic (earnings added and subtracted,
   balance sheet taken at the date, non-December year ends); the answer-key score; decision
   0025; walkthrough.

**Not in M10** (kept small on purpose): the commentary is not redrafted and does not mention
LTM; the PDF is unchanged (seven tearsheets are already at the smaller text size, so an extra
column needs its own look); traffic figures for the half year; the company's own LTM figures
shown beside ours. Natural M11 candidates.

**Cost.** AI tokens for reading only: about 200,000 to 400,000 (nine reports, a few pages of
statements each, plus the answer-key runs; M8's reading cost 168,000, and M8 as a whole came
in at 1.9 times its estimate, so I give a range). No drafting tokens. No new software.

## How we know it works (the M10 checklist)

- [ ] Coverage recorded for all nine companies, go or no-go each; half-year figures loaded for
      at least seven
- [ ] No wrong figure marked verified on the answer key (three companies, written before the AI
      run); every figure that fails a check flagged with its reason
- [ ] For every loaded company, the report's year-end column matches the database line by line,
      or the difference is flagged and explained (a restatement, for example)
- [ ] LTM metrics computed for every loaded company, or missing with a stated reason; unit tests
      for the LTM arithmetic
- [ ] Every H1 and LTM figure traces to its source on click; the 18 tearsheets' annual figures
      and records unchanged; PDF two pages and Excel recalculated, 18 of 18

## Risks, and what I would do

- **A report I cannot fetch or read** (a refused download, a scanned PDF, two statements side by
  side on a page): you supply the PDF; if it still does not read cleanly, that company is a
  no-go for M10 and says so on the page. The gate is seven of nine, not nine.
- **Restated comparatives**: the year-end column then differs from the database. The control
  catches it; the figure waits for your review with both values shown.
- **Thinner notes**: liquidity and short-term cover may be missing at the half-year. Shown as
  missing with the reason; the watchlist falls back on cash alone, as decided in M9.
- **Different half-year dates** (easyJet March, Wizz Air September): each LTM column carries its
  own date; the watchlist shows the date beside each company.
- **Size**: this is a large milestone. If the reading takes longer than planned, I stop after
  item 4 (figures and metrics in the database, tested) and bring items 5 and 6 back to you as a
  second step rather than rush the pages.

## What you do

1. Answer the six questions below.
2. Supply the half-year PDFs I cannot fetch (I give you the exact list after the coverage
   check; likely Air France-KLM and ADP, perhaps others).
3. Review the figures that fail a check, on the Data and audit page.
4. Read the LTM column and the watchlist at LTM, and tell me if a number surprises you.
5. Say go to merge into `main`. After the merge I open the public link myself and confirm it
   (lesson of the M9 deploy, decision 0024).

## Questions for Imane

1. **Scope.** (A) Half-year and LTM credit figures for the nine companies, in the app and the
   watchlist, no commentary and no PDF change; (B) the same for three pilot companies only
   (Finnair, IAG, one airport), the rest in M11; (C) something else first (Icelandair as a tenth
   company, the commentary score, maturity-table coverage). Recommendation: **A**, with the
   seven-of-nine gate as the safety valve.
2. **How the figures come in.** (a) The AI reads the statements and code checks every figure
   against the database's year-end figures; what fails waits for your review; (b) I enter them
   by hand from the PDFs, as for FY2025 Air France-KLM and ADP, with the same control.
   Recommendation: **(a)**: the control is strong enough to trust what passes, and it scales to
   every future half-year; (b) remains the fallback for a report that does not read.
3. **Where the reports come from.** Recommendation: I fetch what is publicly downloadable and
   record each file's fingerprint; you supply the others, as in M1.
4. **Where LTM shows.** (a) The tearsheet's key figures table and the watchlist; (b) also the
   PDF. Recommendation: **(a)** now, the PDF once you have seen the column on screen.
5. **The label.** Half-year statements are unaudited. Recommendation: the LTM column and every
   H1 or LTM source card say "unaudited half-year figures", and the Method page explains LTM
   in two lines.
6. **Which session.** Your rules say one milestone per session, and this session built M9.
   Recommendation: approve here, and I build M10 in a fresh session, starting from this plan.

Sources for the check: [Finnair half-year report, 1 January to 30 June 2026
(PDF)](https://mb.cision.com/Main/3718/4376604/4200218.pdf); [IAG half-year financial report,
six months to 30 June 2026 (PDF)](http://www.rns-pdf.londonstockexchange.com/rns/6982O_1-2026-7-31.pdf).
