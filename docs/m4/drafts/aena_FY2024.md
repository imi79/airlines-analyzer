# Aena, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v3`, fact sheet `8f7fb9ffbcb4` ([fact sheet](../factsheets/aena_FY2024.md)). Tokens: 32,452 in, 4,749 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, ended FY2024 with a stronger credit profile as revenue rose by 14.4% to EUR 5.8bn and EBITDA reached EUR 3.5bn.
Net leverage fell by 0.49x to 1.57x, with the EBITDA margin widening by 0.9 points to 60.9%.
The main point to watch is liquidity: cash liquidity to revenue fell by 15.3 points to 31.6% as cash and cash-like investments declined by 22.9% to EUR 1.8bn.

## Credit metrics

EBITDA increased by 16.1% to EUR 3.5bn on revenue up 14.4% at EUR 5.8bn, lifting the EBITDA margin to 60.9%.
Total debt was reduced by 14.8% to EUR 7.3bn and net debt by 11.6% to EUR 5.5bn, so gross leverage fell by 0.76x to 2.08x.
Cash generation strengthened: FFO rose by 20.3% to EUR 2.9bn, taking FFO to debt up by 11.3 points to 39.0%.
Free cash flow rose by 129.9% to EUR 1.9bn, with FCF to debt up by 16.6 points to 26.3% as capex intensity eased by 13.1 points to 14.3%.
Interest coverage weakened by 0.27x to 12.34x, still a comfortable level against the debt service.

## Operating performance

Passengers rose by 9.2% to 309.3m, although traffic growth slowed by 7.0 points to 9.2% from the rebound of the prior year.
Revenue per passenger increased by 4.7% to EUR 18.63, with aeronautical revenue per passenger up 4.1% at EUR 10.18.
Non-aeronautical activities made up 45.4% of revenue, broadly unchanged on the prior year (0.3 points).

## Liquidity and funding

Cash and cash-like investments fell by 22.9% to EUR 1.8bn, and cash liquidity to revenue declined by 15.3 points to 31.6%.
The cash buffer is thinner than a year earlier, when cash liquidity stood at EUR 2.4bn and liquidity at EUR 4.9bn, including EUR 2.6bn of undrawn committed facilities.
Cash liquidity to revenue of 31.6% is in line with the airport peer median of 31.6%, ranking 2nd of 3.

## Peer positioning

Aena has the highest EBITDA margin among the airport peers (1st of 3), at 60.9% against a median of 42.0%.
Net leverage of 1.57x and gross leverage of 2.08x are in line with the peer medians of 1.57x and 2.08x respectively, ranking 2nd of 3 on net leverage.
FFO to debt of 39.0% and FCF to debt of 26.3% sit at the peer medians of 39.0% and 26.3%, while capex intensity of 14.3% is below the peer median of 16.1%.
Traffic growth of 9.2% is above the peer median of 8.3%, the strongest of the group (1st of 2).

## Watch items

- Liquidity: cash liquidity to revenue fell by 15.3 points to 31.6%, in line with the peer median but with a smaller cash cushion than a year earlier.
- Coverage: interest coverage eased by 0.27x to 12.34x, in line with the peer median of 12.34x.
- Traffic: traffic growth slowed by 7.0 points to 9.2%, so revenue per passenger of EUR 18.63 carries more of the earnings burden.
- Investment: capex intensity of 14.3% is below the peer median of 16.1%, leaving headroom for capital spending at this level.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 11,117 / 3,305 |
| 2 | liquidity_funding, watch_items | 1 errors | 11,036 / 940 |
| 3 | watch_items | passed | 10,299 / 504 |

### Errors found, by try

Try 1:

- [rule 4] liquidity_funding, sentence 3: 'in line' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'rise' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] watch_items, sentence 4: 'increase' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, ended FY2024 with a stronger credit profile as revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}} and EBITDA reached {{ebitda@FY2024}}.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, with the EBITDA margin widening by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} as cash and cash-like investments declined by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} at {{revenue@FY2024}}, lifting the EBITDA margin to {{ebitda_margin@FY2024}}.
- Total debt was reduced by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, so gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, taking FFO to debt up by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}.
- Free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}}, with FCF to debt up by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}} as capex intensity eased by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.
- Interest coverage weakened by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, still a comfortable level against the debt service.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, although traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}} from the rebound of the prior year.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2024}} to {{revenue_per_passenger@FY2024}}, with aeronautical revenue per passenger up {{aero_revenue_per_passenger.change@FY2024}} at {{aero_revenue_per_passenger@FY2024}}.
- Non-aeronautical activities made up {{non_aero_share@FY2024}} of revenue, broadly unchanged on the prior year ({{non_aero_share.change@FY2024}}).

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- The cash buffer is thinner than a year earlier, when cash liquidity stood at {{cash_liquidity@FY2023}} and liquidity at {{liquidity@FY2023}}, including {{undrawn_facilities@FY2023}} of undrawn committed facilities.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} is in line with the airport peer median of {{cash_liquidity_to_revenue.peer_median@2024}}, ranking {{cash_liquidity_to_revenue.peer_rank@2024}}.

`peer_positioning`

- Aena has the highest EBITDA margin among the airport peers ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2024}} against a median of {{ebitda_margin.peer_median@2024}}.
- Net leverage of {{net_leverage@FY2024}} and gross leverage of {{gross_leverage@FY2024}} are in line with the peer medians of {{net_leverage.peer_median@2024}} and {{gross_leverage.peer_median@2024}} respectively, ranking {{net_leverage.peer_rank@2024}} on net leverage.
- FFO to debt of {{ffo_to_debt@FY2024}} and FCF to debt of {{fcf_to_debt@FY2024}} sit at the peer medians of {{ffo_to_debt.peer_median@2024}} and {{fcf_to_debt.peer_median@2024}}, while capex intensity of {{capex_intensity@FY2024}} is below the peer median of {{capex_intensity.peer_median@2024}}.
- Traffic growth of {{traffic_growth@FY2024}} is above the peer median of {{traffic_growth.peer_median@2024}}, the strongest of the group ({{traffic_growth.peer_rank@2024}}).

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, in line with the peer median but with a smaller cash cushion than a year earlier.
- Coverage: interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, in line with the peer median of {{interest_coverage.peer_median@2024}}.
- Traffic: traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}}, so revenue per passenger of {{revenue_per_passenger@FY2024}} carries more of the earnings burden.
- Investment: capex intensity of {{capex_intensity@FY2024}} is below the peer median of {{capex_intensity.peer_median@2024}}, leaving headroom for capital spending at this level.
