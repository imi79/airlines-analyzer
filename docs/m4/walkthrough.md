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
| Extraction 80% on a fresh blind set (tracked, not a gate) | Not started | next |

- **No number ever got past the checker.** In all three runs (54 drafts), no final draft has
  a figure written by the AI.
- **First tries are rarely clean**: 3 of 18 pass at once; the retries fix the rest. The usual
  first-try faults are a direction word about something not in the sentence ("as costs
  rose"), and "up" or "down" on a move the thresholds call flat.
- **The checker caught real errors**, not only style: it refused "the highest in the group" for
  Air France-KLM's advance ticket cover (ranked 1st because it is the *lowest*, lower being
  better), and "worse" where the figure improved over the year but trails peers.
- **One draft needs editing**: IAG FY2024 calls undrawn facilities "a weaker buffer" without
  backing it. That is how it should work: flagged, not published.
- **It took three versions of the instructions** (decision 0016) and about 1.3 million
  tokens, against 300,000 planned: retries resend the whole fact sheet, and two full runs were
  needed. Every answer is recorded, so a rerun costs nothing.

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

Then the M3 carry-over (extraction v4 on a fresh FY2022 blind set) closes M4.

## How to rerun

```bash
uv run tearsheet all --offline
```

rebuilds everything from the cache and the recorded AI answers (no cost), drafts included.
`uv run tearsheet draft` asks the AI only for drafts not yet recorded.
