# M4 plan: the AI drafts the commentary, code writes every number

Status: **proposed, waiting for Imane's approval** (2026-11-03). No M4 code is written until then.

## What M4 is for

M1 to M3 built the numbers: tagged figures, ratios, peers and the operating figures read from
the reports. M4 turns them into the commentary of the tearsheet, the six sections a credit
analyst would write. The rule from the spec holds throughout: **the AI never writes a number.**
It writes sentences with labelled blanks, such as "net leverage fell to {{net_leverage@FY2025}}",
and code fills each blank from the facts database. Think of the AI as the writer of a template
letter and the code as the mail merge: the AI chooses the words, the code supplies every
figure, and a checker reads the letter before it goes out.

## What gets drafted

Six sections per company and year (spec): snapshot (three sentences), credit metrics,
operating performance, liquidity and funding, peer positioning, watch items. **The analyst
view is never drafted**: it stays an empty box for you.

## How it works, step by step

1. **Fact sheet (code).** For one company and year, code gathers what the AI may talk about:
   each metric this year and last year, the change and its direction, the peer median and the
   company's rank, the operating figures, and the reason for anything missing. Each item has an
   id, like `net_leverage@FY2025`, `net_leverage.change@FY2025` or
   `net_leverage.peer_median@2025`. **Only verified figures go in.** Anything unverified or
   missing is listed as "not available, do not discuss", so the AI cannot build a sentence on
   a figure you haven't approved.
2. **Direction computed by code, not the AI.** "Up", "down" or "flat" comes from a threshold per
   metric (question 3), and whether that is better or worse comes from the catalog's
   "higher is better" flag. For example net leverage from 1.71x to 1.62x is "down, better".
3. **Drafting through a form (tool use).** The AI fills one form per tearsheet: for each
   section, a list of sentences, each with its text (blanks only, no digits), the ids it uses,
   and the direction it claims for each one. Your two example notes are shown to it as models
   of the house style (question 1).
4. **The verifier (code).** A draft is rejected if any sentence has:
   1. a number written outside a blank (digits, "%", "x", "bn", or number words such as
      "doubled", "a third"); fiscal-year labels ("FY2025"), years and names such as "IFRS 16"
      or "A321neo" are allowed;
   2. a blank whose id is not in the fact sheet, or points to a figure not available;
   3. a claimed direction that contradicts the computed one ("improved" when it got worse);
   4. direction words in the prose ("rose", "fell", "strengthened") that contradict the
      claimed direction, so the form and the sentence cannot disagree;
   5. ids listed in the form that the sentence doesn't use, or the reverse.
5. **Retries.** A rejected section goes back to the AI with the list of errors, up to two
   times (spec). After that it is kept, flagged "needs manual editing", and never shown as a
   finished draft.
6. **Rendering (code).** Blanks become formatted figures, the same way everywhere: 1.62x,
   18.3%, EUR 1.2bn, NOK 37.6bn, "down 0.09x", "up 1.2 points". Values stay stored with their
   decimals; rounding happens only here.
7. **Record.** Each draft is stored with the text with blanks, the rendered text, the model,
   the prompt version, a fingerprint of the input, the verifier's report and the retries. As in
   M3, identical inputs replay the recorded answer: rerunning costs nothing.

Until the web app (M5), drafts are written to `docs/m4/drafts/` (one page per company and
year), next to the fact sheet they were built from.

## How we know it works (the M4 checklist)

- [ ] **Adversarial suite 100% rejected.** About 30 deliberately bad drafts, written by hand,
      each with one fault: a raw number, a number in words, a made-up id, an id for an
      unverified figure, "improved" on a worsening metric, a prose verb contradicting the form,
      a peer rank claimed "first" when it's third... Every one must be rejected, and a set of
      correct drafts must all pass (so the verifier is not simply rejecting everything).
- [ ] **Gate 2: ten consecutive drafts across companies with zero unreferenced numbers.** Ten
      real drafts in a row, covering all nine companies, each passing the verifier with no
      number outside a blank (after retries; I also report the first-try pass rate).
- [ ] **Commentary score of 4 or more.** You score ten drafts from 1 to 5 on accuracy,
      relevance, concision and credit insight, in a score sheet I prepare.

**Carried over from M3** (decision 0015): the extraction goal of 80% on a fresh blind set,
tracked here, not a gate. Plan: prompt `extract-v4` reverts v2's wording that made the AI quote
row labels without their numbers, plus code fixes for the four known miss types (the figure's
name in the sentence before, comparatives without brackets, part-year hedge words from the
neighbouring column, repeated numbers in a row). Judged on a fourth blind set from the FY2022
reports, written before any change. One extraction run, about 500,000 tokens.

## Order of work

1. Fact sheet builder and direction thresholds, with tests (no AI).
2. Renderer and verifier, with the adversarial suite and the correct drafts (no AI).
3. Drafting prompt, the form, few-shot examples, retries and records; the `drafts` and
   `runs` tables of the spec.
4. Drafts for all nine companies, latest two years (18 drafts, about 300,000 tokens); gate 2.
5. Score sheet for your ten-draft review.
6. The M3 carry-over (extraction v4 and the blind set), then walkthrough, decisions, checklist.

## Known difficulties

- **Missing figures.** Air France-KLM has no RASK or CASK (no group ASK printed), Norwegian
  no group ASK for 2025, airports no hedge ratio. The fact sheet says so, and the AI must not
  fill the gap; the verifier catches an id that doesn't exist.
- **Wording that implies a number.** "Doubled", "halved", "a record" or "the lowest in the
  group" are claims about figures. Number words are rejected; superlatives must come with
  the rank id from the peer table.
- **Different year ends.** easyJet (September) and Wizz Air (March) are compared on their own
  fiscal year, labelled with months, as in the peer tables.
- **Unverified figures waiting for your review** (50 today) are left out of the drafts, so the
  more you approve, the richer the commentary.

## Questions for Imane

1. **Example notes.** The spec has you write two example notes in your sell-side style, used to
   teach the AI the tone (about half a page each, on any two of the nine companies).
   Recommendation: you write them; if easier, I draft two from the fact sheets and you
   rewrite them in your own words.
2. **Language.** English only for v1, French later? (Open question in the spec.)
   Recommendation: English only.
3. **"Flat" thresholds.** Below these changes a metric is called stable. Proposed: leverage and
   coverage 0.1x; margins and other percentages 0.5 point; amounts and traffic 2%; unit
   revenues and costs 1%. Do these match how you would write it?
4. **Gate 2 rule.** Count a draft as passing after the AI's two retries (spec), or only at the
   first attempt? Recommendation: after retries, with the first-try rate reported.
5. **The M3 carry-over.** Include the extraction v4 round in M4 as planned (step 6), or leave it
   for after the web app? Recommendation: include it; it is small and the drafts benefit from
   more verified figures.

Working rule reminder: one milestone per session. Once you approve, I'd start building M4 in a
fresh session, on the branch `m4-drafting-verifier`.
