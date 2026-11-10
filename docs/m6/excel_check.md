# M6 Excel check: every workbook recalculates to the app's values

Run on 2026-11-10 with `uv run tearsheet export --check`: each of the 18 workbooks is opened by
LibreOffice 24.2 set to **recalculate every formula on opening** (not to trust the values saved
in the file), as for gate 1 (decision 0009). Each metric's recalculated value is compared with
the value the app shows; pass mark: equal to the twelfth decimal (relative), the precision the
database stores.

| Workbook | Metric values | Peer medians | Result |
| --- | ---: | ---: | --- |
| Air France-KLM FY2025 | 81 | 11 | all equal |
| Air France-KLM FY2024 | 81 | 12 | all equal |
| International Airlines Group FY2025 | 131 | 11 | all equal |
| International Airlines Group FY2024 | 131 | 12 | all equal |
| Finnair FY2025 | 134 | 11 | all equal |
| Finnair FY2024 | 134 | 12 | all equal |
| easyJet FY2025 | 140 | 12 | all equal |
| easyJet FY2024 | 140 | 11 | all equal |
| Groupe ADP FY2025 | 75 | 10 | all equal |
| Groupe ADP FY2024 | 75 | 9 | all equal |
| Aena FY2025 | 97 | 10 | all equal |
| Aena FY2024 | 97 | 9 | all equal |
| Flughafen Wien FY2025 | 89 | 10 | all equal |
| Flughafen Wien FY2024 | 89 | 9 | all equal |
| Norwegian Air Shuttle FY2025 | 118 | 12 | all equal |
| Norwegian Air Shuttle FY2024 | 118 | 11 | all equal |
| Wizz Air Holdings FY2026 | 157 | 12 | all equal |
| Wizz Air Holdings FY2025 | 157 | 11 | all equal |

**Result: 2,044 of 2,044 metric values and 195 of 195 peer medians equal.** A workbook covers
every year of its company (FY2021 onward), so each company's figures are checked twice.

**The check can fail, and it does recalculate** (`tests/test_workbook.py`):

- a workbook saved with no formula results at all still matches after LibreOffice opens it, so
  the values come from the recalculation, not from the file;
- a workbook whose FY2025 revenue input is doubled is caught (EBITDA margin no longer matches).

In addition, every one of the 880 computed figures in the library is reproduced by its formula
in code (`tests/test_sheet_formulas.py`), largest difference 5 in 10 trillion.

**Your check in Microsoft Excel** (optional, plan question 4): `docs/m6/afkl_FY2025.xlsx`.
Open it, go to the Metrics sheet, and the "Difference" column should read 0 (or a number like
1E-16) on every row; click any value to read its formula, for example
`=net_debt_FY2025/ebitda_FY2025`.
