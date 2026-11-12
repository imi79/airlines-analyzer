# M8 maturity wall against the answer key

| Company | Year | Layer | Basis | Tool | Key | Result |
| --- | --- | --- | --- | --- | --- | --- |
| adp | FY2024 | borrowings | contractual_cash_flows | 0_1 1,456.0, 1_5 4,917.0, 5_plus 5,316.0 | 0_1 1,456.0, 1_5 4,917.0, 5_plus 5,316.0 | flagged: within one year 1,456.0m (with interest) is not between 1,606.5m and 2,852.2m, from the current borrowings of 1,785.0m |
| adp | FY2025 | borrowings | carrying_amount | 0_1 1,139.0, 1_5 4,156.0, 5_plus 4,115.0 |  | flagged: within one year 1,139.0m does not agree with the current borrowings of 1,859.0m on the balance sheet; the table total 9,410.0m does not agree with the borrowings of 10,587.0m on the balance sheet |
| aena | FY2024 | borrowings | contractual_cash_flows | 0_1 2,131.8, 1_2 956.4, 2_5 2,578.7, 5_plus 3,065.2 |  | flagged: within one year 2,131.8m (with interest) is not between 1,206.5m and 2,072.4m, from the current borrowings of 1,340.6m |
| aena | FY2025 | borrowings | contractual_cash_flows | 0_1 1,707.9, 1_2 1,116.7, 2_5 2,298.2, 5_plus 3,853.7 |  | flagged: within one year 1,707.9m (with interest) is not between 777.7m and 1,619.7m, from the current borrowings of 864.1m |
| afkl | FY2024 | borrowings | contractual_cash_flows | 0_1 2,065.0, 1_2 1,848.0, 2_5 3,436.0, 5_plus 3,188.0 | 0_1 2,065.0, 1_2 1,848.0, 2_5 3,436.0, 5_plus 3,188.0 | verified, correct |
| afkl | FY2025 | borrowings | contractual_cash_flows | 0_1 2,113.0, 1_2 959.0, 2_5 4,256.0, 5_plus 3,176.0 |  | verified, not in the key: check by hand |
| easyjet | FY2024 | borrowings | contractual_cash_flows | 0_1 465.0, 1_2 45.0, 2_5 1,115.0, 5_plus 760.0 |  | flagged: row, total: value 2,385 is not printed in the quote |
| easyjet | FY2025 | leases | contractual_cash_flows | 0_1 299.0, 1_5 727.0, 5_plus 186.0 | 0_1 299.0, 1_5 727.0, 5_plus 186.0 | verified, correct |
| finnair | FY2024 | borrowings | principal | 0_1 125.5, 1_2 56.7, 2_5 567.1, 5_plus 112.2 | 0_1 125.5, 1_2 56.7, 2_5 567.1, 5_plus 112.2 | verified, correct |
| finnair | FY2025 | borrowings | principal | 0_1 51.5, 1_2 21.0, 2_5 863.8, 5_plus 87.2 | 0_1 51.5, 1_2 21.0, 2_5 863.8, 5_plus 87.2 | verified, correct |
| iag | FY2024 | borrowings | contractual_cash_flows | 0_1 528.0, 1_2 524.0, 2_5 1,795.0, 5_plus 3,901.0 |  | flagged: within one year 528.0m (with interest) is not between 3,127.5m and 5,209.5m, from the current borrowings of 3,475.0m; the table total 6,748.0m (with interest) is not between 15,610.5m and 27,752.0m, from the borrowings of 17,345.0m |
| iag | FY2025 | borrowings | contractual_cash_flows | 0_1 2,028.0, 1_2 2,059.0, 2_5 5,879.0, 5_plus 7,854.0 | 0_1 2,028.0, 1_2 2,059.0, 2_5 5,879.0, 5_plus 7,854.0 | verified, correct |
| norwegian | FY2025 | borrowings | principal | 0_1 1,495.0, 1_2 0.0, 2_plus 23.0 | 0_1 2,293.0, 1_2 531.0, 2_5 1,511.0, 5_plus 1,513.0 | flagged: row, total: value 1,518 is not printed in the quote; within one year 1,495.0m does not agree with the current borrowings of 2,065.0m on the balance sheet; the table total 1,518.0m does not agree with the borrowings of 5,847.0m on the balance sheet |
| vie | FY2024 | leases | contractual_cash_flows | 0_1 1.9, 1_5 8.0, 5_plus 120.0 |  | flagged: the table does not show its scale (thousand); no tagged current and total lease liabilities to check the table against |

| Count | |
| --- | --- |
| verified_correct | 5 |
| verified_wrong | 0 |
| verified_not_in_key | 1 |
| unverified | 8 |
| key_tables_without_a_verified_wall | 6 |
