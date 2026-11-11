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
https://airlines-analyzer.streamlit.app. **Status: in progress**: gate 3 passed; the rehearsal
remains.

- [x] Public link works in a fresh browser with no key (gate 3): every page, a figure followed
      down to its source, a two-page PDF download and the verifier demo, from a fresh browser,
      not signed in (`docs/m7/gate3.md`); the hosting copy (Debian 12 and 11) and the Docker
      image passed the same tour beforehand
- [ ] Imane can explain every stage of the pipeline without notes: explainer ready
      (`docs/m7/pipeline_explained.md`), rehearsal to do
- Done: verifier demo in the app; Dockerfile; checks on GitHub (tests, style, secret scan);
  README with the architecture diagram; MIT licence; demo script, LinkedIn post and CV line
  drafts; secret scan of the whole history (no leak); history rewritten to the noreply address
  (Imane's go-ahead); gate 2 count corrected (11 in a row); the PDF's bundled font fixed
- Three sample PDFs in `samples/pdf/` (Air France-KLM, easyJet, Aena FY2025) with the analyst
  views Imane adopted (`notes/`); two pages at 8.5 point, bundled font
- Public repository, deployed by Imane
- To do: rehearsal

