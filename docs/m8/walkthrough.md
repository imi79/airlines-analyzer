# M8 walkthrough: cash flow after leases, the maturity wall, a ratings box

**What M8 built.** Three things a sell-side credit note has and v1's tearsheet lacked, under
the same controls as before: tagged figures, figures read from the report with a quote that
code checks, or hand entries with a source and your review.

## What you will see on the tearsheet

| Where | What is new |
| --- | --- |
| Header | A ratings line, from the company's own annual report, with its date ("awaiting review" until you review it) |
| Key figures table | Two rows: **FCF after leases** and **short-term debt cover** (liquidity ÷ debt due within a year) |
| Page 1 chart | **Liquidity against maturities**: this year's liquidity bar beside the debt falling due (within 1 year, 1 to 2, 2 to 5, over 5 years); without a checked maturity table, the debt due within a year from the balance sheet |
| Liquidity and funding, Watch items | Redrafted with the new figures (prompt `draft-v8`); the other four sections keep the M4 text you accepted |
| Source cards | Click a maturity bar: the table's title, its rows as printed, the time span code read from each column label, the checks |

## The three parts, in credit terms

**1. Cash flow after leases.** Under IFRS 16 a lease payment is a debt repayment, so it never
reduces cash from operations: an airline that leases looks more cash-generative than one that
buys, for the same economics (the tenant's rent left out, the owner's purchase counted).
*FCF after leases* = cash from operations − net capex (purchases − disposals, sale-and-leaseback
included) − lease payments − interest paid where the company shows it in financing. Example,
Air France-KLM FY2025: 5,055 − 3,058 − 960 − 670 = **EUR 367m**, against an FCF of 606m.
Checked against figures typed from the published statements: 16 of 16 within tolerance.

**2. The maturity wall.** It sits in the notes, which are not tagged, so the AI reads the
table and code checks it: every quote word for word, code (not the AI) turns each column
label into a time span, each row must add up to its printed total, and the table must agree
with the balance sheet (the first year with the current debt). Result against an answer key I
built from the reports before the AI ran: **4 tables verified, all correct, none wrong**. The
others are flagged with their reasons. A few examples, each a sound reason to stop:
- IAG's convertible bond is in current debt but falls due later;
- at Norwegian the AI picked the parent company's table, not the group's;
- at Aena it took the whole liquidity table, trade payables included.

Coverage is honest but low: 4 of 18 tearsheets show a checked wall (Finnair FY2024 and
FY2025, Air France-KLM FY2024, easyJet FY2025 for its leases).

**3. Ratings.** Nine entries, copied from each company's report with the page and the date;
code checked that each sentence is in the report and shows the agency, rating and outlook.
Three reports name no rating (Norwegian, Wizz Air, Vienna): the box says so, without claiming
the company is unrated. Aena's report rates its 2025 bond, not the company: labelled so. Air
France-KLM's, ADP's and easyJet's dates are more than a year old: flagged.

## Two things worth knowing

- **A correction to M4's fact sheets.** "Load factor" existed twice (the tool's RPK ÷ ASK, and
  the company's printed figure kept as a cross-check); which one the fact sheet took was left
  to chance. It is now always the computed one. Effect: easyJet FY2025's sentence "load factor
  rose" was removed, because it is flat on the computed basis. The snapshots of Finnair FY2024
  and Wizz Air FY2025 no longer pass one direction check and are flagged for you to edit (‡ on
  the PDF). M4's own records are untouched.
- **I had to change the maturity checks after seeing the first answers**, as in M3: the first
  run, with the checks as written, verified 2 tables (both correct); fixes of form, and one
  tighter bound that caught Aena, gave 4. Because the fixes were judged on the same key, read 4
  of 11 as a working figure, not a blind score.

## What you do (about 30 minutes)

1. **Review the nine ratings** in `config/ratings.yaml` (each has the page and the sentence):
   write your name and date in `reviewed_by` for those you accept.
2. **Review four FY2025 hand entries** in `config/manual_figures.yaml` (`pending_review`): Air
   France-KLM disposals 1,391 (statements page 8); ADP lease payments 30 and disposals 35 (French
   statements, page 7). Until then those two tearsheets show FCF after leases as awaiting review.
3. **Review the two FY2025 maturity tables entered by hand** (`config/maturity_entries.yaml`:
   Air France-KLM page 75, ADP pages 57 and 64). ADP's will still be flagged after your review:
   its tables do not agree with the balance sheet (the bank-and-bond table leaves out leases and
   other debt).
4. **Optionally approve flagged maturity tables** in the app (Data and audit), where you judge
   the reason acceptable (for example IAG's convertible bond).
5. **Read two or three redrafted notes** (`docs/m8/drafts/`, or `docs/m8/pdf/`), and edit the
   two flagged snapshots if you wish. One small wording glitch to fix by hand: Finnair FY2025
   says "covered 17.39x times".
6. **Say go to merge into `main`**: the public link updates then.

## Results

| M8 checklist | Result | |
| --- | --- | --- |
| Cash flow after leases for every company and year, tested, second-source check | 9 of 9 companies; 16 of 16 within tolerance | ✓ |
| Maturity wall: no wrong value verified on the answer key; flagged otherwise | 0 wrong, 4 verified, 10 flagged with reasons | ✓ |
| Ratings box complete and reviewed by you | 9 entries checked by code; your review pending | to do |
| The tearsheet stays clean | Sources 18 of 18; PDF two pages 18 of 18; Excel 18 of 18; 52 of 52 faulty sentences rejected; 18 notes in a row with no number outside a blank | ✓ |

AI tokens: about 165,000 for the maturity tables, about 563,000 for the redraft. 638 tests pass.

## Next

- A second prompt round for the maturity tables (group tables only, never compute a total) to
  raise coverage, judged on a fresh set of reports.
- Rating trigger headroom stays out (agency-adjusted figures); covenant headroom is for v2.
