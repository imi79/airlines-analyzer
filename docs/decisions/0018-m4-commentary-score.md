# 0018 · M4: the commentary score, done by Claude against the annual reports

Date: 2026-11-09 · Status: scored; below the pass mark; fixes proposed for Imane's approval

**Who scored.** At Imane's request ("check it yourself with the annual reports of the
companies"), Claude scored the ten drafts of the score sheet, after checking each one against
the company's annual report: every figure the draft uses where the report prints it, and every
statement in words. This is the same arrangement as gate 1 (decision 0009: a second source
built by the AI at Imane's request). It is **not an independent review**: the scorer is the
same kind of model that wrote the drafts. To lean against that, the scale is strict (5
publishable as is, 4 minor edits, 3 usable after editing, 2 significant errors or omissions, 1
misleading on a credit point), and every comment names its evidence in the report. Scores and
comments: `docs/m4/commentary_review.yaml`; the score sheet is written from that file, and a
score counts only for the exact draft it was given to (fingerprint).

## Result: 2.93 of 5, below the pass mark of 4

| Draft | Accuracy | Relevance | Concision | Insight | Average |
| --- | --- | --- | --- | --- | --- |
| Air France-KLM FY2025 | 3 | 3 | 2 | 3 | 2.75 |
| IAG FY2025 | 4 | 3 | 3 | 3 | 3.25 |
| Finnair FY2025 | 2 | 2 | 3 | 2 | 2.25 |
| easyJet FY2025 | 4 | 3 | 3 | 4 | 3.50 |
| Groupe ADP FY2025 | 2 | 3 | 2 | 3 | 2.50 |
| Aena FY2025 | 4 | 3 | 3 | 3 | 3.25 |
| Flughafen Wien FY2025 | 1 | 2 | 2 | 2 | 1.75 |
| Norwegian FY2025 | 4 | 3 | 3 | 3 | 3.25 |
| Wizz Air FY2026 | 4 | 3 | 3 | 4 | 3.50 |
| Air France-KLM FY2024 | 4 | 3 | 3 | 3 | 3.25 |
| **Average** | 3.2 | 2.8 | 2.7 | 3.0 | **2.93** |

**What holds.** Every figure the AI used is what the fact sheet holds, and where the report
prints it, it matches (Air France-KLM revenue 33,007 and current EBITDA 5,058; Wizz Air
operating profit 139.7 vs 167.5; Flughafen Wien EBITDA 412.4, margin 36.5%; Norwegian 27.3m
passengers). The verifier did its job: no figure is invented and no direction contradicts the
data.

**Why it fails: four causes, in order of weight.**

1. **Three wrong figures upstream (M2 and M3), not the AI's writing.** The drafts repeat them
   faithfully, so they reach the page:
   - *Flughafen Wien cash.* The company reports net liquidity of 413.8m (down 19.1%); the tool
     counts 110m of cash and securities and misses about 360m of short-term deposits held in
     receivables ("kurzfristige Veranlagungen"). The draft calls Vienna's liquidity the
     weakest of the group and a thin buffer: wrong.
   - *Finnair interest coverage.* Finnair's interest expense is not tagged, so the tool falls
     back on "financial expenses paid, net", which is after interest received (38.0m in 2024,
     87.4m in 2025). On financial expenses (107.2m, 84.8m) coverage improved from 4.1x to
     4.8x; the draft says it collapsed by 7.03x.
   - *ADP revenue per passenger.* Group revenue (TAV and other airports included) divided by
     Paris passengers: not meaningful, as the catalog itself says, but ADP's setting was never
     filled in.
2. **The year's main story is not in the fact sheet**, so the AI cannot tell it: Finnair's
   strikes (about 68m off the comparable operating result), Wizz Air's grounded aircraft (Pratt
   & Whitney engines, "a defining challenge"), IAG's 1.0bn buyback behind its lower cash,
   easyJet holidays behind easyJet's profit growth. The design allows only figures from the
   fact sheet, on purpose; the cost is relevance.
3. **Habits of the prompt**: liquidity named "the point to watch" in six of ten snapshots,
   even where it ranks first in the group; the same figures repeated in two or three
   sections; three peer sentences that only say the company is the median (in a group of
   three, the middle company is the median); a prior-year figure (fleet, passengers) written
   as if current.
4. **Wording of negatives**: "net debt of GBP -602m", "a net cash position of EUR -54.4m".
   The renderer prints the sign; a credit note says "net cash of 602m".

## Proposed fixes (for Imane's approval, not started)

- **A. Data (M2/M3 corrections, each with a test):** Vienna's short-term deposits entered from
  the note, as for Air France-KLM and ADP (decision 0008), for Imane's review; interest
  coverage on finance costs before net interest paid where interest expense is not tagged;
  ADP revenue per passenger marked not meaningful (and Aena's scope checked).
- **B. Fact sheet and renderer:** net debt below zero given as "net cash" (positive); ratios to
  debt shown as not meaningful when the company has net cash; a figure from a year before the
  sheet's own labelled as such.
- **C. Prompt draft-v4:** name the watch point from the weakest ranks and worst moves, never
  liquidity by default; each figure once in the note; for a median company say "in the middle
  of the group"; no sentence on a prior-year-only figure as if current.
- **D. Context the figures cannot carry (design change):** a short list of the year's events
  per company, each with a verbatim quote from the report, checked by code like the M3
  extraction (quote in the report word for word), which the AI may mention without numbers or
  direction words. Or, simpler, Imane writes them. This changes the plan's rule "only figures
  from the fact sheet" and needs her decision.

Then redraft the ten and score again (by Imane, or by Claude on the same basis).
