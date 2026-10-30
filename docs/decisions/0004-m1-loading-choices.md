# 0004 · How figures are loaded and mapped (M1)

Date: 2026-10-29 · Status: accepted (choices 1a, 2a and 4b by Imane)

1. **Air France-KLM D&A.** Air France-KLM tags one line, "Amortissements, dépréciations et
   provisions", which also includes provisions. We use it as reported, with a footnote, because it
   is the line Air France-KLM's own EBITDA uses. Rebuilding pure D&A would mean adding up three
   notes by hand.
2. **Restated figures.** When a later filing restates a prior year, the tearsheet uses the latest
   restated figure (the comparative column of the newer filing). The figure as first reported
   stays in the facts table with a "restated" flag, so the audit page can show both.
3. **Spot check.** Imane checks Air France-KLM and Groupe ADP, FY2023 and FY2024, against the
   published accounts, using the check sheet in `docs/m1/`.
4. **Missing FY2025 filings (Air France-KLM, ADP).** These are loaded from the ESEF report
   package published by the company, because filings.xbrl.org doesn't have them. Both
   companies' websites turn away automated downloads, so Imane downloads each package in a
   browser and hands it over. The package's hash and origin are recorded like any other filing.
   *Update:* the packages weren't found, so FY2025 was entered from the published statements
   instead (decision 0007).

Further choices made while building:

- **Sign convention.** Costs and cash outflows are stored as positive amounts (capex 3,728, not
  −3,728). When a company tags an outflow as negative, its override file flips the sign and says
  so. The value exactly as tagged is kept next to the canonical value.
- **Company-specific labels** are matched on their name within the company's own taxonomy, not
  on the short prefix, because the prefix changes between years (`AFKLM:` in 2021, `afklm:` later).
- **Capex is cash paid**, which includes the change in amounts owed to fixed-asset suppliers.
  That's the standard IFRS cash-flow basis, and it's what Air France-KLM's capex line shows
  (3,195 + 322 + 195 + 16 = 3,728 in FY2024). For ADP this means "Investissements corporels,
  incorporels et de placement" (where "de placement" is investment property, not financial
  investments) less the change in supplier payables: 1,089 + 80 = 1,169 in FY2024, which
  equals ADP's own cash total. This corrects the M0 reading. ADP's FY2021-FY2022 line doesn't
  show which basis it uses, so it is flagged for checking.
- **Two extra tables** sit beside the spec's `facts` table: `filings` (one row per filing used, with
  hash, origin and links) and `raw_facts` (every number tagged in those filings), so any loaded
  figure can be traced back to the exact tag it came from.
