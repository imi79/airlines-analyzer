# Norwegian Air Shuttle, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `90c8020f7b33` ([fact sheet](../factsheets/norwegian_FY2024.md)). Tokens: 42,130 in, 6,306 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, the low-cost carrier, grew revenue by 38.3% to NOK 35.3bn in FY2024, a year in which the acquisition of Widerøe was finalised and Boeing delivery delays limited fleet growth.
The EBITDA margin narrowed by 3.7 points to 18.9%, while net leverage was broadly unchanged at 0.78x.
The point to watch is cash liquidity, which fell by 6.3 points to 30.8% of revenue, the weakest of the low-cost peers (3rd of 3).

> Event `event:acquisitions_and_disposals`: The acquisition of Widerøe was finalised at the start of the year, adding a large number of employees to the Group and already yielding benefits. Quote (page 3): "A major change was the acquisition of Widerøe which was finalised at the very start of the year. We warmly welcomed nearly 3,500 new employees to the Group and with the integration going well the acquisition has already yielded benefits."

> Event `event:fleet_and_engines`: Delivery delays from Boeing meant Norwegian added only a single new aircraft during the year and added cost and complexity to operations. Quote (page 3): "For Norwegian, there was only a modest increase of one new aircraft for Norwegian from the previous year due to delivery delays from Boeing."

## Credit metrics

EBITDA rose by 15.9% to NOK 6.7bn, but operating profit fell by 16.1% to NOK 1.9bn as depreciation and the weaker krone weighed on the result.
Total debt increased by 14.6% to NOK 16.1bn and net debt by 14.3% to NOK 5.2bn, leaving gross leverage broadly unchanged at 2.41x.
Interest coverage weakened by 0.91x to 5.89x, in line with the peer median.
Free cash flow rose by 20.9% to NOK 5.7bn, lifting FCF to debt by 1.8 points to 35.4%, above the peer median.

> Event `event:one_offs`: The operating result was particularly negatively impacted by the weakening of the Norwegian krone against the US dollar, and the year was affected by weather, air traffic control congestion and cost increases. Quote (page 6): "The operating result was particularly negatively impacted by the weakening of NOK against USD."

> removed by the verifier (still broke a rule after two retries): "FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but FFO to debt slipped by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} as debt rose faster than cash generation." (total_debt.change@FY2024 is listed in the form but not used in the text; 'rose' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers rose by 28.2% to 26.4m, supported by the Widerøe integration.
In FY2023 the group carried 20.6m passengers on 32.3bn available seat kilometres, with a load factor of 84.8%.
Unit economics in FY2023 showed RASK of 79.07 øre against CASK of 72.16 øre, with CASK ex-fuel at 48.27 øre.
The fuel share of costs fell by 5.1 points to 28.0%, in line with the peer median.
The fleet stood at 87 aircraft in FY2023, and Boeing delivery delays meant only a modest addition during FY2024.

> Event `event:acquisitions_and_disposals`: The acquisition of Widerøe was finalised at the start of the year, adding a large number of employees to the Group and already yielding benefits. Quote (page 3): "A major change was the acquisition of Widerøe which was finalised at the very start of the year. We warmly welcomed nearly 3,500 new employees to the Group and with the integration going well the acquisition has already yielded benefits."

> Event `event:fleet_and_engines`: Delivery delays from Boeing meant Norwegian added only a single new aircraft during the year and added cost and complexity to operations. Quote (page 3): "For Norwegian, there was only a modest increase of one new aircraft for Norwegian from the previous year due to delivery delays from Boeing."

## Liquidity and funding

Cash and cash-like investments rose by 14.8% to NOK 10.9bn, and cash liquidity increased by the same 14.8% to NOK 10.9bn.
Cash liquidity to revenue nevertheless fell by 6.3 points to 30.8%, as revenue rose by 38.3% faster than the cash balance.
Contract liabilities rose by 29.4% to NOK 4.1bn, and advance ticket cover increased by 4.3 points to 38.1%, below the peer median.
The Board intends to propose a profit distribution per share, subject to approval from debt instrument holders, and financing terms for upcoming aircraft deliveries improved.

> Event `event:capital_returns`: The Board intends to propose a profit distribution per share for the year, paid as dividend or share buy-back, subject to approval from debt instrument holders. Quote (page 15): "The Board of Directors intends to propose a profit distribution of NOK 0.60 per share for 2024 at the 2025 Annual General Meeting, to be paid out either through dividend or buy-back of shares."

> Event `event:funding_and_rating`: Norwegian secured its best-ever financing terms for a portion of its aircraft order book. Quote (page 3): "Additionally, we are seeing improvements to the financing terms for our upcoming aircraft deliveries, with Norwegian securing the best-ever terms for the first 25 of our 50 aircraft on order in the Company’s history."

## Peer positioning

Norwegian has the lowest gross leverage of the low-cost group (1st of 3) and the strongest FCF to debt (1st of 3), against a peer median of 16.3%.
On EBITDA margin, net leverage, interest coverage and FFO to debt the company sits in the middle of the group, with medians of 18.9%, 0.78x, 5.89x and 35.6% respectively.
Cash liquidity to revenue is the weakest of the group (3rd of 3), against a peer median of 33.0%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 6.3 points to 30.8%, below the peer median of 33.0%.
- Profitability: the EBITDA margin narrowed by 3.7 points to 18.9%, and operating profit fell by 16.1% to NOK 1.9bn.
- Debt service: interest coverage fell by 0.91x to 5.89x as total debt rose by 14.6% to NOK 16.1bn.
- Costs: collective bargaining agreements raised personnel cost across several markets, and capex intensity rose by 1.4 points to 3.5%.

> Event `event:labour`: Several key collective bargaining agreements were concluded, raising personnel cost across markets while reducing the risk of industrial action. Quote (page 4): "During 2024, we concluded several key collective bargaining agreements. While these agreements resulted in increased personnel cost across several markets, they also provide improved visibility for 2025 with a reduced risk of industrial action."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 9 errors | 13,044 / 3,270 |
| 2 | snapshot, credit_metrics, liquidity_funding, peer_positioning | 1 errors | 15,531 / 2,235 |
| 3 | credit_metrics | 2 errors | 13,555 / 801 |

### Errors found, by try

Try 1:

- [rule 5] snapshot, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 4] credit_metrics, sentence 4: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 2: ebitda_margin.peer_median@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 2: net_leverage.peer_median@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 2: interest_coverage.peer_median@FY2024 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 2: ffo_to_debt.peer_median@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 4] credit_metrics, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 5] credit_metrics, sentence 4: total_debt.change@FY2024 is listed in the form but not used in the text
- [rule 4] credit_metrics, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, the low-cost carrier, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, a year in which the acquisition of Widerøe was finalised and Boeing delivery delays limited fleet growth.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, while net leverage was broadly unchanged at {{net_leverage@FY2024}}.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} of revenue, the weakest of the low-cost peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation and the weaker krone weighed on the result.
- Total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, leaving gross leverage broadly unchanged at {{gross_leverage@FY2024}}.
- Interest coverage weakened by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, in line with the peer median.
- Free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}}, lifting FCF to debt by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, above the peer median.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, supported by the Widerøe integration.
- In FY2023 the group carried {{passengers@FY2023}} passengers on {{ask@FY2023}} available seat kilometres, with a load factor of {{load_factor@FY2023}}.
- Unit economics in FY2023 showed RASK of {{rask@FY2023}} against CASK of {{cask@FY2023}}, with CASK ex-fuel at {{cask_ex_fuel@FY2023}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}, in line with the peer median.
- The fleet stood at {{fleet@FY2023}} aircraft in FY2023, and Boeing delivery delays meant only a modest addition during FY2024.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity increased by the same {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue nevertheless fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, as revenue rose by {{revenue.change@FY2024}} faster than the cash balance.
- Contract liabilities rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, and advance ticket cover increased by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, below the peer median.
- The Board intends to propose a profit distribution per share, subject to approval from debt instrument holders, and financing terms for upcoming aircraft deliveries improved.

`peer_positioning`

- Norwegian has the lowest gross leverage of the low-cost group ({{gross_leverage.peer_rank@FY2024}}) and the strongest FCF to debt ({{fcf_to_debt.peer_rank@FY2024}}), against a peer median of {{fcf_to_debt.peer_median@FY2024}}.
- On EBITDA margin, net leverage, interest coverage and FFO to debt the company sits in the middle of the group, with medians of {{ebitda_margin.peer_median@FY2024}}, {{net_leverage.peer_median@FY2024}}, {{interest_coverage.peer_median@FY2024}} and {{ffo_to_debt.peer_median@FY2024}} respectively.
- Cash liquidity to revenue is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), against a peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.
- Profitability: the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, and operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Debt service: interest coverage fell by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}} as total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}.
- Costs: collective bargaining agreements raised personnel cost across several markets, and capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.
