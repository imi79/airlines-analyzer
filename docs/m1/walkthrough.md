# M1 walkthrough: the figures database

**What M1 built.** A database that works like a clean, audited trial balance for each company
and year. Every figure comes straight from the electronic annual report and is translated into
one common chart of accounts of about 25 lines, with an audit trail behind it.

## How it works

1. **Collect.** The tool downloads each company's annual filings and keeps a local copy.
   Re-running it works offline and gives exactly the same result (checked: two runs, identical
   files).
2. **Translate.** Each company's labels are mapped onto our lines in two layers, like a group
   chart of accounts with local adjustments:
   - the **common mapping** (`src/tearsheet/normalize/concept_map.yaml`): official IFRS labels,
     used for everyone;
   - one **adjustment file per company** (`src/tearsheet/normalize/overrides/`): its own
     labels, each with *why* and *where it was checked*. Example: Air France-KLM's
     "Titres de transport émis non utilisés" is advance ticket sales.
3. **One sign convention.** Costs and cash outflows are positive amounts. When a company tags
   them the other way, its file flips the sign and says so.
4. **Latest figure wins.** Each year uses the most recent report that shows it, so 2023 comes
   from the 2023 column of the 2024 report (your choice 2a). The first-reported figure is kept,
   and real restatements are flagged.
5. **Audit trail.** Every figure records the filing it came from (with its digital fingerprint),
   the exact label, the tag reference and the rule used.

## What we found

- **770 figures loaded** across 9 companies and FY2021 to FY2025 (FY2026 for Wizz Air, whose
  year ends in March).
- **Every gap is explained.** 296 are covered by another line (for example "leases included in
  borrowings, see the note"). **6 are truly missing**: Air France-KLM's fuel cost (4 years) and
  Finnair's tax paid (FY2021-FY2022) aren't tagged; fuel will come from the notes in M3.
- **17 real restatements**, for example:
  - Aena FY2021: operating profit restated from -152m to -706m, revenue from 2,319m to 2,428m
  - IAG FY2023: debt reclassified between current and non-current, cash flow restated
  - Norwegian FY2022: about NOK 1.1bn reclassified into depreciation
  - ADP FY2021 and Wizz Air FY2022: cash from operations re-presented

  Rounding differences (millions vs hundred-thousands) are not counted as restatements.
- **Capex is cash paid for everyone.** ADP's capex is "Investissements corporels, incorporels
  et de placement" ("de placement" = investment property) adjusted for amounts owed to
  suppliers: 872m (2023) and 1,169m (2024). This matches how Air France-KLM reports it.
- **Sign slips in the filings are caught.** Flughafen Wien switched its sign convention for
  interest and tax paid in 2023. Air France-KLM's 2021 file tagged capex as negative. Both
  are handled and logged.

## Your part: the spot check

Open `docs/m1/check_sheet.xlsx`. It has one sheet each for Air France-KLM and ADP, with FY2023
and FY2024 laid out like the published statements, in millions.

1. Open the published annual report (consolidated statements).
2. Compare each line and type ✓ in the yellow column, or ✗ with the published figure.
3. Send the file back to me (attach it in the chat).

Costs are shown as positive amounts, while the accounts may show them in brackets. Only the
amount needs to match.

## The 2025 reports for Air France-KLM and ADP

The import route for reports you download yourself is ready. Each zip is converted with Arelle,
the same free tool the filings database uses. Its fingerprint, origin and download date are
recorded, and it's checked to belong to the right company and year. Tested on ADP's 2024
report: exactly the same 343 figures as the database. Once you send the two 2025 zips, they go
through the same mapping as everything else.

## To watch in M2

- **Interest coverage** should use interest expense, not total finance costs. ADP's finance
  costs (1,115m in 2023, 595m in 2024) include more than interest.
- **2021 tax paid is negative** for several companies. These are most likely Covid-era tax
  refunds; Flughafen Wien's refund is confirmed by its filing.
- **ADP's FY2021-FY2022 capex line** doesn't show whether it is cash paid; to confirm against
  the published cash flow statement.

## Where to look

| File | What it is |
| --- | --- |
| `docs/m1/check_sheet.xlsx` | Your spot-check sheet |
| `docs/m1/coverage.md` | Every company, year and line: loaded, covered or missing, with reasons |
| `docs/m1/facts.csv` | Every figure with its source (opens in Excel) |
| `docs/m1/gaps.csv` | Every gap and its reason |
| `docs/m1/filings.csv` | The filings used, with fingerprints and links |
| `src/tearsheet/normalize/overrides/` | One adjustment file per company |
