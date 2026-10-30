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
Walkthrough: `docs/m2/walkthrough.md`. **Status: done; gate 1 passed** (one review left, see
the last item).

- [x] Every catalog metric computed, or missing with a stated reason: 701 values; every n.m.
      or missing value carries its reason; traffic metrics wait for M3
- [x] Unit tests green: one test per metric plus the special cases (94 checks in total)
- [x] Reconciliation within tolerance (gate 1): 62 of 62, Air France-KLM and ADP, FY2024-FY2025,
      against a second-source model built by the AI at Imane's request: inputs read from the
      PDFs, formulas recalculated by LibreOffice (decision 0009, `docs/m2/gate1.md`)
- [ ] Imane accepts the 8 new figures entered by hand (`docs/m1/fy2025_entries.md`, status
      "unverified"). All 8 are confirmed by the machine reading of the PDFs (decision 0009).
