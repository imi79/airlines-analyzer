# 0007 · FY2025 for Air France-KLM and ADP entered from the published statements (M1)

Date: 2026-10-30 · Status: accepted (option 1 chosen by Imane)

**Why.** filings.xbrl.org has no FY2025 filing for Air France-KLM or ADP. Both companies'
websites refuse automated downloads, and the ESEF packages weren't found. Imane supplied the
published consolidated statements as PDFs instead.

**Choice.** The FY2025 figures are entered from those PDFs into `config/manual_figures.yaml`:
19 lines for Air France-KLM and 15 for ADP, the same lines the tagged years carry. Each entry
records the printed page and label, and each document's SHA-256 fingerprint is kept. They load
as facts with source type "manual".

**Controls.**
- **Prior-year column.** Each PDF's FY2024 column is entered too, and compared with the FY2024
  figure the database holds from the tagged filing. 34 of 34 match, which means no typing errors
  and no restatement of FY2024 on these lines (`docs/m1/fy2025_entries.md`).
- **Review before use.** Entries are "unverified" until Imane has reviewed them
  (`reviewed_by` in the file). Unverified figures stay off the tearsheet, as the spec requires
  for anything not checked.
- **Same definitions.** ADP's capex is again cash paid: 1,265 bought less a 47 increase in
  supplier payables = 1,218, which matches ADP's own figure "€1,218 million ... (including
  fixed asset suppliers)".

**Later.** If the ESEF packages turn up, `tearsheet add-package` (decision 0006) loads them,
and these entries are removed.
