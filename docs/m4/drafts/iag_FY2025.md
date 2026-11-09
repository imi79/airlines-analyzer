# International Airlines Group, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `5ea6d9870f97` ([fact sheet](../factsheets/iag_FY2025.md)). Tokens: 46,155 in, 6,384 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, grew revenue by 3.5% to EUR 33.2bn in FY2025, a year in which industrial action and supply-chain constraints disrupted operations.
The EBITDA margin widened by 2.3 points to 23.0% and net leverage fell by 0.35x to 0.78x, the lowest of the network peers (1st of 3).
The point to watch is liquidity: cash liquidity to revenue fell by 5.6 points to 25.0% as cash was returned to shareholders.

> Event `event:one_offs`: A July strike by air traffic control in France led to large daily cancellations and direct costs for the group. Quote (page 45): "ATC strikes caused significant disruption, especially in France, where a July strike resulted in 1,400 daily cancellations and over €120 million in direct costs for the"

> Event `event:fleet_and_engines`: British Airways reduced frequencies to some Middle East destinations because of a lack of available aircraft following Rolls Royce engine problems, while Boeing and Airbus reported delivery shortfalls. Quote (page 44): "Supply chain pressures continued in 2025. British Airways reduced frequencies to some Middle East destinations due to a lack of available aircraft after experiencing Rolls Royce engine problems, and Boeing and Airbus reported delivery shortfalls."

> Event `event:capital_returns`: The company announced a share buyback and a further return of excess cash to shareholders in the coming year. Quote (page 12): "Last February we announced a €1 billion share buyback and we are pleased to be announcing another return of excess cash of €1.5 billion today. This takes the total amount of excess cash returns announced in the last three years to €2.85 billion as we build a track record of cash returns to shareholders."

## Credit metrics

EBITDA increased by 15.1% to EUR 7.7bn, and operating profit rose by 17.3% to EUR 5.0bn even as depreciation, amortisation and impairment grew by 11.2%.
Total debt was reduced by 17.7% to EUR 14.3bn and net debt by 20.9% to EUR 5.9bn, taking gross leverage down by 0.75x to 1.86x.
Interest coverage improved by 2.79x to 11.49x as finance costs fell by 6.1% to EUR 861m.
FFO rose by 15.3% to EUR 6.5bn, lifting FFO to debt by 13.0 points to 45.5%.
Free cash flow fell by 11.5% to EUR 3.1bn as capex rose by 22.2% to EUR 3.4bn, although FCF to debt still improved by 1.6 points to 22.1% on the smaller debt base.

## Operating performance

Capacity grew by 2.4% to 351.4bn available seat kilometres, while traffic was broadly unchanged, with RPK stable at 300.8bn and passengers stable at 121.6m.
Unit revenue improved: RASK rose by 1.1% to 9.45 euro cents and passenger yield by 1.1% to 9.63 euro cents.
CASK fell by 1.0% to 8.02 euro cents, but CASK ex-fuel rose by 2.0% to 6.01 euro cents as fuel cost declined by 6.9% to EUR 7.1bn and its share of costs eased by 2.3 points to 25.1%.
The fleet grew by 4.3% to 627 aircraft at an average age of 12.6 years, broadly unchanged, with engine availability constraining British Airways' Middle East schedule.

> Event `event:fleet_and_engines`: British Airways reduced frequencies to some Middle East destinations because of a lack of available aircraft following Rolls Royce engine problems, while Boeing and Airbus reported delivery shortfalls. Quote (page 44): "Supply chain pressures continued in 2025. British Airways reduced frequencies to some Middle East destinations due to a lack of available aircraft after experiencing Rolls Royce engine problems, and Boeing and Airbus reported delivery shortfalls."

## Liquidity and funding

Liquidity fell by 17.2% to EUR 10.9bn, of which cash and cash-like investments declined by 15.4% to EUR 8.3bn.
Undrawn committed facilities fell by 22.7% to EUR 2.6bn, so the buffer outside cash narrowed as well.
Liquidity to revenue fell by 8.2 points to 33.0%, and cash liquidity to revenue by 5.6 points to 25.0%.
Advance ticket cover rose by 11.8 points to 96.6% while contract liabilities declined by 3.6% to EUR 8.0bn, so a larger share of the cash base is customer prepayments.

## Peer positioning

IAG leads the network airlines on leverage and cash generation, with the lowest net leverage (1st of 3) and gross leverage (1st of 3) and the highest FFO to debt (1st of 3).
Its EBITDA margin is the highest of the group (1st of 3), well above the peer median of 15.3%, and interest coverage also ranks at the top (1st of 3).
The weakest point is customer prepayment cover, where advance ticket cover is the highest of the group (3rd of 3) against a peer median of 67.4%, while capex intensity and cash liquidity to revenue sit in the middle of the group.

## Watch items

- Liquidity: cash liquidity to revenue fell by 5.6 points to 25.0%, in line with the peer median but weaker than a year earlier.
- Cash returns: the group announced a share buyback and a further return of excess cash, which will keep drawing on the cash base that already fell by 15.4% to EUR 8.3bn.
- Customer prepayments: advance ticket cover is above the peer median of 67.4% and the highest of the group (3rd of 3), a sensitivity if bookings slow.
- Unit cost: CASK ex-fuel rose by 2.0% to 6.01 euro cents, so the decline in total unit cost rests on the fuel bill, which fell by 6.9% to EUR 7.1bn.

> Event `event:capital_returns`: The company announced a share buyback and a further return of excess cash to shareholders in the coming year. Quote (page 12): "Last February we announced a €1 billion share buyback and we are pleased to be announcing another return of excess cash of €1.5 billion today. This takes the total amount of excess cash returns announced in the last three years to €2.85 billion as we build a track record of cash returns to shareholders."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 14,337 / 3,709 |
| 2 | snapshot, operating_performance, peer_positioning, watch_items | 2 errors | 16,968 / 2,121 |
| 3 | watch_items | passed | 14,850 / 554 |

### Errors found, by try

Try 1:

- [rule 5] snapshot, sentence 2: net_leverage.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'
- [rule style] peer_positioning, sentence 2: interest_coverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] watch_items, sentence 3: advance_ticket_cover.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 4: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'improvement' needs a 'better' or 'better_than_peers' or 'best_in_group' claim on a figure in the same clause

Try 2:

- [rule 4] watch_items, sentence 4: 'fall' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, a year in which industrial action and supply-chain constraints disrupted operations.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}} and net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, the lowest of the network peers ({{net_leverage.peer_rank@FY2025}}).
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} as cash was returned to shareholders.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} even as depreciation, amortisation and impairment grew by {{dda.change@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as finance costs fell by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- Free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex rose by {{capex.change@FY2025}} to {{capex@FY2025}}, although FCF to debt still improved by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} on the smaller debt base.

`operating_performance`

- Capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres, while traffic was broadly unchanged, with RPK stable at {{rpk@FY2025}} and passengers stable at {{passengers@FY2025}}.
- Unit revenue improved: RASK rose by {{rask.change@FY2025}} to {{rask@FY2025}} and passenger yield by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}.
- CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}}, but CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}} as fuel cost declined by {{fuel_cost.change@FY2025}} to {{fuel_cost@FY2025}} and its share of costs eased by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft at an average age of {{fleet_age@FY2025}}, broadly unchanged, with engine availability constraining British Airways' Middle East schedule.

`liquidity_funding`

- Liquidity fell by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which cash and cash-like investments declined by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
- Undrawn committed facilities fell by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}, so the buffer outside cash narrowed as well.
- Liquidity to revenue fell by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}, and cash liquidity to revenue by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}} while contract liabilities declined by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of the cash base is customer prepayments.

`peer_positioning`

- IAG leads the network airlines on leverage and cash generation, with the lowest net leverage ({{net_leverage.peer_rank@FY2025}}) and gross leverage ({{gross_leverage.peer_rank@FY2025}}) and the highest FFO to debt ({{ffo_to_debt.peer_rank@FY2025}}).
- Its EBITDA margin is the highest of the group ({{ebitda_margin.peer_rank@FY2025}}), well above the peer median of {{ebitda_margin.peer_median@FY2025}}, and interest coverage also ranks at the top ({{interest_coverage.peer_rank@FY2025}}).
- The weakest point is customer prepayment cover, where advance ticket cover is the highest of the group ({{advance_ticket_cover.peer_rank@FY2025}}) against a peer median of {{advance_ticket_cover.peer_median@FY2025}}, while capex intensity and cash liquidity to revenue sit in the middle of the group.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, in line with the peer median but weaker than a year earlier.
- Cash returns: the group announced a share buyback and a further return of excess cash, which will keep drawing on the cash base that already fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
- Customer prepayments: advance ticket cover is above the peer median of {{advance_ticket_cover.peer_median@FY2025}} and the highest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), a sensitivity if bookings slow.
- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, so the decline in total unit cost rests on the fuel bill, which fell by {{fuel_cost.change@FY2025}} to {{fuel_cost@FY2025}}.
