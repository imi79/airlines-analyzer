# Finnair, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `5e48d0d96d5c` ([fact sheet](../factsheets/finnair_FY2025.md)). Tokens: 23,666 in, 4,918 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Finnair, the Finnish network carrier, ended FY2025 with net leverage down to 1.77x from 2.21x, in line with the peer median, while revenue was broadly unchanged at EUR 3.1bn.
The EBITDA margin narrowed by 1.5 points to 13.1%, below the peer median, as EBITDA fell by 8.2% to EUR 408m.
The main point to watch is cash generation: FFO to debt fell by 3.8 points to 18.0% and free cash flow declined by 49.1% to EUR 193m, although liquidity to revenue rose to 40.6%.

## Credit metrics

EBITDA fell by 8.2% to EUR 408m on revenue of EUR 3.1bn, broadly unchanged year on year, and operating profit declined by 43.8% to EUR 64.2m.
Net debt was reduced by 26.4% to EUR 722m and total debt by 4.4% to EUR 1.8bn, which took net leverage down by 0.44x to 1.77x.
Gross leverage rose by 0.17x to 4.37x, above the peer median of 3.07x, as EBITDA fell by 8.2% while total debt was reduced by 4.4%.
Interest coverage weakened by 7.03x to 4.67x, well below the peer median of 8.06x.
FFO fell by 21.2% to EUR 320m, taking FFO to debt down by 3.8 points to 18.0%, while FCF to debt fell by 9.5 points to 10.8% as capex intensity eased to 6.7%.

## Operating performance

Passengers were broadly unchanged at 11.9m, a change of 2.0%, on a fleet that was stable at 79 aircraft with an average age of 14.3 years.
Revenue was broadly unchanged at EUR 3.1bn, a change of 1.9%, so the fall in EBITDA of 8.2% came from the cost side rather than from volumes.
The fuel share of costs fell by 1.6 points to 28.9%, above the peer median of 27.0%, leaving margins exposed to jet fuel prices.

## Liquidity and funding

Liquidity rose by 16.3% to EUR 1.3bn, of which EUR 200m in undrawn committed facilities, stable year on year.
Cash and cash-like investments increased by 20.0% to EUR 1.1bn, lifting cash liquidity to revenue by 5.2 points to 34.2%.
Advance ticket cover fell by 7.1 points to 67.4%, in line with the peer median, while contract liabilities rose by 8.5% to EUR 715m, so a larger share of liquidity is customers' prepayments.

## Peer positioning

Finnair ranks weakest of the network airlines on EBITDA margin (3rd of 3), at 13.1% against a peer median of 15.3%.
Gross leverage of 4.37x is above the peer median of 3.07x and ranks 3rd of 3, while net leverage of 1.77x is in line with the median of 1.71x.
Cash generation lags the group: FFO to debt of 18.0% is below the peer median of 27.4% and ranks 3rd of 3, while FCF to debt of 10.8% is in line with the median.
Cash liquidity to revenue of 34.2% is the strongest of the group (1st of 3), against a peer median of 25.0%.

## Watch items

- Cash generation: FFO to debt fell by 3.8 points to 18.0%, the weakest of the network peers (3rd of 3), so the earnings base needs to stabilise for leverage to hold.
- Coverage: interest coverage fell by 7.03x to 4.67x, below the peer median of 8.06x, which leaves less room if EBITDA weakens again.
- Leverage: gross leverage rose by 0.17x to 4.37x, above the peer median of 3.07x, while net leverage of 1.77x is in line with peers.
- Customer prepayments: contract liabilities of EUR 715m rose by 8.5%, and advance ticket cover of 67.4% is in line with the peer median, so part of the liquidity buffer is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 11,677 / 3,517 |
| 2 | credit_metrics, operating_performance | passed | 11,989 / 1,401 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 3: 'decline' needs a 'down' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 3: 'reduction' needs a 'down' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 2: 'decline' needs a 'down' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, ended FY2025 with net leverage down to {{net_leverage@FY2025}} from {{net_leverage@FY2024}}, in line with the peer median, while revenue was broadly unchanged at {{revenue@FY2025}}.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, below the peer median, as EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- The main point to watch is cash generation: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} and free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}}, although liquidity to revenue rose to {{liquidity_to_revenue@FY2025}}.

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue of {{revenue@FY2025}}, broadly unchanged year on year, and operating profit declined by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Net debt was reduced by {{net_debt.change@FY2025}} to {{net_debt@FY2025}} and total debt by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, which took net leverage down by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- Gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, above the peer median of {{gross_leverage.peer_median@2025}}, as EBITDA fell by {{ebitda.change@FY2025}} while total debt was reduced by {{total_debt.change@FY2025}}.
- Interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, well below the peer median of {{interest_coverage.peer_median@2025}}.
- FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, taking FFO to debt down by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, while FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} as capex intensity eased to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers were broadly unchanged at {{passengers@FY2025}}, a change of {{passengers.change@FY2025}}, on a fleet that was stable at {{fleet@FY2025}} aircraft with an average age of {{fleet_age@FY2025}}.
- Revenue was broadly unchanged at {{revenue@FY2025}}, a change of {{revenue.change@FY2025}}, so the fall in EBITDA of {{ebitda.change@FY2025}} came from the cost side rather than from volumes.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}, above the peer median of {{fuel_share_of_costs.peer_median@2025}}, leaving margins exposed to jet fuel prices.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which {{undrawn_facilities@FY2025}} in undrawn committed facilities, stable year on year.
- Cash and cash-like investments increased by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, lifting cash liquidity to revenue by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover fell by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, in line with the peer median, while contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of liquidity is customers' prepayments.

`peer_positioning`

- Finnair ranks weakest of the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@2025}}), at {{ebitda_margin@FY2025}} against a peer median of {{ebitda_margin.peer_median@2025}}.
- Gross leverage of {{gross_leverage@FY2025}} is above the peer median of {{gross_leverage.peer_median@2025}} and ranks {{gross_leverage.peer_rank@2025}}, while net leverage of {{net_leverage@FY2025}} is in line with the median of {{net_leverage.peer_median@2025}}.
- Cash generation lags the group: FFO to debt of {{ffo_to_debt@FY2025}} is below the peer median of {{ffo_to_debt.peer_median@2025}} and ranks {{ffo_to_debt.peer_rank@2025}}, while FCF to debt of {{fcf_to_debt@FY2025}} is in line with the median.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), against a peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.

`watch_items`

- Cash generation: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, the weakest of the network peers ({{ffo_to_debt.peer_rank@2025}}), so the earnings base needs to stabilise for leverage to hold.
- Coverage: interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, below the peer median of {{interest_coverage.peer_median@2025}}, which leaves less room if EBITDA weakens again.
- Leverage: gross leverage rose by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, above the peer median of {{gross_leverage.peer_median@2025}}, while net leverage of {{net_leverage@FY2025}} is in line with peers.
- Customer prepayments: contract liabilities of {{contract_liabilities@FY2025}} rose by {{contract_liabilities.change@FY2025}}, and advance ticket cover of {{advance_ticket_cover@FY2025}} is in line with the peer median, so part of the liquidity buffer is refundable if bookings slow.
