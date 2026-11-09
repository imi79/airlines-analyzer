# Norwegian Air Shuttle, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `0bf7d0477264` ([fact sheet](../factsheets/norwegian_FY2025.md)). Tokens: 40,227 in, 4,358 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, a low-cost carrier operating a Boeing 737 fleet on Nordic and European routes, grew revenue by 6.6% to NOK 37.6bn in FY2025 while the EBITDA margin widened by 2.3 points to 21.2%.
Net leverage rose by 0.41x to 1.19x as net debt increased by 82.6% to NOK 9.5bn, leaving leverage in line with the peer median.
The point to watch is cash liquidity, which fell by 4.1 points to 26.7% of revenue, below the peer median, while free cash flow declined by 49.9% to NOK 2.9bn.

## Credit metrics

EBITDA increased by 19.2% to NOK 8.0bn, and operating profit rose by 99.3% to NOK 3.7bn.
Total debt rose by 21.6% to NOK 19.6bn, so gross leverage was broadly unchanged at 2.46x and net leverage increased to 1.19x.
Interest coverage improved to 6.27x, up 0.38x, and FFO rose by 21.1% to NOK 6.9bn, leaving FFO to debt stable at 35.4%.
Free cash flow fell by 49.9% to NOK 2.9bn as capex intensity rose by 9.7 points to 13.2%, taking FCF to debt down by 20.8 points to 14.6%.

## Operating performance

Passengers rose by 3.4% to 27.3m, supported by a summer programme that added new leisure routes.
Revenue rose by 6.6% to NOK 37.6bn, with the EBITDA margin widening by 2.3 points to 21.2%.
Fuel made up 28.2% of costs, broadly unchanged on the prior year, in line with the peer median.

> Event `event:capacity_and_network`: The summer programme featured a large number of routes, including new routes to leisure destinations, and the winter season operated routes to many destinations. Quote (page 3): "Norwegian’s summer 2025 programme featured nearly 350 routes, including 17 new routes to attractive leisure destinations."

> removed by the verifier (still broke a rule after two retries): "The company acquired previously leased Boeing 737-800 aircraft, which contributed accounting gains and recurring cost savings, and exercised its option for additional 737 MAX 8 aircraft." (number written outside a blank: '0')

## Liquidity and funding

Cash liquidity fell by 7.5% to NOK 10.1bn, with cash and cash-like investments down by 7.5% to NOK 10.1bn.
Cash liquidity to revenue fell by 4.1 points to 26.7%, below the peer median of 34.3%.
Customer prepayments rose: contract liabilities increased by 6.1% to NOK 4.4bn, and advance ticket cover rose by 5.6 points to 43.7%.
The company redeemed its New Capital Perpetual Bonds in full during the year and paid an initial dividend to shareholders in August.

> Event `event:funding_and_rating`: Norwegian announced it would redeem all outstanding New Capital Perpetual Bonds and launched an offer to repurchase part of them, after which the bonds were redeemed in full. Quote (page 20): "During the second quarter of 2025, Norwegian announced that it would exercise its call option to redeem all outstanding New Capital Perpetual Bonds bonds, totalling NOK 1,501 million, and that the company would launch an offer to repurchase up to 50 percent of these bonds. Following these transactions, the convertible bonds were redeemed in full."

> Event `event:capital_returns`: The company paid an initial dividend to its shareholders in August. Quote (page 6): "In 2025, the company paid its first-ever dividend, distributing NOK 0.90 per share to its nearly 75,000 shareholders in August."

## Peer positioning

Norwegian sits in the middle of the low-cost group on EBITDA margin, net leverage, gross leverage, interest coverage, FFO to debt and FCF to debt, ranking 2nd of 3 on net leverage.
Its strongest metric is advance ticket cover, the lowest of the group (1st of 3), below the peer median of 55.1%.
The weakest position is cash liquidity to revenue, the lowest of the group (3rd of 3), while capex intensity is above the peer median of 9.9%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 4.1 points to 26.7%, the weakest of the low-cost peers (3rd of 3).
- Leverage: net leverage rose by 0.41x to 1.19x as net debt increased by 82.6% to NOK 9.5bn.
- Cash generation: free cash flow fell by 49.9% to NOK 2.9bn and FCF to debt dropped by 20.8 points to 14.6%, with capex intensity up by 9.7 points to 13.2%.
- Customer prepayments: advance ticket cover rose by 5.6 points to 43.7%, so a larger share of cash is customers' prepayments.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 13,033 / 3,173 |
| 2 | operating_performance, peer_positioning | 1 errors | 13,914 / 758 |
| 3 | operating_performance | 1 errors | 13,280 / 427 |

### Errors found, by try

Try 1:

- [rule 1] operating_performance, sentence 1: number written outside a blank: '350'
- [rule 4] operating_performance, sentence 2: 'widening' needs a 'up' claim on a figure in the same clause
- [rule 1] operating_performance, sentence 4: number written outside a blank: '0'
- [rule style] peer_positioning, sentence 2: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 1] operating_performance, sentence 4: number written outside a blank: '0'

Try 3:

- [rule 1] operating_performance, sentence 4: number written outside a blank: '0'

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, a low-cost carrier operating a Boeing 737 fleet on Nordic and European routes, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while the EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, leaving leverage in line with the peer median.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} of revenue, below the peer median, while free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, so gross leverage was broadly unchanged at {{gross_leverage@FY2025}} and net leverage increased to {{net_leverage@FY2025}}.
- Interest coverage improved to {{interest_coverage@FY2025}}, up {{interest_coverage.change@FY2025}}, and FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, leaving FFO to debt stable at {{ffo_to_debt@FY2025}}.
- Free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, taking FCF to debt down by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, supported by a summer programme that added new leisure routes.
- Revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, with the EBITDA margin widening by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Fuel made up {{fuel_share_of_costs@FY2025}} of costs, broadly unchanged on the prior year, in line with the peer median.

`liquidity_funding`

- Cash liquidity fell by {{cash_liquidity.change@FY2025}} to {{cash_liquidity@FY2025}}, with cash and cash-like investments down by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.
- The company redeemed its New Capital Perpetual Bonds in full during the year and paid an initial dividend to shareholders in August.

`peer_positioning`

- Norwegian sits in the middle of the low-cost group on EBITDA margin, net leverage, gross leverage, interest coverage, FFO to debt and FCF to debt, ranking {{net_leverage.peer_rank@FY2025}} on net leverage.
- Its strongest metric is advance ticket cover, the lowest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), below the peer median of {{advance_ticket_cover.peer_median@FY2025}}.
- The weakest position is cash liquidity to revenue, the lowest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while capex intensity is above the peer median of {{capex_intensity.peer_median@FY2025}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the low-cost peers ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).
- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FCF to debt dropped by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with capex intensity up by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, so a larger share of cash is customers' prepayments.
