# International Airlines Group, FY2024: draft commentary

Status: **needs manual editing** (some sections still rejected after two retries). First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v3`, fact sheet `8bbbc1e5102e` ([fact sheet](../factsheets/iag_FY2024.md)). Tokens: 34,451 in, 4,712 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2024 with a stronger credit profile as revenue rose by 9.0% to EUR 32.1bn.
Net leverage fell by 0.53x to 1.13x, with the EBITDA margin up 1.8 points to 20.7%.
The main point to watch is the funding mix: undrawn committed facilities fell by 22.9% to EUR 3.4bn while total debt rose by 7.9% to EUR 17.3bn.

## Credit metrics

EBITDA increased by 19.3% to EUR 6.6bn and operating profit by 22.1% to EUR 4.3bn.
Gross leverage fell by 0.28x to 2.61x and net leverage by 0.53x to 1.13x, as net debt was reduced by 18.7% to EUR 7.5bn.
Interest coverage improved by 3.16x to 8.70x, in line with the peer median.
Cash generation strengthened: FFO rose by 31.9% to EUR 5.6bn, taking FFO to debt up 5.9 points to 32.5%.
Free cash flow rose by 169.4% to EUR 3.6bn, lifting FCF to debt by 12.3 points to 20.5%, helped by capex intensity easing by 2.3 points to 8.8%.

## Operating performance

Capacity grew by 6.2% to 343.3bn available seat kilometres, carrying 122.0m passengers.
Unit revenue outpaced unit cost: RASK rose by 2.6% to 9.35 euro cents, while CASK was broadly unchanged at 8.10 euro cents.
CASK ex-fuel rose by 3.4% to 5.89 euro cents, a weaker trend than the headline unit cost, with passenger yield at 9.52 euro cents.
The fuel share of costs fell by 1.7 points to 27.4%, below the peer median.
The fleet grew by 3.3% to 601 aircraft, with an average age of 12.4 years.

## Liquidity and funding

Liquidity rose by 17.6% to EUR 13.2bn, of which EUR 3.4bn in undrawn committed facilities.
Cash and cash-like investments increased by 43.7% to EUR 9.8bn, taking cash liquidity to revenue up 7.4 points to 30.6%.
Undrawn committed facilities fell by 22.9% to EUR 3.4bn, so the buffer relies more on cash than on committed lines.
Advance ticket cover fell by 28.8 points to 84.8%, while contract liabilities rose by 7.3% to EUR 8.3bn.

## Peer positioning

IAG leads the network airlines on EBITDA margin (1st of 3), at 20.7% against a peer median of 14.6%.
Net leverage of 1.13x and gross leverage of 2.61x are both below the peer medians of 1.88x and 3.56x, ranking 1st of 3 and 1st of 3.
FFO to debt of 32.5% is above the peer median of 23.4% (1st of 3), while FCF to debt of 20.5% is in line with the median of 20.3%.
Cash liquidity to revenue of 30.6% is the strongest of the group (1st of 3), against a peer median of 29.0%.

## Watch items (needs manual editing)

- Customer prepayments: advance ticket cover of 84.8% is above the peer median of 74.5% but ranks 3rd of 3, the weakest of the group.
- Committed lines: undrawn facilities fell by 22.9% to EUR 3.4bn, a weaker buffer even as liquidity rose to EUR 13.2bn.
- Unit cost: CASK ex-fuel rose by 3.4% to 5.89 euro cents, so the margin gain rests on unit revenue rather than on cost.
- Debt and fleet: total debt rose by 7.9% to EUR 17.3bn and the average fleet age by 3.3% to 12.4 years, which keeps refinancing and replacement needs in view.

> verifier: [rule 4] watch_items, sentence 2: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 1 errors | 11,977 / 3,584 |
| 2 | watch_items | 1 errors | 11,237 / 564 |
| 3 | watch_items | 1 errors | 11,237 / 564 |

### Errors found, by try

Try 1:

- [rule 4] watch_items, sentence 2: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

Try 2:

- [rule 4] watch_items, sentence 2: 'worse' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 2: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2024 with a stronger credit profile as revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}}.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, with the EBITDA margin up {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- The main point to watch is the funding mix: undrawn committed facilities fell by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}} while total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} and operating profit by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} and net leverage by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, as net debt was reduced by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, in line with the peer median.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, taking FFO to debt up {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}.
- Free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}}, lifting FCF to debt by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, helped by capex intensity easing by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Capacity grew by {{ask.change@FY2024}} to {{ask@FY2024}} available seat kilometres, carrying {{passengers@FY2024}} passengers.
- Unit revenue outpaced unit cost: RASK rose by {{rask.change@FY2024}} to {{rask@FY2024}}, while CASK was broadly unchanged at {{cask@FY2024}}.
- CASK ex-fuel rose by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, a weaker trend than the headline unit cost, with passenger yield at {{passenger_yield@FY2024}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}, below the peer median.
- The fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft, with an average age of {{fleet_age@FY2024}}.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2024}} to {{liquidity@FY2024}}, of which {{undrawn_facilities@FY2024}} in undrawn committed facilities.
- Cash and cash-like investments increased by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue up {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Undrawn committed facilities fell by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}, so the buffer relies more on cash than on committed lines.
- Advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, while contract liabilities rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}.

`peer_positioning`

- IAG leads the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2024}} against a peer median of {{ebitda_margin.peer_median@2024}}.
- Net leverage of {{net_leverage@FY2024}} and gross leverage of {{gross_leverage@FY2024}} are both below the peer medians of {{net_leverage.peer_median@2024}} and {{gross_leverage.peer_median@2024}}, ranking {{net_leverage.peer_rank@2024}} and {{gross_leverage.peer_rank@2024}}.
- FFO to debt of {{ffo_to_debt@FY2024}} is above the peer median of {{ffo_to_debt.peer_median@2024}} ({{ffo_to_debt.peer_rank@2024}}), while FCF to debt of {{fcf_to_debt@FY2024}} is in line with the median of {{fcf_to_debt.peer_median@2024}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), against a peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`watch_items`

- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2024}} is above the peer median of {{advance_ticket_cover.peer_median@2024}} but ranks {{advance_ticket_cover.peer_rank@2024}}, the weakest of the group.
- Committed lines: undrawn facilities fell by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}, a weaker buffer even as liquidity rose to {{liquidity@FY2024}}.
- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, so the margin gain rests on unit revenue rather than on cost.
- Debt and fleet: total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and the average fleet age by {{fleet_age.change@FY2024}} to {{fleet_age@FY2024}}, which keeps refinancing and replacement needs in view.
