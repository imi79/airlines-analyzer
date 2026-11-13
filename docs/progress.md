# Progress

## M0 · Data feasibility spike

Tool: `spikes/m0/coverage.py` (see its header for how to run it). Results: `docs/m0/`.
Walkthrough: `docs/m0/walkthrough.md`. **Status: done.**

- [x] Matrix covers all ten candidates (plus four reserves)
- [x] At least eight issuers confirmed with three or more years: **9 in v1** (7 of the
      original 10, plus Norwegian and Wizz Air in place of Ryanair; decision 0001)
- [x] Go or no-go per issuer recorded in `docs/decisions/` (0001, with 0002 and 0003)

## M1 · Ingestion and normalisation

Branch: `m1-load-figures`. Run: `uv run tearsheet all` (add `--offline` to use the cache only).
Results: `docs/m1/`. Walkthrough: `docs/m1/walkthrough.md`. **Status: done.**

- [x] Core statement lines loaded for every v1 issuer and year: 804 figures to FY2025, every
      gap explained (7 not tagged, with reasons)
- [x] Two issuers × two years spot-checked against the published statements: 100% match.
      Air France-KLM and ADP, FY2023-FY2024: 68 of 68 figures match the statements Imane
      supplied (`docs/m1/spot_check.md`)
- [x] A rerun from cache works offline and changes nothing (two runs, identical files)
- [x] FY2025 for Air France-KLM and ADP loaded: entered from the published statements, with
      34 of 34 prior-year controls matching (decision 0007, `docs/m1/fy2025_entries.md`).
      Reviewed by Imane on 2026-10-30; stored as verified.

## M2 · Metrics engine and peers

Branch: `m2-metrics`. Run: `uv run tearsheet all`. Results: `docs/m2/`.
Walkthrough: `docs/m2/walkthrough.md`. **Status: done; gate 1 passed.**

- [x] Every catalog metric computed, or missing with a stated reason: 701 values; every n.m.
      or missing value carries its reason; traffic metrics wait for M3
- [x] Unit tests green: one test per metric plus the special cases (94 checks in total)
- [x] Reconciliation within tolerance (gate 1): 62 of 62, Air France-KLM and ADP, FY2024-FY2025,
      against a second-source model built by the AI at Imane's request: inputs read from the
      PDFs, formulas recalculated by LibreOffice (decision 0009, `docs/m2/gate1.md`)
- [x] Imane accepts the 8 new figures entered by hand (`docs/m1/fy2025_entries.md`): accepted
      on 2026-11-01 and now stored as verified. All 8 were also confirmed by the machine reading
      of the PDFs (decision 0009). No figure changed; only the review status did.

## M3 · Extraction with grounding

Branch: `m3-extraction-grounding`. Run: `uv run tearsheet all --offline` (replays the recorded AI
answers; `uv run tearsheet extract` asks the AI for reports not yet read). Results: `docs/m3/`.
Walkthrough: `docs/m3/walkthrough.md`. **Status: done; closed by Imane on the safety result
(decision 0015).**

Answer key built by code at Imane's request (decision 0012), in three sets each written before
the step it judges (decision 0014): first 25, held-out 23, blind 23. The blind set is the clean
measure of the final code.

- [x] No wrong value marked verified on the labelled set: 0 of 71
- [ ] At least 80% of labelled values verified automatically: blind 18 of 23 (78%), all 56 of
      71 (79%). **Waived by Imane on 2026-11-03**: M3 closed on the safety result; the 80%
      becomes a tracked goal in M4, on a fresh blind set (decision 0015)
- [x] Every unverified value visibly flagged: 50 of 50 listed with quote and reason in
      `docs/m3/extractions.md`, marked \*, and every ratio using one marked \* in `docs/m2/`
- Three runs on all nine companies (prompts `extract-v1`, `-v2`, `-v3`), 41 reports each,
  about 500,000 tokens per run; reports use v3: 228 figures, 178 verified. Undrawn facilities
  are general-purpose only (decision 0015). Check changes in decisions 0013 and 0014

## M4 · Drafting and verifier

Branch: `m4-drafting-verifier`. Plan: `docs/m4/plan.md`. Run: `uv run tearsheet all --offline`
(replays the recorded drafts; `uv run tearsheet draft` asks the AI for drafts not yet
recorded). Results: `docs/m4/`. Walkthrough: `docs/m4/walkthrough.md`. Decisions 0016-0018.
**Status: done; gate 2 passed; closed by Imane on 2026-11-09 on the safety result, with the
commentary score at 3.78 of 5 (decision 0018).**

- [x] Adversarial suite 100% rejected: 47 of 47 faulty sentences, each for its rule; 15
      correct but risky sentences and a full correct draft pass (`tests/test_adversarial.py`)
- [x] Ten consecutive drafts across issuers with zero unreferenced numbers (gate 2): 11 in a
      row, all nine companies (corrected in M7 from "17", which the record never showed: only
      16 of 18 drafts pass; decision 0021); 16 of 18 pass with prompt `draft-v7`, the year's events and the
      cause lines, 6 sentences removed by the verifier after two retries (rule confirmed by
      Imane, decision 0018); no number outside a blank on the page (`docs/m4/drafts.md`)
- [ ] Commentary score of 4 or more: **3.78 of 5** (rounds 1 to 4: 2.93, 3.50, 3.70, 3.75). **Waived by
      Imane on 2026-11-09**: M4 closed on the safety result (decision 0018). Scored by
      Claude at Imane's request after checking the ten drafts against the annual reports
      (decision 0018, `docs/m4/commentary_review.yaml`, `docs/m4/score_sheet.xlsx`)
- Vienna's short-term deposits entered from its notes, approved by Imane on 2026-11-09
- Example notes drafted for Imane to rewrite (`docs/m4/example_notes.md`)
- Tracked, not a gate (decision 0015): extraction 80% verified on a fresh blind set. Not met:
  13 of 22 (59%) on the fourth set (FY2022 reports), written before prompt `extract-v4` and
  four check fixes; 0 of 93 wrong values verified. **Closed by Imane on 2026-11-03 on the
  safety result** (decision 0017)

## M5 · Web app

Branch: `m5-web-app`. Plan: `docs/m5/plan.md`. Run: `uv run tearsheet app` (demo mode; live
mode appears where `uv run tearsheet all` has built the database). Demo files: `uv run
tearsheet samples`. Results: `docs/m5/`. Walkthrough: `docs/m5/walkthrough.md`. Decision
0019. **Status: done.**

- [x] A pre-generated tearsheet opens in under ten seconds: 18 of 18, slowest 2.0 seconds,
      each from a fresh browser tab (`docs/m5/timing.md`)
- [x] Every figure on screen shows its source on click: KPI cards, table rows, chart points,
      commentary sentences, peer rows and medians, audit rows; a test follows every figure of
      all 18 tearsheets and every peer table down to a filing fact, a quote or a hand entry
      (1,986 of 1,986 figures trace; `tests/test_sources.py`, screenshots in `docs/m5/`)
- [x] Demo mode works without a key: every page and all 18 tearsheets open with no key, no
      database and the network blocked (`tests/test_app.py`)
- Four pages (Tearsheet, Peers, Data and audit, Method); commentary editing with untraced
  figures flagged; analyst view; approve or correct with a reason (saved in live mode only);
  live redraft through the existing drafting and verifier. Ratios to a very small debt shown
  as n.m., as in the M4 fact sheets. 480 tests, 99 new. No AI tokens spent

## M6 · Exports

Branch: `m6-exports`. Plan: `docs/m6/plan.md`. Run: `uv run tearsheet export` (add `--check` to
recalculate every workbook with LibreOffice), or the Export buttons on the app's Tearsheet page.
Results: `docs/m6/`. Walkthrough: `docs/m6/walkthrough.md`. Decision 0020. **Status: done.**

- [x] PDF fits two pages for every v1 issuer, with no overflow: 18 of 18, every section on its
      page, no table out of its column and no hidden lines, measured on the laid-out page, also
      with a full analyst view and an edited sentence (`tests/test_pdf.py`); 16 at 8.5 point,
      two at 8.0. All 18 in `docs/m6/pdf/`
- [x] Excel recalculates to the app's values: 18 of 18 workbooks recalculated by LibreOffice,
      2,044 of 2,044 metric values and 195 of 195 medians equal (`docs/m6/excel_check.md`);
      every formula lives in `catalog.yaml`. Imane's check in Microsoft Excel is optional
      (`docs/m6/afkl_FY2025.xlsx`)
- [x] Manifest lists filing hashes, model and prompt version: every filing and report behind
      every figure with its SHA-256, the drafting, extraction and events models and prompt
      versions, the code version (`tests/test_manifest.py`)
- Also fixed: filing links in the app (relative addresses since M5). 533 tests, 52 new. No AI
  tokens spent

## M7 · Portfolio packaging

Branch: `m7-portfolio`. Plan: `docs/m7/plan.md`. Decision 0021. Live:
https://airlines-analyzer.streamlit.app. Walkthrough: `docs/m7/walkthrough.md`. **Status: done;
gate 3 passed; v1 complete. Closed by Imane on 2026-11-11.**

- [x] Public link works in a fresh browser with no key (gate 3): every page, a figure followed
      down to its source, a two-page PDF download and the verifier demo, from a fresh browser,
      not signed in (`docs/m7/gate3.md`); the hosting copy (Debian 12 and 11) and the Docker
      image passed the same tour beforehand
- [x] Imane can explain every stage of the pipeline without notes: rehearsal held in the chat on
      2026-11-11, nine interview questions (the seven stages and two follow-ups), every stage
      explained correctly; ticked by Imane. Explainer: `docs/m7/pipeline_explained.md`
- Done: verifier demo in the app; Dockerfile; checks on GitHub (tests, style, secret scan);
  README with the architecture diagram; MIT licence; demo script, LinkedIn post and CV line
  drafts; secret scan of the whole history (no leak); history rewritten to the noreply address
  (Imane's go-ahead); gate 2 count corrected (11 in a row); the PDF's bundled font fixed
- Three sample PDFs in `samples/pdf/` (Air France-KLM, easyJet, Aena FY2025) with the analyst
  views Imane adopted (`notes/`); two pages at 8.5 point, bundled font
- Public repository, deployed by Imane
- Next (not started): M8 candidates in `docs/m7/walkthrough.md`

## M8 · Cash flow after leases, refinancing and ratings (after v1)

Branch: `m8-cash-flow-refinancing`. Plan: `docs/m8/plan.md`. Run: `uv run tearsheet all
--offline` (replays the recorded AI answers; `uv run tearsheet extract` reads the maturity
tables not yet read, `uv run tearsheet draft` redrafts). Results: `docs/m8/`. Walkthrough:
`docs/m8/walkthrough.md`. Decision 0022. **Status: done; ratings reviewed and merged into
`main` by Imane's go-ahead (2026-11-11); hand entries reviewed by Imane the same day. Still
open: the other flagged maturity tables (approve if she wishes; IAG FY2025 approved by her on
2026-11-12). The three flagged
snapshots were rewritten as Imane's edits on 2026-11-12.**

- [x] Cash flow after leases computed for every issuer and year, or missing with a stated
      reason: net capex, FCF after leases and its ratio to debt for 9 of 9 companies (Vienna's
      ratio n.m. on its very small debt); one unit test per new metric; second-source check
      16 of 16 within tolerance (`docs/m8/cash_flow_check.md`). Air France-KLM and ADP FY2025
      use three new hand entries, reviewed by Imane on 2026-11-11
- [x] Maturity wall: no wrong value marked verified on the answer key (eight company-years,
      eleven tables, committed before the AI run): 0 wrong; 4 verified and correct; every other
      table flagged with its reasons (`docs/m8/maturity_score.md`). First run with the checks as
      written: 2 verified, both correct; four form fixes and a tighter interest bound after it
      (decision 0022). Coverage is low: a wall on 6 of 18 tearsheets, including Air France-KLM
      FY2025 (entered by hand from the PDF, reviewed by Imane) and IAG FY2025 (approved by
      Imane: it matches the key, flagged only because IAG's convertible bond sits in current
      debt). ADP FY2025's hand entries, also reviewed, still disagree with the balance sheet and
      stay flagged
- [x] Ratings box complete: nine entries with agency, rating, outlook, date and source, each
      quote checked against its report by code (`config/ratings.yaml`); reviewed by Imane on
      2026-11-11. A rating is offered to the commentary only in the note of its report's year
- [x] The tearsheet stays clean: every new figure traces to its source on click (all source
      tests pass on the 18 tearsheets); PDF two pages 18 of 18; Excel recalculated 18 of 18;
      adversarial suite 52 of 52 rejected (5 new: typed ratings and maturities); redraft 14 in a
      row with no number outside a blank, 15 of 18 pass the verifier in full (three kept M4
      snapshots flagged: Finnair FY2024 and Wizz Air FY2025, already flagged in M4, and Aena
      FY2024 for a rating typed in M4, "upgraded to A"; all three rewritten as Imane's edits
      on 2026-11-12, so no section is left flagged on the page or in the PDFs)
- Prompt `draft-v8`: about 1,420,000 tokens in and 96,000 out over five rounds (first draft;
  the figure-name phrases; after the ratings review; ratings limited to their own year; after
  the hand entries' review, two notes), 1.9
  times the plan's estimate; maturity tables `maturity-v1`: about 168,000 tokens. 638 tests
  pass

## M9 · Watchlist of credit triggers

Branch: `m9-watchlist`. Plan: `docs/m9/plan.md`, approved by Imane on 2026-11-12 with every
recommendation. Run: `uv run tearsheet app`, Watchlist page; the triggers are in
`config/watchlist.yaml`. Walkthrough: `docs/m9/walkthrough.md`. Decision 0023. **Status: done; merged
into `main` by Imane's go-ahead (2026-11-12), after she kept the liquidity floor and asked for
the short-term cover floor.**

- [x] Every trigger in `config/watchlist.yaml` evaluated for every company and year shown, from
      verified figures only; missing or unverified figures shown as "cannot assess" with the reason:
      every company and year in the library (FY2021-FY2026), seven triggers (liquidity to
      revenue for airlines only); on the 18 tearsheets 120 checks: 9 fired, 107 clear, 4 cannot
      assess (all Flughafen Wien), each with its reason. Liquidity and short-term cover decided
      on cash alone where cash already clears the threshold (floors kept and added by Imane on
      2026-11-12, decision 0023: 7 and 10 tearsheets)
- [x] Every fired trigger traces to the figure behind it on click (test over all 18 tearsheets):
      9 of 9 fired triggers lead down to filing facts, quotes or hand entries; they are part of
      the page's figures, so the source test and the export manifest cover them
- [x] Unit tests for each trigger kind, the edges (exactly at the threshold) and "cannot assess":
      levels above and below, below zero, moves up and down, each exactly at the threshold;
      missing, not meaningful, awaiting review, last year missing; both floors
      (`tests/test_watchlist.py`); the new ratio `cash_short_term_debt_cover` has its unit tests
- [x] The PDF still fits two pages for all 18 tearsheets: 18 of 18, with the watchlist line
      under the ratings; no text size changed (11 at 8.5 point, 7 at 8.0, as before M9). Excel
      recalculated 18 of 18
- Watchlist page (filters for fired and new warnings, source cards), a line on each tearsheet
  and PDF, a paragraph on the Method page. No AI tokens; the commentary is not redrafted.
  New catalog ratio: short-term debt cover, cash only (watchlist only, never offered to the
  AI: the recorded drafts are unchanged). Open for Imane: thresholds after the first results.
  723 tests pass (85 new)
- After the merge, the public link failed on every visit: the hosting service had updated the
  running app without restarting it, and the new page met a module still in memory from before
  M9. Reproduced locally and fixed at Imane's request: the app now reloads its code when the
  files change (decision 0024). The running copy recovered on 2026-11-13 at the next push to
  `main`, through the guard itself; the public link was then opened from a fresh browser and
  every page checked. 724 tests pass

## M10 · Half-year and last-twelve-months figures

Branch: `m10-half-year-ltm`. Plan: `docs/m10/plan.md`, approved by Imane on 2026-11-13 with every
recommendation. Run: `uv run tearsheet app` (Tearsheet: the LTM column; Watchlist: "Latest
(LTM)"; Data and audit: the half-year section). Walkthrough: `docs/m10/walkthrough.md`. Decision
0025. **Status: built and tested; waiting for Imane's review of the flagged lines and her
go-ahead to merge into `main`.**

- [x] Coverage recorded for all nine companies, go or no-go each; half-year figures loaded for
      at least seven: **nine of nine** (`docs/m10/coverage.md`): eight read by the AI with code
      checks, Flughafen Wien entered by hand (its PDF gives no text for its figures), waiting
      for Imane's check. No PDF needed from Imane
- [x] No wrong figure marked verified on the answer key (three companies, written before the AI
      run); every figure that fails a check flagged with its reason: 58 lines (Finnair, IAG,
      ADP), **56 verified and correct, 0 verified but wrong**, 2 flagged (ADP capex, wrong and
      caught; ADP lease payments, right) (`docs/m10/answer_key_score.md`); 42 of 173 lines
      awaiting review, each with its reason (`docs/m10/half_year.md`)
- [x] For every loaded company, the report's year-end column matches the database line by line,
      or the difference is flagged and explained: all nine tie at 31 December (6 to 9 lines
      each; Norwegian's two debt rows, printed with leases inside, tie as a total). Full-year
      columns, where printed: Finnair all equal; Norwegian D&A (the AI took another row) and
      capex (printed net of proceeds) flagged and explained in the walkthrough
- [x] LTM metrics computed for every loaded company, or missing with a stated reason; unit tests
      for the LTM arithmetic (`tests/test_ltm.py`: earnings added and subtracted, balance sheet
      at the date, a non-December year end, a line missing at the half year never counted as
      zero, statuses)
- [x] Every H1 and LTM figure traces to its source on click (335 LTM figures, test); the 18
      tearsheets' annual figures and records unchanged (byte for byte, no "figures have
      changed" warning); PDF two pages and Excel recalculated, 18 of 18 (11 at 8.5 point, 7 at
      8.0, as before)
- AI tokens: about 60,000 for reading (prompt `halfyear-v1`), against 200,000 to 400,000
  planned; no drafting tokens; no new software; no catalog metric added (golden files and fact
  sheets unchanged). 804 tests pass (80 new)
- Open for Imane: Flughafen Wien's hand entries; the flagged lines (suggestions in the
  walkthrough); Air France-KLM's new income statement format (IFRS 18), an M11 candidate
