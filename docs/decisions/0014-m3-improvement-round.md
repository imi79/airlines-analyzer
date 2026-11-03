# 0014 · M3 improvement round: prompt extract-v2, judged on held-out lines

Date: 2026-11-03 · Status: accepted (Imane chose option b of the M3 walkthrough)

**Why.** The first run scored 19 of 25 (76%) on the answer key, short of the 80% target, with
no wrong value verified. Imane chose one improvement round.

**Keeping the test fair.** A prompt tuned after seeing which key lines failed would be graded
on its own homework. So before changing anything, 23 more lines were read by code from each
airline's previous-year report, with the same rule as the first 25 (every figure printed as
one number on the scope wanted; decision 0012), and committed before the second run. The score
report shows the first lines, the held-out lines and both together. The 80% box is ticked only
if it is met on all lines **and** on the held-out lines alone.

On the first run's answers the held-out lines already scored 16 of 23 (70%), with one figure
verified that differs from the key (IAG undrawn facilities at end 2024: 3,400m kept by the
tool, 3,534m in the key; see "Open definition questions").

**What changed in extract-v2** (`extract/prompts/extract_v2.md`; v1 kept for the record). Each
change answers a failure type seen in the first run, not a single figure:

1. **Header with the years.** Where a table has several header lines, the AI copies the one
   with the years (Finnair's traffic table: the AI had copied "Passenger revenue ASK RPK PLF").
2. **Caption.** A new form field for the table's title or unit line ("(Miles de euros)",
   "EUR mill."). Code accepts it only if it is in the report word for word on the quote's page
   or the page before, so it cannot be borrowed from another table. Airport segment tables
   print the unit there, not in the row.
3. **Hedge ratio defined in the prompt.** Next twelve months or the next fiscal year as a
   whole; in a table by year of use, next year's column; a part-year figure is "not found".
4. **Scope printed in parts.** Each part is recorded as a component and code adds them up (for
   example Finnair's own fleet and the fleet Norra flies for it). Before, only credit
   facilities could be recorded in parts.
5. **A row includes its label**, never the numbers alone (the check from decision 0013).

The scope of Finnair's fleet in `config/extraction.yaml` now says the two fleets are added
together; the old wording referred to a fleet total the report does not print.

**Open definition questions** (for Imane; the key is not changed until she decides):
- Air France-KLM undrawn lines at end 2024: €2.5bn printed in one place, €1,405m + €1,000m =
  €2,405m in another.
- IAG undrawn facilities at end 2024: €3,534m "in total" includes €134m of facilities tied to
  two specific Iberia aircraft; €3,400m are the general-purpose facilities. Same at end 2023:
  €4,787m in total, €4,412m general-purpose.

## Result

**The prompt alone did not help.** Scored before any further code change, extract-v2 gave the
same 35 of 48 (73%), held-out 16 of 23 (70%). The AI did follow the new rules on most targeted
cases (it copied Finnair's year header, split Finnair's fleet into its two parts, named Air
France-KLM's 2023 hedge column), but the checks then tripped on two reading bugs: a header that
repeats the years over each measure ("2025 2024 | 2025 2024 | 2025 2024"), and an icon
character from the report's fonts inside Finnair's fleet table.

**A third, blind set.** Fixing those bugs after seeing them on held-out lines would spoil the
held-out set. So 23 more lines were read by code from the FY2023 reports and committed first;
only then were the two fixes made (with tests), and the recorded v2 answers replayed. No new AI
call was needed.

| | First (25) | Held-out (23) | Blind (23) | All (71) |
| --- | --- | --- | --- | --- |
| Verified and correct | 20 (80%) | 16 (70%) | **15 (65%)** | 51 (72%) |
| Verified but different from the key | 0 | 0 | **1** | 1 |

The blind column is the clean measure of the final code. The one figure verified but
different is IAG's undrawn facilities at end 2023: 4,412m (general-purpose facilities, kept by
the tool) against 4,787m in the key ("in total", adding 375m of aircraft-specific facilities).
It is the same definition question as IAG at end 2024 (above); if Imane chooses
general-purpose facilities, the key's two IAG lines (FY2023, FY2024) change, no figure on any
set is verified wrongly, and the blind score becomes 16 of 23 (70%).

**The blind misses that remain all stay unverified**, so none reaches the tearsheet. By type:

- The figure's name is outside the quote: easyJet's "This amounted to £1.8 billion" (the word
  "undrawn" is in the sentence before); Finnair's "Total" row (the column names ASK, RPK sit
  in a header line of their own).
- Comparative without brackets: Norwegian's "87 aircraft at year-end, up from 70 aircraft at
  year-end 2022" is tied to 2022, the nearest year.
- Our own part-year hedge check is too broad: Wizz Air's "12 months 6 months" header makes the
  F24 column (12 months, 56%) look like a part-year figure because of the F25 column's
  "6 months".
- A row with several equal numbers and no year (IAG "ASKs (millions) 323,111 323,111").
- The AI missed IAG's "115.6 million passengers" (an infographic).

**A regression in v2's wording.** The new sentence "a table row includes its label, never
the numbers alone" was often read as "give the label only": 16 answers quote a row label
without its number ("Total ASKs (’000 km)"), against 1 under v1. The checks refuse every one
("value is not printed in the quote"), so nothing wrong gets through, but figures are lost:
Wizz Air's FY2024 column is empty, and Air France-KLM's 2022 hedge (the AI had picked the
right column, 51%) cannot be verified. The airport segment tables gained from the caption field
(Aena: 12 of 15 figures verified, 3 before).

**Not done, on purpose.** Each of these could be fixed in code, but every fix so far has shown
the next layer, and fixing them now would leave no clean set to judge the result. That choice
goes back to Imane.
