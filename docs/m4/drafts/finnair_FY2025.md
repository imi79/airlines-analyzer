# Finnair, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `756ae089497b` ([fact sheet](../factsheets/finnair_FY2025.md)). Tokens: 41,997 in, 6,745 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Finnair, the Finnish network carrier, closed FY2025 with a weaker earnings profile as prolonged industrial action in the first half weighed on the result, with EBITDA down 8.2% to EUR 408m.
Net leverage nevertheless fell by 0.44x to 1.77x as net debt was reduced by 26.4% to EUR 722m.
The point to watch is profitability against the network peers: the EBITDA margin fell by 1.5 points to 13.1%, the weakest of the group (3rd of 3).

> Event `event:labour`: Industrial action in the first half of the year had an immediate negative impact on the comparable operating result, and increased environmental regulation costs as well as higher navigation and landing charges also weighed on the result. Quote (page 3): "The prolonged industrial action during the first half of the year had an immediate negative impact of approximately 68 million euros on the comparable operating result. In addition, increased costs related to environmental regulation as well as higher navigation and landing charges weighed on the result."

## Credit metrics

Revenue was broadly unchanged at EUR 3.1bn, a move of 1.9%, but EBITDA declined by 8.2% to EUR 408m and operating profit by 43.8% to EUR 64.2m.
Total debt was reduced by 4.4% to EUR 1.8bn, yet gross leverage rose by 0.17x to 4.37x as EBITDA fell by 8.2%.
Interest coverage improved by 0.83x to 4.98x, but FFO fell by 21.2% to EUR 320m and FFO to debt by 3.8 points to 18.0%.
Free cash flow fell by 49.1% to EUR 193m, taking FCF to debt down by 9.5 points to 10.8%, while capex intensity eased by 1.0 point to 6.7%.

## Operating performance

Passengers were broadly stable at 11.9m, a move of 2.0%, with the fleet little changed at 79 aircraft and an average age of 14.3 years.
The fuel share of costs fell by 1.6 points to 28.9%, though costs related to environmental regulation and navigation charges weighed on the result.
During the year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date.

> Event `event:costs`: Costs related to environmental regulation increased significantly in 2025, with increased use of sustainable aviation fuel and changes to the EU Emissions Trading System weighing on the result. Quote (page 4): "In 2025, costs related to environmental regulation increased significantly, and the increased use of sustainable aviation fuel as well as changes to the EU Emissions Trading System weighed on the result."

> Event `event:fleet_and_engines`: During the financial year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date. Quote (page 163): "During the financial year Finnair purchased four leased A321 aircraft. All aircraft were in operative use as at the balance sheet date."

## Liquidity and funding

Liquidity rose by 16.3% to EUR 1.3bn, of which cash and cash-like investments of EUR 1.1bn were up 20.0%.
Undrawn committed facilities were stable at EUR 200m, and liquidity to revenue rose by 5.0 points to 40.6%.
Advance ticket cover fell by 7.1 points to 67.4%, while contract liabilities rose by 8.5% to EUR 715m.
Finnair issued a bond towards the end of the year to strengthen its financial position and support strategic investments.

> Event `event:funding_and_rating`: Finnair issued a bond towards the end of the year to further strengthen its financial position and support execution of strategic investments. Quote (page 4): "To further strengthen our financial position, we issued a 300million-euro bond towards the end of the year, supporting the execution of strategic investments in the coming years."

## Peer positioning

Finnair's EBITDA margin of 13.1% is below the network median of 15.3% and ranks 3rd of 3.
Gross leverage ranks 3rd of 3 against a peer median of 3.07x, and interest coverage ranks 3rd of 3 against 8.06x.
FFO to debt ranks 3rd of 3 against a median of 27.4%, while FCF to debt sits in the middle of the group (2nd of 3).
Cash liquidity to revenue is the strongest of the group (1st of 3), above the peer median of 25.0%, and capex intensity is below the median of 10.4%.

## Watch items

- Profitability: the EBITDA margin of 13.1% is the weakest of the network peers (3rd of 3), and FFO to debt of 18.0% is below the median of 27.4%.
- Cash generation: free cash flow fell by 49.1% to EUR 193m, and FCF to debt declined by 9.5 points to 10.8%.
- Leverage: gross leverage rose by 0.17x to 4.37x, above the peer median of 3.07x, and interest coverage of 4.98x is below the median of 8.06x.

> removed by the verifier (still broke a rule after two retries): "Costs: the fuel share of costs of {{fuel_share_of_costs@FY2025}} is above the peer median of {{fuel_share_of_costs.peer_median@FY2025}}, and costs related to environmental regulation increased during the year." ('increased' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 12,937 / 3,372 |
| 2 | credit_metrics, operating_performance, watch_items | 3 errors | 14,775 / 1,835 |
| 3 | credit_metrics, watch_items | 1 errors | 14,285 / 1,538 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 2: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule 3] watch_items, sentence 3: 'worse' claimed on interest_coverage@FY2025, but it is better
- [rule 4] watch_items, sentence 4: 'increased' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 5] credit_metrics, sentence 2: ebitda.change@FY2025 is listed in the form but not used in the text
- [rule 4] credit_metrics, sentence 2: 'declined' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 4: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, closed FY2025 with a weaker earnings profile as prolonged industrial action in the first half weighed on the result, with EBITDA down {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- Net leverage nevertheless fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt was reduced by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- The point to watch is profitability against the network peers: the EBITDA margin fell by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, the weakest of the group ({{ebitda_margin.peer_rank@FY2025}}).

`credit_metrics`

- Revenue was broadly unchanged at {{revenue@FY2025}}, a move of {{revenue.change@FY2025}}, but EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, yet gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} as EBITDA fell by {{ebitda.change@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, but FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}} and FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- Free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}}, taking FCF to debt down by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, while capex intensity eased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers were broadly stable at {{passengers@FY2025}}, a move of {{passengers.change@FY2025}}, with the fleet little changed at {{fleet@FY2025}} aircraft and an average age of {{fleet_age@FY2025}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}, though costs related to environmental regulation and navigation charges weighed on the result.
- During the year Finnair purchased leased A321 aircraft, and all aircraft were in operative use at the balance sheet date.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which cash and cash-like investments of {{cash_like@FY2025}} were up {{cash_like.change@FY2025}}.
- Undrawn committed facilities were stable at {{undrawn_facilities@FY2025}}, and liquidity to revenue rose by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}.
- Advance ticket cover fell by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, while contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}.
- Finnair issued a bond towards the end of the year to strengthen its financial position and support strategic investments.

`peer_positioning`

- Finnair's EBITDA margin of {{ebitda_margin@FY2025}} is below the network median of {{ebitda_margin.peer_median@FY2025}} and ranks {{ebitda_margin.peer_rank@FY2025}}.
- Gross leverage ranks {{gross_leverage.peer_rank@FY2025}} against a peer median of {{gross_leverage.peer_median@FY2025}}, and interest coverage ranks {{interest_coverage.peer_rank@FY2025}} against {{interest_coverage.peer_median@FY2025}}.
- FFO to debt ranks {{ffo_to_debt.peer_rank@FY2025}} against a median of {{ffo_to_debt.peer_median@FY2025}}, while FCF to debt sits in the middle of the group ({{fcf_to_debt.peer_rank@FY2025}}).
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), above the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}, and capex intensity is below the median of {{capex_intensity.peer_median@FY2025}}.

`watch_items`

- Profitability: the EBITDA margin of {{ebitda_margin@FY2025}} is the weakest of the network peers ({{ebitda_margin.peer_rank@FY2025}}), and FFO to debt of {{ffo_to_debt@FY2025}} is below the median of {{ffo_to_debt.peer_median@FY2025}}.
- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}}, and FCF to debt declined by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}.
- Leverage: gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, above the peer median of {{gross_leverage.peer_median@FY2025}}, and interest coverage of {{interest_coverage@FY2025}} is below the median of {{interest_coverage.peer_median@FY2025}}.
