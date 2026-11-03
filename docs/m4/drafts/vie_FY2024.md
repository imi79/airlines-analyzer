# Flughafen Wien, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `c8f722347dfb` ([fact sheet](../factsheets/vie_FY2024.md)). Tokens: 25,121 in, 6,440 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport operator, grew revenue by 13.0% to EUR 1.1bn in FY2024, with EBITDA up 12.3% to EUR 442m.
The EBITDA margin was broadly unchanged at 42.0%, and net leverage stayed at a net cash position of -0.04x, the lowest of the airport peers (1st of 3).
The main point to watch is liquidity: cash liquidity to revenue fell by 1.0 point to 6.9%, well below the peer median of 31.6%.

## Credit metrics

EBITDA rose by 12.3% to EUR 442m and operating profit by 16.9% to EUR 306m, on revenue up 13.0%.
Total debt was stable at EUR 55.6m, so gross leverage held at 0.13x, below the peer median, and net debt remained negative at EUR -17.2m.
Interest coverage improved to 201.87x, up 168.89x, reflecting a very low interest burden relative to EBITDA.
FFO rose by 3.4% to EUR 358m, lifting FFO to debt by 17.8 points to 644.0%.
Free cash flow declined by 4.6% to EUR 274m as capex intensity rose by 5.6 points to 16.1%, leaving FCF to debt lower at 492.4%.

## Operating performance

Passengers rose by 7.3% to 31.7m, with traffic growth of 7.3% below the peer median of 8.3%.
Revenue per passenger increased by 5.3% to EUR 33.21, with aeronautical revenue per passenger up 10.4% to EUR 15.98.
The non-aeronautical share of revenue fell by 2.2 points to 51.9%, so commercial income contributed less to the revenue base.

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at EUR 72.8m, a change of 1.6%.
Cash liquidity to revenue fell by 1.0 point to 6.9%, against a peer median of 31.6%.
The cash buffer is small relative to revenue, so the funding profile rests on the low absolute debt of EUR 55.6m rather than on a large liquidity reserve.

## Peer positioning

Flughafen Wien ranks at the top of the airport peers on net leverage (1st of 3) and gross leverage (1st of 3), at -0.04x and 0.13x against medians of 1.57x and 2.08x.
It also leads on cash generation, with FFO to debt of 644.0% and FCF to debt of 492.4% (1st of 3 and 1st of 3), and on interest coverage of 201.87x (1st of 3).
The EBITDA margin of 42.0% is in line with the peer median of 42.0%, ranking 2nd of 3.
Cash liquidity to revenue is the weakest of the group (3rd of 3), and traffic growth ranks 2nd of 2 at 7.3% against a peer median of 8.3%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 1.0 point to 6.9%, the weakest of the airport peers (3rd of 3).
- Investment: capex intensity rose by 5.6 points to 16.1%, in line with the peer median, and free cash flow fell by 4.6% to EUR 274m.
- Traffic: traffic growth of 7.3% sits below the peer median of 8.3%, which limits the operating leverage behind the revenue base.
- Revenue mix: the non-aeronautical share fell by 2.2 points to 51.9%, so revenue depends more on regulated aeronautical charges.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 9 errors | 11,016 / 3,390 |
| 2 | snapshot, credit_metrics, operating_performance, peer_positioning, watch_items | passed | 14,105 / 3,050 |

### Errors found, by try

Try 1:

- [rule 3] snapshot, sentence 2: 'better' claimed on net_leverage@FY2024, but it is neither better nor worse
- [rule 3] credit_metrics, sentence 2: 'better' claimed on gross_leverage@FY2024, but it is neither better nor worse
- [rule 5] operating_performance, sentence 1: traffic_growth@FY2024 is listed in the form but not used in the text
- [rule 1] peer_positioning, sentence 1: word that states a number: 'first'
- [rule 3] peer_positioning, sentence 1: 'better' claimed on net_leverage@FY2024, but it is neither better nor worse
- [rule 3] peer_positioning, sentence 1: 'better' claimed on gross_leverage@FY2024, but it is neither better nor worse
- [rule 3] peer_positioning, sentence 2: 'better' claimed on fcf_to_debt@FY2024, but it is worse
- [rule 5] watch_items, sentence 3: traffic_growth@FY2024 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport operator, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, with EBITDA up {{ebitda.change@FY2024}} to {{ebitda@FY2024}}.
- The EBITDA margin was broadly unchanged at {{ebitda_margin@FY2024}}, and net leverage stayed at a net cash position of {{net_leverage@FY2024}}, the lowest of the airport peers ({{net_leverage.peer_rank@2024}}).
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, well below the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} and operating profit by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}, on revenue up {{revenue.change@FY2024}}.
- Total debt was stable at {{total_debt@FY2024}}, so gross leverage held at {{gross_leverage@FY2024}}, below the peer median, and net debt remained negative at {{net_debt@FY2024}}.
- Interest coverage improved to {{interest_coverage@FY2024}}, up {{interest_coverage.change@FY2024}}, reflecting a very low interest burden relative to EBITDA.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, lifting FFO to debt by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}.
- Free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, leaving FCF to debt lower at {{fcf_to_debt@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, with traffic growth of {{traffic_growth@FY2024}} below the peer median of {{traffic_growth.peer_median@2024}}.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2024}} to {{revenue_per_passenger@FY2024}}, with aeronautical revenue per passenger up {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}.
- The non-aeronautical share of revenue fell by {{non_aero_share.change@FY2024}} to {{non_aero_share@FY2024}}, so commercial income contributed less to the revenue base.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2024}}, a change of {{cash_like.change@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, against a peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- The cash buffer is small relative to revenue, so the funding profile rests on the low absolute debt of {{total_debt@FY2024}} rather than on a large liquidity reserve.

`peer_positioning`

- Flughafen Wien ranks at the top of the airport peers on net leverage ({{net_leverage.peer_rank@2024}}) and gross leverage ({{gross_leverage.peer_rank@2024}}), at {{net_leverage@FY2024}} and {{gross_leverage@FY2024}} against medians of {{net_leverage.peer_median@2024}} and {{gross_leverage.peer_median@2024}}.
- It also leads on cash generation, with FFO to debt of {{ffo_to_debt@FY2024}} and FCF to debt of {{fcf_to_debt@FY2024}} ({{ffo_to_debt.peer_rank@2024}} and {{fcf_to_debt.peer_rank@2024}}), and on interest coverage of {{interest_coverage@FY2024}} ({{interest_coverage.peer_rank@2024}}).
- The EBITDA margin of {{ebitda_margin@FY2024}} is in line with the peer median of {{ebitda_margin.peer_median@2024}}, ranking {{ebitda_margin.peer_rank@2024}}.
- Cash liquidity to revenue is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), and traffic growth ranks {{traffic_growth.peer_rank@2024}} at {{traffic_growth@FY2024}} against a peer median of {{traffic_growth.peer_median@2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the airport peers ({{cash_liquidity_to_revenue.peer_rank@2024}}).
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, in line with the peer median, and free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- Traffic: traffic growth of {{traffic_growth@FY2024}} sits below the peer median of {{traffic_growth.peer_median@2024}}, which limits the operating leverage behind the revenue base.
- Revenue mix: the non-aeronautical share fell by {{non_aero_share.change@FY2024}} to {{non_aero_share@FY2024}}, so revenue depends more on regulated aeronautical charges.
