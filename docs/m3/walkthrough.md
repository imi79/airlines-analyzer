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

## The run

- **41 reports read**, one request each: all nine companies, FY2021 to FY2025 (Wizz Air to
  FY2026). About 445,000 tokens sent and 54,000 received. The key you set works
  (`tearsheet llm-check`); DeepSeek serves our `deepseek-chat` setting with its model
  `deepseek-flash`. No price is entered in `config/models.yaml`, so the cost isn't computed:
  add DeepSeek's price per million tokens there and the report shows it.
- Every answer is recorded (`records/llm/`): rerunning costs nothing and gives the same result.
- **230 figures read, 155 verified (67%), 75 waiting for your review.** Full list:
  `docs/m3/extractions.md`; every line the AI wrote: `docs/m3/extractions.csv`.

## The M3 checklist, against the answer key

At your request the answer key was built by code, without AI (decision 0012): 25 figures for
the six airlines, each read from the report with the page and the text around it
(`docs/m3/answer_key.csv`). It was committed before the AI read anything.

| Test | Result | |
| --- | --- | --- |
| No wrong value marked verified | **0 of 25** | ✓ |
| At least 80% verified automatically | **19 of 25 (76%)** | ✗, 1 figure short |
| Every unverified value visibly flagged | **75 of 75** listed and marked \* | ✓ |

Full table: `docs/m3/answer_key_score.md`. The six misses:

| Figure | What happened | Safe? |
| --- | --- | --- |
| Air France-KLM undrawn lines FY2024 | AI: €2,405m (€1,405m + €1,000m, "non tirées"). Key: €2.5bn ("2,5 milliards… de lignes de crédit non tirées"). Left unverified | ✓ Yes. See question 2: the key may be the one that's off |
| Finnair ASK, RPK FY2025 | Right values, but Finnair's table has two header rows and the AI copied the one without the years; the scrambled text adds to it | ✓ Left unverified |
| Finnair fleet FY2025 | AI gave 55 (Finnair's own certificate); our scope is all 79 aircraft flown for Finnair (55 + 24 by Norra) | ✓ Left unverified |
| Norwegian fleet FY2025 | Right (146), but the sentence also gives 95 and 51 (the two airlines). A safety rule holds back a figure that has look-alikes and no year | ✓ Left unverified |
| Norwegian hedge FY2025 | The AI said "not found": it judged "45 percent… for 2026" not to be a twelve-month figure. Too cautious | ✓ Nothing shown |

## What the first run taught us (decision 0013)

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

**By company** (latest year):

- **easyJet and Wizz Air read cleanly**: 36 of 37 and 41 of 43 figures verified, five years of
  passengers, ASK, RPK and fleet. Wizz Air FY2026: 69.7m passengers, 132.0bn ASK, 262 aircraft.
- **IAG**: traffic, fleet and credit lines verified. Total liquidity comes to €10,948m for
  2025, the same as IAG's own figure (€8,319m cash + €2,629m undrawn lines).
- **Air France-KLM doesn't print group ASK or RPK**, only per business (Réseaux, Transavia),
  and the AI rightly refused to add them up. So RASK, CASK and yield stay empty for Air
  France-KLM. Your FY2025 PDF holds the financial statements only, so FY2025 has no traffic.
- **Norwegian prints ASK and RPK per airline** (Norwegian, Widerøe), not for the group, so
  group ASK is missing from FY2025. Its earlier years mix perimeters; worth a look in review.
- **Finnair's report text is badly scrambled** ("tr affic capac ity"): passengers and credit
  lines verify; most traffic figures wait for review.
- **Airports**: passengers are mostly verified (ADP 103.4m for 2024, Paris only; Flughafen Wien
  32.6m for 2025, Vienna only). ADP's 2025 figure (107.0m) waits for review: in the PDF the
  number sits in a jumbled list of airports, and the quote is the bare number. Aeronautical revenue mostly waits for review, because the caption "in thousands of
  euros" sits above the table, outside the row the AI quotes.

**Peer view, 2025.** Load factor: IAG 85.6%, Finnair 76.9%\*. Liquidity to revenue: Finnair
40.6%, IAG 33.0%, Air France-KLM 28.1%\*. Low-cost 2024: easyJet 90.8% (RPK ÷ ASK), Wizz Air
91.3%, Norwegian 84.3%\*.

## Questions for you

1. **The 80% target.** Two options:
   (a) **accept 76% for now** and close M3 on your review: the safety test, the one that
   matters for credit work, is passed;
   (b) **one improvement round** (recommended): a prompt v2 that asks for the header row that
   holds the years and units, and says "hedged for 2026" counts as next year. It costs one
   more run (about 500,000 tokens). To keep the test fair, I would add about 15 new key lines
   from FY2024 reports, built before the run, and score on those as well.
2. **Air France-KLM undrawn lines, end 2024**: the report gives €2.5bn in one place and
   €1,405m + €1,000m = €2,405m in another. Which do you want as the figure? If €2,405m, the
   key line changes and the AI's reading is right.
3. **Spot-check the answer key**: five lines of `docs/m3/answer_key.csv` (about ten
   minutes): search the report for the text in the `snippet` column.
4. **Review queue**: 75 figures. I suggest starting with FY2024-FY2025 (they feed the
   tearsheet); they come first in each company's list in `docs/m3/extractions.md`.

## How to rerun

```bash
uv run tearsheet all --offline
```

replays the recorded answers (no cost) and rebuilds every report. `uv run tearsheet extract`
asks the AI only for reports it has not read yet. `uv run python -m spikes.m3.answer_key`
rebuilds the answer key.
