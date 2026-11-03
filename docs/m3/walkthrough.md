# M3 walkthrough: reading the operating figures, and proving each one

**What M3 built.** A reader for the figures the tagged statements don't carry: passengers,
ASK, RPK, fleet, fuel hedging, undrawn credit lines and airport aeronautical revenue. The AI
does the reading; code does the checking. Think of the AI as a junior analyst who must staple
a photocopy of the page to every figure, and the code as the reviewer who checks the photocopy
against the original report before the figure goes into the model.

## How it works

1. **The report as text.** Each filing's annual report (and your two 2025 PDFs) is turned into
   plain text, page by page.
2. **The right pages only.** Code picks the passages around words such as "available seat
   kilometres", "sièges-kilomètres offerts", "undrawn", "hedged". The AI sees a few pages, not
   the whole 300-page report.
3. **A form, not free text.** The AI (DeepSeek) fills a fixed form: figure, year, number as
   printed, the exact sentence or table row, the page. Or "not found".
4. **The checks.** A figure is **verified** only if code confirms: the quote is in the report
   word for word; it is about that figure; the number, its scale (million, thousand) and
   currency are printed there; it belongs to the right year, not the comparative in brackets;
   it is plausible; it agrees with the next year's report; RPK ÷ ASK matches the printed load
   factor. Anything else is **unverified**: kept off the tearsheet, marked \*, and listed for
   you with the quote and the reason (decision 0010).
5. **Your review.** You approve or correct an unverified figure in
   `config/extraction_reviews.yaml` (the file explains how); a correction is kept with your
   name, date and reason.

## Status: M3 closed on the safety result (decision 0015)

You chose general-purpose credit lines only and to close M3 on the safety result. The final run
(prompt `extract-v3`, which adds only that definition) gives:

| Test | First 25 | Held-out 23 | Blind 23 | All 71 | |
| --- | --- | --- | --- | --- | --- |
| No wrong value marked verified | 0 | 0 | 0 | **0** | ✓ |
| At least 80% verified automatically | 20 (80%) | 18 (78%) | **18 (78%)** | 56 (79%) | waived, goal for M4 |
| Every unverified value visibly flagged | | | | 50 of 50 | ✓ |

- **228 figures read, 178 verified (78%), 50 waiting for your review** in
  `docs/m3/extractions.md`; every line the AI wrote is in `docs/m3/extractions.csv`.
- **The model varies from run to run.** With almost the same instructions, v2 and v3 differ by
  about three answer-key figures: the "label without its number" quotes fell from 16 to 5. So
  78% and 80% are, in practice, the same result; M4 will measure on a fresh blind set.
- **Three runs**, about 500,000 tokens each; all answers are recorded (`records/llm/`), so a
  rerun costs nothing. DeepSeek serves our `deepseek-chat` setting with `deepseek-flash`. Add
  DeepSeek's price per million tokens in `config/models.yaml` to see the cost.
- **IAG liquidity** now counts general-purpose lines only: same as IAG's own figure at end 2025
  (€10,948m), lower at end 2023 and 2024, where IAG also counts aircraft-specific lines.
- **Air France-KLM end 2024** was not settled by the definition (both figures are
  general-purpose): the key keeps the printed €2.5bn, and the AI's €2,405m waits for your
  review.

The history below explains how we got here.

## The improvement round (decision 0014)

**What changed.** Prompt v2: copy the header line that holds the years; a new "caption" field
for the table's title or unit line (accepted only from the quote's page or the page before);
the hedge ratio defined in the prompt; a scope printed in parts recorded as components and
added up by code. Then two reading bugs in our checks, found on held-out lines and fixed only
after the blind set was written: headers that repeat the years over each measure, and icon
characters in the report's text.

**What it did.**
- **The score didn't move.** The AI followed most of the new rules, but the gains were eaten by
  a regression in my wording (below) and by the checks' strictness on other cases. On lines
  it was never tuned on, the final code verifies 15 of 23 (65%).
- **The one wrong verified value is a definition question, not a misreading.** IAG at end
  2023: the tool kept €4,412m of general-purpose facilities; the key has IAG's "in total"
  €4,787m, which adds €375m of facilities tied to specific aircraft deliveries. The same
  question arises at end 2024 (€3,400m vs €3,534m), where the figure was held back.
- **A regression in v2's wording.** I added "a table row includes its label, never the numbers
  alone"; the AI often took it as "give the label only". 16 answers quote a label without its
  number, against 1 in the first run. The checks refuse them all (no harm), but figures are
  lost: Wizz Air's FY2024 column is now empty.
- **The caption field helped the airports**: Aena 12 of 15 figures verified, against 3.

**What the blind misses are** (all stay unverified, none reaches the tearsheet):
- the figure's name sits outside the quote (easyJet: "This amounted to £1.8 billion", "undrawn"
  is in the sentence before; Finnair: the column names are a header line of their own);
- a comparative without brackets ("87 aircraft at year-end, up from 70 aircraft at year-end
  2022" is tied to 2022);
- our part-year hedge check is too broad (Wizz Air's 12-month column is refused because the
  next column says "6 months");
- equal numbers in a row with no year (IAG "ASKs (millions) 323,111 323,111");
- one AI miss (IAG's "115.6 million passengers" in an infographic).

I stopped here on purpose: each fix so far has uncovered the next layer, and fixing these now
would leave no clean set to judge the result.

## What the first run taught us (decision 0013, earlier)

I went through every figure the checks had passed, not only the answer key. That review found
two weaknesses the answer key could not see, and two reading errors in our own checks.

- **Hedge ratios: five of the seven verified were wrong by definition.** Finnair's "8 per cent
  … for the first six months of 2022" had passed as the twelve-month hedge, and once the AI's
  quote even stopped at "for the first", leaving out "six months". In Air France-KLM's 2022
  table, the AI took the 2022 column (73%, the year just ended) instead of 2023 (51%, the year
  ahead). Like reading a swap's notional for the wrong period. The checks now refuse part-year
  hedges, read the report to the end of the sentence, and require next year's column. Two
  remain verified: Norwegian 2022 (15% of 2023 fuel) and 2023 (50% of 2024).
- **A bare number is not evidence.** ADP's 2025 passengers were "verified" on the quote
  "107,0" alone. It is almost certainly Paris (103.4m × 1.034), but the quote can't show whose
  row it is. A quote must now contain the row's words.
- **IAG's passenger row was read one column off**, because "‘000" (thousands) after the label
  was taken for a number. Fixed; IAG's 121.6m passengers now verify.
- **easyJet and Wizz Air define load factor as seats sold ÷ seats offered** (easyJet: 93.4m
  passengers ÷ 104.0m seats = 89.8%), not RPK ÷ ASK (90.8%). The RPK ÷ ASK check doesn't apply
  to them; it is now skipped for those two, with the evidence in `config/extraction.yaml`.

Before these fixes the score was 14 of 25 (56%). Two of the fixes were found on answer-key
figures, so the 76% is a little flattered; the hedge fixes only take figures away.

## What we found

**By company** (latest year, second run):

- **easyJet and Wizz Air read cleanly**: 37 of 39 and 34 of 36 figures verified, five years of
  passengers, ASK, RPK and fleet. Wizz Air FY2026: 69.7m passengers, 132.0bn ASK, 262 aircraft.
- **IAG**: traffic, fleet and credit lines verified. Total liquidity comes to €10,948m for
  2025, the same as IAG's own figure (€8,319m cash + €2,629m undrawn lines).
- **Air France-KLM doesn't print group ASK or RPK**, only per business (Réseaux, Transavia),
  and the AI rightly refused to add them up. So RASK, CASK and yield stay empty for Air
  France-KLM. Your FY2025 PDF holds the financial statements only, so FY2025 has no traffic.
- **Norwegian prints ASK and RPK per airline** (Norwegian, Widerøe), not for the group, so
  group ASK is missing from FY2025.
- **Finnair's report text is badly scrambled** ("tr affic capac ity"): passengers, fleet (now
  all 79 aircraft flown for Finnair) and credit lines verify; most traffic waits for review.
- **Airports**: passengers mostly verified (ADP 103.4m for 2024, Paris only; Aena 321.6m for
  2025, Spain only; Flughafen Wien 32.6m, Vienna only). ADP's 2025 figure (107.0m) waits for
  review: in the PDF it sits in a jumbled list of airports.

**Peer view, 2025.** Load factor: IAG 85.6%, Finnair 76.9%\*. Liquidity to revenue: Finnair
40.6%, IAG 33.0%, Air France-KLM 28.1%\*. Low-cost 2024: easyJet 90.8% (RPK ÷ ASK), Wizz Air
91.3%, Norwegian 84.3%\*.

## Next steps for you

1. **Spot-check the answer key**: five lines of `docs/m3/answer_key.csv` (about ten
   minutes): search the report for the text in the `snippet` column.
2. **Review queue**: 50 figures in `docs/m3/extractions.md`, newest years first. Approve or
   correct them in `config/extraction_reviews.yaml` (the file explains how).

## How to rerun

```bash
uv run tearsheet all --offline
```

replays the recorded answers (no cost) and rebuilds every report. `uv run tearsheet extract`
asks the AI only for reports it has not read yet. `uv run python -m spikes.m3.answer_key`
rebuilds the answer key.
