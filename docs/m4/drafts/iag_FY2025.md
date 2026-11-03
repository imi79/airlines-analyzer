# International Airlines Group, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `bc8628f5a628` ([fact sheet](../factsheets/iag_FY2025.md)). Tokens: 24,556 in, 5,022 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2025 with a stronger credit profile as EBITDA rose by 15.1% to EUR 7.7bn on revenue up 3.5% to EUR 33.2bn.
Net leverage fell by 0.35x to 0.78x, with the EBITDA margin up 2.3 points to 23.0%.
The point to watch is liquidity: cash liquidity to revenue fell by 5.6 points to 25.0% as cash and cash-like investments declined by 15.4% to EUR 8.3bn.

## Credit metrics

EBITDA increased by 15.1% to EUR 7.7bn and operating profit by 17.3% to EUR 5.0bn, on revenue of EUR 33.2bn.
Total debt was reduced by 17.7% to EUR 14.3bn and net debt by 20.9% to EUR 5.9bn, taking gross leverage down by 0.75x to 1.86x.
Cash generation strengthened: FFO rose by 15.3% to EUR 6.5bn, lifting FFO to debt by 13.0 points to 45.5% and FCF to debt to 22.1%.
Free cash flow declined by 11.5% to EUR 3.1bn as capex intensity rose by 1.6 points to 10.4%, while interest coverage improved by 2.79x to 11.49x.

## Operating performance

Capacity grew by 2.4% to 351.4bn available seat kilometres, while traffic was broadly unchanged, with RPK at 300.8bn on a change of 1.3%.
Passengers were stable at 121.6m, a change of 0.4%, and passenger yield rose by 1.1% to 9.63 euro cents.
Unit revenue rose by 1.1% to 9.45 euro cents while CASK fell by 1.0% to 8.02 euro cents, although CASK ex-fuel increased by 2.0% to 6.01 euro cents.
The fuel share of costs fell by 2.3 points to 25.1%, and the fleet grew by 4.3% to 627 aircraft at an average age of 12.6 years.

## Liquidity and funding

Liquidity fell by 17.2% to EUR 10.9bn, of which EUR 2.6bn in undrawn committed facilities, down 22.7%.
Cash and cash-like investments declined by 15.4% to EUR 8.3bn, taking liquidity to revenue down by 8.2 points to 33.0%.
Advance ticket cover rose by 11.8 points to 96.6%, so a larger share of the cash base is customer prepayments, while contract liabilities eased to EUR 8.0bn.

## Peer positioning

IAG leads the network airlines on EBITDA margin (1st of 3), net leverage (1st of 3) and gross leverage (1st of 3).
It also leads on interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3).
Net leverage of 0.78x is below the peer median of 1.71x, and FFO to debt of 45.5% is above the median of 27.4%.
Cash liquidity to revenue of 25.0% is in line with the peer median of 25.0%, ranking 2nd of 3.

## Watch items

- Liquidity: liquidity to revenue fell by 8.2 points to 33.0% and undrawn committed facilities were reduced by 22.7% to EUR 2.6bn, so the buffer against maturities is thinner.
- Customer prepayments: advance ticket cover of 96.6% is above the peer median of 67.4% and the weakest in the group (3rd of 3), a sensitivity if bookings slow.
- Cash flow: free cash flow declined by 11.5% to EUR 3.1bn as capex intensity rose by 1.6 points to 10.4%, in line with the peer median of 10.4%.
- Unit cost: CASK ex-fuel increased by 2.0% to 6.01 euro cents, so the fall in total CASK to 8.02 euro cents rests on the lower fuel share of costs of 25.1%.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 12,141 / 3,713 |
| 2 | operating_performance, peer_positioning | passed | 12,415 / 1,309 |

### Errors found, by try

Try 1:

- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2025 with a stronger credit profile as EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}}.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, with the EBITDA margin up {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} as cash and cash-like investments declined by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, on revenue of {{revenue@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} and FCF to debt to {{fcf_to_debt@FY2025}}.
- Free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, while interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.

`operating_performance`

- Capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres, while traffic was broadly unchanged, with RPK at {{rpk@FY2025}} on a change of {{rpk.change@FY2025}}.
- Passengers were stable at {{passengers@FY2025}}, a change of {{passengers.change@FY2025}}, and passenger yield rose by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}.
- Unit revenue rose by {{rask.change@FY2025}} to {{rask@FY2025}} while CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}}, although CASK ex-fuel increased by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}, and the fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft at an average age of {{fleet_age@FY2025}}.

`liquidity_funding`

- Liquidity fell by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which {{undrawn_facilities@FY2025}} in undrawn committed facilities, down {{undrawn_facilities.change@FY2025}}.
- Cash and cash-like investments declined by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking liquidity to revenue down by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, so a larger share of the cash base is customer prepayments, while contract liabilities eased to {{contract_liabilities@FY2025}}.

`peer_positioning`

- IAG leads the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@2025}}), net leverage ({{net_leverage.peer_rank@2025}}) and gross leverage ({{gross_leverage.peer_rank@2025}}).
- It also leads on interest coverage ({{interest_coverage.peer_rank@2025}}), FFO to debt ({{ffo_to_debt.peer_rank@2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@2025}}).
- Net leverage of {{net_leverage@FY2025}} is below the peer median of {{net_leverage.peer_median@2025}}, and FFO to debt of {{ffo_to_debt@FY2025}} is above the median of {{ffo_to_debt.peer_median@2025}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is in line with the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}, ranking {{cash_liquidity_to_revenue.peer_rank@2025}}.

`watch_items`

- Liquidity: liquidity to revenue fell by {{liquidity_to_revenue.change@FY2025}} to {{liquidity_to_revenue@FY2025}} and undrawn committed facilities were reduced by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}, so the buffer against maturities is thinner.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is above the peer median of {{advance_ticket_cover.peer_median@2025}} and the weakest in the group ({{advance_ticket_cover.peer_rank@2025}}), a sensitivity if bookings slow.
- Cash flow: free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, in line with the peer median of {{capex_intensity.peer_median@2025}}.
- Unit cost: CASK ex-fuel increased by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, so the fall in total CASK to {{cask@FY2025}} rests on the lower fuel share of costs of {{fuel_share_of_costs@FY2025}}.
