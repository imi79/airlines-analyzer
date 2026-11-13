# M10 coverage check: the half-year reports

Done on 2026-11-13, before anything else was built (plan item 1). For each of the nine
companies: is the latest half-year report public, can it be fetched, in which language, are the
three statements there, and do they read cleanly as text?

**Result: go for all nine.** Eight are read by the AI with code checks; Flughafen Wien is
entered by hand (its PDF shows the figures but does not give them as text). No PDF is needed
from Imane: Air France-KLM's and ADP's sites, which refused automated downloads in M1, served
their half-year reports this time.

| Company | Half-year to | Report | Language | Statements | Columns printed | Reads as text | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Air France-KLM | 30 Jun 2026 | Half Year Report (74 pages) | English | income p.33, balance sheet p.35-36, cash flow p.38 | H1 2026, H1 2025 restated; 31 Dec 2025 | yes | **go**, with a warning (below) |
| IAG | 30 Jun 2026 | Interim management report (50 pages) | English | p.20, 22, 23 | H1 2026, H1 2025; 31 Dec 2025 | yes | **go** |
| Finnair | 30 Jun 2026 | Half-year report (41 pages) | English | p.28, 29, 31 | Q2 and H1 2026 and 2025, full year 2025; 30 Jun 2026, 30 Jun 2025, 31 Dec 2025 | yes | **go** |
| easyJet | 31 Mar 2026 | Half-year results (47 pages) | English | p.20, 22, 24 | H1 FY2026, H1 FY2025 (headline, non-headline, total); 30 Sep 2025 | yes (a few labels overlap) | **go** |
| Norwegian | 30 Jun 2026 | Q2 and first half report (34 pages) | English | p.12, 14, 15 | Q2 and H1 2026 and 2025, full year 2025; three balance sheet dates | yes | **go** (condensed cash flow: capex is net of sale proceeds) |
| Wizz Air | 30 Sep 2026 | Half-year results, published 12 Nov 2026 (45 pages) | English | p.11-14 | H1 FY2027, H1 FY2026; 31 Mar 2026 | yes | **go** |
| Groupe ADP | 30 Jun 2026 | Rapport financier semestriel (99 pages) | French | p.36, 38, 39 | S1 2026, S1 2025; 31 Dec 2025 | yes | **go** |
| Aena | 30 Jun 2026 | Estados financieros intermedios, with the limited review report (127 pages) | Spanish (as its annual filing, so row labels compare) | p.7, 8, 11-12 | H1 2026, H1 2025; 31 Dec 2025 | yes (thousands of euros) | **go** |
| Flughafen Wien | 30 Jun 2026 | Quarterly report 2/2026 (54 pages) | English | p.28, 30, 31 | H1 2026, H1 2025, Q2; 31 Dec 2025 | **no**: the digits of the tables are drawn with a font that carries no text, in the English and the German version alike | **go by hand entry** (plan question 2, fallback b): entered from the pages, unverified until Imane reviews |

All nine are unaudited (Aena's and ADP's carry an auditor's limited review, which is less than
an audit). The files are in `documents/half-year/`, registered with their source address and
fingerprint in `config/half_year_reports.yaml`.

## Three things the check found

1. **Only two reports print the full year beside the half year** (Finnair, Norwegian). For the
   other seven, the income statement and the cash flow show the two half years only. The
   balance sheet control (the 31 December column must equal our database) works for all nine;
   the full-year control works for two. For the others, the code adds a third control so that
   a row is not trusted on the AI's word: the row's label must be the one under which the
   annual report prints the figure our database holds.
2. **Air France-KLM changed its income statement format in 2026** (new accounting standard
   IFRS 18, note 4 of its report) and restated the first half of 2025 the same way. Its
   "operating profit" is no longer the line our FY2025 figure was built on (currency effects
   and one-off items are now inside it). LTM = FY2025 + H1 2026 - H1 2025 would mix two
   definitions for the full year part. The controls flag these lines; they wait for Imane's
   review instead of being shown as verified.
3. **Different dates.** easyJet's half year ends on 31 March 2026 (LTM to March 2026, on
   FY2025 to September 2025). Wizz Air's ends on 30 September 2026 (LTM to September 2026, on
   FY2026 to March 2026). The other seven are at 30 June 2026 on FY2025.
