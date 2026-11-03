# easyJet, FY2024 (Oct 2023 to Sep 2024): draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `d02678c8a45b` ([fact sheet](../factsheets/easyjet_FY2024.md)). Tokens: 12,020 in, 3,213 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 13.9% to GBP 9.3bn in FY2024, with EBITDA up 20.7% to GBP 1.4bn.
The EBITDA margin widened by 0.8 points to 14.6%, while net leverage was broadly unchanged at -0.13x, a net cash position.
The main point to watch is cash generation: free cash flow fell by 32.7% to GBP 536m as capex intensity rose to 10.0%.

## Credit metrics

EBITDA rose by 20.7% to GBP 1.4bn and operating profit by 30.0% to GBP 589m, on revenue up 13.9%.
Gross leverage fell by 0.15x to 2.41x, even as total debt increased by 13.7% to GBP 3.3bn.
Interest coverage improved by 4.04x to 10.30x, and FFO to debt rose by 5.1 points to 38.1%.
Cash flow against debt weakened: FCF to debt fell by 11.3 points to 16.3%, with capex intensity up 0.8 points to 10.0%.

## Operating performance

Passengers rose by 8.3% to 89.7m, with capacity up 8.4% to 122.9bn available seat kilometres and revenue passenger kilometres up 8.4%.
The load factor was stable at 89.3% and passenger yield broadly unchanged at 5.12 pence.
Unit revenue rose by 5.1% to 7.58 pence, but unit cost rose by 4.2% to 7.10 pence and CASK ex-fuel by 5.4% to 5.29 pence.
The fleet grew by 3.3% to 347 aircraft, with an average age of 10.2 years, and fuel made up 25.5% of costs.

## Liquidity and funding

Cash and cash-like investments rose by 18.3% to GBP 3.5bn, and cash liquidity to revenue increased by 1.4 points to 37.2%.
Advance ticket cover eased by 1.0 point to 50.2%, while contract liabilities from advance ticket sales rose by 16.0% to GBP 1.7bn.
Undrawn committed facilities stood at GBP 1.8bn at the prior year end, a buffer that sits alongside the cash balance.

## Peer positioning

easyJet has the lowest net leverage in the low-cost peer group (1st of 3), at -0.13x against a peer median of 0.78x.
It leads the group on interest coverage (1st of 3) at 10.30x and on FFO to debt (1st of 3) at 38.1%.
Its EBITDA margin of 14.6% is the weakest of the group (3rd of 3), below the peer median of 18.9%, while gross leverage is in line with the median at 2.41x.
Cash liquidity to revenue is the strongest of the group (1st of 3), at 37.2% against a median of 33.0%.

## Watch items

- Cash generation: FCF to debt fell by 11.3 points to 16.3%, in line with the peer median of 16.3%.
- Investment: capex intensity rose by 0.8 points to 10.0%, above the peer median of 5.4%.
- Profitability: the EBITDA margin of 14.6% is below the peer median of 18.9%, the weakest of the group (3rd of 3).
- Customer prepayments: advance ticket cover of 50.2% is in line with the peer median of 50.2%, so contract liabilities of GBP 1.7bn remain a refund sensitivity.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 12,020 / 3,213 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, with EBITDA up {{ebitda.change@FY2024}} to {{ebitda@FY2024}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, while net leverage was broadly unchanged at {{net_leverage@FY2024}}, a net cash position.
- The main point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose to {{capex_intensity@FY2024}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} and operating profit by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}, on revenue up {{revenue.change@FY2024}}.
- Gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}, even as total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, and FFO to debt rose by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}.
- Cash flow against debt weakened: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, with capex intensity up {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, with capacity up {{ask.change@FY2024}} to {{ask@FY2024}} available seat kilometres and revenue passenger kilometres up {{rpk.change@FY2024}}.
- The load factor was stable at {{load_factor@FY2024}} and passenger yield broadly unchanged at {{passenger_yield@FY2024}}.
- Unit revenue rose by {{rask.change@FY2024}} to {{rask@FY2024}}, but unit cost rose by {{cask.change@FY2024}} to {{cask@FY2024}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}.
- The fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft, with an average age of {{fleet_age@FY2024}}, and fuel made up {{fuel_share_of_costs@FY2024}} of costs.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Advance ticket cover eased by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, while contract liabilities from advance ticket sales rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}.
- Undrawn committed facilities stood at {{undrawn_facilities@FY2023}} at the prior year end, a buffer that sits alongside the cash balance.

`peer_positioning`

- easyJet has the lowest net leverage in the low-cost peer group ({{net_leverage.peer_rank@2024}}), at {{net_leverage@FY2024}} against a peer median of {{net_leverage.peer_median@2024}}.
- It leads the group on interest coverage ({{interest_coverage.peer_rank@2024}}) at {{interest_coverage@FY2024}} and on FFO to debt ({{ffo_to_debt.peer_rank@2024}}) at {{ffo_to_debt@FY2024}}.
- Its EBITDA margin of {{ebitda_margin@FY2024}} is the weakest of the group ({{ebitda_margin.peer_rank@2024}}), below the peer median of {{ebitda_margin.peer_median@2024}}, while gross leverage is in line with the median at {{gross_leverage@FY2024}}.
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), at {{cash_liquidity_to_revenue@FY2024}} against a median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, in line with the peer median of {{fcf_to_debt.peer_median@2024}}.
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the peer median of {{capex_intensity.peer_median@2024}}.
- Profitability: the EBITDA margin of {{ebitda_margin@FY2024}} is below the peer median of {{ebitda_margin.peer_median@2024}}, the weakest of the group ({{ebitda_margin.peer_rank@2024}}).
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2024}} is in line with the peer median of {{advance_ticket_cover.peer_median@2024}}, so contract liabilities of {{contract_liabilities@FY2024}} remain a refund sensitivity.
