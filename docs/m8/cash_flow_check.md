# M8 second-source check: cash flow after leases

Inputs typed from the published statements (pages in `spikes/m8/second_source.py`),
computed with their own arithmetic, against the tool. Tolerance: 0.1 point on ratios,
the million on amounts (gate 1).

| Company | Year | Metric | Second source | Tool | Difference | |
| --- | --- | --- | --- | --- | --- | --- |
| Air France-KLM | FY2025 | net_capex | 3,058 | 3,058 | +0.0 | ✓ |
| Air France-KLM | FY2025 | fcf_after_leases | 367 | 367 | +0.0 | ✓ |
| Air France-KLM | FY2025 | fcf_after_leases_to_debt | 2.37% | 2.37% | +0.00 pt | ✓ |
| Air France-KLM | FY2025 | debt_due_1y | 2,761 | 2,761 | +0.0 | ✓ |
| Air France-KLM | FY2024 | net_capex | 3,050 | 3,050 | +0.0 | ✓ |
| Air France-KLM | FY2024 | fcf_after_leases | -1,109 | -1,109 | +0.0 | ✓ |
| Air France-KLM | FY2024 | fcf_after_leases_to_debt | -7.57% | -7.57% | +0.00 pt | ✓ |
| Air France-KLM | FY2024 | debt_due_1y | 2,674 | 2,674 | +0.0 | ✓ |
| Groupe ADP | FY2025 | net_capex | 1,183 | 1,183 | +0.0 | ✓ |
| Groupe ADP | FY2025 | fcf_after_leases | 130 | 130 | +0.0 | ✓ |
| Groupe ADP | FY2025 | fcf_after_leases_to_debt | 1.23% | 1.23% | -0.00 pt | ✓ |
| Groupe ADP | FY2025 | debt_due_1y | 1,859 | 1,859 | +0.0 | ✓ |
| Groupe ADP | FY2024 | net_capex | 1,156 | 1,156 | +0.0 | ✓ |
| Groupe ADP | FY2024 | fcf_after_leases | 42 | 42 | +0.0 | ✓ |
| Groupe ADP | FY2024 | fcf_after_leases_to_debt | 0.39% | 0.39% | +0.00 pt | ✓ |
| Groupe ADP | FY2024 | debt_due_1y | 1,785 | 1,785 | +0.0 | ✓ |

**16 of 16 within tolerance.**
