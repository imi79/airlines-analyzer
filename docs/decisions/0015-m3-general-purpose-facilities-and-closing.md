# 0015 · Undrawn facilities are general-purpose only; M3 closed on the safety result

Date: 2026-11-03 · Status: accepted (Imane: "general-purpose only, and close M3 on the safety
result")

**Undrawn facilities: general-purpose only.** Liquidity counts committed facilities the company
can draw for any purpose: revolving credit facilities and other committed general or overdraft
lines. Facilities that can only finance specific aircraft (or other specific assets) are left
out: they fund those deliveries, not a liquidity shortfall. Applied in three places:

- the figure's definition (`src/tearsheet/extract/items.yaml`) and prompt rule 11, so prompt
  `extract-v3` (otherwise as v2; v1 and v2 kept with their recorded answers);
- the answer key's IAG lines, which now read IAG's "total committed and undrawn general and
  overdraft facilities": 2,629m (end 2025, unchanged, as IAG had no aircraft facilities then),
  3,400m (end 2024, was 3,534m with 134m of aircraft facilities) and 4,412m (end 2023, was
  4,787m with 375m);
- liquidity and liquidity to revenue, which add the figure to cash.

This changes IAG's total liquidity from IAG's own definition (which includes aircraft
facilities) at end 2023 and 2024; at end 2025 both are 10,948m.

**Air France-KLM end 2024 is not settled by this choice.** Both of its figures are
general-purpose: "2,5 milliards d'euros de lignes de crédit non tirées" and the two revolving
credit facilities of €1,405m and €1,000m (€2,405m). The key keeps the total as printed
(€2.5bn); the AI's €2,405m stays unverified and in the review queue.

**The v3 run** (41 reports, about 516,000 tokens). Answer key: **0 of 71 wrong values
verified**; verified and correct: blind 18 of 23 (78%), held-out 18 of 23 (78%), all 56 of 71
(79%). Unverified figures: 50 of 50 listed. Of the blind set's three extra figures, one comes
from the definition (IAG end 2023) and two from the AI answering differently with an almost
identical prompt: row labels quoted without their numbers fell from 16 answers (v2) to 5 (v3).
Run-to-run variation of the model is therefore about two or three key lines; the 78% sits
within it, just below the target.

**M3 closed on the safety result.** The 80% target is not met: 78% on the blind set (decision 0014,
`docs/m3/answer_key_score.md`). Imane closes M3 because no wrong figure is verified and every
unverified figure is listed for review; the 80% becomes a tracked goal in M4, measured on a
fresh blind set, not a gate. Known causes to work on, all recorded in decision 0014: the v2
wording that makes the AI quote row labels without their numbers, the figure's name sitting
outside the quote, comparatives without brackets, and the part-year hedge check reading the
neighbouring column.
