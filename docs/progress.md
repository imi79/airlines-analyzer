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
**Status: in progress; gate 2 passed; commentary score 3.50 of 5 after fixes A to D, below
the mark; Imane to review the entered Vienna deposits and confirm the sentence-removal rule.**

- [x] Adversarial suite 100% rejected: 47 of 47 faulty sentences, each for its rule; 15
      correct but risky sentences and a full correct draft pass (`tests/test_adversarial.py`)
- [x] Ten consecutive drafts across issuers with zero unreferenced numbers (gate 2): 11 in a
      row, all nine companies; 17 of 18 pass with prompt `draft-v5` and the year's events,
      14 sentences removed by the verifier after two retries (decision 0018, for Imane to
      confirm); no number outside a blank on the page (`docs/m4/drafts.md`)
- [ ] Commentary score of 4 or more: **3.50 of 5** (round 1: 2.93), scored by Claude at
      Imane's request after checking the ten drafts against the annual reports (decision 0018,
      `docs/m4/commentary_review.yaml`, `docs/m4/score_sheet.xlsx`)
- Example notes drafted for Imane to rewrite (`docs/m4/example_notes.md`)
- Tracked, not a gate (decision 0015): extraction 80% verified on a fresh blind set. Not met:
  13 of 22 (59%) on the fourth set (FY2022 reports), written before prompt `extract-v4` and
  four check fixes; 0 of 93 wrong values verified. **Closed by Imane on 2026-11-03 on the
  safety result** (decision 0017)
