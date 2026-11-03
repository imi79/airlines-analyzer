# Groupe ADP, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `4215457cfaae` ([fact sheet](../factsheets/adp_FY2024.md)). Tokens: 21,224 in, 4,456 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the French airport group, grew revenue by 12.1% to EUR 6.2bn in FY2024, but earnings quality weakened as the EBITDA margin fell by 2.0 points to 33.7%.
Net leverage was stable at 4.13x, with net debt up 8.2% to EUR 8.6bn and gross leverage down to 5.14x.
The main point to watch is cash generation: free cash flow fell by 50.3% to EUR 355m as capex intensity rose by 3.1 points to 19.0%.

## Credit metrics

EBITDA increased by 6.0% to EUR 2.1bn on revenue up 12.1%, but operating profit fell by 20.0% to EUR 994m.
Total debt rose by 2.7% to EUR 10.7bn, while gross leverage narrowed by 0.16x to 5.14x and net leverage was stable at 4.13x.
Interest coverage improved by 0.23x to 6.97x, but FFO to debt was stable at 14.0% with FFO broadly unchanged at EUR 1.5bn.
FCF to debt fell by 3.6 points to 3.3%, as free cash flow declined by 50.3% to EUR 355m and capex intensity rose to 19.0%.

## Operating performance

Passengers reached 103.4m in FY2024, with revenue per passenger of EUR 59.55.
Revenue rose by 12.1% to EUR 6.2bn, while the EBITDA margin fell by 2.0 points to 33.7%, so cost growth outpaced the top line.
Capex intensity rose by 3.1 points to 19.0%, above the peer median of 16.1%, reflecting the investment programme across the airport estate.

## Liquidity and funding

Cash and cash-like investments fell by 14.8% to EUR 2.1bn, and cash liquidity declined by the same 14.8% to EUR 2.1bn.
Cash liquidity to revenue fell by 10.8 points to 34.0%, still above the peer median of 31.6%.
Total debt of EUR 10.7bn against cash of EUR 2.1bn leaves net debt at EUR 8.6bn, so the buffer covers a modest share of the debt stack.

## Peer positioning

Groupe ADP has the weakest EBITDA margin in the airport peer group (3rd of 3), at 33.7% against a median of 42.0%.
Leverage is the highest of the group, with net leverage of 4.13x against a peer median of 1.57x (3rd of 3) and gross leverage of 5.14x against 2.08x.
Cash generation trails the group: FFO to debt of 14.0% and FCF to debt of 3.3% both rank 3rd of 3 against medians of 39.0% and 26.3% respectively.
The offset is liquidity: cash liquidity to revenue of 34.0% is the strongest of the group (1st of 3), above the median of 31.6%.

## Watch items

- Cash generation: FCF to debt fell by 3.6 points to 3.3%, well below the peer median of 26.3%, as free cash flow declined by 50.3% to EUR 355m.
- Investment: capex intensity rose by 3.1 points to 19.0%, above the peer median of 16.1%, which keeps pressure on free cash flow.
- Liquidity: cash and cash-like investments fell by 14.8% to EUR 2.1bn, taking cash liquidity to revenue down by 10.8 points to 34.0%, still above the peer median of 31.6%.
- Profitability: the EBITDA margin of 33.7% is the weakest in the peer group (3rd of 3) and below the median of 42.0%, with profit for the year down 34.2% to EUR 516m.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 10,606 / 3,306 |
| 2 | operating_performance, watch_items | passed | 10,618 / 1,150 |

### Errors found, by try

Try 1:

- [rule 4] operating_performance, sentence 3: 'behind' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule 1] watch_items, sentence 1: word that states a number: 'halved'

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the French airport group, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, but earnings quality weakened as the EBITDA margin fell by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Net leverage was stable at {{net_leverage@FY2024}}, with net debt up {{net_debt.change@FY2024}} to {{net_debt@FY2024}} and gross leverage down to {{gross_leverage@FY2024}}.
- The main point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, while gross leverage narrowed by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} and net leverage was stable at {{net_leverage@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, but FFO to debt was stable at {{ffo_to_debt@FY2024}} with FFO broadly unchanged at {{ffo@FY2024}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, as free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}} and capex intensity rose to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers reached {{passengers@FY2024}} in FY2024, with revenue per passenger of {{revenue_per_passenger@FY2024}}.
- Revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}}, while the EBITDA margin fell by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, so cost growth outpaced the top line.
- Capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the peer median of {{capex_intensity.peer_median@2024}}, reflecting the investment programme across the airport estate.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity declined by the same {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, still above the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- Total debt of {{total_debt@FY2024}} against cash of {{cash_like@FY2024}} leaves net debt at {{net_debt@FY2024}}, so the buffer covers a modest share of the debt stack.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin in the airport peer group ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2024}} against a median of {{ebitda_margin.peer_median@2024}}.
- Leverage is the highest of the group, with net leverage of {{net_leverage@FY2024}} against a peer median of {{net_leverage.peer_median@2024}} ({{net_leverage.peer_rank@2024}}) and gross leverage of {{gross_leverage@FY2024}} against {{gross_leverage.peer_median@2024}}.
- Cash generation trails the group: FFO to debt of {{ffo_to_debt@FY2024}} and FCF to debt of {{fcf_to_debt@FY2024}} both rank {{ffo_to_debt.peer_rank@2024}} against medians of {{ffo_to_debt.peer_median@2024}} and {{fcf_to_debt.peer_median@2024}} respectively.
- The offset is liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), above the median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, well below the peer median of {{fcf_to_debt.peer_median@2024}}, as free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the peer median of {{capex_intensity.peer_median@2024}}, which keeps pressure on free cash flow.
- Liquidity: cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, still above the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- Profitability: the EBITDA margin of {{ebitda_margin@FY2024}} is the weakest in the peer group ({{ebitda_margin.peer_rank@2024}}) and below the median of {{ebitda_margin.peer_median@2024}}, with profit for the year down {{profit.change@FY2024}} to {{profit@FY2024}}.
