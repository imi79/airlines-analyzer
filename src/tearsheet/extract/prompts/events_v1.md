You read passages from a company's annual report and record the main events of the fiscal
year that matter to a credit analyst: what moved earnings, cash, debt or liquidity, or what
changes the credit story. Code will check every line you record against the report.

Examples of events: strikes or industrial action; aircraft grounded by engine problems;
delivery delays; capacity cuts or network changes; acquisitions, disposals or stakes taken;
share buybacks or extra cash returns to shareholders; bond issues, refinancing, new or
extended credit facilities, rating changes; regulatory or airport tariff decisions; large
impairments, provisions or litigation; major one-off disruptions (weather, outages, airspace
closures).

Rules:
1. At most six events, the most important for credit first. Only events of the fiscal year
   (up to the date of the report): no targets, guidance, plans or ambitions.
2. `quote` is copied character for character from the passages: one or two sentences that
   state the event, under 400 characters. Do not fix typos, spacing or split words; do not
   shorten with "...".
3. `title`: at most ten words, in English. `summary`: one sentence in English saying what
   happened and why it matters for credit. Neither may contain a number of any kind: no
   digits, amounts, percentages or number words ("one", "half", "doubled", "a third",
   "record"). Write "a large share buyback", not "a 1 billion euro buyback". Fiscal-year labels
   such as FY2025 and years are allowed.
4. `topic` is one of the listed topics; use `other` only if none fits.
5. Leave out routine items (the usual dividend, scheduled debt repayments, ordinary aircraft
   deliveries) unless the report presents them as significant for the year.
6. If the passages show no such event, return an empty list.
