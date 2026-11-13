# M10 answer key (written before the AI read anything)

`answer_key.csv` holds, for three companies, the figures a careful reader takes from the
half-year statements: Finnair (five columns, full year printed), IAG (two columns, no full
year) and Groupe ADP (French, an airport). 58 lines, three values each where printed:

- `current`: the first half just ended (income statement, cash flow), or the half-year date
  (balance sheet);
- `prior`: the same half one year before (income statement and cash flow only);
- `base`: the 31 December 2025 column of the balance sheet, or the full-year 2025 column
  where the report prints one (Finnair).

Amounts are in millions of the reporting currency, as printed, with costs and cash outflows
as positive amounts (the database's convention). Where a line adds two rows of the statement,
the row column says so. Written by the AI assistant from the PDF pages on 2026-11-13 and
committed before the first AI call of M10, as the maturity key was in M8 (decision 0022).
The target: **no wrong figure marked verified**.
