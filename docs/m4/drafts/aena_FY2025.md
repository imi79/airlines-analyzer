# Aena, FY2025: draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `9def316ca700` ([fact sheet](../factsheets/aena_FY2025.md)). Tokens: 11,349 in, 3,489 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, ended FY2025 with revenue up 8.9% to EUR 6.3bn and net leverage down to 1.46x from 1.57x.
The EBITDA margin eased by 0.6 points to 60.3%, still the highest of the airport peers (1st of 3).
The point to watch is liquidity: total liquidity fell by 6.3% to EUR 4.3bn as undrawn committed facilities declined by 18.7% to EUR 2.2bn.

## Credit metrics

EBITDA increased by 7.8% to EUR 3.8bn and operating profit by 12.2% to EUR 3.0bn, on revenue up 8.9%.
Net debt was stable at EUR 5.5bn while total debt rose by 3.2% to EUR 7.6bn, so net leverage fell by 0.11x to 1.46x and gross leverage was broadly unchanged at 2.00x.
Interest coverage improved to 14.72x from 12.34x, and FFO to debt rose by 0.6 points to 39.6% on FFO up 4.8% to EUR 3.0bn.
Free cash flow declined by 10.2% to EUR 1.7bn as capex intensity rose by 2.6 points to 16.9%, taking FCF to debt down to 22.9%.

## Operating performance

Passengers rose by 3.9% to 321.6m, with traffic growth of 3.9% below the 9.2% of the prior year.
Revenue per passenger increased by 4.8% to EUR 19.52, while aeronautical revenue per passenger was stable at EUR 10.25.
Non-aeronautical activities made up 47.5% of revenue, up 2.1 points from 45.4%.

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, but total liquidity fell by 6.3% to EUR 4.3bn as undrawn committed facilities declined by 18.7% to EUR 2.2bn.
Liquidity to revenue fell by 11.1 points to 68.4%, while cash liquidity to revenue rose by 1.0 point to 32.6%.

## Peer positioning

Aena has the highest EBITDA margin in the airport group (1st of 3), at 60.3% against a peer median of 36.5%.
Net leverage of 1.46x and gross leverage of 2.00x are in line with the peer medians of 1.46x and 2.00x respectively, ranking 2nd of 3 on net leverage.
Cash liquidity to revenue is the strongest of the group (1st of 3), at 32.6% against a median of 30.1%, and traffic growth of 3.9% ranks 1st of 3.
FFO to debt of 39.6% and FCF to debt of 22.9% are in line with the peer medians of 39.6% and 22.9%, while capex intensity of 16.9% is below the peer median of 18.2%.

## Watch items

- Cash generation: FCF to debt fell by 3.4 points to 22.9% as capex intensity rose by 2.6 points to 16.9%.
- Liquidity: liquidity to revenue fell by 11.1 points to 68.4%, and undrawn committed facilities declined by 18.7% to EUR 2.2bn.
- Margins: the EBITDA margin eased by 0.6 points to 60.3%, with aeronautical revenue per passenger broadly unchanged at EUR 10.25.
- Traffic: traffic growth slowed by 5.3 points to 3.9%, in line with the peer median of 3.5%.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 11,349 / 3,489 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, ended FY2025 with revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}} and net leverage down to {{net_leverage@FY2025}} from {{net_leverage@FY2024}}.
- The EBITDA margin eased by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, still the highest of the airport peers ({{ebitda_margin.peer_rank@2025}}).
- The point to watch is liquidity: total liquidity fell by {{liquidity.change@FY2025}} to {{liquidity@FY2025}} as undrawn committed facilities declined by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, on revenue up {{revenue.change@FY2025}}.
- Net debt was stable at {{net_debt@FY2025}} while total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, so net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} and gross leverage was broadly unchanged at {{gross_leverage@FY2025}}.
- Interest coverage improved to {{interest_coverage@FY2025}} from {{interest_coverage@FY2024}}, and FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} on FFO up {{ffo.change@FY2025}} to {{ffo@FY2025}}.
- Free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, taking FCF to debt down to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, with traffic growth of {{traffic_growth@FY2025}} below the {{traffic_growth@FY2024}} of the prior year.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2025}} to {{revenue_per_passenger@FY2025}}, while aeronautical revenue per passenger was stable at {{aero_revenue_per_passenger@FY2025}}.
- Non-aeronautical activities made up {{non_aero_share@FY2025}} of revenue, up {{non_aero_share.change@FY2025}} from {{non_aero_share@FY2024}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, but total liquidity fell by {{liquidity.change@FY2025}} to {{liquidity@FY2025}} as undrawn committed facilities declined by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}.
- Liquidity to revenue fell by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}, while cash liquidity to revenue rose by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.

`peer_positioning`

- Aena has the highest EBITDA margin in the airport group ({{ebitda_margin.peer_rank@2025}}), at {{ebitda_margin@FY2025}} against a peer median of {{ebitda_margin.peer_median@2025}}.
- Net leverage of {{net_leverage@FY2025}} and gross leverage of {{gross_leverage@FY2025}} are in line with the peer medians of {{net_leverage.peer_median@2025}} and {{gross_leverage.peer_median@2025}} respectively, ranking {{net_leverage.peer_rank@2025}} on net leverage.
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), at {{cash_liquidity_to_revenue@FY2025}} against a median of {{cash_liquidity_to_revenue.peer_median@2025}}, and traffic growth of {{traffic_growth@FY2025}} ranks {{traffic_growth.peer_rank@2025}}.
- FFO to debt of {{ffo_to_debt@FY2025}} and FCF to debt of {{fcf_to_debt@FY2025}} are in line with the peer medians of {{ffo_to_debt.peer_median@2025}} and {{fcf_to_debt.peer_median@2025}}, while capex intensity of {{capex_intensity@FY2025}} is below the peer median of {{capex_intensity.peer_median@2025}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Liquidity: liquidity to revenue fell by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}, and undrawn committed facilities declined by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}.
- Margins: the EBITDA margin eased by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, with aeronautical revenue per passenger broadly unchanged at {{aero_revenue_per_passenger@FY2025}}.
- Traffic: traffic growth slowed by {{traffic_growth.change@FY2025}} to {{traffic_growth@FY2025}}, in line with the peer median of {{traffic_growth.peer_median@2025}}.
