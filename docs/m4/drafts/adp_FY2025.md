# Groupe ADP, FY2025: draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `a6cbeaf4eaf8` ([fact sheet](../factsheets/adp_FY2025.md)). Tokens: 10,797 in, 3,198 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the French airport group, had a stronger FY2025 as revenue rose by 8.9% to EUR 6.7bn and the EBITDA margin widened by 1.0 point to 34.7%.
Net leverage fell by 0.45x to 3.68x, with net debt broadly unchanged at EUR 8.6bn.
The point to watch is liquidity: cash liquidity to revenue declined by 3.9 points to 30.1%, in line with the peer median.

## Credit metrics

EBITDA increased by 12.1% to EUR 2.3bn and operating profit by 16.7% to EUR 1.2bn, on revenue up 8.9%.
Total debt was stable at EUR 10.6bn and net debt at EUR 8.6bn, so gross leverage fell by 0.59x to 4.55x.
Interest coverage improved by 0.92x to 7.89x.
FFO rose by 11.2% to EUR 1.7bn, lifting FFO to debt by 1.7 points to 15.7%.
Free cash flow increased by 18.3% to EUR 420m, taking FCF to debt to 4.0% as capex intensity eased by 0.8 points to 18.2%.

## Operating performance

Passengers rose by 3.5% to 107.0m, with traffic growth of 3.5%.
Revenue per passenger increased by 5.2% to EUR 62.65, so revenue per passenger grew faster than traffic.
Revenue reached EUR 6.7bn, up 8.9%, with EBITDA of EUR 2.3bn at a margin of 34.7%.

## Liquidity and funding

Cash and cash-like investments fell by 3.8% to EUR 2.0bn, and cash liquidity declined by 3.8% to EUR 2.0bn.
Cash liquidity to revenue fell by 3.9 points to 30.1%, in line with the peer median of 30.1%.
Total debt was stable at EUR 10.6bn against cash of EUR 2.0bn, so the buffer against maturities rests on the cash balance rather than on new funding.

## Peer positioning

Groupe ADP ranks last of the airport peers on EBITDA margin (3rd of 3), at 34.7% against a median of 36.5%.
Leverage is the weakest in the group: net leverage of 3.68x ranks 3rd of 3 against a median of 1.46x, and gross leverage of 4.55x ranks 3rd of 3.
Cash generation trails the peers: FFO to debt of 15.7% and FCF to debt of 4.0% both rank 3rd of 3 against medians of 39.6% and 22.9%.
Interest coverage of 7.89x is below the peer median of 14.72x and ranks 3rd of 3, while capex intensity of 18.2% is in line with the median.

## Watch items

- Leverage: net leverage of 3.68x is above the peer median of 1.46x and ranks 3rd of 3, so the ratio remains the main constraint on the credit profile.
- Cash generation: FFO to debt of 15.7% is below the peer median of 39.6%, and FCF to debt of 4.0% leaves little room after capital spending.
- Liquidity: cash liquidity to revenue fell by 3.9 points to 30.1%, with cash and cash-like investments down by 3.8% to EUR 2.0bn.
- Investment: capex intensity of 18.2% is in line with the peer median of 18.2%, so free cash flow of EUR 420m stays thin relative to debt of EUR 10.6bn.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 10,797 / 3,198 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the French airport group, had a stronger FY2025 as revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}} and the EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, with net debt broadly unchanged at {{net_debt@FY2025}}.
- The point to watch is liquidity: cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, in line with the peer median.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, on revenue up {{revenue.change@FY2025}}.
- Total debt was stable at {{total_debt@FY2025}} and net debt at {{net_debt@FY2025}}, so gross leverage fell by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- Free cash flow increased by {{fcf.change@FY2025}} to {{fcf@FY2025}}, taking FCF to debt to {{fcf_to_debt@FY2025}} as capex intensity eased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, with traffic growth of {{traffic_growth@FY2025}}.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2025}} to {{revenue_per_passenger@FY2025}}, so revenue per passenger grew faster than traffic.
- Revenue reached {{revenue@FY2025}}, up {{revenue.change@FY2025}}, with EBITDA of {{ebitda@FY2025}} at a margin of {{ebitda_margin@FY2025}}.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity declined by {{cash_liquidity.change@FY2025}} to {{cash_liquidity@FY2025}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, in line with the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.
- Total debt was stable at {{total_debt@FY2025}} against cash of {{cash_like@FY2025}}, so the buffer against maturities rests on the cash balance rather than on new funding.

`peer_positioning`

- Groupe ADP ranks last of the airport peers on EBITDA margin ({{ebitda_margin.peer_rank@2025}}), at {{ebitda_margin@FY2025}} against a median of {{ebitda_margin.peer_median@2025}}.
- Leverage is the weakest in the group: net leverage of {{net_leverage@FY2025}} ranks {{net_leverage.peer_rank@2025}} against a median of {{net_leverage.peer_median@2025}}, and gross leverage of {{gross_leverage@FY2025}} ranks {{gross_leverage.peer_rank@2025}}.
- Cash generation trails the peers: FFO to debt of {{ffo_to_debt@FY2025}} and FCF to debt of {{fcf_to_debt@FY2025}} both rank {{ffo_to_debt.peer_rank@2025}} against medians of {{ffo_to_debt.peer_median@2025}} and {{fcf_to_debt.peer_median@2025}}.
- Interest coverage of {{interest_coverage@FY2025}} is below the peer median of {{interest_coverage.peer_median@2025}} and ranks {{interest_coverage.peer_rank@2025}}, while capex intensity of {{capex_intensity@FY2025}} is in line with the median.

`watch_items`

- Leverage: net leverage of {{net_leverage@FY2025}} is above the peer median of {{net_leverage.peer_median@2025}} and ranks {{net_leverage.peer_rank@2025}}, so the ratio remains the main constraint on the credit profile.
- Cash generation: FFO to debt of {{ffo_to_debt@FY2025}} is below the peer median of {{ffo_to_debt.peer_median@2025}}, and FCF to debt of {{fcf_to_debt@FY2025}} leaves little room after capital spending.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, with cash and cash-like investments down by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
- Investment: capex intensity of {{capex_intensity@FY2025}} is in line with the peer median of {{capex_intensity.peer_median@2025}}, so free cash flow of {{fcf@FY2025}} stays thin relative to debt of {{total_debt@FY2025}}.
