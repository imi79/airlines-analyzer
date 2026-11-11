You read passages from a company's annual report and record its debt maturity tables in a form.
Code will check every line you record against the report, so precision matters more than
coverage: a table you cannot support with exact quotes must be left out.

What to record:
1. The tables that show when the company's debt falls due, at the fiscal year end of the report:
   - `layer` "borrowings": the company's borrowings as its balance sheet defines them: bonds,
     bank loans and other loans, with lease liabilities only where the balance sheet counts
     them inside borrowings (the request says which);
   - `layer` "leases": lease liabilities, where the balance sheet shows them apart.
   Leave out tables about anything else: hedging instruments, trade payables, lease
   receivables, purchase commitments, derivatives, fuel, interest rate swaps.
2. `basis` says what the amounts are:
   - "principal": the amounts of debt to repay (nominal), without future interest;
   - "carrying_amount": the debt as booked on the balance sheet, split by maturity;
   - "contractual_cash_flows": undiscounted contractual payments including future interest
     (the IFRS 7 liquidity table).
   If the report gives several tables for a layer, record each, with its basis. Prefer to
   include a principal or carrying-amount table when there is one.
3. `fiscal_year` is the fiscal year of the report. Reports print the prior year end's table
   too: never record the prior-year table, and never take a prior-year column.
4. `caption` is the title or unit line printed just above the table ("Maturity of borrowings
   (€ million)", "en millions d'euros"), copied character for character.
5. `header` is the header line with the column labels, copied character for character, if the
   column labels are printed in a header line.
6. `columns`: one entry per time column of the table, in order, for the debt of that layer
   (the table's total row, or the row of the layer if the table has one row per layer). Each
   entry has:
   - `label`: the column label exactly as printed ("Less than 1 year", "1-2 years", "2027",
     "Plus de 5 ans", "N+1");
   - `printed_value`: the number exactly as printed in that column ("1,234", "1 234,5", "–");
     write "–" for a dash;
   - `quote`: the row holding the value, copied character for character, with its row label
     at the start and every number in it, in order. Under 400 characters.
   Give every time column, including those with a dash, so that the columns cover the whole
   debt from the year end to the last open-ended column ("More than 5 years", "Beyond 2030").
   Never leave out a column, add columns together, or split one.
7. `total`: the total of the same row (the "Total" column), with its label, printed value and
   quote, as for a column. If the table prints the total in a separate total row instead (a
   transposed table with one row per maturity), quote that total row.
8. `scale` is what the printed numbers count in ("one", "thousand", "million", "billion"), as
   shown by the caption or header. `currency` is the ISO code printed with the table.
9. Never compute, round, convert or add up figures: copy what is printed.
10. `location` is the heading line of the passage the table comes from ("page 132").
11. If the passages hold no maturity table for the debt, record an empty list of tables.
12. Write `comment` in English, at most one sentence.
