# Finnair, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `a6e9c5fbd38f` ([fact sheet](../factsheets/finnair_FY2025.md)). Tokens: 45,547 in, 7,062 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Finnair, the Finnish network carrier, closed FY2025 with revenue broadly unchanged at EUR 3.1bn and EBITDA of EUR 408m, as prolonged industrial action in the first half weighed on the result.
Net leverage fell by 0.44x to 1.77x as net debt was reduced by 26.4% to EUR 722m.
The point to watch is earnings quality: the EBITDA margin narrowed by 1.5 points to 13.1%, the weakest of the network peers (3rd of 3), with FFO to debt down to 18.0%.

> Event `event:labour`: Industrial action in the first half of the year had an immediate negative impact on the comparable operating result, and increased environmental regulation costs as well as higher navigation and landing charges also weighed on the result. Quote (page 3): "The prolonged industrial action during the first half of the year had an immediate negative impact of approximately 68 million euros on the comparable operating result. In addition, increased costs related to environmental regulation as well as higher navigation and landing charges weighed on the result."

## Credit metrics

EBITDA declined by 8.2% to EUR 408m on revenue of EUR 3.1bn, broadly unchanged on the prior year.
Operating profit fell by 43.8% to EUR 64.2m as depreciation, amortisation and impairment rose by 4.1% to EUR 344m.
Total debt was reduced by 4.4% to EUR 1.8bn, but gross leverage rose by 0.17x to 4.37x as EBITDA declined by 8.2%.
Interest coverage improved by 0.83x to 4.98x as finance costs fell by 23.6% to EUR 81.9m.
Cash generation weakened: FFO fell by 21.2% to EUR 320m and FCF by 49.1% to EUR 193m, taking FFO to debt down by 3.8 points to 18.0% and FCF to debt to 10.8%.

## Operating performance

Passengers were broadly stable at 11.9m, a change of 2.0%, with the fleet at 79 aircraft and an average age of 14.3 years.
Fuel cost was broadly unchanged at EUR 879m, a change of 1.7%, and the fuel share of costs fell by 1.6 points to 28.9%.
Finnair purchased leased A321 aircraft during the year, and all aircraft were in operative use at the balance sheet date.

> Event `event:fleet_and_engines`: During the financial year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date. Quote (page 163): "During the financial year Finnair purchased four leased A321 aircraft. All aircraft were in operative use as at the balance sheet date."

> removed by the verifier (still broke a rule after two retries): "Costs related to environmental regulation increased significantly during the year, with sustainable aviation fuel use and changes to the EU Emissions Trading System weighing on the result." ('increased' needs a 'up' claim on a figure in the same clause)

## Liquidity and funding

Liquidity rose by 16.3% to EUR 1.3bn, of which EUR 200m in undrawn committed facilities, broadly unchanged on the prior year.
Cash and cash-like investments increased by 20.0% to EUR 1.1bn, lifting cash liquidity to revenue by 5.2 points to 34.2%.
Advance ticket cover fell by 7.1 points to 67.4%, while contract liabilities rose by 8.5% to EUR 715m.
Towards the end of the year Finnair issued a bond to further strengthen its financial position and support the execution of strategic investments.

> Event `event:funding_and_rating`: Finnair issued a bond towards the end of the year to further strengthen its financial position and support execution of strategic investments. Quote (page 4): "To further strengthen our financial position, we issued a 300million-euro bond towards the end of the year, supporting the execution of strategic investments in the coming years."

## Peer positioning

Finnair's strongest position is liquidity: cash liquidity to revenue is the highest of the network peers (1st of 3), against a median of 25.0%.
It is weakest on earnings and leverage: the EBITDA margin is the lowest of the group (3rd of 3), and gross leverage is above the peer median of 3.07x.
FCF to debt ranks 2nd of 3 and advance ticket cover 2nd of 3, so both sit in the middle of the group.

## Watch items

- Earnings: the EBITDA margin narrowed by 1.5 points to 13.1%, below the peer median of 15.3%, with industrial action in the first half weighing on the result.
- Cash generation: FFO to debt fell by 3.8 points to 18.0%, below the peer median of 27.4%, as cash from operations declined by 34.4% to EUR 402m.
- Leverage: gross leverage rose by 0.17x to 4.37x, above the peer median of 3.07x, and interest coverage of 4.98x remains below the peer median of 8.06x.

> Event `event:labour`: Industrial action in the first half of the year had an immediate negative impact on the comparable operating result, and increased environmental regulation costs as well as higher navigation and landing charges also weighed on the result. Quote (page 3): "The prolonged industrial action during the first half of the year had an immediate negative impact of approximately 68 million euros on the comparable operating result. In addition, increased costs related to environmental regulation as well as higher navigation and landing charges weighed on the result."

> removed by the verifier (still broke a rule after two retries): "Cost base: the fuel share of costs of {{fuel_share_of_costs@FY2025}} is above the peer median of {{fuel_share_of_costs.peer_median@FY2025}}, and costs related to environmental regulation increased significantly during the year." ('increased' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 9 errors | 13,805 / 3,290 |
| 2 | credit_metrics, operating_performance, peer_positioning, watch_items | 4 errors | 16,403 / 2,286 |
| 3 | operating_performance, peer_positioning, watch_items | 2 errors | 15,339 / 1,486 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 3: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 3] operating_performance, sentence 1: 'up' claimed on passengers.change@FY2025, but it moved flat
- [rule 3] operating_performance, sentence 2: 'down' claimed on fuel_cost.change@FY2025, but it moved flat
- [rule 4] operating_performance, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: cash_liquidity_to_revenue@FY2025 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: fcf_to_debt@FY2025 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'increased' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] operating_performance, sentence 3: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 5] peer_positioning, sentence 3: fcf_to_debt.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: advance_ticket_cover.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] operating_performance, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, closed FY2025 with revenue broadly unchanged at {{revenue@FY2025}} and EBITDA of {{ebitda@FY2025}}, as prolonged industrial action in the first half weighed on the result.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt was reduced by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- The point to watch is earnings quality: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, the weakest of the network peers ({{ebitda_margin.peer_rank@FY2025}}), with FFO to debt down to {{ffo_to_debt@FY2025}}.

`credit_metrics`

- EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue of {{revenue@FY2025}}, broadly unchanged on the prior year.
- Operating profit fell by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} as depreciation, amortisation and impairment rose by {{dda.change@FY2025}} to {{dda@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, but gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} as EBITDA declined by {{ebitda.change@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as finance costs fell by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}.
- Cash generation weakened: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}} and FCF by {{fcf.change@FY2025}} to {{fcf@FY2025}}, taking FFO to debt down by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} and FCF to debt to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Passengers were broadly stable at {{passengers@FY2025}}, a change of {{passengers.change@FY2025}}, with the fleet at {{fleet@FY2025}} aircraft and an average age of {{fleet_age@FY2025}}.
- Fuel cost was broadly unchanged at {{fuel_cost@FY2025}}, a change of {{fuel_cost.change@FY2025}}, and the fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- Finnair purchased leased A321 aircraft during the year, and all aircraft were in operative use at the balance sheet date.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which {{undrawn_facilities@FY2025}} in undrawn committed facilities, broadly unchanged on the prior year.
- Cash and cash-like investments increased by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, lifting cash liquidity to revenue by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover fell by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, while contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}.
- Towards the end of the year Finnair issued a bond to further strengthen its financial position and support the execution of strategic investments.

`peer_positioning`

- Finnair's strongest position is liquidity: cash liquidity to revenue is the highest of the network peers ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), against a median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- It is weakest on earnings and leverage: the EBITDA margin is the lowest of the group ({{ebitda_margin.peer_rank@FY2025}}), and gross leverage is above the peer median of {{gross_leverage.peer_median@FY2025}}.
- FCF to debt ranks {{fcf_to_debt.peer_rank@FY2025}} and advance ticket cover {{advance_ticket_cover.peer_rank@FY2025}}, so both sit in the middle of the group.

`watch_items`

- Earnings: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, below the peer median of {{ebitda_margin.peer_median@FY2025}}, with industrial action in the first half weighing on the result.
- Cash generation: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, below the peer median of {{ffo_to_debt.peer_median@FY2025}}, as cash from operations declined by {{cfo.change@FY2025}} to {{cfo@FY2025}}.
- Leverage: gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, above the peer median of {{gross_leverage.peer_median@FY2025}}, and interest coverage of {{interest_coverage@FY2025}} remains below the peer median of {{interest_coverage.peer_median@FY2025}}.
