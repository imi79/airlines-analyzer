# M0 walkthrough: can we get the data?

**The question.** Before building anything, we checked whether the free filings database
(filings.xbrl.org) has the annual reports we need, and whether the key figures in them are
labelled in a way a program can pick up.

**How it works, in analyst terms.** Each figure in an electronic annual report carries a label,
like a cell carrying an account code in a chart of accounts. Most companies use the official IFRS
codes ("Revenue", "LeaseLiabilities"...). Some invent their own codes for some lines. The script
goes through each company and year and ticks a checklist of about 20 lines:

- ✓ **found**: official IFRS code. Easy to pick up.
- **ext**: the company's own code. Usable, but we write a mapping rule once per company.
- – **missing**: not labelled. We'd have to read it from the text.

A company passes if it has three years or more where the eight lines we need for leverage,
coverage and cash flow are all ✓ or ext.

## What we found

1. **Seven of the ten companies pass**: Air France-KLM, IAG, Finnair, easyJet, ADP, Aena and
   Flughafen Wien.
2. **Lufthansa, Fraport and Ryanair can't be used from this database.** It holds no German and
   no Irish filings at all. That's a gap in the database, not in the companies' reporting.
3. **Good replacements exist.** Norwegian and Wizz Air (low-cost) and Icelandair (network) pass.
   Copenhagen Airports does not.
4. **Four companies don't show leases on their own line.** IAG, Aena, ADP and Wizz Air put lease
   debt inside borrowings. We read each debt note to confirm it, and recorded the quote.
   Flughafen Wien uses one combined line. Total debt is complete in all five cases.
5. **Two companies have holes in the database.** Air France-KLM and ADP have no FY2023 or FY2025
   report. We recover FY2023 from the prior-year column of the FY2024 report, as an analyst
   would. FY2025 is not available.
6. **One figure needs care.** Air France-KLM's D&A line also includes provisions. Using it
   as-is would overstate EBITDA, so M1 will take pure D&A from the notes.
7. **The text the AI will read later is there.** Every airline's report mentions ASK, RPK,
   passengers, load factor, fleet and fuel hedging. Some reports have broken spacing
   ("2. 7 %"), so the check on the AI's quotes must ignore spaces.
8. **Exchange rates work.** The ECB publishes monthly average and month-end rates for GBP, NOK,
   USD and DKK.

**Spot check.** IAG 2024 revenue (€32.1bn), easyJet FY2024 revenue (£9.3bn), Air France-KLM 2024
revenue (€31.5bn) and Aena 2024 revenue (€5.76bn) all match the published figures.

## Your decision

Which line-up for v1? The options are in `docs/decisions/0001-issuer-go-no-go.md`. The
recommended one swaps Ryanair for Norwegian and Wizz Air, which gives 9 companies.

## Where to look

| File | What it is |
| --- | --- |
| `docs/m0/coverage.md` | The full checklist, company by company and year by year |
| `docs/m0/go_no_go.csv` | The pass / fail table (opens in Excel) |
| `docs/m0/coverage_detail.csv` | Every line with the label used and the value (opens in Excel) |
| `docs/m0/filings.csv` | Every report found, and which one was used and why |
| `docs/m0/report_text.csv` | Traffic terms found in each airline's report, with a snippet |
| `docs/decisions/` | The three decisions taken in M0 |
