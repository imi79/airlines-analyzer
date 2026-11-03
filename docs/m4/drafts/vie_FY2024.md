# Flughafen Wien, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `a1f2504b2f8d` ([fact sheet](../factsheets/vie_FY2024.md)). Tokens: 24,914 in, 5,887 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport operator, ended FY2024 with revenue up 13.0% to EUR 1.1bn and an EBITDA margin broadly unchanged at 42.0%.
Net leverage was broadly unchanged at -0.04x, a net cash position, with gross leverage stable at 0.13x.
The point to watch is liquidity: cash liquidity to revenue fell by 1.0 point to 6.9%, the weakest of the airport peers (3rd of 3).

## Credit metrics

EBITDA increased by 12.3% to EUR 442m on revenue of EUR 1.1bn, and operating profit rose by 16.9% to EUR 306m.
Total debt was stable at EUR 55.6m, so gross leverage held at 0.13x and net debt remained a net cash position of EUR -17.2m.
Interest coverage improved to 201.87x, up 168.89x, reflecting the very small interest bill against EBITDA.
FFO rose by 3.4% to EUR 358m, lifting FFO to debt by 17.8 points to 644.0%.
Free cash flow declined by 4.6% to EUR 274m as capex intensity rose by 5.6 points to 16.1%, leaving FCF to debt at 492.4%.

## Operating performance

Passengers rose by 7.3% to 31.7m, although traffic growth of 7.3% was below the peer median of 8.3%.
Revenue per passenger increased by 5.3% to EUR 33.21, with aeronautical revenue per passenger up 7.6% to EUR 15.57.
The non-aeronautical share of revenue fell by 1.0 point to 53.1%, so commercial income lagged the aeronautical base.

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at EUR 72.8m, a change of 1.6% on the year.
Cash liquidity of EUR 72.8m equates to 6.9% of revenue, well below the peer median of 31.6%.
With total debt of only EUR 55.6m and a net cash position, the thin cash buffer is offset by very low refinancing needs.

## Peer positioning

Flughafen Wien has the lowest net leverage in the airport group (1st of 3), at -0.04x against a peer median of 1.57x.
It also leads on gross leverage (1st of 3), interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3).
The EBITDA margin of 42.0% is in line with the peer median of 42.0%, ranking 2nd of 3, and capex intensity of 16.1% also matches the median.
The weak spot is liquidity, where cash liquidity to revenue of 6.9% ranks 3rd of 3 against a median of 31.6%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 1.0 point to 6.9%, the weakest of the group (3rd of 3), with no undrawn committed facilities disclosed.
- Investment: capex intensity rose by 5.6 points to 16.1%, in line with the peer median, and free cash flow fell by 4.6% to EUR 274m as a result.
- Traffic: traffic growth of 7.3% was below the peer median of 8.3%, and the non-aeronautical share of revenue fell by 1.0 point to 53.1%.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 11,073 / 3,098 |
| 2 | snapshot, credit_metrics, operating_performance, peer_positioning, watch_items | passed | 13,841 / 2,789 |

### Errors found, by try

Try 1:

- [rule 1] snapshot, sentence 2: word that states a number: 'zero'
- [rule 3] snapshot, sentence 2: 'better' claimed on net_leverage@FY2024, but it is neither better nor worse
- [rule 3] snapshot, sentence 2: 'better' claimed on gross_leverage@FY2024, but it is neither better nor worse
- [rule 3] credit_metrics, sentence 2: 'better' claimed on gross_leverage@FY2024, but it is neither better nor worse
- [rule 4] operating_performance, sentence 3: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 3] peer_positioning, sentence 1: 'better' claimed on net_leverage@FY2024, but it is neither better nor worse
- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'
- [rule 4] watch_items, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport operator, ended FY2024 with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}} and an EBITDA margin broadly unchanged at {{ebitda_margin@FY2024}}.
- Net leverage was broadly unchanged at {{net_leverage@FY2024}}, a net cash position, with gross leverage stable at {{gross_leverage@FY2024}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the airport peers ({{cash_liquidity_to_revenue.peer_rank@2024}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue of {{revenue@FY2024}}, and operating profit rose by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt was stable at {{total_debt@FY2024}}, so gross leverage held at {{gross_leverage@FY2024}} and net debt remained a net cash position of {{net_debt@FY2024}}.
- Interest coverage improved to {{interest_coverage@FY2024}}, up {{interest_coverage.change@FY2024}}, reflecting the very small interest bill against EBITDA.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, lifting FFO to debt by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}.
- Free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, leaving FCF to debt at {{fcf_to_debt@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, although traffic growth of {{traffic_growth@FY2024}} was below the peer median of {{traffic_growth.peer_median@2024}}.
- Revenue per passenger increased by {{revenue_per_passenger.change@FY2024}} to {{revenue_per_passenger@FY2024}}, with aeronautical revenue per passenger up {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}.
- The non-aeronautical share of revenue fell by {{non_aero_share.change@FY2024}} to {{non_aero_share@FY2024}}, so commercial income lagged the aeronautical base.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2024}}, a change of {{cash_like.change@FY2024}} on the year.
- Cash liquidity of {{cash_liquidity@FY2024}} equates to {{cash_liquidity_to_revenue@FY2024}} of revenue, well below the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- With total debt of only {{total_debt@FY2024}} and a net cash position, the thin cash buffer is offset by very low refinancing needs.

`peer_positioning`

- Flughafen Wien has the lowest net leverage in the airport group ({{net_leverage.peer_rank@2024}}), at {{net_leverage@FY2024}} against a peer median of {{net_leverage.peer_median@2024}}.
- It also leads on gross leverage ({{gross_leverage.peer_rank@2024}}), interest coverage ({{interest_coverage.peer_rank@2024}}), FFO to debt ({{ffo_to_debt.peer_rank@2024}}) and FCF to debt ({{fcf_to_debt.peer_rank@2024}}).
- The EBITDA margin of {{ebitda_margin@FY2024}} is in line with the peer median of {{ebitda_margin.peer_median@2024}}, ranking {{ebitda_margin.peer_rank@2024}}, and capex intensity of {{capex_intensity@FY2024}} also matches the median.
- The weak spot is liquidity, where cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} ranks {{cash_liquidity_to_revenue.peer_rank@2024}} against a median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), with no undrawn committed facilities disclosed.
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, in line with the peer median, and free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as a result.
- Traffic: traffic growth of {{traffic_growth@FY2024}} was below the peer median of {{traffic_growth.peer_median@2024}}, and the non-aeronautical share of revenue fell by {{non_aero_share.change@FY2024}} to {{non_aero_share@FY2024}}.
