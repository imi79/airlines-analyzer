# Norwegian Air Shuttle, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `a8bca9431028` ([fact sheet](../factsheets/norwegian_FY2025.md)). Tokens: 41,832 in, 5,622 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, a low-cost carrier operating a Boeing 737 fleet on a broad European route network, grew revenue by 6.6% to NOK 37.6bn in FY2025 while paying a dividend to shareholders.
The EBITDA margin widened by 2.3 points to 21.2%, but net leverage rose to 1.19x from 0.78x as net debt increased.
The point to watch is cash liquidity, which fell by 4.1 points to 26.7% of revenue, the weakest of the low-cost peers (3rd of 3).

> Event `event:capital_returns`: The company paid a dividend to its shareholders in August. Quote (page 6): "In 2025, the company paid its first-ever dividend, distributing NOK 0.90 per share to its nearly 75,000 shareholders in August."

## Credit metrics

EBITDA increased by 19.2% to NOK 8.0bn, lifting operating profit by 99.3% to NOK 3.7bn.
Total debt rose by 21.6% to NOK 19.6bn and net debt by 82.6% to NOK 9.5bn, so net leverage increased by 0.41x to 1.19x.
Gross leverage was stable at 2.46x, and interest coverage improved by 0.38x to 6.27x.
FFO rose by 21.1% to NOK 6.9bn, leaving FFO to debt broadly unchanged at 35.4%, but free cash flow fell by 49.9% to NOK 2.9bn as capex intensity climbed by 9.7 points to 13.2%.
FCF to debt fell by 20.8 points to 14.6%, a weaker cash buffer against the larger debt stock.

## Operating performance

Passengers rose by 3.4% to 27.3m, supported by a summer programme with a large number of routes including new leisure destinations.
Revenue grew by 6.6% to NOK 37.6bn, faster than the 3.4% increase in passenger volumes, so revenue per passenger rose.
Fuel made up 28.2% of costs, broadly unchanged on the prior year, in line with the peer median.
The company acquired previously leased Boeing 737-800 aircraft and exercised its option for additional 737 MAX 8 aircraft, which it says supports recurring cost savings and a more fuel-efficient fleet.

> Event `event:capacity_and_network`: The summer programme featured a large number of routes, including new routes to leisure destinations, and the winter season operated routes to many destinations. Quote (page 3): "Norwegian’s summer 2025 programme featured nearly 350 routes, including 17 new routes to attractive leisure destinations."

> Event `event:fleet_and_engines`: Norwegian acquired previously leased Boeing 737-800 aircraft, which contributed accounting gains and recurring cost savings. Quote (page 3): "Norwegian's acquisition of 13 previously leased Boeing 737-800 aircraft contributed to accounting gains in 2025 and recurring cost savings, further strengthening our financial position."

> Event `event:fleet_and_engines-2`: The company exercised its option to purchase additional Boeing 737 MAX 8 aircraft on top of its previous order. Quote (page 3): "We also exercised our option to purchase 30 additional Boeing 737 MAX 8 aircraft, adding to the previous 50 aircraft order, reinforcing our commitment to a modern and fuel-efficient fleet."

## Liquidity and funding

Cash and cash-like investments fell by 7.5% to NOK 10.1bn, taking cash liquidity to revenue down by 4.1 points to 26.7%.
Advance ticket cover rose by 5.6 points to 43.7%, with contract liabilities up by 6.1% to NOK 4.4bn, so a larger share of the cash balance is customer prepayments.
During the year the company redeemed its New Capital Perpetual Bonds in full after a partial repurchase offer, and it paid a dividend to shareholders in August.

> Event `event:funding_and_rating`: Norwegian announced it would redeem all outstanding New Capital Perpetual Bonds and launched an offer to repurchase part of them, after which the bonds were redeemed in full. Quote (page 20): "During the second quarter of 2025, Norwegian announced that it would exercise its call option to redeem all outstanding New Capital Perpetual Bonds bonds, totalling NOK 1,501 million, and that the company would launch an offer to repurchase up to 50 percent of these bonds. Following these transactions, the convertible bonds were redeemed in full."

> Event `event:capital_returns`: The company paid a dividend to its shareholders in August. Quote (page 6): "In 2025, the company paid its first-ever dividend, distributing NOK 0.90 per share to its nearly 75,000 shareholders in August."

## Peer positioning

Norwegian sits in the middle of the low-cost group on EBITDA margin, net leverage, gross leverage, interest coverage, FFO to debt and FCF to debt, ranking 2nd of 3 on net leverage.
Its strongest relative position is advance ticket cover, the lowest of the group (1st of 3), below the peer median of 55.1%.
The weakest is cash liquidity to revenue, the lowest of the group (3rd of 3), while capex intensity is above the peer median of 9.9%.

## Watch items

- Leverage: net leverage rose by 0.41x to 1.19x as net debt increased by 82.6%, reversing part of the prior year's deleveraging.
- Cash generation: free cash flow fell by 49.9% to NOK 2.9bn and FCF to debt by 20.8 points to 14.6%, with capex intensity of 13.2% above the peer median of 9.9%.
- Liquidity: cash liquidity to revenue of 26.7% is below the peer median of 34.3% and the weakest of the group (3rd of 3).
- Customer prepayments: advance ticket cover of 43.7% is below the peer median of 55.1%, so a slowdown in bookings would weigh on the cash position.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 13,004 / 3,080 |
| 2 | snapshot, operating_performance, peer_positioning, watch_items | 2 errors | 15,080 / 1,805 |
| 3 | operating_performance, peer_positioning | passed | 13,748 / 737 |

### Errors found, by try

Try 1:

- [rule 1] snapshot, sentence 1: word that states a number: 'first'
- [rule 1] operating_performance, sentence 1: number written outside a blank: '350'
- [rule 5] operating_performance, sentence 2: passengers.change@FY2025 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 2: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] watch_items, sentence 4: 'above_peers' claimed on advance_ticket_cover@FY2025, but it is below

Try 2:

- [rule 5] operating_performance, sentence 2: passengers.change@FY2025 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 2: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, a low-cost carrier operating a Boeing 737 fleet on a broad European route network, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while paying a dividend to shareholders.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, but net leverage rose to {{net_leverage@FY2025}} from {{net_leverage@FY2024}} as net debt increased.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} of revenue, the weakest of the low-cost peers ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, lifting operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, so net leverage increased by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- Gross leverage was stable at {{gross_leverage@FY2025}}, and interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, leaving FFO to debt broadly unchanged at {{ffo_to_debt@FY2025}}, but free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity climbed by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, a weaker cash buffer against the larger debt stock.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, supported by a summer programme with a large number of routes including new leisure destinations.
- Revenue grew by {{revenue.change@FY2025}} to {{revenue@FY2025}}, faster than the {{passengers.change@FY2025}} increase in passenger volumes, so revenue per passenger rose.
- Fuel made up {{fuel_share_of_costs@FY2025}} of costs, broadly unchanged on the prior year, in line with the peer median.
- The company acquired previously leased Boeing 737-800 aircraft and exercised its option for additional 737 MAX 8 aircraft, which it says supports recurring cost savings and a more fuel-efficient fleet.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, with contract liabilities up by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of the cash balance is customer prepayments.
- During the year the company redeemed its New Capital Perpetual Bonds in full after a partial repurchase offer, and it paid a dividend to shareholders in August.

`peer_positioning`

- Norwegian sits in the middle of the low-cost group on EBITDA margin, net leverage, gross leverage, interest coverage, FFO to debt and FCF to debt, ranking {{net_leverage.peer_rank@FY2025}} on net leverage.
- Its strongest relative position is advance ticket cover, the lowest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), below the peer median of {{advance_ticket_cover.peer_median@FY2025}}.
- The weakest is cash liquidity to revenue, the lowest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while capex intensity is above the peer median of {{capex_intensity.peer_median@FY2025}}.

`watch_items`

- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}}, reversing part of the prior year's deleveraging.
- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with capex intensity of {{capex_intensity@FY2025}} above the peer median of {{capex_intensity.peer_median@FY2025}}.
- Liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}} and the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is below the peer median of {{advance_ticket_cover.peer_median@FY2025}}, so a slowdown in bookings would weigh on the cash position.
