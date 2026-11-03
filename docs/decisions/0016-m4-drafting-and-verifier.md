# 0016 · M4: how the AI drafts, and what the verifier checks

Date: 2026-11-03 · Status: accepted (M4 plan approved by Imane; choices below made while
building, for her review)

**The fact sheet** (`src/tearsheet/narrative/factsheet.py`) is all the AI may talk about. Each
figure has an id: `net_leverage@FY2025`, `net_leverage@FY2024`, `net_leverage.change@FY2025`,
`net_leverage.peer_median@2025`, `net_leverage.peer_rank@2025`. Choices:

- **Verified only.** Unverified, missing and not-meaningful figures are listed under "not
  available, do not discuss" with their reason. A peer median or rank is withheld if any peer's
  value is unverified, so the comparison never rests on a figure Imane hasn't approved.
- **Peer group:** the company's own group (network, low-cost, airports), not "all airlines".
- **Directions:** up, down or flat against the approved thresholds, now in `catalog.yaml`;
  better or worse from "higher is better". Fleet age (years, not in the approved list) uses
  the 2% of amounts and traffic. Against peers: above, below or in line with the median, with
  the same threshold.
- **Changes print without a sign** ("0.17x", "2.2 points", "4.9%"): the AI's own verb carries
  the direction, and the verifier checks it. Changes in multiples and percentages are
  computed from the two levels as printed, so the page adds up (1.88x to 1.71x is "0.17x",
  even if the stored values differ by 0.165). A percentage change is not given when either
  year is negative or zero; the direction still is.
- **Statement lines** offered besides the catalog metrics: revenue, operating profit, profit,
  contract liabilities and undrawn facilities (`config/narrative.yaml`).

**The form.** For each sentence: the text with `{{id}}` blanks, and for each id the claims
the sentence makes: `up`, `down`, `flat`, `better`, `worse`, `above_peers`, `below_peers`,
`in_line_with_peers`, `better_than_peers`, `worse_than_peers`, `best_in_group`,
`worst_in_group`. Sentence counts per section are in `config/narrative.yaml` (snapshot exactly
three, others two to five).

**The verifier** (`verifier.py`, word lists in `vocabulary.yaml`): the plan's five rules, plus
the form's shape. How rule 4 reads a sentence:

- It splits the sentence into clauses (commas, colons, semicolons, "and", "while", "but"...)
  and requires each direction word to be backed by a matching claim on a figure of the same
  clause, or on another figure of the same metric in the sentence ("FCF to debt rose to
  {{a}}, below the median of {{b}}": "below" may rest on {{a}}).
- A clause with no blank borrows the claims of the whole sentence. This is the known soft
  spot: "earnings fell" in a sentence that also says the margin narrowed passes on the
  margin's claim. The words stay true to some figure of the sentence, never to nothing.
- A clause with no blank that states a scenario ("if bookings slow", "would", "could") is
  not read: it says nothing about a reported figure. A clause with a blank is always read, so
  "net leverage rose to {{x}} if leases are included" is still rejected.
- "Highest" and "lowest" must fit the metric: the lowest leverage is the best, the lowest
  margin the worst. "Last" counts as a rank word only as "ranks last" or "last in/of/among".

**Example notes.** I drafted two (IAG and Aena, FY2023: not drafted years, so the AI cannot
copy them) for Imane to rewrite (`docs/m4/example_notes.md`). Both pass the verifier.

**Retries.** Only the rejected sections go back, with the error list and the previous text,
up to two times. A section still rejected is kept, flagged "needs manual editing", and never
shown as finished. A section the AI leaves out of a retry keeps its previous version (bug
found in the v2 run).

**Gate 2, as counted.** Drafting order: the latest year of all nine companies, then the year
before; a draft counts if it passes the verifier after retries with no number outside a blank
(Imane's choice 4). Ten in a row then always cover all nine companies.

## Three prompt versions

| Prompt | Run | Passed after retries | First try | Tokens |
| --- | --- | --- | --- | --- |
| draft-v1 | Air France-KLM only, as a first test | 0 of 2 | 0 | 90,000 |
| draft-v2 | all 18 drafts | 6 of 18 | 0 | 699,000 |
| draft-v3 | all 18 drafts | **17 of 18** | 3 | 513,000 |

- **v1 → v2.** The AI called a first rank "the highest" for advance ticket cover, where lower
  is better, and claimed "worse" (year on year) where it meant "worse than peers". v2 explains
  both. The verifier then also accepted a peer claim on the company's figure for the same
  metric (it had wrongly rejected "FCF to debt of {{a}}, below the median of {{b}}").
- **v2 → v3.** In v2 no number ever got past the verifier, but most rejections were direction
  words about figures not in the sentence ("earnings growth", "as costs rose") and "up" on a
  figure the fact sheet calls flat. v3 says so explicitly. The verifier stopped reading
  scenario clauses with no blank. Both are changes made after seeing the v2 drafts; the
  adversarial suite was extended at the same time and is still rejected in full.
- **v3 result.** Gate 2 passed: drafts 1 to 10 (nine companies' latest year, then Air
  France-KLM FY2024) all pass; 17 of 18 overall. The one left, IAG FY2024, has a watch item
  calling undrawn facilities "a weaker buffer" without the claim; it is flagged for editing.
  No final draft of any run has a number outside a blank.
- **After extraction v4** (decision 0017) the fact sheets of ten drafts changed, so those were
  redrafted with the same prompt: still 17 of 18, gate 2 still passed (drafts 1 to 10), now 5
  at the first try.
- **Tokens:** about 1.55 million in all (1.3 million for the three versions, 240,000 for the
  redraft), against about 300,000 planned. Retries resend the full fact sheet, and two full
  runs were needed. All answers are recorded: replaying costs nothing.
