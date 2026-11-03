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
  two specific Iberia aircraft; €3,400m are the general-purpose facilities.
