# M9 walkthrough: a watchlist of credit triggers

**What M9 built.** The first thing a credit analyst looks at each morning: *which of my names
crossed a trigger, and why?* You set the triggers, like covenants you write for yourself; the
tool checks every company and year against them, from verified figures only, and every flag
opens on the figures behind it, down to the filing. No new data, no AI tokens; the commentary is
not redrafted.

## What you will see

| Where | What is new |
| --- | --- |
| **Watchlist page** (new, in the left menu) | Companies down the side, your seven triggers across the top, for one year. Each cell: **fired**, **clear** or **cannot assess**, with the figure. Filters: "with a trigger fired", "with a new warning" (fired this year, not the year before). Below the table: each fired trigger in one sentence, with a source button; the "cannot assess" list with the reason for each |
| **Tearsheet**, under the ratings | One line: "Watchlist: 1 trigger fired (net leverage above 3.0x); 4 clear, 1 cannot be assessed", a source button, and a link to the page |
| **PDF**, under the ratings | The same line |
| **Method page** | A short paragraph on how the watchlist works |

![The Watchlist page, 2025](watchlist_page.png)

![The line on the tearsheet](tearsheet_line.png)

![The line on the PDF](pdf_line.png)

## Your seven triggers

They live in `config/watchlist.yaml`, written the way you would read them, each with its reason,
your name and the date (2026-11-12). To change a threshold, change the number there: "3.0x"
becomes "3.5x", and the page and the PDFs follow, with no rebuild.

| Trigger | Kind | Applies to |
| --- | --- | --- |
| Net leverage above 3.0x | level | all |
| Interest coverage below 3.0x | level | all |
| Short-term debt cover below 1.0x | level | all |
| Cash flow after leases negative | level | all |
| Liquidity to revenue below 20% | level | airlines only |
| Net leverage up more than 0.5x | move on the year | all |
| EBITDA margin down more than 3 points | move on the year | all |

**Three rules, in covenant terms.**

1. **The threshold is strict**, as in a covenant test: "above 3.0x" breaches only above it.
   Exactly 3.0x is compliant.
2. **The test uses the exact figure, not the rounded one.** Aena FY2022's net leverage is
   3.0031x, printed "3.00x": it fires. The card says "stored value 3.0031x", so you are not
   left wondering why 3.00x breached 3.0x.
3. **What the tool cannot see, it does not pass.** If the figure is missing, not meaningful
   (for example leverage when EBITDA is negative, or a ratio to a very small debt) or still
   awaiting your review, the cell says **cannot assess**, with the reason. A watchlist that
   quietly passes what it cannot see is worse than none (your answer to question 4).

**Two floors: liquidity, and short-term debt cover** (the first added beyond the plan; you
kept it and asked for the second on 2026-11-12).
Liquidity is cash plus the undrawn credit lines. The undrawn lines are often the missing piece
(not in the report, or awaiting your review). But if cash alone is already 20% of revenue or
more, liquidity is too: the credit lines can only add to it. In that case the trigger shows
**clear**, and its card says it was decided on cash alone. Think of it as a lender who sees
enough cash on deposit to pass the test without looking at the revolver. It can only clear the
trigger, never fire it, and is not used where liquidity itself is verified. It decides 7 of
the 12 airline tearsheets (Air France-KLM, easyJet FY2024, Norwegian, Wizz Air).

Short-term debt cover works the same way: a new ratio, **short-term debt cover, cash only**
(cash and liquid investments ÷ debt due within a year), which can only be lower than the full
cover. If cash alone already covers the debt due, the trigger is clear. It decides 10 of the 18
tearsheets. It feeds the watchlist only: it is in the Excel backup but not on the tearsheet's
table, and it is never shown to the AI, so the commentary you accepted is untouched.
(Decision 0023.)

On the page, a result decided on cash alone shows with "≥", for example "clear · ≥ 1.08x":
the full figure is at least that.

## The findings: what fired

On the 18 tearsheets: **9 triggers fired, 107 clear, 4 cannot assess** (120 checks).

| Company and year | Trigger | Figure |
| --- | --- | --- |
| Groupe ADP FY2024 | Net leverage above 3.0x | 4.13x |
| Groupe ADP FY2025 | Net leverage above 3.0x | 3.68x (down from 4.13x, still above) |
| Wizz Air FY2025 (Apr 2024 to Mar 2025) | Net leverage above 3.0x | 4.28x |
| Wizz Air FY2026 (Apr 2025 to Mar 2026) | Net leverage above 3.0x | 3.79x |
| Air France-KLM FY2024 | Cash flow after leases negative | EUR −1.1bn |
| Air France-KLM FY2024 | Net leverage up more than 0.5x | 1.29x to 1.88x, up 0.59x |
| Finnair FY2024 | EBITDA margin down more than 3 points | 18.0% to 14.6%, down 3.4 points |
| Norwegian FY2024 | EBITDA margin down more than 3 points | 22.6% to 18.9%, down 3.7 points |
| Flughafen Wien FY2025 | EBITDA margin down more than 3 points | 42.0% to 36.5%, down 5.5 points (new this year) |

None of these is a surprise for a credit reader, which is what you want from a first set of
thresholds: ADP and Wizz Air carry the most leverage of their groups; Air France-KLM's 2024 cash
burn after leases and the margin drops at Finnair and Norwegian are in their commentary. Vienna's
margin drop is the one "new warning" of 2025; its leverage is net cash, so it is a profitability
signal, not a solvency one.

**Where the tool cannot tell (4), all Flughafen Wien.**

- **Short-term debt cover, FY2024 and FY2025**: Vienna does not report its current borrowings
  separately, so the debt due within a year, and both cover ratios, cannot be built. The card
  gives both reasons.
- **Interest coverage, FY2024 and FY2025**: its debt is very small, so the ratio is not
  meaningful (the same rule as the peer tables since M4).

**Close calls on short-term cover** (clear, but only just on cash alone): Groupe ADP FY2025,
cash covers **1.08x** the debt due within a year; Wizz Air FY2025, **1.14x**; ADP FY2024,
**1.17x**. Their undrawn lines are not in the reports, so the full cover is higher, but these
are the names to watch if cash falls.

**Your thresholds, after these results** (plan question 2 said you would adjust them). Two
observations to help: at 3.0x, net leverage flags the two names everyone would flag (ADP, Wizz
Air) and nothing else; interest coverage below 3.0x and short-term cover below 1.0x fire
nowhere in 2024-2025 (their lowest are Finnair FY2024 at 4.15x coverage, and IAG FY2025 at 3.59x cover
among the tearsheets with the full ratio), so they act as tail-risk alarms, not daily
signals.

## How to try it

1. Open the app (`uv run tearsheet app`, or the public link once merged) and click
   **Watchlist** in the left menu. The year starts at the year of the tearsheet you were on.
2. Choose **With a new warning**: only Flughafen Wien FY2025 remains.
3. Click the ⓘ next to "Groupe ADP FY2025 · Net leverage above 3.0x": the card shows 3.68x
   against 3.0x, why the trigger matters, who set it and when; click "Net leverage" under
   "Built from" and follow it down to net debt and EBITDA, then to the filing.
4. Click a row of the table: every trigger for that company, each with its figures.
5. On the Tearsheet page, the line under the ratings has its own ⓘ and a "Watchlist page" link.
6. In demo mode, approve Air France-KLM's FY2025 undrawn lines on the Data and audit page: the
   liquidity trigger now uses liquidity itself instead of the cash floor. Nothing is saved.

## The checklist

| Item | Result | |
| --- | --- | --- |
| Every trigger evaluated for every company and year shown, from verified figures only; missing or unverified figures "cannot assess" with the reason | 120 checks on the 18 tearsheets: 9 fired, 107 clear, 4 cannot assess. Every company and every year in the library (FY2021-FY2026), every trigger that applies: a result, and a reason for each cannot-assess; no fired or clear result rests on an unverified figure (`tests/test_watchlist.py`) | ✓ |
| Every fired trigger traces to the figure behind it on click | 18 of 18 tearsheets: each fired trigger's card leads down to filing facts, quotes or hand entries, all checkable; also part of the page's figures, so the existing source test and the export manifest cover them | ✓ |
| Unit tests for each trigger kind, the edges and "cannot assess" | Level above and below, cash flow below zero, moves up and down (in points), exactly at the threshold for each, missing, not meaningful, awaiting review, last year missing, both floors (clears, exactly at the threshold, cannot decide, never overrides, both reasons when neither ratio exists); the new ratio has its own unit tests, and never exceeds the full cover | ✓ |
| The PDF still fits two pages for all 18 tearsheets | 18 of 18; the new line changed no text size (11 at 8.5 point, 7 at 8.0, as before M9). Excel recalculated 18 of 18 | ✓ |

## What I need from you

1. Read the Watchlist page and tell me if a fired trigger surprises you, or a threshold should
   move.
2. Say go to merge into `main` (the public link follows `main`).
