# M8 plan: cash flow after leases, the maturity wall and a ratings box

Status: **approved by Imane** (2026-11-11) with every recommendation: 1. all three parts,
without rating trigger headroom; 2. principal maturity walls where printed; 3. ratings from the
companies' own reports; 4. two sections redrafted; 5. the page 1 chart becomes liquidity against
maturities. Built on `m8-cash-flow-refinancing` (decision 0022, `docs/m8/walkthrough.md`).

## What M8 is for

v1 is complete and live. Set beside a sell-side credit note, the tearsheet still misses three
things a credit reader looks for (the candidates listed at the end of the M7 walkthrough):

1. **Cash flow after leases.** Under IFRS 16, a lease payment is a debt repayment, so it sits
   in financing cash flows and never reduces cash from operations. An airline that leases its
   aircraft therefore shows a better free cash flow than one that buys them, for the same
   economics. Think of two households, one paying a mortgage and one paying rent: today's free
   cash flow counts the mortgage holder's house purchase but not the tenant's rent. Taking
   lease payments out puts the two on the same footing.
2. **The debt maturity wall.** Leverage says how much debt there is; the maturity wall says
   *when* it must be repaid. Liquidity set against the debt due in the next one to two years is
   the first refinancing question in any credit committee.
3. **A ratings box.** The spec already leaves room for "rating if entered" in the header; v1
   left ratings out (decision 0008). M8 enters them by hand, with source and date.

Every new figure goes through the same controls as today: tagged in the filing, read from the
report with a quote that code checks, or entered by hand with a source and your review.

## What I found before writing this plan

I checked the newest filings of the seven companies with an electronic FY2025 filing:

- **Lease payments** are tagged in all seven. Gaps in older years: ADP FY2023 to FY2025 and
  Wizz Air FY2021 to FY2024 (company-specific lines; to be mapped as in M1).
- **Proceeds from selling aircraft and other fixed assets** (including sale-and-leaseback) are
  tagged with the standard line by easyJet, Wizz Air, Aena and Vienna; IAG, Finnair and
  Norwegian use their own lines or show them together with other items (to be mapped, or
  missing with a stated reason).
- **Maturity tables are not tagged** (they sit in the notes, which are tagged only as blocks of
  text). The maturity wall therefore comes from the report text, read by the AI and checked by
  code, as the traffic figures were in M3. Air France-KLM and ADP FY2025 have no electronic
  filing: their tables are entered by hand from the PDFs you supplied, as in decision 0007.

## What gets built

1. **Cash flow after leases** (all tagged figures, no AI).
   - New line: proceeds from disposals of fixed assets, mapped per company.
   - New metrics in `catalog.yaml`, each with a unit test:
     - **Net capex** = purchases of PP&E and intangibles − disposal proceeds.
     - **FCF after leases** = cash from operations − net capex − lease principal payments.
     - **FCF after leases to debt** = FCF after leases ÷ total debt (ranked in peer views).
   - Today's FCF stays as it is (it passed gate 1); the new figure sits beside it.
2. **Refinancing risk.**
   - **Debt due within one year** (tagged: current borrowings + current lease liabilities) and
     **short-term debt cover** = liquidity ÷ debt due within one year.
   - **The maturity wall**, read from the debt note for each tearsheet year: amounts due within
     1 year, 1 to 2 years, 2 to 5 years and over 5 years (question 2 for the definition).
     Checks in code, on top of the M3 quote checks: **the table must foot** (the buckets add up
     to the total printed in the same table), and **the first bucket must agree** with the
     tagged current debt on the balance sheet (within a tolerance written before the run).
     A table that fails stays flagged and off the page until you approve or correct it.
3. **Ratings box** (hand entries, `config/ratings.yaml`): agency, long-term rating, outlook,
   date of the rating action, source (page of the annual report or the company's own investor
   page), entered by, reviewed by. Shown in the tearsheet header with "as at" its date, and
   flagged if older than twelve months; "not rated" where no agency rates the company. Not
   ranked or compared in peer views.
4. **On the page.** App, PDF and Excel get the new figures, each with its source card:
   - KPI table: two new rows (FCF after leases, short-term debt cover).
   - Page 1: the liquidity chart becomes **liquidity against maturities** (the liquidity bar
     beside the maturity buckets); liquidity over four years stays in the KPI table
     (question 5).
   - Header: the ratings box.
   - Excel: the new metrics as live formulas; the maturity tables with their quotes on the
     Extracted sheet.
5. **Commentary** (question 4): the fact sheet gains the new figures; the "Liquidity and
   funding" and "Watch items" sections are redrafted with a new prompt version (`draft-v8`),
   through the same verifier. The verifier learns one new rule: a rating may only appear
   through a blank, like any number (so the AI can't type "BBB-" or "Baa2" itself).
6. **Spec and records**: an M8 section in `docs/SPEC.md` with its checklist, decision 0022
   (ratings now shown, the maturity wall definition), README and Method page updated.

## How we know it works (the M8 checklist)

- [ ] **Cash flow after leases computed** for every issuer and year, or missing with a stated
      reason; one unit test per new metric; checked against a second-source model for Air
      France-KLM and ADP FY2024-FY2025 within the gate 1 tolerances (0.1 point on ratios).
- [ ] **Maturity wall: no wrong value marked verified** on an answer key of at least eight
      issuer-years, written before the extraction runs; every table foots or is flagged; every
      unverified bucket visibly flagged.
- [ ] **Ratings box complete**: every entry with agency, rating, outlook, date and source,
      reviewed by you.
- [ ] **The tearsheet stays clean**: every new figure traces to its source on click; the PDF
      still fits two pages for all 18 tearsheets; Excel recalculates 18 of 18; the adversarial
      suite, extended with maturity and rating sentences, 100% rejected; ten consecutive
      redrafts with zero unreferenced numbers.

Tests green throughout. The public app does not change until the end (see below).

## What you do

1. Answer the five questions below.
2. Review the hand entries: the ratings, and the Air France-KLM and ADP FY2025 maturity tables
   (about 20 minutes; page references given for each figure).
3. Approve or correct any maturity table the checks leave flagged, in the app, with a reason.
4. Give the go-ahead to merge into `main`. **The public link follows `main`**, so the live app
   changes only at that moment, once every check is green.

## Order of work

1. Mapping: disposal proceeds and the lease payment gaps; new metrics, unit tests.
2. Second-source check of the cash flow metrics (Air France-KLM and ADP).
3. Ratings entries for your review.
4. Answer key for the maturity tables (written and committed before the AI runs), then
   extraction, foot and cross-checks, and the hand entries for the two PDFs.
5. Fact sheet, prompt `draft-v8`, verifier rule, redrafts.
6. App, PDF, Excel; the 18 PDFs and workbooks re-checked; sample PDFs regenerated.
7. Spec, decision 0022, README, walkthrough, checklist.

**AI tokens** (estimate): about 150,000 for the maturity tables, and about 790,000 for the
redrafts (one M4 drafting round was 686,799 in and 99,656 out). Recorded answers are replayed,
so reruns cost nothing.

## New software

None. Everything uses the stack already in place.

## Known difficulties

- **Maturity tables differ by company**: some give principal repayments, others contractual
  cash flows including interest (the IFRS 7 table); buckets differ (some split years 2 to 5
  year by year). Code adds narrower buckets into the four standard ones; a table on another
  basis is labelled as such and kept out of peer comparisons.
- **Two-page limit**: two tearsheets already need 8.0 point type. The chart swap (question 5)
  keeps the page budget roughly even; if a tearsheet overflows, the PDF test will say so.
- **Ratings change.** The box shows its "as at" date and flags entries older than a year; it
  is a record of a public rating, not an opinion.
- **Redrafts change the commentary** of all 18 tearsheets, including the three samples. Your
  analyst views (`notes/`) are not touched.

## Questions for Imane

1. **Scope.** (a) All three parts as above; (b) cash flow after leases and the maturity wall,
   ratings later; (c) cash flow after leases only (small, no AI). Recommendation: (a). I would
   **leave out rating trigger headroom**: agencies set their thresholds on their own adjusted
   figures (pensions, hybrids, leases treated their way), which this tool deliberately doesn't
   compute, so headroom measured on our figures against their thresholds would look precise and
   be wrong. Covenant headroom from the filings is the better version, in v2.
2. **Definition of the maturity wall.** (a) Principal repayments of borrowings (bonds, bank
   debt) with lease liabilities as a separate layer, in four buckets: within 1 year, 1 to 2,
   2 to 5, over 5; (b) the IFRS 7 contractual cash flows, interest included (every company
   publishes this table, but it doesn't add up to the debt figure). Recommendation: (a), so the
   wall adds up to total debt, with (b) used only where a company gives nothing else, labelled.
3. **Source of the ratings.** (a) The company's own annual report or investor page, with page or
   link and date, reviewed by you; (b) the agencies' websites. Recommendation: (a): a public,
   citable source on the company's side, and no agency content reproduced (spec, legal).
4. **Commentary.** (a) Redraft "Liquidity and funding" and "Watch items" with the new figures
   (prompt `draft-v8`, about 790,000 tokens, all checked by the verifier); (b) new figures in
   tables and charts only, commentary unchanged. Recommendation: (a): a funding paragraph that
   ignores the maturity wall reads incomplete to a credit reader.
5. **Page 1 chart.** (a) Replace the liquidity trend chart with liquidity against maturities;
   (b) keep both, shrinking the charts; (c) put the maturity wall on page 2 instead.
   Recommendation: (a): it answers a sharper question, and the trend stays in the KPI table.

Working rule reminder: one milestone per session. Once you approve, I build M8 on
`m8-cash-flow-refinancing` and merge into `main` only when the checklist is green and you say go.
