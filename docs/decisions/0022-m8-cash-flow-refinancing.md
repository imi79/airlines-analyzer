# 0022 · M8: cash flow after leases, the maturity wall and a ratings box

Date: 2026-11-11 · Status: plan approved by Imane with every recommendation ("approved with
all recommendations, go ahead on m8-cash-flow-refinancing"); ratings reviewed and merged into
`main` on her go-ahead ("I reviewed the ratings, merge into main")

**Choices approved with the plan** (`docs/m8/plan.md`):

1. **All three parts**, without rating trigger headroom: agencies set their thresholds on their
   own adjusted figures, which this tool does not compute. Covenant headroom is for v2.
2. **The maturity wall is principal (or carrying amount) where the company prints it**, with
   the IFRS 7 contractual cash flows (interest included) used where nothing else is printed,
   labelled as such. Four standard buckets: within 1 year, 1 to 2, 2 to 5, over 5 years.
3. **Ratings from the company's own report**, with the page, the date and the exact sentence;
   no agency research reproduced.
4. **Two sections redrafted** ("Liquidity and funding", "Watch items") with prompt `draft-v8`;
   the other four keep the draft-v7 text Imane accepted in M4.
5. **The page 1 chart becomes liquidity against maturities**; liquidity over four years stays
   in the KPI table.

**Cash flow after leases.**

- **New statement line**: proceeds from disposals of fixed assets, sale-and-leaseback
  included, optional (a year without disposals counts as zero in net capex, said in the note).
  Company lines: Air France-KLM ("Produits de cessions d'immobilisations"), easyJet (its
  sale-and-leaseback line added to the standard one). FY2025 hand entries for Air France-KLM
  (disposals 1,391) and ADP (disposals 35, lease payments 30), each with its prior-year
  control matching the database (39 of 39), **waiting for Imane's review** (`pending_review`).
- **Lease payments filled in**: ADP from FY2023 tags one line, the cash outflow for leases,
  which includes the interest on leases (its interest paid excludes it, so nothing counts
  twice); Wizz Air tagged its lease repayments as "repayments of borrowings" until FY2025
  (the FY2026 filing tags the same FY2025 amount, 720.0, as lease payments).
- **Interest paid is taken out only where the company shows it in financing**, read year by
  year from the tagged concept (Air France-KLM moved it to financing from FY2023); for a
  company concept or a hand entry, from `metric_settings.yaml` with the evidence (ADP, and Air
  France-KLM FY2025). Otherwise companies that put interest in financing would look better.
- **Today's FCF is unchanged** (gate 1). New metrics: net capex, FCF after leases, FCF after
  leases to debt (ranked; "not meaningful" for Vienna's very small debt, as FCF to debt).
- **Second-source check**: 16 of 16 within the gate 1 tolerances (Air France-KLM and ADP,
  FY2024-FY2025), from figures typed from the published statements (`docs/m8/cash_flow_check.md`).

**Refinancing.**

- **Debt due within one year** is tagged (current borrowings + current lease liabilities, or
  current borrowings alone where leases sit inside them); **short-term debt cover** is
  liquidity over it, so it needs the undrawn facilities read in M3.
- **Borrowings due within two years** and its cover come from the maturity wall: only where
  the table shows the second year on its own (a "1 to 5 years" column gives none).

**The maturity wall.**

- **A separate AI job** (`maturity-v1`), so the M3 extraction requests and their recorded
  answers stay as they were. One call per report, the latest two years, about 10,000 tokens
  each (16 reports, about 165,000 tokens in all).
- **Rows, not only totals**: some companies print the layer as several rows with no subtotal
  (IAG: asset financing, leases, fixed and floating rate borrowings). The form takes the rows,
  code adds them up. "Borrowings" means the company's own balance sheet line: lease liabilities
  are inside it at IAG, ADP, Aena and Wizz Air.
- **Code, not the AI, reads the column labels** ("Less than 1 year", "2027", "Plus de 5 ans",
  "N+1", "Y+1", "Later" after a year column, "Siguientes"). A label it cannot read leaves the
  table unverified.
- **The checks**: every quote word for word near the table's caption; each value printed in
  its row; where a row shows two years, the value in the fiscal year's column; the columns
  run from the year end to an open end without gaps; each row foots to its printed total; the
  first year agrees with the current debt on the balance sheet and the total with the whole
  layer (principal within 10%; contractual cash flows between 90% of the debt and the debt
  plus a year's interest).
- **The Air France-KLM and ADP FY2025 PDFs lose their table rows when turned into text**, so
  their tables are entered by hand (`config/maturity_entries.yaml`) and run through the same
  label, foot and balance sheet checks; unverified until Imane reviews.
- **Answer key first** (`spikes/m8/maturity_key.py`, committed before the AI read any table):
  eight company-years, eleven tables, read by code without AI (method of decision 0012).
- **First run, checks as written**: 2 tables verified (Finnair FY2024 and FY2025), both
  correct. **Changes after the first run**, each for a reason seen in the answers: the AI
  separates header cells with "|" (removed before matching); the unit is printed once at the
  top of the page ("Importes en miles de euros"); a total row is often unlabelled; a number
  inside a row label ("N+1") is not a column. These let through Aena's whole liquidity table
  (trade payables and estimated interest added to the debt), so the bound on a year's interest
  was tightened from 15% to 10% of the debt: above any rate these companies pay. **After the
  changes: 4 verified, all correct, none wrong; 10 flagged** with their reasons
  (`docs/m8/maturity_score.md`). The changes were judged on the same key, so 4 of 11 is not a
  blind measure.
- **Coverage is low and stated**: of 18 tearsheets, 4 show a checked wall. The rest show the
  debt due within one year from the balance sheet, and the flagged tables wait for review in
  the app. A second prompt round (the parent company's table picked instead of the group's at
  Norwegian, totals computed by the AI where none is printed) is a candidate for later.

**Ratings.** Nine entries in `config/ratings.yaml`, each quote checked against its report by
code, all waiting for Imane's review. Three reports give none (Norwegian, Wizz Air, Vienna):
the box says the report gives no rating, not that the company is unrated. Aena's report gives
the rating of its 2025 bond issue only, labelled so. Air France-KLM's and ADP's latest ratings
in the reports date from 2024 and are flagged as more than a year old. A rating reaches the
commentary only through a blank: the verifier now rejects "BBB+" or "Baa2" typed by the AI (5
new adversarial cases, 52 in all, all rejected).

**Keeping M4 reproducible.**

- **The fact sheets the recorded draft-v7 answers were sent are frozen** in
  `records/factsheets/draft-v7/` (copied from the committed `docs/m4/factsheets/`), and the
  M4 replay reads them, so the new metrics in the catalog do not change what was sent.
- **A tie fixed**: "load factor" exists twice for a company-year (RPK ÷ ASK, and the printed
  figure kept as a cross-check). Which one the fact sheet took was left to the database's row
  order, and it changed when M8 added rows. The computed one is now always kept. The frozen
  M4 fact sheets keep what was sent; the M8 fact sheets use the fixed rule.
- **The maturity tables are kept out of the M1 and M3 reports**, which are unchanged.

**After Imane's review of the ratings.**

- **Her review is recorded as "Imane (2026-11-11)"** on all nine entries, as for the M1 hand
  entries. The reviewed ratings became figures the AI may cite (through a blank), which changed
  the fact sheets of the twelve notes with a rating; those notes were redrafted.
- **A rating belongs to the note of its report's year.** The first redraft after the review
  offered the FY2025 report's rating to the FY2024 note too (Aena FY2024 cited a rating dated
  after its year end). The fact sheet now offers a rating only to its own year; the six notes
  concerned were redrafted. The header still shows the latest rating with its date.
- **A rating typed in M4.** Aena FY2024's draft-v7 snapshot says Fitch "upgraded its long-term
  rating to A", written without a blank. The M8 checks now catch a lone "A" after "to", "at",
  "of", "is" or "rated" (narrowly, so ordinary prose passes), in the redraft only so the M4
  record stays as it was; the snapshot is flagged for editing.
- **Tokens**: the redraft took about 1,340,000 in and 91,000 out over four rounds, 1.8 times
  the plan's estimate of 790,000; the maturity tables about 168,000.
- **Final**: 15 of 18 notes pass the verifier in full; 14 in a row with no number outside a
  blank (the checklist asks for ten); three kept M4 snapshots flagged for Imane.

