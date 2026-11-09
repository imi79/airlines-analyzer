# Finnair, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `d91fc2fa3471` ([fact sheet](../factsheets/finnair_FY2025.md)). Tokens: 43,262 in, 6,966 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Finnair, the Finnish network carrier, kept revenue broadly unchanged at EUR 3.1bn in FY2025, a year in which prolonged industrial action in the first half weighed on the comparable operating result.
Net leverage fell by 0.44x to 1.77x as net debt was reduced by 26.4% to EUR 722m.
The point to watch is earnings quality: the EBITDA margin narrowed by 1.5 points to 13.1%, the weakest of the network peers (3rd of 3), with FFO to debt down to 18.0%.

> Event `event:labour`: Industrial action in the first half of the year had an immediate negative impact on the comparable operating result, and increased environmental regulation costs as well as higher navigation and landing charges also weighed on the result. Quote (page 3): "The prolonged industrial action during the first half of the year had an immediate negative impact of approximately 68 million euros on the comparable operating result. In addition, increased costs related to environmental regulation as well as higher navigation and landing charges weighed on the result."

## Credit metrics

EBITDA fell by 8.2% to EUR 408m on revenue of EUR 3.1bn, and operating profit declined by 43.8% to EUR 64.2m.
Total debt was reduced by 4.4% to EUR 1.8bn, but gross leverage rose by 0.17x to 4.37x as EBITDA declined by 8.2%.
Interest coverage improved by 0.83x to 4.98x, still below the peer median of 8.06x.
Cash generation weakened: FFO fell by 21.2% to EUR 320m, taking FFO to debt down by 3.8 points to 18.0%, and free cash flow declined by 49.1% to EUR 193m.
FCF to debt fell by 9.5 points to 10.8%, while capex intensity eased by 1.0 point to 6.7%.

## Operating performance

Passengers were broadly unchanged at 11.9m, a move of 2.0%, with the fleet stable at 79 aircraft and an average age of 14.3 years.
The fuel share of costs fell by 1.6 points to 28.9%, above the peer median of 27.0%.
During the year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date.

> Event `event:fleet_and_engines`: During the financial year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date. Quote (page 163): "During the financial year Finnair purchased four leased A321 aircraft. All aircraft were in operative use as at the balance sheet date."

> removed by the verifier (still broke a rule after two retries): "Costs related to environmental regulation increased significantly during the year, with greater use of sustainable aviation fuel and changes to the EU Emissions Trading System weighing on the result." ('increased' needs a 'up' claim on a figure in the same clause)

## Liquidity and funding

Liquidity rose by 16.3% to EUR 1.3bn, of which cash and cash-like investments of EUR 1.1bn were up 20.0%.
Undrawn committed facilities were stable at EUR 200m, and liquidity to revenue rose by 5.0 points to 40.6%.
Customer prepayments grew: contract liabilities rose by 8.5% to EUR 715m, while advance ticket cover fell by 7.1 points to 67.4%.
Towards the end of the year Finnair issued a bond to further strengthen its financial position and support the execution of strategic investments.

> Event `event:funding_and_rating`: Finnair issued a bond towards the end of the year to further strengthen its financial position and support execution of strategic investments. Quote (page 4): "To further strengthen our financial position, we issued a 300million-euro bond towards the end of the year, supporting the execution of strategic investments in the coming years."

## Peer positioning

Finnair's clearest strength is cash liquidity to revenue of 34.2%, the highest of the network peers (1st of 3) against a median of 25.0%.
Profitability is the weak spot: the EBITDA margin of 13.1% is the lowest of the group (3rd of 3) against a median of 15.3%, and gross leverage ranks 3rd of 3 against a median of 3.07x.
Net leverage and FCF to debt sit in the middle of the group, while FFO to debt ranks 3rd of 3 against a median of 27.4%.

## Watch items

- Earnings: the EBITDA margin narrowed by 1.5 points to 13.1%, below the peer median of 15.3%, with industrial action in the first half weighing on the result.
- Cash generation: FFO to debt fell by 3.8 points to 18.0%, below the peer median of 27.4%, and FCF to debt dropped by 9.5 points to 10.8%.
- Leverage: gross leverage rose by 0.17x to 4.37x, above the peer median of 3.07x, while net leverage improved to 1.77x as net debt was reduced by 26.4%.
- Costs and distributions: the fuel share of costs of 28.9% is above the peer median of 27.0%, and the Board proposes a return of capital to shareholders.

> Event `event:labour`: Industrial action in the first half of the year had an immediate negative impact on the comparable operating result, and increased environmental regulation costs as well as higher navigation and landing charges also weighed on the result. Quote (page 3): "The prolonged industrial action during the first half of the year had an immediate negative impact of approximately 68 million euros on the comparable operating result. In addition, increased costs related to environmental regulation as well as higher navigation and landing charges weighed on the result."

> Event `event:capital_returns`: The Board of Directors proposes a return of capital per share to the Annual General Meeting, supported by the company's financial position. Quote (page 4): "Our financial position also enables us to reward our shareholders, and the Board of Directors proposes a return of capital of 0.09 euros per share to the Annual General Meeting."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 7 errors | 13,180 / 3,377 |
| 2 | credit_metrics, operating_performance, peer_positioning, watch_items | 2 errors | 15,830 / 2,466 |
| 3 | operating_performance, watch_items | 1 errors | 14,252 / 1,123 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 2: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 3] operating_performance, sentence 1: 'up' claimed on passengers.change@FY2025, but it moved flat
- [rule 4] operating_performance, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: fcf_to_debt@FY2025 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 3: 'improvement' needs a 'better' or 'better_than_peers' or 'best_in_group' claim on a figure in the same clause

Try 2:

- [rule 4] operating_performance, sentence 3: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'improvement' needs a 'better' or 'better_than_peers' or 'best_in_group' claim on a figure in the same clause

Try 3:

- [rule 4] operating_performance, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, kept revenue broadly unchanged at {{revenue@FY2025}} in FY2025, a year in which prolonged industrial action in the first half weighed on the comparable operating result.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt was reduced by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- The point to watch is earnings quality: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, the weakest of the network peers ({{ebitda_margin.peer_rank@FY2025}}), with FFO to debt down to {{ffo_to_debt@FY2025}}.

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue of {{revenue@FY2025}}, and operating profit declined by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, but gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} as EBITDA declined by {{ebitda.change@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, still below the peer median of {{interest_coverage.peer_median@FY2025}}.
- Cash generation weakened: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, taking FFO to debt down by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, and free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, while capex intensity eased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers were broadly unchanged at {{passengers@FY2025}}, a move of {{passengers.change@FY2025}}, with the fleet stable at {{fleet@FY2025}} aircraft and an average age of {{fleet_age@FY2025}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}, above the peer median of {{fuel_share_of_costs.peer_median@FY2025}}.
- During the year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which cash and cash-like investments of {{cash_like@FY2025}} were up {{cash_like.change@FY2025}}.
- Undrawn committed facilities were stable at {{undrawn_facilities@FY2025}}, and liquidity to revenue rose by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}.
- Customer prepayments grew: contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, while advance ticket cover fell by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.
- Towards the end of the year Finnair issued a bond to further strengthen its financial position and support the execution of strategic investments.

`peer_positioning`

- Finnair's clearest strength is cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}}, the highest of the network peers ({{cash_liquidity_to_revenue.peer_rank@FY2025}}) against a median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- Profitability is the weak spot: the EBITDA margin of {{ebitda_margin@FY2025}} is the lowest of the group ({{ebitda_margin.peer_rank@FY2025}}) against a median of {{ebitda_margin.peer_median@FY2025}}, and gross leverage ranks {{gross_leverage.peer_rank@FY2025}} against a median of {{gross_leverage.peer_median@FY2025}}.
- Net leverage and FCF to debt sit in the middle of the group, while FFO to debt ranks {{ffo_to_debt.peer_rank@FY2025}} against a median of {{ffo_to_debt.peer_median@FY2025}}.

`watch_items`

- Earnings: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, below the peer median of {{ebitda_margin.peer_median@FY2025}}, with industrial action in the first half weighing on the result.
- Cash generation: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, below the peer median of {{ffo_to_debt.peer_median@FY2025}}, and FCF to debt dropped by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}.
- Leverage: gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, above the peer median of {{gross_leverage.peer_median@FY2025}}, while net leverage improved to {{net_leverage@FY2025}} as net debt was reduced by {{net_debt.change@FY2025}}.
- Costs and distributions: the fuel share of costs of {{fuel_share_of_costs@FY2025}} is above the peer median of {{fuel_share_of_costs.peer_median@FY2025}}, and the Board proposes a return of capital to shareholders.
