# Wizz Air Holdings, FY2026 (Apr 2025 to Mar 2026): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v3`, fact sheet `85737c655e0f` ([fact sheet](../factsheets/wizz_FY2026.md)). Tokens: 37,731 in, 7,347 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Wizz Air, the low-cost carrier, grew revenue by 8.0% to EUR 5.7bn in FY2026, but operating profit fell by 16.6% to EUR 140m as CASK ex-fuel increased by 5.7%.
Net leverage fell by 0.49x to 3.79x and gross leverage by 0.53x to 5.28x, helped by EBITDA up 16.2% to EUR 1.3bn.
The main point to watch is the gap to peers: net leverage of 3.79x is above the peer median of 1.19x, and FFO to debt of 15.2% sits below the peer median of 35.4%.

## Credit metrics

EBITDA rose by 16.2% to EUR 1.3bn on revenue up 8.0% to EUR 5.7bn, lifting the EBITDA margin by 1.7 points to 23.2%.
Total debt increased by 5.6% to EUR 7.0bn and net debt by 3.1% to EUR 5.0bn, so net leverage fell by 0.49x to 3.79x only because EBITDA grew by 16.2%.
FFO rose by 20.9% to EUR 1.1bn, taking FFO to debt up by 2.0 points to 15.2%, while interest coverage improved by 0.31x to 5.39x.
Free cash flow was stable at EUR 772m, so FCF to debt fell by 0.8 points to 11.1% as capex intensity rose by 1.8 points to 7.2%.

## Operating performance

Passengers rose by 10.0% to 69.7m on capacity up 8.5% to 132.0bn available seat kilometres, with RPK up 7.9% to 119.9bn revenue passenger kilometres.
The load factor slipped by 0.5 points to 90.7%, in line with the peer median of 90.7%.
Unit revenue was stable, with RASK at 4.31 euro cents and passenger yield at 2.64 euro cents, while CASK was broadly unchanged at 4.20 euro cents.
CASK ex-fuel rose by 5.7% to 2.87 euro cents, the cost line that offset the fuel benefit, as the fuel share of costs fell by 3.4 points to 31.8%.
The fleet grew by 13.4% to 262 aircraft, with an average age of 4.6 years.

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, taking cash liquidity to revenue up by 1.3 points to 34.3%.
Cash liquidity to revenue of 34.3% is in line with the peer median of 34.3%, ranking 2nd of 3.
Customer prepayments rose: advance ticket cover increased by 2.1 points to 60.5% and contract liabilities by 16.5% to EUR 1.2bn, so a larger share of liquidity is refundable cash.

## Peer positioning

Wizz Air has the highest EBITDA margin in the low-cost peer group (1st of 3), at 23.2% against a median of 21.2%.
Leverage is the weakest in the group: net leverage of 3.79x ranks 3rd of 3 against a peer median of 1.19x, and gross leverage of 5.28x ranks 3rd of 3.
Cash generation and coverage trail the group: FFO to debt of 15.2% and FCF to debt of 11.1% both rank 3rd of 3 against medians of 35.4% and 14.6%, and interest coverage of 5.39x ranks 3rd of 3.

## Watch items

- Costs: CASK ex-fuel rose by 5.7% to 2.87 euro cents while RASK was stable at 4.31 euro cents, so unit profitability depends on non-fuel cost control.
- Leverage: net leverage of 3.79x is above the peer median of 1.19x and ranks 3rd of 3, with total debt up 5.6% to EUR 7.0bn.
- Cash flow: FCF to debt fell by 0.8 points to 11.1% as capex intensity rose by 1.8 points to 7.2%, below the peer median of 9.9% but rising with fleet growth.
- Customer prepayments: advance ticket cover of 60.5% is above the peer median of 55.1% and ranks 3rd of 3, so liquidity of EUR 2.0bn carries a refund exposure if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 12,046 / 3,890 |
| 2 | snapshot, credit_metrics, operating_performance, liquidity_funding | 1 errors | 14,154 / 2,581 |
| 3 | credit_metrics | passed | 11,531 / 876 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] snapshot, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 2: 'improved' needs a 'better' or 'better_than_peers' or 'best_in_group' claim on a figure in the same clause
- [rule 1] operating_performance, sentence 1: word that states a number: 'billion'
- [rule 4] liquidity_funding, sentence 2: 'in line' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 2: 'fell' needs a 'down' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the low-cost carrier, grew revenue by {{revenue.change@FY2026}} to {{revenue@FY2026}} in FY2026, but operating profit fell by {{operating_profit.change@FY2026}} to {{operating_profit@FY2026}} as CASK ex-fuel increased by {{cask_ex_fuel.change@FY2026}}.
- Net leverage fell by {{net_leverage.change@FY2026}} to {{net_leverage@FY2026}} and gross leverage by {{gross_leverage.change@FY2026}} to {{gross_leverage@FY2026}}, helped by EBITDA up {{ebitda.change@FY2026}} to {{ebitda@FY2026}}.
- The main point to watch is the gap to peers: net leverage of {{net_leverage@FY2026}} is above the peer median of {{net_leverage.peer_median@2025}}, and FFO to debt of {{ffo_to_debt@FY2026}} sits below the peer median of {{ffo_to_debt.peer_median@2025}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2026}} to {{ebitda@FY2026}} on revenue up {{revenue.change@FY2026}} to {{revenue@FY2026}}, lifting the EBITDA margin by {{ebitda_margin.change@FY2026}} to {{ebitda_margin@FY2026}}.
- Total debt increased by {{total_debt.change@FY2026}} to {{total_debt@FY2026}} and net debt by {{net_debt.change@FY2026}} to {{net_debt@FY2026}}, so net leverage fell by {{net_leverage.change@FY2026}} to {{net_leverage@FY2026}} only because EBITDA grew by {{ebitda.change@FY2026}}.
- FFO rose by {{ffo.change@FY2026}} to {{ffo@FY2026}}, taking FFO to debt up by {{ffo_to_debt.change@FY2026}} to {{ffo_to_debt@FY2026}}, while interest coverage improved by {{interest_coverage.change@FY2026}} to {{interest_coverage@FY2026}}.
- Free cash flow was stable at {{fcf@FY2026}}, so FCF to debt fell by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}} as capex intensity rose by {{capex_intensity.change@FY2026}} to {{capex_intensity@FY2026}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2026}} to {{passengers@FY2026}} on capacity up {{ask.change@FY2026}} to {{ask@FY2026}} available seat kilometres, with RPK up {{rpk.change@FY2026}} to {{rpk@FY2026}} revenue passenger kilometres.
- The load factor slipped by {{load_factor.change@FY2026}} to {{load_factor@FY2026}}, in line with the peer median of {{load_factor.peer_median@2025}}.
- Unit revenue was stable, with RASK at {{rask@FY2026}} and passenger yield at {{passenger_yield@FY2026}}, while CASK was broadly unchanged at {{cask@FY2026}}.
- CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}}, the cost line that offset the fuel benefit, as the fuel share of costs fell by {{fuel_share_of_costs.change@FY2026}} to {{fuel_share_of_costs@FY2026}}.
- The fleet grew by {{fleet.change@FY2026}} to {{fleet@FY2026}} aircraft, with an average age of {{fleet_age@FY2026}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2026}} to {{cash_like@FY2026}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2026}} to {{cash_liquidity_to_revenue@FY2026}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2026}} is in line with the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}, ranking {{cash_liquidity_to_revenue.peer_rank@2025}}.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2026}} to {{advance_ticket_cover@FY2026}} and contract liabilities by {{contract_liabilities.change@FY2026}} to {{contract_liabilities@FY2026}}, so a larger share of liquidity is refundable cash.

`peer_positioning`

- Wizz Air has the highest EBITDA margin in the low-cost peer group ({{ebitda_margin.peer_rank@2025}}), at {{ebitda_margin@FY2026}} against a median of {{ebitda_margin.peer_median@2025}}.
- Leverage is the weakest in the group: net leverage of {{net_leverage@FY2026}} ranks {{net_leverage.peer_rank@2025}} against a peer median of {{net_leverage.peer_median@2025}}, and gross leverage of {{gross_leverage@FY2026}} ranks {{gross_leverage.peer_rank@2025}}.
- Cash generation and coverage trail the group: FFO to debt of {{ffo_to_debt@FY2026}} and FCF to debt of {{fcf_to_debt@FY2026}} both rank {{ffo_to_debt.peer_rank@2025}} against medians of {{ffo_to_debt.peer_median@2025}} and {{fcf_to_debt.peer_median@2025}}, and interest coverage of {{interest_coverage@FY2026}} ranks {{interest_coverage.peer_rank@2025}}.

`watch_items`

- Costs: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}} while RASK was stable at {{rask@FY2026}}, so unit profitability depends on non-fuel cost control.
- Leverage: net leverage of {{net_leverage@FY2026}} is above the peer median of {{net_leverage.peer_median@2025}} and ranks {{net_leverage.peer_rank@2025}}, with total debt up {{total_debt.change@FY2026}} to {{total_debt@FY2026}}.
- Cash flow: FCF to debt fell by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}} as capex intensity rose by {{capex_intensity.change@FY2026}} to {{capex_intensity@FY2026}}, below the peer median of {{capex_intensity.peer_median@2025}} but rising with fleet growth.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2026}} is above the peer median of {{advance_ticket_cover.peer_median@2025}} and ranks {{advance_ticket_cover.peer_rank@2025}}, so liquidity of {{cash_like@FY2026}} carries a refund exposure if bookings slow.
