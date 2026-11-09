# 0018 · M4: the commentary score, done by Claude against the annual reports

Date: 2026-11-09 · Status: fixes A to D done (Imane: "go with A, B, C and D with ai writing the events
like in M3"); Vienna's deposits approved, removal rule confirmed, last round done (Imane:
"approve vienna figures, confirm removal rule, do the last round"); third score 3.70; a fourth
round with fixes 1 and 2 ("do one more round with fixes 1 and 2"): 3.75, below the pass mark

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

## Proposed fixes (round 1)

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

## What was done (round 2)

- **A. Data.** Flughafen Wien's short-term placements entered from the capital management
  note of each report (30.7m to 494.4m over 2021-2025); net debt now equals the company's
  printed net liquidity in every year (2025: 413.8m net cash). Stored unverified until Imane
  approves them. Finnair's coverage on finance costs (its cash flow prints interest paid net
  of interest received): 4.15x in 2024, 4.98x in 2025, improving. Revenue per passenger and
  non-aeronautical share not meaningful for ADP, Aena and Flughafen Wien (group revenue covers
  airports outside the passenger and segment scope). Golden files rebuilt after review.
- **B. Fact sheet.** Net cash given as a positive figure; ratios to debt left out below 0.5x
  gross leverage (and such a company left out of those peer medians); a company that is its
  group's median flagged. Peer ids end with the fiscal year like every other id (the AI kept
  writing them so). Rule 6: a figure from an earlier year, used on its own, names its year.
- **D. Events** read by the AI (prompt `events-v2`: the summary says only what the quote
  says) and checked by code: the quote is in the report word for word, title and summary hold
  no number; one retry rewrites wording rejected on numbers. 104 of 107 events checked over
  the 18 reports (`docs/m4/events.md`). A sentence cites an event by id. Code cannot check
  that an English summary is a fair reading of a French or German quote: in two of about
  twenty read, the summary added a detail (ADP tariffs, Vienna's "price-cap formula").
- **C. Prompt** `draft-v5` (v4 was run once and replaced): events, the point to watch from
  weak figures, net cash, the median company, one body section per figure.

**Changes to the verifier made along the way** (each with tests, the adversarial suite still
rejected in full, now 47 sentences):
- *Repetition is a style note, not a rejection.* As a rejection it flagged drafts for padding
  rather than for being wrong (v4 and v5 runs: 1 of 18 drafts passing). It is fed back on a
  retry, and a rewrite asked for style is kept only if it breaks no rule.
- *A clause with no blank that describes a cited event and names no figure* is not read for
  direction words ("Fitch upgraded the rating"); "strikes hit the year, and revenue fell" still
  is, because "revenue" names a figure.
- *Retries* show the sections already accepted, ask to rewrite only the failing sentences, and
  put back a sentence that passed before if a retry breaks it.
- *A sentence still breaking a rule after the two retries is removed* when its section keeps
  its minimum number of sentences, and shown as removed on the draft page; otherwise the
  section stays flagged, as before. This changes the plan's retry rule: nothing that broke a
  rule reaches the page, but a draft can be shorter. **Confirmed by Imane on 2026-11-09.**

**Gate 2 after the redraft:** 17 of 18 drafts pass (Finnair FY2024 flagged), 11 in a row
across all nine companies; 14 sentences removed in all, most of them causal side remarks
("as depreciation charges increased") with a direction word no figure of the sentence backs.
No number outside a blank on the page.

## Second score: 3.50 of 5

| Draft | Accuracy | Relevance | Concision | Insight | Average | Round 1 |
| --- | --- | --- | --- | --- | --- | --- |
| Air France-KLM FY2025 | 4 | 4 | 3 | 3 | 3.50 | 2.75 |
| IAG FY2025 | 4 | 4 | 3 | 4 | 3.75 | 3.25 |
| Finnair FY2025 | 4 | 4 | 4 | 4 | 4.00 | 2.25 |
| easyJet FY2025 | 4 | 4 | 3 | 4 | 3.75 | 3.50 |
| Groupe ADP FY2025 | 3 | 3 | 3 | 3 | 3.00 | 2.50 |
| Aena FY2025 | 4 | 3 | 4 | 3 | 3.50 | 3.25 |
| Flughafen Wien FY2025 | 3 | 3 | 3 | 3 | 3.00 | 1.75 |
| Norwegian FY2025 | 4 | 3 | 3 | 3 | 3.25 | 3.25 |
| Wizz Air FY2026 | 3 | 4 | 3 | 4 | 3.50 | 3.50 |
| Air France-KLM FY2024 | 4 | 4 | 3 | 4 | 3.75 | 3.25 |
| **Average** | 3.7 | 3.6 | 3.2 | 3.5 | **3.50** | 2.93 |

The three wrong figures are gone and the year's story is there (Finnair's strikes, Wizz Air's
grounded aircraft, IAG's buyback, Air France-KLM's hybrid redemption). What keeps the score
below 4:
- **Figures waiting for Imane's review**: Vienna's liquidity (the AI then wrote that it was
  "not disclosed in the fact base"), Air France-KLM's undrawn lines (liquidity judged on cash
  only), Aena's 2025 passengers (traffic only for 2024).
- **Reasoning the verifier cannot check**: Wizz Air's operating profit "absorbed by interest
  charges" (interest sits below operating profit); Norwegian's best-in-group advance ticket
  cover listed as a watch item.
- **Concision**: peer sections that list ranks one after another, some figures restated.
- **Event choice and wording** for ADP (minor events; one summary adds a detail).

Tokens: about 6.0 million for M4 AI calls in all (drafts, events, extraction v4).

## Last round (round 3)

- **Vienna's five deposit figures approved by Imane** (2026-11-09): its net cash and liquidity
  are now verified and in the fact sheets.
- **Prompt `draft-v6`**: peer positioning in two or three sentences, a rank only for a first
  or last place; a move explained only by a figure or event of the sentence, in the order of
  the income statement; never a word on the fact sheet or missing data; cash liquidity never
  called the company's liquidity; watch items only on weak figures or events.
- **A score now names the prompt version** as well as the fact sheet fingerprint: seven fact
  sheets were unchanged since round 2, so the fingerprint alone would have kept round 2's
  scores on round 3's texts.
- **Gate 2:** 17 of 18 drafts pass, 17 in a row across all nine companies; 16 sentences
  removed after two retries; no number outside a blank on the page.

| Draft | Accuracy | Relevance | Concision | Insight | Round 3 | Round 2 | Round 1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Air France-KLM FY2025 | 4 | 4 | 3 | 4 | 3.75 | 3.50 | 2.75 |
| IAG FY2025 | 4 | 4 | 4 | 4 | 4.00 | 3.75 | 3.25 |
| Finnair FY2025 | 4 | 4 | 4 | 4 | 4.00 | 4.00 | 2.25 |
| easyJet FY2025 | 4 | 4 | 3 | 4 | 3.75 | 3.75 | 3.50 |
| Groupe ADP FY2025 | 3 | 3 | 3 | 4 | 3.25 | 3.00 | 2.50 |
| Aena FY2025 | 4 | 3 | 4 | 3 | 3.50 | 3.50 | 3.25 |
| Flughafen Wien FY2025 | 4 | 4 | 3 | 4 | 3.75 | 3.00 | 1.75 |
| Norwegian FY2025 | 4 | 3 | 3 | 3 | 3.25 | 3.25 | 3.25 |
| Wizz Air FY2026 | 4 | 4 | 4 | 4 | 4.00 | 3.50 | 3.50 |
| Air France-KLM FY2024 | 4 | 4 | 3 | 4 | 3.75 | 3.75 | 3.25 |
| **Average** | 3.9 | 3.7 | 3.4 | 3.8 | **3.70** | 3.50 | 2.93 |

**Still below 4.** Accuracy is now 4 everywhere but ADP. What remains, with its cause:
- **The same figure under two names** (four drafts: "cash fell 7.5% to NOK 10.1bn, so cash
  liquidity fell 7.5% to NOK 10.1bn"): cash and cash-like investments and cash liquidity are
  equal when there are no undrawn lines, and the fact sheet offers both. A fact sheet fix.
- **A name the verifier does not know**: "Boeing 737-800" (the allowed names stop at
  "737-8"), so Norwegian's sentence on buying its leased aircraft, the reason for its capex
  jump, was removed. A one-line fix.
- **Figures waiting for Imane's review**: Air France-KLM's undrawn lines, Aena's 2025
  passengers (53 figures in the M3 review queue).
- **Event choice**: ADP's events come from the consolidated statements only (minor items such
  as a Turkish tax dispute); one tariff sentence still adds a detail its quote does not hold.
- **Peer sentences** that still list ranks in three drafts.

Tokens: about 6.8 million for M4 AI calls in all.

## Round 4: one name per figure, "737-800" allowed

- **The same figure under two names**: cash liquidity equals cash and cash-like investments
  whenever no undrawn lines are added (always, by definition), so the fact sheet now offers
  it once (`same_figure` in `config/narrative.yaml`). The doubled sentences are gone.
- **"Boeing 737-800"** and the like are allowed names; Norwegian's sentence on buying its
  leased 737-800s stays.
- **Gate 2:** 17 of 18 drafts, 17 in a row across all nine companies; 8 sentences removed (16
  before); no number outside a blank.

| Draft | Round 4 | Round 3 | Round 2 | Round 1 |
| --- | --- | --- | --- | --- |
| Air France-KLM FY2025 | 4.00 | 3.75 | 3.50 | 2.75 |
| IAG FY2025 | 3.50 | 4.00 | 3.75 | 3.25 |
| Finnair FY2025 | 4.00 | 4.00 | 4.00 | 2.25 |
| easyJet FY2025 | 3.75 | 3.75 | 3.75 | 3.50 |
| Groupe ADP FY2025 | 3.50 | 3.25 | 3.00 | 2.50 |
| Aena FY2025 | 3.75 | 3.50 | 3.50 | 3.25 |
| Flughafen Wien FY2025 | 3.75 | 3.75 | 3.00 | 1.75 |
| Norwegian FY2025 | 3.50 | 3.25 | 3.25 | 3.25 |
| Wizz Air FY2026 | 4.00 | 4.00 | 3.50 | 3.50 |
| Air France-KLM FY2024 | 3.75 | 3.75 | 3.75 | 3.25 |
| **Average** | **3.75** | 3.70 | 3.50 | 2.93 |

By criterion: accuracy 3.9, relevance 3.8, concision 3.5, credit insight 3.8.

**Why it stops at 3.75.** The two fixes did what they were for, but each redraft is a new
throw of the dice: this time IAG lost its traffic sentence (removed for writing "broadly
unchanged ... up") and Wizz Air again lost its explanation of operating profit (depreciation
is not a fact-sheet figure, so "as depreciation increased" is refused). What remains:
- **Things the fact sheet cannot say**: depreciation, causes in general. The verifier refuses
  direction words it cannot check, so the AI's best explanations are sometimes removed.
- **Figures waiting for Imane's review** (Air France-KLM's undrawn lines, Aena's 2025
  passengers).
- **ADP**: event summaries that add a detail, minor events from the statements only.
- **Peer sentences** that still list ranks or compare a company with itself as the median.

Tokens: about 7.6 million for M4 AI calls in all.
