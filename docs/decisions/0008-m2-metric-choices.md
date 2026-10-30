# 0008 · Metric choices (M2)

Date: 2026-10-30 · Status: accepted (choices 1a to 7a by Imane)

| # | Question | Choice | How it is applied |
| --- | --- | --- | --- |
| 1 | Peer groups | Network, low-cost and airports, plus "all airlines" | `config/peers.yaml` |
| 2 | Cash-like investments in net debt | Each company's own net debt definition | `config/metric_settings.yaml`, with the evidence for each company |
| 3 | EBITDA | Operating profit + D&A, with associates' results taken out where they sit inside operating profit | Only ADP (-292m in 2024); checked by ADP's own arithmetic (994 - 152 = 842 before tax) |
| 4 | Interest coverage | Interest expense (lease interest included) where tagged, else interest paid | Interest expense for Air France-KLM, easyJet, Norwegian, Aena; interest paid for the others, said in each note |
| 5 | Different year-ends | Peer year = the 31 December within six months of the year end | Wizz Air's year to March 2026 and easyJet's to September 2025 sit in 2025, labelled with their months |
| 6 | Credit ratings | Not shown in v1 | – |
| 7 | Liquidity before M3 | "Cash liquidity" (cash + cash-like), labelled partial | Undrawn facilities are added in M3 |

**Cash-like items per company** (choice 2):

- Air France-KLM: marketable securities over 3 months and bonds (note 32).
- ADP: restricted bank balances (note 9.4.2).
- IAG: interest-bearing deposits over 3 months.
- Finnair: other current financial assets.
- easyJet: money market deposits.
- Norwegian: money market funds.
- Wizz Air: short-term deposits and restricted cash.
- Aena: cash only.
- Flughafen Wien: current investments and securities.

Air France-KLM's and ADP's items aren't tagged, so they are entered from the notes in Imane's
PDFs. They cover FY2023-FY2025; earlier years show net debt as missing rather than understated.

**Other rules.**
- When EBITDA (or interest) is zero or negative, leverage and coverage are "n.m." and are left
  out of peer medians and ranks.
- A metric with a missing input is shown as missing with the reason, never as zero.
- Every value carries a note listing what was used (Imane's request), for example "Operating
  profit 994 − share of associates (−292) + D&A 791 = 2,077".
- A metric is "verified" only if all its inputs are. Figures entered by hand and not yet
  reviewed are marked * in the reports.
- No pension or hybrid adjustments in v1 (spec). Air France-KLM's perpetual bonds stay in
  equity.

**Our net debt vs the companies' own figures (FY2024).** IAG 7,517 (company: about 7.5bn).
ADP 8,576 (company 8,572: it also adds a minority put and deducts derivative assets). Air
France-KLM 7,710 (company 7,332: it also deducts accrued interest, debt-related deposits and
derivatives). The definition here is simpler and the same for everyone; the differences are
explained above.
