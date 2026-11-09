# Wizz Air Holdings, FY2026 (Apr 2025 to Mar 2026): draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v5`, fact sheet `88d9ba71e1c5` ([fact sheet](../factsheets/wizz_FY2026.md)). Tokens: 28,980 in, 5,566 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Wizz Air, the low-cost carrier operating a unified Airbus fleet, grew revenue by 8.0% to EUR 5.7bn in FY2026 while the Pratt & Whitney GTF engine issue continued to ground aircraft and weigh on utilisation and costs.
The EBITDA margin widened by 1.7 points to 23.2% and net leverage fell by 0.49x to 3.79x, though leverage remains well above the peer median.
The point to watch is cash generation against a growing debt stock: FCF to debt slipped to 11.1% as total debt rose by 5.6% to EUR 7.0bn.

> Event `event:fleet_and_engines`: The Pratt & Whitney GTF engine issue continued to ground aircraft, affecting capacity, utilisation and cost performance, though fewer aircraft were grounded on average than in the prior year. Quote (page 4): "As in the previous year, the Pratt & Whitney Geared Turbofan (GTF) engine issue was a defining challenge for the Company in F26, although we saw improving trends with fewer aircraft grounded on average this year and slightly better turnaround times on our engines. With that said, fleet groundings have continued to affect capacity, utilisation and cost performance, creating structural headwinds largely beyond management’s direct control."

## Credit metrics

EBITDA increased by 16.2% to EUR 1.3bn, but operating profit fell by 16.6% to EUR 140m as depreciation and interest charges absorbed the gain.
Gross leverage fell by 0.53x to 5.28x and net leverage to 3.79x, although net debt rose by 3.1% to EUR 5.0bn.
FFO rose by 20.9% to EUR 1.1bn, lifting FFO to debt by 2.0 points to 15.2%, and interest coverage improved by 0.31x to 5.39x.
Free cash flow was broadly unchanged at EUR 772m, so FCF to debt fell by 0.8 points to 11.1% as capex intensity rose by 1.8 points to 7.2%.

## Operating performance

Passengers rose by 10.0% to 69.7m on capacity up 8.5% to 132.0bn available seat kilometres, with RPK up 7.9% to 119.9bn.
The load factor slipped by 0.5 points to 90.7% as capacity outgrew traffic, while passenger yield was broadly unchanged at 2.64 euro cents.
RASK was stable at 4.31 euro cents and CASK at 4.20 euro cents, but CASK ex-fuel rose by 5.7% to 2.87 euro cents, so the cost base outside fuel carried the pressure.
The fuel share of costs fell by 3.4 points to 31.8%, and the fleet grew by 13.4% to 262 aircraft with an average age of 4.6 years.

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, taking cash liquidity to revenue up by 1.3 points to 34.3%.
Advance ticket cover rose by 2.1 points to 60.5%, with contract liabilities up 16.5% to EUR 1.2bn, so a larger share of the cash balance is customer prepayment.
The company repaid its eurobond out of free cash and renewed its Euro Medium Term Note programme, while Fitch and Moody's issued ratings with stable and negative outlooks respectively.

> Event `event:funding_and_rating`: The company repaid its eurobond out of free cash, and Fitch and Moody's issued credit ratings with stable and negative outlooks respectively. Quote (page 96): "None of these borrowings contain any financial covenants and the €500.0 million, 1.00 per cent Eurobond was repaid in January 2026 out of free cash. Two ratings agencies, Fitch and Moody’s, issued updates during the fourth quarter with Fitch updating Wizz Air’s credit rating to BB with a stable outlook, while Moody’s issued a Ba2 rating with a negative outlook."

> Event `event:funding_and_rating-2`: The company renewed its Euro Medium Term Note programme for possible future euro bond issuance. Quote (page 64): "The Company renewed the Euro Medium Term Note Program with the total amount of EUR 3bn, for the possibility of future EUR Bond issuance in December 2025."

## Peer positioning

Wizz Air has the highest EBITDA margin in the low-cost peer group (1st of 3), against a median of 21.2%.
Leverage is the weakest in the group: net leverage ranks 3rd of 3 against a median of 1.19x, and gross leverage ranks 3rd of 3 against a median of 2.46x.
Cash generation is the weakest in the group, with FFO to debt ranking 3rd of 3 against a median of 35.4% and FCF to debt ranking 3rd of 3 against a median of 14.6%.
Cash liquidity to revenue sits in the middle of the group (2nd of 3), while interest coverage ranks 3rd of 3 against a median of 6.27x.

## Watch items

- Leverage: net leverage of 3.79x is above the peer median of 1.19x and ranks 3rd of 3, the weakest in the group, so the pace of deleveraging matters most.
- Cash generation: FFO to debt of 15.2% and FCF to debt of 11.1% both sit below the peer medians of 35.4% and 14.6%.
- Customer prepayments: advance ticket cover of 60.5% is above the peer median of 55.1% and ranks 3rd of 3, the weakest in the group, a sensitivity if bookings slow.
- Costs and fleet: CASK ex-fuel rose by 5.7% to 2.87 euro cents while the GTF engine issue continued to ground aircraft, and the fleet grew by 13.4% to 262 aircraft.

> Event `event:fleet_and_engines`: The Pratt & Whitney GTF engine issue continued to ground aircraft, affecting capacity, utilisation and cost performance, though fewer aircraft were grounded on average than in the prior year. Quote (page 4): "As in the previous year, the Pratt & Whitney Geared Turbofan (GTF) engine issue was a defining challenge for the Company in F26, although we saw improving trends with fewer aircraft grounded on average this year and slightly better turnaround times on our engines. With that said, fleet groundings have continued to affect capacity, utilisation and cost performance, creating structural headwinds largely beyond management’s direct control."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 13,475 / 3,538 |
| 2 | operating_performance, peer_positioning, watch_items | passed | 15,505 / 2,028 |

### Errors found, by try

Try 1:

- [rule 1] operating_performance, sentence 1: word that states a number: 'billion'
- [rule 4] peer_positioning, sentence 3: 'trails' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 4: capex_intensity@FY2026 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause
- [rule 5] watch_items, sentence 3: advance_ticket_cover.peer_rank@FY2026 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the low-cost carrier operating a unified Airbus fleet, grew revenue by {{revenue.change@FY2026}} to {{revenue@FY2026}} in FY2026 while the Pratt & Whitney GTF engine issue continued to ground aircraft and weigh on utilisation and costs.
- The EBITDA margin widened by {{ebitda_margin.change@FY2026}} to {{ebitda_margin@FY2026}} and net leverage fell by {{net_leverage.change@FY2026}} to {{net_leverage@FY2026}}, though leverage remains well above the peer median.
- The point to watch is cash generation against a growing debt stock: FCF to debt slipped to {{fcf_to_debt@FY2026}} as total debt rose by {{total_debt.change@FY2026}} to {{total_debt@FY2026}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2026}} to {{ebitda@FY2026}}, but operating profit fell by {{operating_profit.change@FY2026}} to {{operating_profit@FY2026}} as depreciation and interest charges absorbed the gain.
- Gross leverage fell by {{gross_leverage.change@FY2026}} to {{gross_leverage@FY2026}} and net leverage to {{net_leverage@FY2026}}, although net debt rose by {{net_debt.change@FY2026}} to {{net_debt@FY2026}}.
- FFO rose by {{ffo.change@FY2026}} to {{ffo@FY2026}}, lifting FFO to debt by {{ffo_to_debt.change@FY2026}} to {{ffo_to_debt@FY2026}}, and interest coverage improved by {{interest_coverage.change@FY2026}} to {{interest_coverage@FY2026}}.
- Free cash flow was broadly unchanged at {{fcf@FY2026}}, so FCF to debt fell by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}} as capex intensity rose by {{capex_intensity.change@FY2026}} to {{capex_intensity@FY2026}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2026}} to {{passengers@FY2026}} on capacity up {{ask.change@FY2026}} to {{ask@FY2026}} available seat kilometres, with RPK up {{rpk.change@FY2026}} to {{rpk@FY2026}}.
- The load factor slipped by {{load_factor.change@FY2026}} to {{load_factor@FY2026}} as capacity outgrew traffic, while passenger yield was broadly unchanged at {{passenger_yield@FY2026}}.
- RASK was stable at {{rask@FY2026}} and CASK at {{cask@FY2026}}, but CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}}, so the cost base outside fuel carried the pressure.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2026}} to {{fuel_share_of_costs@FY2026}}, and the fleet grew by {{fleet.change@FY2026}} to {{fleet@FY2026}} aircraft with an average age of {{fleet_age@FY2026}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2026}} to {{cash_like@FY2026}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2026}} to {{cash_liquidity_to_revenue@FY2026}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2026}} to {{advance_ticket_cover@FY2026}}, with contract liabilities up {{contract_liabilities.change@FY2026}} to {{contract_liabilities@FY2026}}, so a larger share of the cash balance is customer prepayment.
- The company repaid its eurobond out of free cash and renewed its Euro Medium Term Note programme, while Fitch and Moody's issued ratings with stable and negative outlooks respectively.

`peer_positioning`

- Wizz Air has the highest EBITDA margin in the low-cost peer group ({{ebitda_margin.peer_rank@FY2026}}), against a median of {{ebitda_margin.peer_median@FY2026}}.
- Leverage is the weakest in the group: net leverage ranks {{net_leverage.peer_rank@FY2026}} against a median of {{net_leverage.peer_median@FY2026}}, and gross leverage ranks {{gross_leverage.peer_rank@FY2026}} against a median of {{gross_leverage.peer_median@FY2026}}.
- Cash generation is the weakest in the group, with FFO to debt ranking {{ffo_to_debt.peer_rank@FY2026}} against a median of {{ffo_to_debt.peer_median@FY2026}} and FCF to debt ranking {{fcf_to_debt.peer_rank@FY2026}} against a median of {{fcf_to_debt.peer_median@FY2026}}.
- Cash liquidity to revenue sits in the middle of the group ({{cash_liquidity_to_revenue.peer_rank@FY2026}}), while interest coverage ranks {{interest_coverage.peer_rank@FY2026}} against a median of {{interest_coverage.peer_median@FY2026}}.

`watch_items`

- Leverage: net leverage of {{net_leverage@FY2026}} is above the peer median of {{net_leverage.peer_median@FY2026}} and ranks {{net_leverage.peer_rank@FY2026}}, the weakest in the group, so the pace of deleveraging matters most.
- Cash generation: FFO to debt of {{ffo_to_debt@FY2026}} and FCF to debt of {{fcf_to_debt@FY2026}} both sit below the peer medians of {{ffo_to_debt.peer_median@FY2026}} and {{fcf_to_debt.peer_median@FY2026}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2026}} is above the peer median of {{advance_ticket_cover.peer_median@FY2026}} and ranks {{advance_ticket_cover.peer_rank@FY2026}}, the weakest in the group, a sensitivity if bookings slow.
- Costs and fleet: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}} while the GTF engine issue continued to ground aircraft, and the fleet grew by {{fleet.change@FY2026}} to {{fleet@FY2026}} aircraft.
