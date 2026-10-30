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
Results: `docs/m1/`. Walkthrough: `docs/m1/walkthrough.md`. **Status: in progress.**

- [x] Core statement lines loaded for every v1 issuer and year: 770 figures, every gap
      explained (6 not tagged, with reasons)
- [x] Two issuers × two years spot-checked against the published statements: 100% match.
      Air France-KLM and ADP, FY2023-FY2024: 68 of 68 figures match the statements Imane
      supplied (`docs/m1/spot_check.md`)
- [x] A rerun from cache works offline and changes nothing (two runs, identical files)
- [ ] FY2025 for Air France-KLM and ADP loaded from the company packages (decision 0004, 4b).
      The import route is built and checked (decision 0006); waiting for the two packages.
