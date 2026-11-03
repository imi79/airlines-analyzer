# 0017 · M4: the M3 carry-over, extraction v4 on a fourth blind set

Date: 2026-11-03 · Status: accepted; goal closed by Imane on the safety result ("close the 80%
goal on the safety result")

**Keeping the test fair.** A fourth answer-key set was written first, from the FY2022 reports
of IAG, Finnair, easyJet, Norwegian and Wizz Air (22 lines, same rule as before: a figure
printed as one number on the scope wanted), and committed before any change. Air France-KLM's
FY2022 report had already given held-out lines. The lines left out, with their reasons, are
listed in `spikes/m3/answer_key.py`. One line's outcome was known beforehand: Norwegian's 2022
hedge (15% of 2023 fuel), already discussed in decision 0013.

**What changed** (all from the miss types recorded in decision 0014, not from the new lines):

1. Prompt `extract-v4`: a table row is copied whole, "the label at its start and every number
   in it". v2's wording ("never the numbers alone") had led the AI to quote labels without
   their numbers.
2. The figure's name in the sentence before: a quote starting with a pointing word ("This
   amounted to £1.8 billion") may take the figure's name from the report's sentence just
   before it. Only after a pointing word (this, these, it, which...), so a quote cut at random
   does not borrow a name.
3. Comparatives without brackets: in "87 aircraft at year-end, up from 70 aircraft at year-end
   2022", the year after "up from" (or "compared with", "frente a", "contre"...) belongs to the
   70, not the 87.
4. Hedge tables with a period per column ("12 months 6 months", then "56 % 14 %"): the value's
   own column decides; a twelve-month column is no longer refused for its neighbour's "6
   months". If periods and values don't pair up, the old rule applies.
5. A value printed twice at the start of a row ("ASKs (millions) 323,111 323,111 263,592": as
   reported and before exceptional items) is taken as the report's own year. Only the first
   values, only when equal as printed.

## Result

| | First (25) | Held-out (23) | Blind (23) | **Fourth (22)** | All (93) | Wrong verified |
| --- | --- | --- | --- | --- | --- | --- |
| extract-v3, before the changes | 20 | 18 | 18 | **13 (59%)** | 69 | 0 |
| extract-v3 answers, new checks | 20 | 18 | 20 | **13 (59%)** | 71 | 0 |
| extract-v4, new checks | 20 | 17 | 20 | **13 (59%)** | 70 | 0 |

- **The 80% goal is not met on the fresh set: 13 of 22 (59%).** Safety holds: no wrong value
  verified on any of the 93 lines.
- **The check changes work on the cases they were written for** (blind set 18 to 20: Norwegian's
  87 aircraft, Wizz Air's 56% hedge; also Aena's passengers, "frente a"), but the fresh set's
  misses are of other kinds.
- **What the fourth set's misses are:** long tables with no year in the row (Norwegian's
  ten-year summary, Finnair's traffic table with years and column names interleaved: five
  lines), a fleet printed in two parts beside similar numbers (Finnair), two figures the AI
  did not find (IAG's fleet, Wizz Air's twelve-month hedge), and one figure held back because
  the next report restates it (Wizz Air's capacity, 55.79bn vs 55.66bn). None is a wrong value.
- **The new prompt did not change the score**: extract-v4 is within the model's run-to-run
  variation of v3 (decision 0015: two or three lines). It is kept, as planned.
- **Cost:** about 517,000 tokens for the run, as planned. Ten drafts' fact sheets changed
  (more or fewer verified figures), so they were redrafted (about 240,000 tokens; a draft is
  tied to its fact sheet's fingerprint): gate 2 still passes, 17 of 18 drafts.

**Not done, on purpose.** Fixing the fourth set's misses now would tune on the only clean set
left. If the goal is ever reopened, a new round should start with a fifth set (FY2021 reports)
and target long tables: read the row against a summary table's own year header, or prefer the
report's sentence when both exist.

**Closed on the safety result.** Imane closes the 80% goal as she did for M3 (decision 0015):
no wrong value is verified on any of the 93 answer-key lines, and every unverified figure
stays off the tearsheet and is listed for her review (53 today). The share verified
automatically (59% on the fourth set, 75% on all lines) is a matter of convenience, not of
correctness: what the checks don't verify waits for her, it is never published unchecked. The
goal is no longer tracked; extraction stays as it is (prompt extract-v4, the checks of this
note).
