# Aena, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `1555da187909` ([fact sheet](../factsheets/aena_FY2024.md)). Tokens: 21,920 in, 3,820 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, had a stronger FY2024 as revenue rose by 14.4% to EUR 5.8bn and net leverage fell to 1.57x from 2.06x.
The EBITDA margin widened by 0.9 points to 60.9%, the highest of the airport peers (1st of 3).
The point to watch is liquidity: cash liquidity to revenue fell by 15.3 points to 31.6%, in line with the peer median.

## Credit metrics

EBITDA increased by 16.1% to EUR 3.5bn on revenue up 14.4% at EUR 5.8bn, and operating profit rose by 20.9% to EUR 2.7bn.
Total debt was reduced by 14.8% to EUR 7.3bn and net debt by 11.6% to EUR 5.5bn, so gross leverage fell by 0.76x to 2.08x.
Cash generation strengthened: FFO rose by 20.3% to EUR 2.9bn, taking FFO to debt up by 11.3 points to 39.0%.
Free cash flow rose by 129.9% to EUR 1.9bn as capex intensity eased by 13.1 points to 14.3%, lifting FCF to debt to 26.3%.
Interest coverage narrowed by 0.27x to 12.34x, still in line with the peer median.

## Operating performance

Passengers rose by 9.2% to 309.4m, although traffic growth slowed by 7.0 points to 9.2%, still above the peer median of 8.3%.
Revenue per passenger increased by 4.7% to EUR 18.63, with aeronautical revenue per passenger up 4.1% to EUR 10.17.
The non-aeronautical share of revenue was broadly unchanged at 45.4%, a change of 0.3 points.

## Liquidity and funding

Liquidity fell by 6.8% to EUR 4.6bn, of which EUR 2.8bn in undrawn committed facilities.
Undrawn committed facilities increased by 8.0%, partly offsetting cash and cash-like investments that fell by 22.9% to EUR 1.8bn.
Liquidity to revenue declined by 18.1 points to 79.5%, and cash liquidity to revenue by 15.3 points to 31.6%.

## Peer positioning

Aena has the highest EBITDA margin among the airport peers (1st of 3), at 60.9% against a median of 42.0%.
Leverage sits at the group median, with net leverage of 1.57x (2nd of 3) and gross leverage of 2.08x (2nd of 3).
Cash flow metrics are in line with the median, with FFO to debt of 39.0% and FCF to debt of 26.3%, both ranking 2nd of 3.
Capex intensity of 14.3% is below the peer median of 16.1%, and traffic growth ranks 1st of 2 at 9.2%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 15.3 points to 31.6%, in line with the peer median of 31.6% but a thinner buffer than a year earlier.
- Coverage: interest coverage eased by 0.27x to 12.34x, in line with the peer median of 12.34x.
- Traffic: traffic growth slowed by 7.0 points to 9.2%, so revenue per passenger of EUR 18.63 carries more of the earnings burden.
- Investment: capex intensity of 14.3% is below the peer median of 16.1%, leaving room for capital spending to absorb more cash as the investment plan proceeds.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 1 errors | 11,348 / 3,272 |
| 2 | watch_items | passed | 10,572 / 548 |

### Errors found, by try

Try 1:

- [rule 4] watch_items, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, had a stronger FY2024 as revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}} and net leverage fell to {{net_leverage@FY2024}} from {{net_leverage@FY2023}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, the highest of the airport peers ({{ebitda_margin.peer_rank@2024}}).
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, in line with the peer median.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} at {{revenue@FY2024}}, and operating profit rose by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt was reduced by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, so gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, taking FFO to debt up by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}.
- Free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity eased by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, lifting FCF to debt to {{fcf_to_debt@FY2024}}.
- Interest coverage narrowed by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, still in line with the peer median.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, although traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}}, still above the peer median of {{traffic_growth.peer_median@2024}}.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2024}} to {{revenue_per_passenger@FY2024}}, with aeronautical revenue per passenger up {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}.
- The non-aeronautical share of revenue was broadly unchanged at {{non_aero_share@FY2024}}, a change of {{non_aero_share.change@FY2024}}.

`liquidity_funding`

- Liquidity fell by {{liquidity.change@FY2024}} to {{liquidity@FY2024}}, of which {{undrawn_facilities@FY2024}} in undrawn committed facilities.
- Undrawn committed facilities increased by {{undrawn_facilities.change@FY2024}}, partly offsetting cash and cash-like investments that fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.
- Liquidity to revenue declined by {{liquidity_to_revenue.change@FY2024}} to {{liquidity_to_revenue@FY2024}}, and cash liquidity to revenue by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.

`peer_positioning`

- Aena has the highest EBITDA margin among the airport peers ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2024}} against a median of {{ebitda_margin.peer_median@2024}}.
- Leverage sits at the group median, with net leverage of {{net_leverage@FY2024}} ({{net_leverage.peer_rank@2024}}) and gross leverage of {{gross_leverage@FY2024}} ({{gross_leverage.peer_rank@2024}}).
- Cash flow metrics are in line with the median, with FFO to debt of {{ffo_to_debt@FY2024}} and FCF to debt of {{fcf_to_debt@FY2024}}, both ranking {{ffo_to_debt.peer_rank@2024}}.
- Capex intensity of {{capex_intensity@FY2024}} is below the peer median of {{capex_intensity.peer_median@2024}}, and traffic growth ranks {{traffic_growth.peer_rank@2024}} at {{traffic_growth@FY2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, in line with the peer median of {{cash_liquidity_to_revenue.peer_median@2024}} but a thinner buffer than a year earlier.
- Coverage: interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, in line with the peer median of {{interest_coverage.peer_median@2024}}.
- Traffic: traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}}, so revenue per passenger of {{revenue_per_passenger@FY2024}} carries more of the earnings burden.
- Investment: capex intensity of {{capex_intensity@FY2024}} is below the peer median of {{capex_intensity.peer_median@2024}}, leaving room for capital spending to absorb more cash as the investment plan proceeds.
