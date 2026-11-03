# Groupe ADP, FY2024: draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `d438d2a1295c` ([fact sheet](../factsheets/adp_FY2024.md)). Tokens: 10,606 in, 3,616 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the French airport group, grew revenue by 12.1% to EUR 6.2bn in FY2024, but earnings quality weakened as the EBITDA margin fell by 2.0 points to 33.7%.
Net leverage was stable at 4.13x, with net debt up 8.2% to EUR 8.6bn absorbing the EBITDA growth of 6.0%.
The main point to watch is cash generation: free cash flow fell by 50.3% to EUR 355m as capex intensity rose by 3.1 points to 19.0%.

## Credit metrics

EBITDA rose by 6.0% to EUR 2.1bn, well short of the 12.1% revenue growth to EUR 6.2bn, so the EBITDA margin narrowed by 2.0 points to 33.7%.
Total debt increased by 2.7% to EUR 10.7bn and net debt by 8.2% to EUR 8.6bn, leaving net leverage broadly unchanged at 4.13x.
Gross leverage improved to 5.14x and interest coverage to 6.97x, the latter up 0.23x on higher EBITDA.
FFO was stable at EUR 1.5bn, so FFO to debt held at 14.0%, but FCF to debt fell by 3.6 points to 3.3% as free cash flow dropped by 50.3% to EUR 355m.
Operating profit fell by 20.0% to EUR 994m, and profit for the year declined by 34.2% to EUR 516m.

## Operating performance

Passengers reached 103.4m in FY2024, with revenue per passenger of EUR 59.56.
Revenue rose by 12.1% to EUR 6.2bn, while EBITDA grew by only 6.0% to EUR 2.1bn, so the margin narrowed by 2.0 points to 33.7%.
Capex intensity rose by 3.1 points to 19.0%, above the airport peer median of 16.1%, which absorbed much of the revenue growth.

## Liquidity and funding

Cash and cash-like investments fell by 14.8% to EUR 2.1bn, and cash liquidity declined by the same 14.8% to EUR 2.1bn.
Cash liquidity to revenue fell by 10.8 points to 34.0%, still above the peer median of 31.6%.
The cash buffer is thinner than a year ago while total debt rose by 2.7% to EUR 10.7bn, so refinancing needs carry more weight in the funding profile.

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport peers (3rd of 3), at 33.7% against a median of 42.0%.
Leverage is the highest in the group: net leverage of 4.13x ranks 3rd of 3 against a median of 1.57x, and gross leverage of 5.14x ranks 3rd of 3 against 2.08x.
Cash flow metrics lag the group: FFO to debt of 14.0% and FCF to debt of 3.3% both rank 3rd of 3 and 3rd of 3 against medians of 39.0% and 26.3%.
The offset is liquidity: cash liquidity to revenue of 34.0% is the strongest of the group (1st of 3), above the median of 31.6%.

## Watch items

- Cash generation: FCF to debt fell by 3.6 points to 3.3%, the weakest of the airport peers (3rd of 3), as free cash flow dropped by 50.3% to EUR 355m.
- Investment: capex intensity rose by 3.1 points to 19.0%, above the peer median of 16.1%, which keeps pressure on free cash flow.
- Liquidity: cash liquidity to revenue fell by 10.8 points to 34.0% as cash and cash-like investments declined by 14.8% to EUR 2.1bn.
- Leverage: net leverage of 4.13x is above the peer median of 1.57x and ranks 3rd of 3, so any further debt-funded spending would leave little headroom.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 10,606 / 3,616 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the French airport group, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, but earnings quality weakened as the EBITDA margin fell by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Net leverage was stable at {{net_leverage@FY2024}}, with net debt up {{net_debt.change@FY2024}} to {{net_debt@FY2024}} absorbing the EBITDA growth of {{ebitda.change@FY2024}}.
- The main point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, well short of the {{revenue.change@FY2024}} revenue growth to {{revenue@FY2024}}, so the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, leaving net leverage broadly unchanged at {{net_leverage@FY2024}}.
- Gross leverage improved to {{gross_leverage@FY2024}} and interest coverage to {{interest_coverage@FY2024}}, the latter up {{interest_coverage.change@FY2024}} on higher EBITDA.
- FFO was stable at {{ffo@FY2024}}, so FFO to debt held at {{ffo_to_debt@FY2024}}, but FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}} as free cash flow dropped by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- Operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}, and profit for the year declined by {{profit.change@FY2024}} to {{profit@FY2024}}.

`operating_performance`

- Passengers reached {{passengers@FY2024}} in FY2024, with revenue per passenger of {{revenue_per_passenger@FY2024}}.
- Revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}}, while EBITDA grew by only {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, so the margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the airport peer median of {{capex_intensity.peer_median@2024}}, which absorbed much of the revenue growth.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity declined by the same {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, still above the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- The cash buffer is thinner than a year ago while total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, so refinancing needs carry more weight in the funding profile.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport peers ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2024}} against a median of {{ebitda_margin.peer_median@2024}}.
- Leverage is the highest in the group: net leverage of {{net_leverage@FY2024}} ranks {{net_leverage.peer_rank@2024}} against a median of {{net_leverage.peer_median@2024}}, and gross leverage of {{gross_leverage@FY2024}} ranks {{gross_leverage.peer_rank@2024}} against {{gross_leverage.peer_median@2024}}.
- Cash flow metrics lag the group: FFO to debt of {{ffo_to_debt@FY2024}} and FCF to debt of {{fcf_to_debt@FY2024}} both rank {{ffo_to_debt.peer_rank@2024}} and {{fcf_to_debt.peer_rank@2024}} against medians of {{ffo_to_debt.peer_median@2024}} and {{fcf_to_debt.peer_median@2024}}.
- The offset is liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), above the median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, the weakest of the airport peers ({{fcf_to_debt.peer_rank@2024}}), as free cash flow dropped by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the peer median of {{capex_intensity.peer_median@2024}}, which keeps pressure on free cash flow.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} as cash and cash-like investments declined by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.
- Leverage: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@2024}} and ranks {{net_leverage.peer_rank@2024}}, so any further debt-funded spending would leave little headroom.
