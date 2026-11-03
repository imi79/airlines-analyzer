# Flughafen Wien, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `4a8191ee7ea5` ([fact sheet](../factsheets/vie_FY2025.md)). Tokens: 23,277 in, 5,117 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport operator, grew revenue by 7.2% to EUR 1.1bn in FY2025, but earnings fell and the EBITDA margin narrowed by 5.5 points to 36.5%.
Net leverage stayed broadly unchanged at -0.13x, a net cash position, with total debt flat at EUR 55.9m.
The point to watch is cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex intensity rose by 8.0 points to 24.1%.

## Credit metrics

EBITDA declined by 6.7% to EUR 412m and operating profit by 8.7% to EUR 280m, and the EBITDA margin fell by 5.5 points to 36.5%.
Gross leverage was stable at 0.14x and total debt was broadly unchanged at EUR 55.9m, while net debt moved to EUR -54.4m and net leverage stayed at -0.13x.
Interest coverage improved to 208.53x, up 6.66x, on a very small debt stock.
Cash flow against debt weakened: FFO fell by 31.0% to EUR 247m, taking FFO to debt down by 202.1 points to 441.9%.
FCF to debt fell by 382.0 points to 110.4%, with capex intensity at 24.1% absorbing most of the cash generated.

## Operating performance

Passengers rose by 2.8% to 32.6m, although traffic growth slowed by 4.5 points to 2.8%.
Revenue per passenger increased by 4.3% to EUR 34.63, with aeronautical revenue per passenger up 3.1% to EUR 16.05.
Non-aeronautical activities made up 53.6% of revenue, up 0.5 points, which supports the resilience of the top line.

## Liquidity and funding

Cash and cash-like investments rose by 51.5% to EUR 110m, and cash liquidity to revenue increased by 2.9 points to 9.8%.
The buffer is modest in scale: cash liquidity of EUR 110m covers a small share of revenue, and the company carries total debt of only EUR 55.9m.
Funding needs are limited by the net cash position of EUR -54.4m, so refinancing risk is low relative to the airport peers.

## Peer positioning

Flughafen Wien has the lowest net leverage in the airport group (1st of 3), at -0.13x against a peer median of 1.46x.
It also leads the group on gross leverage (1st of 3), interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3).
The EBITDA margin of 36.5% is in line with the peer median of 36.5%, ranking 2nd of 3.
Cash liquidity to revenue of 9.8% is the weakest of the group (3rd of 3), well below the peer median of 30.1%.

## Watch items

- Cash generation: FCF to debt fell by 382.0 points to 110.4% and FFO to debt by 202.1 points to 441.9%, so the earnings-to-cash conversion is the metric to track.
- Investment: capex intensity rose by 8.0 points to 24.1%, above the peer median of 18.2%, and free cash flow declined by 77.5% to EUR 61.7m.
- Margins: the EBITDA margin narrowed by 5.5 points to 36.5%, now only in line with the peer median of 36.5%.
- Liquidity: cash liquidity to revenue of 9.8% is the weakest of the group (3rd of 3) against a peer median of 30.1%, a thin buffer for an investment-heavy year.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 11,038 / 3,070 |
| 2 | credit_metrics, peer_positioning, watch_items | passed | 12,239 / 2,047 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 1: 'narrowed' needs a 'down' claim on a figure in the same clause
- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'
- [rule 4] watch_items, sentence 2: 'fall' needs a 'down' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport operator, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, but earnings fell and the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Net leverage stayed broadly unchanged at {{net_leverage@FY2025}}, a net cash position, with total debt flat at {{total_debt@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`credit_metrics`

- EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, and the EBITDA margin fell by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Gross leverage was stable at {{gross_leverage@FY2025}} and total debt was broadly unchanged at {{total_debt@FY2025}}, while net debt moved to {{net_debt@FY2025}} and net leverage stayed at {{net_leverage@FY2025}}.
- Interest coverage improved to {{interest_coverage@FY2025}}, up {{interest_coverage.change@FY2025}}, on a very small debt stock.
- Cash flow against debt weakened: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, taking FFO to debt down by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with capex intensity at {{capex_intensity@FY2025}} absorbing most of the cash generated.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, although traffic growth slowed by {{traffic_growth.change@FY2025}} to {{traffic_growth@FY2025}}.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2025}} to {{revenue_per_passenger@FY2025}}, with aeronautical revenue per passenger up {{aero_revenue_per_passenger.change@FY2025}} to {{aero_revenue_per_passenger@FY2025}}.
- Non-aeronautical activities made up {{non_aero_share@FY2025}} of revenue, up {{non_aero_share.change@FY2025}}, which supports the resilience of the top line.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- The buffer is modest in scale: cash liquidity of {{cash_liquidity@FY2025}} covers a small share of revenue, and the company carries total debt of only {{total_debt@FY2025}}.
- Funding needs are limited by the net cash position of {{net_debt@FY2025}}, so refinancing risk is low relative to the airport peers.

`peer_positioning`

- Flughafen Wien has the lowest net leverage in the airport group ({{net_leverage.peer_rank@2025}}), at {{net_leverage@FY2025}} against a peer median of {{net_leverage.peer_median@2025}}.
- It also leads the group on gross leverage ({{gross_leverage.peer_rank@2025}}), interest coverage ({{interest_coverage.peer_rank@2025}}), FFO to debt ({{ffo_to_debt.peer_rank@2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@2025}}).
- The EBITDA margin of {{ebitda_margin@FY2025}} is in line with the peer median of {{ebitda_margin.peer_median@2025}}, ranking {{ebitda_margin.peer_rank@2025}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), well below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} and FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, so the earnings-to-cash conversion is the metric to track.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@2025}}, and free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}}.
- Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, now only in line with the peer median of {{ebitda_margin.peer_median@2025}}.
- Liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}) against a peer median of {{cash_liquidity_to_revenue.peer_median@2025}}, a thin buffer for an investment-heavy year.
