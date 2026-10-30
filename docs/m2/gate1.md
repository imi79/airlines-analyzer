# Gate 1: second-source model vs the tool

Built by the AI at Imane's request (decision 0009). Inputs are read mechanically from
the published 2025 statements (PDF text, page and line recorded in
`docs/m2/hand_model_inputs.csv`); every metric is an Excel formula recalculated by
LibreOffice (`docs/m2/hand_model.xlsx`). Tolerances: leverage and coverage 0.05x,
margins and ratios 0.1 point, amounts EUR 0.5m (rounding).

**Result: 62 of 62 comparisons within tolerance.**

| Company | Metric | Year | Model | Tool | Difference | Within tolerance |
| --- | --- | --- | --- | --- | --- | --- |
| afkl | ebitda | FY2025 | 5,056 | 5,056 | +0.0 | ✓ |
| afkl | ebitda | FY2024 | 4,109 | 4,109 | +0.0 | ✓ |
| afkl | ebitda_margin | FY2025 | 15.3% | 15.3% | -0.0000 | ✓ |
| afkl | ebitda_margin | FY2024 | 13.1% | 13.1% | -0.0000 | ✓ |
| afkl | total_debt | FY2025 | 15,513 | 15,513 | +0.0 | ✓ |
| afkl | total_debt | FY2024 | 14,642 | 14,642 | +0.0 | ✓ |
| afkl | cash_like | FY2025 | 6,858 | 6,858 | +0.0 | ✓ |
| afkl | cash_like | FY2024 | 6,932 | 6,932 | +0.0 | ✓ |
| afkl | net_debt | FY2025 | 8,655 | 8,655 | +0.0 | ✓ |
| afkl | net_debt | FY2024 | 7,710 | 7,710 | +0.0 | ✓ |
| afkl | net_leverage | FY2025 | 1.71x | 1.71x | -0.0000 | ✓ |
| afkl | net_leverage | FY2024 | 1.88x | 1.88x | -0.0000 | ✓ |
| afkl | gross_leverage | FY2025 | 3.07x | 3.07x | -0.0000 | ✓ |
| afkl | gross_leverage | FY2024 | 3.56x | 3.56x | -0.0000 | ✓ |
| afkl | interest_coverage | FY2025 | 8.06x | 8.06x | -0.0000 | ✓ |
| afkl | interest_coverage | FY2024 | 6.51x | 6.51x | +0.0000 | ✓ |
| afkl | ffo | FY2025 | 4,250 | 4,250 | +0.0 | ✓ |
| afkl | ffo | FY2024 | 3,425 | 3,425 | +0.0 | ✓ |
| afkl | ffo_to_debt | FY2025 | 27.4% | 27.4% | -0.0000 | ✓ |
| afkl | ffo_to_debt | FY2024 | 23.4% | 23.4% | +0.0000 | ✓ |
| afkl | capex | FY2025 | 4,449 | 4,449 | +0.0 | ✓ |
| afkl | capex | FY2024 | 3,728 | 3,728 | +0.0 | ✓ |
| afkl | fcf | FY2025 | 606 | 606 | +0.0 | ✓ |
| afkl | fcf | FY2024 | -232 | -232 | +0.0 | ✓ |
| afkl | fcf_to_debt | FY2025 | 3.9% | 3.9% | -0.0000 | ✓ |
| afkl | fcf_to_debt | FY2024 | -1.6% | -1.6% | -0.0000 | ✓ |
| afkl | capex_intensity | FY2025 | 13.5% | 13.5% | -0.0000 | ✓ |
| afkl | capex_intensity | FY2024 | 11.9% | 11.9% | -0.0000 | ✓ |
| afkl | cash_liquidity_to_revenue | FY2025 | 20.8% | 20.8% | +0.0000 | ✓ |
| afkl | cash_liquidity_to_revenue | FY2024 | 22.0% | 22.0% | +0.0000 | ✓ |
| afkl | advance_ticket_cover | FY2025 | 62.2% | 62.2% | -0.0000 | ✓ |
| afkl | advance_ticket_cover | FY2024 | 59.1% | 59.1% | +0.0000 | ✓ |
| adp | ebitda | FY2025 | 2,328 | 2,328 | +0.0 | ✓ |
| adp | ebitda | FY2024 | 2,077 | 2,077 | +0.0 | ✓ |
| adp | ebitda_margin | FY2025 | 34.7% | 34.7% | +0.0000 | ✓ |
| adp | ebitda_margin | FY2024 | 33.7% | 33.7% | -0.0000 | ✓ |
| adp | total_debt | FY2025 | 10,587 | 10,587 | +0.0 | ✓ |
| adp | total_debt | FY2024 | 10,672 | 10,672 | +0.0 | ✓ |
| adp | cash_like | FY2025 | 2,017 | 2,017 | +0.0 | ✓ |
| adp | cash_like | FY2024 | 2,096 | 2,096 | +0.0 | ✓ |
| adp | net_debt | FY2025 | 8,570 | 8,570 | +0.0 | ✓ |
| adp | net_debt | FY2024 | 8,576 | 8,576 | +0.0 | ✓ |
| adp | net_leverage | FY2025 | 3.68x | 3.68x | +0.0000 | ✓ |
| adp | net_leverage | FY2024 | 4.13x | 4.13x | -0.0000 | ✓ |
| adp | gross_leverage | FY2025 | 4.55x | 4.55x | +0.0000 | ✓ |
| adp | gross_leverage | FY2024 | 5.14x | 5.14x | -0.0000 | ✓ |
| adp | interest_coverage | FY2025 | 7.89x | 7.89x | -0.0000 | ✓ |
| adp | interest_coverage | FY2024 | 6.97x | 6.97x | +0.0000 | ✓ |
| adp | ffo | FY2025 | 1,663 | 1,663 | +0.0 | ✓ |
| adp | ffo | FY2024 | 1,496 | 1,496 | +0.0 | ✓ |
| adp | ffo_to_debt | FY2025 | 15.7% | 15.7% | +0.0000 | ✓ |
| adp | ffo_to_debt | FY2024 | 14.0% | 14.0% | -0.0000 | ✓ |
| adp | capex | FY2025 | 1,218 | 1,218 | +0.0 | ✓ |
| adp | capex | FY2024 | 1,169 | 1,169 | +0.0 | ✓ |
| adp | fcf | FY2025 | 420 | 420 | +0.0 | ✓ |
| adp | fcf | FY2024 | 355 | 355 | +0.0 | ✓ |
| adp | fcf_to_debt | FY2025 | 4.0% | 4.0% | +0.0000 | ✓ |
| adp | fcf_to_debt | FY2024 | 3.3% | 3.3% | +0.0000 | ✓ |
| adp | capex_intensity | FY2025 | 18.2% | 18.2% | -0.0000 | ✓ |
| adp | capex_intensity | FY2024 | 19.0% | 19.0% | -0.0000 | ✓ |
| adp | cash_liquidity_to_revenue | FY2025 | 30.1% | 30.1% | +0.0000 | ✓ |
| adp | cash_liquidity_to_revenue | FY2024 | 34.0% | 34.0% | +0.0000 | ✓ |
