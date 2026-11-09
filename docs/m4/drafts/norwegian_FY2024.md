# Norwegian Air Shuttle, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `aa1fbe4e3a6e` ([fact sheet](../factsheets/norwegian_FY2024.md)). Tokens: 44,846 in, 6,755 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, the Norwegian low-cost carrier, grew revenue by 38.3% to NOK 35.3bn in FY2024, a year in which the acquisition of Widerøe was finalised and delivery delays from Boeing constrained fleet growth.
The EBITDA margin narrowed by 3.7 points to 18.9%, while net leverage was broadly unchanged at 0.78x.
The point to watch is cash liquidity, which fell by 6.3 points to 30.8% of revenue, the weakest of the low-cost peer group (3rd of 3).

> Event `event:acquisitions_and_disposals`: The acquisition of Widerøe was finalised at the start of the year, adding a large number of employees to the Group and already yielding benefits. Quote (page 3): "A major change was the acquisition of Widerøe which was finalised at the very start of the year. We warmly welcomed nearly 3,500 new employees to the Group and with the integration going well the acquisition has already yielded benefits."

> Event `event:fleet_and_engines`: Delivery delays from Boeing meant Norwegian added only a single new aircraft during the year and added cost and complexity to operations. Quote (page 3): "For Norwegian, there was only a modest increase of one new aircraft for Norwegian from the previous year due to delivery delays from Boeing."

## Credit metrics

EBITDA rose by 15.9% to NOK 6.7bn, but operating profit fell by 16.1% to NOK 1.9bn as depreciation, amortisation and impairment increased by 36.0% to NOK 4.8bn.
Total debt increased by 14.6% to NOK 16.1bn and net debt by 14.3% to NOK 5.2bn, leaving gross leverage broadly unchanged at 2.41x.
Interest coverage weakened to 5.89x as finance costs rose by 33.8% to NOK 1.1bn.
Cash generation improved: FFO rose by 11.1% to NOK 5.7bn and free cash flow by 20.9% to NOK 5.7bn, although FFO to debt eased by 1.1 points to 35.6% as total debt increased by 14.6%.
FCF to debt improved by 1.8 points to 35.4%, with capex intensity rising by 1.4 points to 3.5% as capital spending increased by 129.9% to NOK 1.2bn.

## Operating performance

Passengers rose by 28.2% to 26.4m, supported by the Widerøe acquisition completed at the start of the year.
Fuel cost increased by 21.5% to NOK 9.4bn, while the fuel share of costs fell by 5.1 points to 28.0% as revenue rose by 38.3%.
The operating result was held back by the weakening of the Norwegian krone against the US dollar and by external disruptions during the year, with operating profit down 16.1% to NOK 1.9bn.
Collective bargaining agreements concluded during the year raised personnel cost across several markets while reducing the risk of industrial action.

> Event `event:acquisitions_and_disposals`: The acquisition of Widerøe was finalised at the start of the year, adding a large number of employees to the Group and already yielding benefits. Quote (page 3): "A major change was the acquisition of Widerøe which was finalised at the very start of the year. We warmly welcomed nearly 3,500 new employees to the Group and with the integration going well the acquisition has already yielded benefits."

> Event `event:one_offs`: The operating result was particularly negatively impacted by the weakening of the Norwegian krone against the US dollar, and the year was affected by weather, air traffic control congestion and cost increases. Quote (page 6): "The operating result was particularly negatively impacted by the weakening of NOK against USD."

> Event `event:labour`: Several key collective bargaining agreements were concluded, raising personnel cost across markets while reducing the risk of industrial action. Quote (page 4): "During 2024, we concluded several key collective bargaining agreements. While these agreements resulted in increased personnel cost across several markets, they also provide improved visibility for 2025 with a reduced risk of industrial action."

> verifier: [rule style] operating_performance, sentence 3: operating_profit.change@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)

> verifier: [rule style] operating_performance, sentence 3: operating_profit@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)

## Liquidity and funding

Cash and cash-like investments rose by 14.8% to NOK 10.9bn, taking cash liquidity to revenue down to 30.8%.
Advance ticket cover rose by 4.3 points to 38.1%, with contract liabilities up by 29.4% to NOK 4.1bn, so a larger part of the cash balance is customers' prepayments.
Financing terms for upcoming aircraft deliveries improved, with the company securing its best-ever terms for part of its order book.
The Board intends to propose a profit distribution per share for the year, subject to approval from debt instrument holders.

> Event `event:funding_and_rating`: Norwegian secured its best-ever financing terms for a portion of its aircraft order book. Quote (page 3): "Additionally, we are seeing improvements to the financing terms for our upcoming aircraft deliveries, with Norwegian securing the best-ever terms for the first 25 of our 50 aircraft on order in the Company’s history."

> Event `event:capital_returns`: The Board intends to propose a profit distribution per share for the year, paid as dividend or share buy-back, subject to approval from debt instrument holders. Quote (page 15): "The Board of Directors intends to propose a profit distribution of NOK 0.60 per share for 2024 at the 2025 Annual General Meeting, to be paid out either through dividend or buy-back of shares."

## Peer positioning

Norwegian has the lowest gross leverage of the low-cost group (1st of 3) and the strongest FCF to debt (1st of 3), against a peer median of 16.3%.
Cash liquidity to revenue is the weakest of the group (3rd of 3), against a peer median of 33.0%.
On EBITDA margin, net leverage, interest coverage and FFO to debt the company sits in the middle of the group, and its advance ticket cover is the lowest of the peers (1st of 3).

## Watch items

- Liquidity: cash liquidity to revenue fell by 6.3 points to 30.8%, below the peer median of 33.0%.
- Margins: the EBITDA margin narrowed by 3.7 points to 18.9%, with operating profit down 16.1% as depreciation, amortisation and impairment rose by 36.0%.
- Debt service: interest coverage eased by 0.91x to 5.89x as finance costs rose by 33.8%.
- Customer prepayments: advance ticket cover rose by 4.3 points to 38.1%, so a larger share of the cash balance is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 13,652 / 3,161 |
| 2 | credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 16,681 / 2,713 |
| 3 | operating_performance, liquidity_funding | passed | 14,513 / 881 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 4: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 3: 'weakening' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 1: 'grew' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: cash_liquidity_to_revenue@FY2024 is already given in liquidity_funding, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: advance_ticket_cover@FY2024 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 2: 'rose' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] operating_performance, sentence 3: 'weakening' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 1: revenue.change@FY2024 is already given in operating_performance, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)

Try 3:

- [rule style] operating_performance, sentence 3: operating_profit.change@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 3: operating_profit@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, the Norwegian low-cost carrier, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, a year in which the acquisition of Widerøe was finalised and delivery delays from Boeing constrained fleet growth.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, while net leverage was broadly unchanged at {{net_leverage@FY2024}}.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} of revenue, the weakest of the low-cost peer group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation, amortisation and impairment increased by {{dda.change@FY2024}} to {{dda@FY2024}}.
- Total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, leaving gross leverage broadly unchanged at {{gross_leverage@FY2024}}.
- Interest coverage weakened to {{interest_coverage@FY2024}} as finance costs rose by {{finance_costs.change@FY2024}} to {{finance_costs@FY2024}}.
- Cash generation improved: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}} and free cash flow by {{fcf.change@FY2024}} to {{fcf@FY2024}}, although FFO to debt eased by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} as total debt increased by {{total_debt.change@FY2024}}.
- FCF to debt improved by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, with capex intensity rising by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}} as capital spending increased by {{capex.change@FY2024}} to {{capex@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, supported by the Widerøe acquisition completed at the start of the year.
- Fuel cost increased by {{fuel_cost.change@FY2024}} to {{fuel_cost@FY2024}}, while the fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}} as revenue rose by {{revenue.change@FY2024}}.
- The operating result was held back by the weakening of the Norwegian krone against the US dollar and by external disruptions during the year, with operating profit down {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Collective bargaining agreements concluded during the year raised personnel cost across several markets while reducing the risk of industrial action.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue down to {{cash_liquidity_to_revenue@FY2024}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, with contract liabilities up by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, so a larger part of the cash balance is customers' prepayments.
- Financing terms for upcoming aircraft deliveries improved, with the company securing its best-ever terms for part of its order book.
- The Board intends to propose a profit distribution per share for the year, subject to approval from debt instrument holders.

`peer_positioning`

- Norwegian has the lowest gross leverage of the low-cost group ({{gross_leverage.peer_rank@FY2024}}) and the strongest FCF to debt ({{fcf_to_debt.peer_rank@FY2024}}), against a peer median of {{fcf_to_debt.peer_median@FY2024}}.
- Cash liquidity to revenue is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), against a peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.
- On EBITDA margin, net leverage, interest coverage and FFO to debt the company sits in the middle of the group, and its advance ticket cover is the lowest of the peers ({{advance_ticket_cover.peer_rank@FY2024}}).

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.
- Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, with operating profit down {{operating_profit.change@FY2024}} as depreciation, amortisation and impairment rose by {{dda.change@FY2024}}.
- Debt service: interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}} as finance costs rose by {{finance_costs.change@FY2024}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, so a larger share of the cash balance is refundable if bookings slow.
