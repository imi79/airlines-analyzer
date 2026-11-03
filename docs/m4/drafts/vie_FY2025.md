# Flughafen Wien, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `050c63327889` ([fact sheet](../factsheets/vie_FY2025.md)). Tokens: 22,987 in, 4,508 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport operator, grew revenue by 7.2% to EUR 1.1bn in FY2025, but earnings fell and the EBITDA margin narrowed by 5.5 points to 36.5%.
Net leverage stayed flat at -0.13x, a net cash position, with total debt broadly unchanged at EUR 55.9m.
The point to watch is cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex intensity rose by 8.0 points to 24.1%.

## Credit metrics

EBITDA declined by 6.7% to EUR 412m, and operating profit fell by 8.7% to EUR 280m.
Gross leverage was stable at 0.14x and net debt moved to EUR -54.4m, so the balance sheet carries no meaningful debt burden.
Interest coverage improved to 208.53x, up 6.66x, reflecting the very low interest bill on total debt of EUR 55.9m.
Cash flow against debt weakened: FFO fell by 31.0% to EUR 247m, taking FFO to debt down by 202.1 points to 441.9%.
FCF to debt fell by 382.0 points to 110.4%, as capex intensity rose to 24.1%.

## Operating performance

Passengers rose by 2.8% to 32.6m, although traffic growth of 2.8% was below the peer median of 3.5%.
Revenue per passenger increased by 4.3% to EUR 34.63, while aeronautical revenue per passenger was stable at EUR 16.05.
Non-aeronautical activities made up 53.6% of revenue, up 1.7 points, which supports the resilience of the revenue base.

## Liquidity and funding

Cash and cash-like investments rose by 51.5% to EUR 110m, and cash liquidity increased by 51.5% to EUR 110m.
Cash liquidity to revenue rose by 2.9 points to 9.8%, still well below the peer median of 30.1%.
Total debt of EUR 55.9m is small against cash of EUR 110m, so refinancing risk is limited and the funding question is the pace of capital spending rather than maturities.

## Peer positioning

Flughafen Wien has the lowest net leverage in the airport group (1st of 3), at -0.13x against a peer median of 1.46x.
It also leads the group on gross leverage (1st of 3), interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3).
The EBITDA margin of 36.5% is in line with the peer median of 36.5%, ranking 2nd of 3.
Cash liquidity to revenue is the weakest of the group (3rd of 3), and traffic growth ranks last (3rd of 3).

## Watch items

- Cash generation: FFO fell by 31.0% to EUR 247m and free cash flow by 77.5% to EUR 61.7m, so the buffer against capital spending is thinner.
- Investment: capex intensity rose by 8.0 points to 24.1%, above the peer median of 18.2%, which will keep free cash flow under pressure while the programme runs.
- Margins: the EBITDA margin narrowed by 5.5 points to 36.5%, leaving it in line with the peer median.
- Liquidity: cash liquidity to revenue of 9.8% is below the peer median of 30.1% and the weakest in the group (3rd of 3), so the cash buffer is thin relative to revenue.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 11,077 / 2,936 |
| 2 | liquidity_funding, peer_positioning, watch_items | passed | 11,910 / 1,572 |

### Errors found, by try

Try 1:

- [rule 5] liquidity_funding, sentence 1: cash_liquidity.change@FY2025 is listed in the form but not used in the text
- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'
- [rule 4] watch_items, sentence 3: 'ahead' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport operator, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, but earnings fell and the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Net leverage stayed flat at {{net_leverage@FY2025}}, a net cash position, with total debt broadly unchanged at {{total_debt@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`credit_metrics`

- EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit fell by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Gross leverage was stable at {{gross_leverage@FY2025}} and net debt moved to {{net_debt@FY2025}}, so the balance sheet carries no meaningful debt burden.
- Interest coverage improved to {{interest_coverage@FY2025}}, up {{interest_coverage.change@FY2025}}, reflecting the very low interest bill on total debt of {{total_debt@FY2025}}.
- Cash flow against debt weakened: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, taking FFO to debt down by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, as capex intensity rose to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, although traffic growth of {{traffic_growth@FY2025}} was below the peer median of {{traffic_growth.peer_median@2025}}.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2025}} to {{revenue_per_passenger@FY2025}}, while aeronautical revenue per passenger was stable at {{aero_revenue_per_passenger@FY2025}}.
- Non-aeronautical activities made up {{non_aero_share@FY2025}} of revenue, up {{non_aero_share.change@FY2025}}, which supports the resilience of the revenue base.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity increased by {{cash_liquidity.change@FY2025}} to {{cash_liquidity@FY2025}}.
- Cash liquidity to revenue rose by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, still well below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.
- Total debt of {{total_debt@FY2025}} is small against cash of {{cash_like@FY2025}}, so refinancing risk is limited and the funding question is the pace of capital spending rather than maturities.

`peer_positioning`

- Flughafen Wien has the lowest net leverage in the airport group ({{net_leverage.peer_rank@2025}}), at {{net_leverage@FY2025}} against a peer median of {{net_leverage.peer_median@2025}}.
- It also leads the group on gross leverage ({{gross_leverage.peer_rank@2025}}), interest coverage ({{interest_coverage.peer_rank@2025}}), FFO to debt ({{ffo_to_debt.peer_rank@2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@2025}}).
- The EBITDA margin of {{ebitda_margin@FY2025}} is in line with the peer median of {{ebitda_margin.peer_median@2025}}, ranking {{ebitda_margin.peer_rank@2025}}.
- Cash liquidity to revenue is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), and traffic growth ranks last ({{traffic_growth.peer_rank@2025}}).

`watch_items`

- Cash generation: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}} and free cash flow by {{fcf.change@FY2025}} to {{fcf@FY2025}}, so the buffer against capital spending is thinner.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@2025}}, which will keep free cash flow under pressure while the programme runs.
- Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, leaving it in line with the peer median.
- Liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}} and the weakest in the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), so the cash buffer is thin relative to revenue.
