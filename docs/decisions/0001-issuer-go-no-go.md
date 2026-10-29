# 0001 · Issuer go / no-go (M0)

Date: 2026-10-29 · Status: **proposed, waiting for Imane's choice of replacements**

## Rule

An issuer is **go** when at least three fiscal years from FY2021 have every critical line
tagged, either with a standard IFRS concept or with a company-specific (extension) concept:
revenue, operating profit, D&A, cash, borrowings, lease liabilities, cash from operations, capex.
Leases count as covered when the issuer shows them inside borrowings and the debt note confirms
it (evidence recorded in `config/issuers.yaml`). Full results: `docs/m0/coverage.md`.

## Result for the ten v1 candidates: 7 go, 3 no-go

| Issuer | Decision | Years usable | Why |
| --- | --- | --- | --- |
| Air France-KLM | go | 2021–2024 | FY2023 and FY2025 filings are missing from the database; FY2023 is read from the FY2024 comparatives. FY2025 is not available. |
| IAG | go | 2021–2025 | Leases sit inside "interest-bearing borrowings" (confirmed in the note). |
| Finnair | go | 2021–2025 | Capex is split into aircraft and other capex (two company tags). |
| easyJet | go | 2021–2025 | FY2021 (to Sep 2021) comes from the FY2022 comparatives. |
| Groupe ADP | go | 2021–2024 | Same database gaps as Air France-KLM (no FY2023 or FY2025). Leases sit inside borrowings. |
| Aena | go | 2021–2025 | Leases sit inside "Deuda financiera". |
| Flughafen Wien | go | 2021–2025 | Borrowings and leases share one company tag ("Finanz- und Leasingverbindlichkeiten"). |
| Deutsche Lufthansa | **no-go** | none | Listed in the database, but no filings. The database holds no German filings at all. |
| Fraport | **no-go** | none | Not in the database (Germany). |
| Ryanair | **no-go** | none | Not in the database. The database holds no Irish filings at all. |

The spec's bar is eight issuers, so **the original list misses it by one**.

## Reserve candidates checked

| Issuer | Decision | Years usable | Notes |
| --- | --- | --- | --- |
| Norwegian Air Shuttle | go | 2021–2025 | Low-cost; reports in NOK. |
| Wizz Air | go | FY2021–FY2026 (year to March) | Low-cost; EUR; FY2024 comes from comparatives; leases inside borrowings (confirmed). |
| Icelandair | go | 2021–2025 | Network; reports in USD; revenue tagged together with other operating income. |
| Copenhagen Airports | no-go | none | Lease liabilities not identified, and its report text comes out garbled (letter-by-letter conversion from PDF). |

## Options for Imane

1. **Swap in reserves (recommended).** Norwegian and Wizz Air replace Ryanair as the low-cost
   pair with easyJet, which gives 9 issuers (6 airlines, 3 airports) and passes the bar.
   Icelandair can be added as a seventh airline. No airport replacement passed.
2. **Keep Lufthansa, Fraport and Ryanair by loading their filings from another source.**
   The companies publish the same ESEF files on their investor sites. M1 would need a second
   way in (a downloaded file instead of the database). That's more work, and those files would
   have to be refreshed by hand.
3. **Go with 7.** That's below the spec's bar, and there would be no low-cost peer for easyJet.

## Carried to later milestones

- **M1 · Air France-KLM D&A.** The only tag is "Amortissements, dépréciations et provisions",
  which includes provisions, so EBITDA would be overstated. Take pure D&A from the notes or
  use an override.
- **M1 · ADP capex.** Two company tags exist ("FluxDinvestissementCorporelsIncorporels" and
  "InvestissementsCorporelsIncorporelsEtDePlacement", the second one including placements).
  Pick one and record it in the overrides.
- **M1 · Latest year.** Air France-KLM's and ADP's latest year is FY2024, while their peers
  are on FY2025. Either flag it on the tearsheet or source FY2025 directly (option 2).
- **M3 · Spacing.** In some reports the text has broken spacing ("2. 7 %", "A SK"). The quote
  check must ignore spaces when matching.
- **M3 · Notes for FY2021.** Notes are not tagged for FY2021 (the text blocks became mandatory
  in FY2022), so FY2021 note items need the full report text.
