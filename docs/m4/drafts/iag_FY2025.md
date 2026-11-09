# International Airlines Group, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `1bbd381c6a23` ([fact sheet](../factsheets/iag_FY2025.md)). Tokens: 43,212 in, 6,602 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2025 with a stronger credit profile as revenue rose by 3.5% to EUR 33.2bn and EBITDA by 15.1% to EUR 7.7bn.
Net leverage fell by 0.35x to 0.78x and gross leverage by 0.75x to 1.86x, with the EBITDA margin up 2.3 points to 23.0%.
The point to watch is liquidity: cash and cash-like investments fell by 15.4% to EUR 8.3bn and liquidity to revenue by 8.2 points to 33.0%, alongside the announced return of excess cash to shareholders.

> Event `event:capital_returns`: The company announced a share buyback and a further return of excess cash to shareholders in the coming year. Quote (page 12): "Last February we announced a €1 billion share buyback and we are pleased to be announcing another return of excess cash of €1.5 billion today. This takes the total amount of excess cash returns announced in the last three years to €2.85 billion as we build a track record of cash returns to shareholders."

## Credit metrics

EBITDA increased by 15.1% to EUR 7.7bn and operating profit by 17.3% to EUR 5.0bn, lifting the EBITDA margin to 23.0%.
Total debt was reduced by 17.7% to EUR 14.3bn and net debt by 20.9% to EUR 5.9bn, so gross leverage fell to 1.86x from 2.61x.
Cash generation strengthened: FFO rose by 15.3% to EUR 6.5bn, taking FFO to debt up by 13.0 points to 45.5%.
Free cash flow declined by 11.5% to EUR 3.1bn as capex intensity rose by 1.6 points to 10.4%, although FCF to debt still improved to 22.1%.

> removed by the verifier (still broke a rule after two retries): "Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, with the reduction in total debt and the rise in EBITDA both supporting the ratio." (total_debt.change@FY2025 is listed in the form but not used in the text; ebitda.change@FY2025 is listed in the form but not used in the text)

## Operating performance

Capacity grew by 2.4% to 351.4bn available seat kilometres, while passengers were broadly unchanged at 121.6m and RPK at 300.8bn.
Unit revenue improved: RASK rose by 1.1% to 9.45 euro cents and passenger yield by 1.1% to 9.63 euro cents.
CASK fell by 1.0% to 8.02 euro cents, but CASK ex-fuel rose by 2.0% to 6.01 euro cents, so the unit cost gain came from fuel.
Fuel made up 25.1% of costs, down 2.3 points from the prior year.
The fleet grew by 4.3% to 627 aircraft at an average age of 12.6 years, broadly unchanged year on year, with supply chain pressures limiting availability after Rolls Royce engine problems.

> Event `event:fleet_and_engines`: British Airways reduced frequencies to some Middle East destinations because of a lack of available aircraft following Rolls Royce engine problems, while Boeing and Airbus reported delivery shortfalls. Quote (page 44): "Supply chain pressures continued in 2025. British Airways reduced frequencies to some Middle East destinations due to a lack of available aircraft after experiencing Rolls Royce engine problems, and Boeing and Airbus reported delivery shortfalls."

## Liquidity and funding

Liquidity fell by 17.2% to EUR 10.9bn, of which EUR 2.6bn in undrawn committed facilities, down 22.7%.
Cash and cash-like investments declined by 15.4% to EUR 8.3bn, taking cash liquidity to revenue down by 5.6 points to 25.0%.
Advance ticket cover rose by 11.8 points to 96.6%, while contract liabilities were reduced by 3.6% to EUR 8.0bn, so a larger share of the cash base is customers' prepayments.

## Peer positioning

IAG leads the network airlines on EBITDA margin (1st of 3), net leverage (1st of 3) and gross leverage (1st of 3).
It also ranks at the top on interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3), against a peer median FFO to debt of 27.4%.
Capex intensity and cash liquidity to revenue sit in the middle of the group, with cash liquidity to revenue ranking 2nd of 3.
Advance ticket cover is the weakest of the group (3rd of 3), above the peer median of 67.4%.

## Watch items

- Liquidity: liquidity to revenue fell by 8.2 points to 33.0% and undrawn committed facilities by 22.7% to EUR 2.6bn, a thinner buffer as cash is returned to shareholders.
- Customer prepayments: advance ticket cover of 96.6% is the highest of the group (3rd of 3), so a larger part of liquidity is refundable if bookings slow.
- Unit cost: CASK ex-fuel rose by 2.0% to 6.01 euro cents, so the decline in total CASK rests on the reduced fuel share of 25.1%.
- Cash flow: free cash flow fell by 11.5% to EUR 3.1bn as capex intensity rose by 1.6 points to 10.4%, in line with the peer median.

> Event `event:capital_returns`: The company announced a share buyback and a further return of excess cash to shareholders in the coming year. Quote (page 12): "Last February we announced a €1 billion share buyback and we are pleased to be announcing another return of excess cash of €1.5 billion today. This takes the total amount of excess cash returns announced in the last three years to €2.85 billion as we build a track record of cash returns to shareholders."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 13,457 / 3,698 |
| 2 | credit_metrics, peer_positioning, watch_items | 2 errors | 15,476 / 2,027 |
| 3 | credit_metrics | 2 errors | 14,279 / 877 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 5: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'
- [rule 4] watch_items, sentence 3: 'fall' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause

Try 2:

- [rule 5] credit_metrics, sentence 5: total_debt.change@FY2025 is listed in the form but not used in the text
- [rule 5] credit_metrics, sentence 5: ebitda.change@FY2025 is listed in the form but not used in the text

Try 3:

- [rule 5] credit_metrics, sentence 5: total_debt.change@FY2025 is listed in the form but not used in the text
- [rule 5] credit_metrics, sentence 5: ebitda.change@FY2025 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2025 with a stronger credit profile as revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}} and EBITDA by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} and gross leverage by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, with the EBITDA margin up {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The point to watch is liquidity: cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}} and liquidity to revenue by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}, alongside the announced return of excess cash to shareholders.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, lifting the EBITDA margin to {{ebitda_margin@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, so gross leverage fell to {{gross_leverage@FY2025}} from {{gross_leverage@FY2024}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, taking FFO to debt up by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- Free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, although FCF to debt still improved to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres, while passengers were broadly unchanged at {{passengers@FY2025}} and RPK at {{rpk@FY2025}}.
- Unit revenue improved: RASK rose by {{rask.change@FY2025}} to {{rask@FY2025}} and passenger yield by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}.
- CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}}, but CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, so the unit cost gain came from fuel.
- Fuel made up {{fuel_share_of_costs@FY2025}} of costs, down {{fuel_share_of_costs.change@FY2025}} from the prior year.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft at an average age of {{fleet_age@FY2025}}, broadly unchanged year on year, with supply chain pressures limiting availability after Rolls Royce engine problems.

`liquidity_funding`

- Liquidity fell by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which {{undrawn_facilities@FY2025}} in undrawn committed facilities, down {{undrawn_facilities.change@FY2025}}.
- Cash and cash-like investments declined by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, while contract liabilities were reduced by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of the cash base is customers' prepayments.

`peer_positioning`

- IAG leads the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@FY2025}}), net leverage ({{net_leverage.peer_rank@FY2025}}) and gross leverage ({{gross_leverage.peer_rank@FY2025}}).
- It also ranks at the top on interest coverage ({{interest_coverage.peer_rank@FY2025}}), FFO to debt ({{ffo_to_debt.peer_rank@FY2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@FY2025}}), against a peer median FFO to debt of {{ffo_to_debt.peer_median@FY2025}}.
- Capex intensity and cash liquidity to revenue sit in the middle of the group, with cash liquidity to revenue ranking {{cash_liquidity_to_revenue.peer_rank@FY2025}}.
- Advance ticket cover is the weakest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), above the peer median of {{advance_ticket_cover.peer_median@FY2025}}.

`watch_items`

- Liquidity: liquidity to revenue fell by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}} and undrawn committed facilities by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}, a thinner buffer as cash is returned to shareholders.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is the highest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), so a larger part of liquidity is refundable if bookings slow.
- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, so the decline in total CASK rests on the reduced fuel share of {{fuel_share_of_costs@FY2025}}.
- Cash flow: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, in line with the peer median.
