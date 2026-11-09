# M4 walkthrough: the AI writes the words, code writes every number

**What M4 builds.** The commentary of the tearsheet: snapshot, credit metrics, operating
performance, liquidity and funding, peer positioning, watch items. The analyst view is never
drafted. Think of a template letter and a mail merge: the AI chooses the words and leaves a
labelled blank wherever a figure goes ("net leverage fell to {{net_leverage@FY2025}}"); code
fills each blank from the verified figures; and a checker reads every sentence before it goes
out.

## How it works

1. **Fact sheet.** For each company and year, code lists the figures the AI may use: this
   year, last year, the change, the peer median and the rank, each with a label. Only figures
   that are verified (or approved by you) go in. Everything else is listed as "not available,
   do not discuss", with the reason. Example: `docs/m4/factsheets/afkl_FY2025.md`.
2. **Directions are computed by code.** Up, down or flat against your thresholds (0.1x, half
   a point, 2% for amounts and traffic, 1% for unit revenue and cost), and better or worse
   from the catalog's "higher is better". Net leverage from 1.88x to 1.71x: "down, better".
3. **A form, not free text.** For each sentence the AI fills in the text with blanks and, for
   each figure, the claim it makes: up, down, better, below peers, best in the group...
4. **The verifier rejects** a sentence with: a number outside a blank (digits, "%", "bn",
   "doubled", "a third", "record"); a blank that isn't in the fact sheet or isn't verified;
   a claim that contradicts the computed direction; a direction word ("rose", "improved",
   "lowest") that the form doesn't back; figures listed but not used, or the reverse.
5. **Two retries.** A rejected section goes back to the AI with the errors. Still wrong after
   two retries: kept, flagged "needs manual editing", never shown as finished.
6. **Code prints every figure** the same way: 1.71x, 15.3%, EUR 5.1bn, NOK 37.6bn, 8.45 euro
   cents, "2nd of 3".

## Results

| M4 checklist | Result | |
| --- | --- | --- |
| Adversarial suite 100% rejected | 43 of 43 bad sentences rejected, each for the right reason; 13 correct but risky sentences and a full correct draft pass | ✓ |
| Gate 2: ten drafts in a row, all nine companies, no unreferenced number | Drafts 1 to 10 all pass; 17 of 18 overall | ✓ |
| Commentary score of 4 or more | Waiting for your scores (`docs/m4/score_sheet.xlsx`) | to do |
| Extraction 80% on a fresh blind set (tracked, not a gate) | 13 of 22 (59%) on the new FY2022 set; still no wrong figure verified | not met |

- **No number ever got past the checker.** In all three runs (54 drafts), no final draft has
  a figure written by the AI.
- **First tries are rarely clean**: 5 of 18 pass at once; the retries fix the rest. The usual
  first-try faults are a direction word about something not in the sentence ("as costs
  rose"), and "up" or "down" on a move the thresholds call flat.
- **The checker caught real errors**, not only style: it refused "the highest in the group" for
  Air France-KLM's advance ticket cover (ranked 1st because it is the *lowest*, lower being
  better), and "worse" where the figure improved over the year but trails peers.
- **One draft needs editing**: IAG FY2024 calls undrawn facilities "a weaker buffer" without
  backing it. That is how it should work: flagged, not published.
- **It took three versions of the instructions** (decision 0016) and about 1.55 million
  tokens, against 300,000 planned: retries resend the whole fact sheet, two full runs were
  needed, and ten drafts were redone after extraction v4 changed their figures. Every answer
  is recorded, so a rerun costs nothing.

**A reading tip.** Each draft page (`docs/m4/drafts/`) shows the text as printed, then each
try with the checker's errors, then the text with blanks as the AI wrote it. The summary with
gate 2 is `docs/m4/drafts.md`.

**Known soft spot.** A clause with no figure borrows the claims of the rest of its sentence:
"earnings fell" passes if the same sentence says the margin narrowed. The words always agree
with some figure in the sentence, but not necessarily the one they name. Your scoring will
show whether this matters in practice.

## Next steps for you

1. **Score ten drafts** in `docs/m4/score_sheet.xlsx` (yellow cells, 1 to 5, about 30
   minutes): accuracy, relevance, concision, credit insight. Each draft is printed on its own
   tab. The pass mark is an average of 4.
2. **Rewrite the two example notes** in your own words (`docs/m4/example_notes.md`, plain text
   is fine). They teach the AI your style; I will put them back into the form.

## The M3 carry-over: extraction v4 (decision 0017)

The goal was 80% of figures verified automatically on lines never used for tuning. To keep it
fair, I first read 22 figures from the FY2022 reports by code (no AI) and committed them, then
made the planned changes: clearer instructions on copying table rows, and four check fixes
for the misses seen in M3 ("This amounted to £1.8 billion", "up from 70 aircraft at year-end
2022", a hedge table with a 12-month and a 6-month column, a number printed twice in a row).

- **Result: 13 of 22 (59%), unchanged.** The fixes work on the cases they were written for
  (the earlier blind set rises from 18 to 20 of 23), but the new set fails for other reasons:
  long multi-year summary tables with no year in the row (Norwegian, Finnair), a fleet in two
  parts beside similar numbers, two figures the AI missed (IAG's fleet, Wizz Air's hedge),
  and one figure held back because the next report restates it.
- **Safety holds: 0 wrong figures verified on all 93 lines.** Every miss stays visibly
  unverified and waits for your review, as before.
- **Across all 41 reports:** 230 figures read, 177 verified; the review queue is now 53
  figures (`docs/m3/extractions.md`). Some drafts changed with their figures (for example
  Aena's passengers are now verified), so ten drafts were redone; gate 2 still passes.
- **I stopped there on purpose**: fixing these now would tune on the only clean set left. A
  further round would start with a fifth set (FY2021 reports) and target the long tables.

**Your decision (2026-11-03): goal closed on the safety result**, as for M3. No wrong figure
is verified; everything the checks don't verify waits for your review and stays off the
tearsheet. The goal is no longer tracked (decision 0017).

## The commentary score (decision 0018)

You asked me to check the drafts myself against the annual reports. I did, draft by draft, and
scored them strictly; the scores and a comment per draft are in the score sheet. Keep in mind I
am the same kind of model that wrote them, so this is not an independent review: change any
score you disagree with.

**Result: 2.93 of 5, below the pass mark of 4.** The figures the AI used are right, and the
checker kept every direction honest. What pulls the score down:

1. **Three wrong figures from earlier milestones**, which the drafts repeated faithfully:
   Flughafen Wien's cash misses about 360m of short-term deposits (the company reports net
   liquidity of 414m; the draft calls its liquidity the weakest of the group); Finnair's
   interest coverage uses interest paid *net of interest received*, so it "collapses" when on
   Finnair's own financial expenses it improved; ADP's revenue per passenger divides group
   revenue by Paris passengers only.
2. **The story of the year is missing**: Finnair's strikes, Wizz Air's grounded aircraft,
   IAG's 1.0bn buyback, easyJet holidays. The fact sheet holds figures only, by design.
3. **Habits**: liquidity named the point to watch by reflex (six of ten), figures repeated
   across sections, "in line with the median" when the company *is* the median.
4. **Negatives**: "net debt of GBP -602m" instead of "net cash of 602m".

**Your decision:** the fixes are listed in decision 0018. A to C are corrections within the
current design (data, wording, prompt). D changes a rule of the plan: letting the drafts
mention the year's events, either from a list you write, or read from the report with a
quote that code checks. Tell me which you want, then I redraft the ten and we score again.

## After the fixes (decision 0018, round 2)

You chose fixes A to D, with the AI reading the year's events from the reports. What changed:

- **The three wrong figures are corrected.** Vienna's deposits are entered from its notes
  (its net cash now equals the company's own figure, €413.8m) and **wait for your approval**;
  Finnair's coverage now improves (4.15x to 4.98x); revenue per passenger is "not meaningful"
  for the three airports.
- **The year's story is in the notes**: the AI reads each report for events (strikes, grounded
  aircraft, buybacks, bond issues, rating changes), each with its exact quote, checked by
  code (`docs/m4/events.md`). Please read the quotes: code can't check that the English
  summary is a fair reading of a French or German quote, and two of about twenty I read add a
  detail.
- **Net cash** reads "net cash of GBP 602m"; figures from an earlier year say so.
- **A sentence that still breaks a rule after two retries is now removed** when its section
  can stand without it (14 sentences across 18 drafts, each shown on its draft page). Nothing
  that broke a rule reaches the page, but this changes the plan's retry rule: please confirm.

**Results.** Gate 2 still passes (11 drafts in a row, 17 of 18). The commentary score rises
from 2.93 to **3.50**, still below 4. What remains: figures waiting for your review (Vienna's
liquidity, Air France-KLM's undrawn lines, Aena's 2025 passengers), two reasoning slips the
checker can't see (Wizz Air's "interest charges" inside operating profit; Norwegian's best
figure listed as a watch item), peer sections that list ranks, and ADP's minor events.

**Your decisions:**
1. Approve Vienna's five entered deposit figures (`config/manual_figures.yaml`; each year's net
   cash matches the company's printed net liquidity).
2. Confirm or refuse the sentence-removal rule.
3. Then either a last round on concision and the watch point (about 800,000 tokens), or accept
   3.50 and close M4 on the safety result, as for the extraction goal.

## The last round (decision 0018, round 3)

With Vienna's figures approved and the removal rule confirmed, the instructions were tightened
(shorter peer sections, causes only from the sentence's own figures or events, no word on
missing data, watch items only on weak figures). **Gate 2 still passes** (17 drafts in a row);
**the score rises to 3.70**, with accuracy at 4 in nine drafts of ten. IAG, Finnair and Wizz
Air reach 4.0; Vienna goes from 1.75 in round 1 to 3.75.

What still separates 3.70 from 4, in order of ease:
1. **The same figure under two names** ("cash fell to EUR 2.0bn, so cash liquidity fell to
   EUR 2.0bn"): my fact sheet offers both when there are no undrawn lines. A fact sheet fix.
2. **"Boeing 737-800" unknown to the verifier**, which removed Norwegian's best sentence. A
   one-line fix.
3. **Your review queue**: Air France-KLM's undrawn lines and Aena's 2025 passengers are among
   the 53 figures waiting (`docs/m3/extractions.md`).
4. **ADP's events** come from its statements only (no annual report with the Paris story).

**Your decision:** close M4 at 3.70 on the safety result, as for the extraction goal, or one
more round with fixes 1 and 2 (about 800,000 tokens) and, ideally, the review of the queue.

## How to rerun

```bash
uv run tearsheet all --offline
```

rebuilds everything from the cache and the recorded AI answers (no cost), drafts included.
`uv run tearsheet draft` asks the AI only for drafts not yet recorded.
