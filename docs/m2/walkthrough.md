# M2 walkthrough: from statements to credit ratios

**What M2 built.** A ratio rulebook applied the same way to every company, a calculation for each
ratio that records what went into it, and peer tables with medians and ranks. Think of it as
the ratio tab of a credit model, built once and reused for all nine companies.

## How it works

1. **One rulebook** (`src/tearsheet/metrics/catalog.yaml`). Each metric has one written
   definition, its unit and whether higher is better. The definition doubles as the tearsheet
   footnote. Example: *net leverage = net debt ÷ EBITDA; n.m. when EBITDA is zero or negative*.
2. **Company settings, with evidence** (`config/metric_settings.yaml`):
   - **Cash-like items:** which short-term investments each company counts in its own net debt,
     with the quote that shows it.
   - **Associates:** whether its operating profit includes associates' results (only ADP).
3. **A note on every number.** Each value says what was used, for example "Operating profit
   994 − share of associates (−292) + D&A 791 = 2,077".
4. **Honest gaps.** A missing input gives "missing" with the reason, and negative EBITDA gives
   "n.m.". Neither is ever shown as zero. Traffic ratios (ASK, RASK, CASK...) wait for M3.
5. **Peers.** Each metric is lined up across the group, with the median and a rank (1 =
   strongest). Wizz Air's year to March 2026 sits beside the others' 2025, with its months
   shown.

## What we found (FY2025, or the year ending closest to December 2025)

| | Net leverage | EBITDA margin | FFO / debt |
| --- | --- | --- | --- |
| **Network airlines** | | | |
| IAG | 0.78x | 23.0% | 45.5% |
| Air France-KLM | 1.71x * | 15.3% | 27.4% |
| Finnair | 1.77x | 13.1% | 18.0% |
| **Low-cost airlines** | | | |
| easyJet (year to Sep 2025) | net cash (−0.42x) | 14.2% | 44.0% |
| Norwegian | 1.19x | 21.2% | 35.4% |
| Wizz Air (year to Mar 2026) | 3.79x | 23.2% | 15.2% |
| **Airports** | | | |
| Aena | 1.46x | 60.3% | 39.6% |
| ADP | 3.68x * | 34.7% * | 15.7% * |
| Flughafen Wien | net cash (−0.13x) | 36.5% | very small debt |

\* Uses figures you haven't reviewed yet (see below). Full tables: `docs/m2/metrics.md` and
`docs/m2/peers.md`.

- **Our net debt is close to the companies' own figures, and the gaps are explained.** IAG
  7,517 vs about 7.5bn. ADP 8,576 vs 8,572 (ADP also adds a minority put and deducts
  derivative assets). Air France-KLM 7,710 vs 7,332 (Air France-KLM also deducts accrued
  interest, debt-related deposits and derivatives).
- **ADP's EBITDA after taking out associates** is 2,077 for 2024, close to its own recurring
  EBITDA of 2,068. This confirms choice 3a.
- **2021 (Covid) shows "n.m."** for leverage at most airlines, because EBITDA was negative.

## Your two tasks

1. **Gate 1: the reconciliation** (`docs/m2/reconciliation.xlsx`). Build your own model of Air
   France-KLM and ADP for FY2024 and FY2025 from the statements, using the "Definitions" sheet.
   Type your results in the yellow cells. The sheet checks each one: leverage within 0.05x,
   margins and ratios within 0.1 point. Please build the model before looking at the tool's
   figures.
2. **Review 8 new hand-entered figures** in `docs/m1/fy2025_entries.md` (status "unverified"):
   - Air France-KLM: interest expense 2025 (627, page 3), and marketable securities + bonds from
     note 32 (2023: 1,097 + 966; 2024: 1,046 + 1,057; 2025: 988 + 1,156)
   - ADP: share of associates 2025 (−165, page 4), and restricted bank balances from note 9.4.2
     (2023: 118; 2024: 138; 2025: 125)
