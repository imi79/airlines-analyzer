# 0013 · M3: changes to the checks after the first full run

Date: 2026-11-01 · Status: made by the AI; for Imane to confirm

The first run of the AI on all 41 reports (DeepSeek, prompt `extract-v1`) was replayed through
the checks and reviewed line by line. The AI's answers were not changed and not re-asked; only
the code checks changed. Each change has a test built from the real report text.

**Stricter (they stop wrong figures).** Found by reviewing figures outside the answer key:

1. **A hedge for part of a year is not a twelve-month hedge.** Finnair's "8 per cent … for the
   first six months of 2022" and Wizz Air's "hedge coverage for the period 56%" (a six-month
   period) had been verified as the hedge ratio for the next twelve months. Now a quote naming
   a first half, H1, a quarter or a number of months below twelve stays unverified.
2. **A quote cut short cannot hide the period.** For Finnair 2022 and 2024 the AI's quote
   stopped at "… fuel purchases for the first". The check now reads the report itself to the
   end of the sentence ("… six months of 2023").
3. **In a hedge table, the next year's column.** Air France-KLM's 2022 table prints the share
   hedged by year of use: 2022 73 %, 2023 51 %, 2024 4 %. At the end of 2022 the position
   for the next twelve months is the 2023 column (51 %), not 73 %.

4. **A bare number is not a quote.** Groupe ADP's 2025 passengers (107.0m) were verified on
   the quote "107,0" with a header found elsewhere on the page; in the PDF the number sits in
   a jumbled list of airports. A quote must now hold the row's words, not only numbers.

Effect: 7 hedge ratios verified before, 2 after (Norwegian 2022 and 2023, both "fuel
consumption for the next year"). The other 5 were wrong by definition and no longer pass. ADP 2025 passengers wait for review.

**Fairer (they stop right figures being refused).** Found on figures in the answer key:

5. **"‘000" after a row label means thousands; it is not a column.** IAG's table row
   "Passengers carried ‘000 121,560 122,047 …" was read one column off, so the right 2025
   figure was refused as 2024.
6. **Seat-based load factors** (`config/extraction.yaml`). easyJet and Wizz Air print load factor
   as seats sold ÷ seats offered (easyJet 93.4m ÷ 104.0m = 89.8%), not RPK ÷ ASK (90.8%). The
   cross-check RPK ÷ ASK = printed load factor is skipped for them, with a note; their ASK and
   RPK go through every other check. The tool's own load factor stays RPK ÷ ASK for every
   airline, so easyJet shows 90.8% where it reports 89.8%; the tearsheet footnote saying so
   comes with the fact sheet in M4.
7. **A number printed with spaces inside** ("3 0, 2 2 7. 3" in Finnair's scrambled table) is
   found in its quote, so it can be shown for review. It still cannot be verified there (the
   table's header names no year).

**Housekeeping.** Figures for FY2020, read as comparatives in the FY2021 reports, serve the
cross-checks only and are not stored (v1 starts at FY2021). The M1 coverage report and check
sheet leave text-read figures to `docs/m3/`.

**Score on the answer key** (25 figures): before these changes 14 verified and correct (56%),
after 19 (76%); verified but wrong 0 both times. Changes 5 and 6 were found on key figures, so
the 76% is somewhat flattered; changes 1 to 4 only remove verified figures and do not touch the
key (none of its lines is a hedge ratio for part of a year).
