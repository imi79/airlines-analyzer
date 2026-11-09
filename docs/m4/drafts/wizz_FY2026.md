# Wizz Air Holdings, FY2026 (Apr 2025 to Mar 2026): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `2d87de752355` ([fact sheet](../factsheets/wizz_FY2026.md)). Tokens: 45,904 in, 8,037 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Wizz Air, the Central and Eastern European low-cost carrier, grew revenue by 8.0% to EUR 5.7bn in FY2026 while the Pratt & Whitney GTF engine issue continued to ground aircraft and weigh on capacity, utilisation and cost performance.
The EBITDA margin widened by 1.7 points to 23.2%, and net leverage fell by 0.49x to 3.79x.
The point to watch is leverage against the low-cost peer group: net leverage of 3.79x and gross leverage of 5.28x both sit above the peer medians of 1.19x and 2.46x.

> Event `event:fleet_and_engines`: The Pratt & Whitney GTF engine issue continued to ground aircraft, affecting capacity, utilisation and cost performance, though fewer aircraft were grounded on average than in the prior year. Quote (page 4): "As in the previous year, the Pratt & Whitney Geared Turbofan (GTF) engine issue was a defining challenge for the Company in F26, although we saw improving trends with fewer aircraft grounded on average this year and slightly better turnaround times on our engines. With that said, fleet groundings have continued to affect capacity, utilisation and cost performance, creating structural headwinds largely beyond management’s direct control."

## Credit metrics

Total debt rose by 5.6% to EUR 7.0bn and net debt by 3.1% to EUR 5.0bn, yet gross leverage fell by 0.53x to 5.28x.
FFO rose by 20.9% to EUR 1.1bn, lifting FFO to debt by 2.0 points to 15.2%, and interest coverage improved by 0.31x to 5.39x.
Free cash flow was broadly unchanged at EUR 772m, so FCF to debt slipped by 0.8 points to 11.1% as capex intensity rose by 1.8 points to 7.2%.

> removed by the verifier (still broke a rule after two retries): "EBITDA rose by {{ebitda.change@FY2026}} to {{ebitda@FY2026}} on revenue up {{revenue.change@FY2026}}, but operating profit fell by {{operating_profit.change@FY2026}} to {{operating_profit@FY2026}} as depreciation increased with a larger fleet." ('increased' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers rose by 10.0% to 69.7m on capacity up 8.5% to 132.0bn available seat kilometres, with RPK up 7.9% to 119.9bn revenue passenger kilometres.
The load factor slipped by 0.5 points to 90.7% as capacity rose by 8.5% and traffic by 7.9%.
Unit revenue was stable, with passenger yield at 2.64 euro cents and RASK at 4.31 euro cents, while CASK was broadly unchanged at 4.20 euro cents but CASK ex-fuel rose by 5.7% to 2.87 euro cents.
The fuel share of costs fell by 3.4 points to 31.8%, and the fleet grew by 13.4% to 262 aircraft with an average age of 4.6 years.

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, taking cash liquidity to revenue up by 1.3 points to 34.3%.
Customer prepayments grew: contract liabilities rose by 16.5% to EUR 1.2bn, and advance ticket cover rose by 2.1 points to 60.5%.
The company repaid its eurobond out of free cash and renewed its Euro Medium Term Note programme, while Fitch and Moody's issued ratings with stable and negative outlooks respectively.

> Event `event:funding_and_rating`: The company repaid its eurobond out of free cash, and Fitch and Moody's issued credit ratings with stable and negative outlooks respectively. Quote (page 96): "None of these borrowings contain any financial covenants and the €500.0 million, 1.00 per cent Eurobond was repaid in January 2026 out of free cash. Two ratings agencies, Fitch and Moody’s, issued updates during the fourth quarter with Fitch updating Wizz Air’s credit rating to BB with a stable outlook, while Moody’s issued a Ba2 rating with a negative outlook."

> Event `event:funding_and_rating-2`: The company renewed its Euro Medium Term Note programme for possible future euro bond issuance. Quote (page 64): "The Company renewed the Euro Medium Term Note Program with the total amount of EUR 3bn, for the possibility of future EUR Bond issuance in December 2025."

## Peer positioning

Wizz Air has the highest EBITDA margin of the low-cost group (1st of 3), at 23.2% against a median of 21.2%.
Leverage is the weakest part of the profile: net leverage ranks 3rd of 3 and gross leverage 3rd of 3, with FFO to debt ranking 3rd of 3 against a peer median of 35.4%.
Cash liquidity to revenue sits in the middle of the group, and capex intensity is below the peer median of 9.9%.

## Watch items

- Leverage: net leverage of 3.79x and gross leverage of 5.28x remain well above the peer medians of 1.19x and 2.46x, the weakest position in the group (3rd of 3).
- Cash generation: FCF to debt fell by 0.8 points to 11.1%, below the peer median of 14.6%, as capex intensity rose to 7.2%.
- Customer prepayments: advance ticket cover of 60.5% is above the peer median of 55.1% and ranks 3rd of 3, so a larger share of cash is refundable if bookings slow.
- Costs: CASK ex-fuel rose by 5.7% to 2.87 euro cents while RASK was broadly unchanged at 4.31 euro cents, and the GTF engine groundings continued to affect capacity, utilisation and cost performance.

> Event `event:fleet_and_engines`: The Pratt & Whitney GTF engine issue continued to ground aircraft, affecting capacity, utilisation and cost performance, though fewer aircraft were grounded on average than in the prior year. Quote (page 4): "As in the previous year, the Pratt & Whitney Geared Turbofan (GTF) engine issue was a defining challenge for the Company in F26, although we saw improving trends with fewer aircraft grounded on average this year and slightly better turnaround times on our engines. With that said, fleet groundings have continued to affect capacity, utilisation and cost performance, creating structural headwinds largely beyond management’s direct control."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 13,716 / 3,448 |
| 2 | credit_metrics, operating_performance, peer_positioning, watch_items | 4 errors | 16,455 / 2,610 |
| 3 | credit_metrics, peer_positioning, watch_items | 1 errors | 15,733 / 1,979 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 1] operating_performance, sentence 1: word that states a number: 'billion'
- [rule 4] operating_performance, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: ffo_to_debt@FY2026 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2026 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause
- [rule 5] watch_items, sentence 3: advance_ticket_cover.peer_rank@FY2026 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 4: 'stable' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 1: 'increased' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: ffo_to_debt@FY2026 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2026 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'stable' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 1: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the Central and Eastern European low-cost carrier, grew revenue by {{revenue.change@FY2026}} to {{revenue@FY2026}} in FY2026 while the Pratt & Whitney GTF engine issue continued to ground aircraft and weigh on capacity, utilisation and cost performance.
- The EBITDA margin widened by {{ebitda_margin.change@FY2026}} to {{ebitda_margin@FY2026}}, and net leverage fell by {{net_leverage.change@FY2026}} to {{net_leverage@FY2026}}.
- The point to watch is leverage against the low-cost peer group: net leverage of {{net_leverage@FY2026}} and gross leverage of {{gross_leverage@FY2026}} both sit above the peer medians of {{net_leverage.peer_median@FY2026}} and {{gross_leverage.peer_median@FY2026}}.

`credit_metrics`

- Total debt rose by {{total_debt.change@FY2026}} to {{total_debt@FY2026}} and net debt by {{net_debt.change@FY2026}} to {{net_debt@FY2026}}, yet gross leverage fell by {{gross_leverage.change@FY2026}} to {{gross_leverage@FY2026}}.
- FFO rose by {{ffo.change@FY2026}} to {{ffo@FY2026}}, lifting FFO to debt by {{ffo_to_debt.change@FY2026}} to {{ffo_to_debt@FY2026}}, and interest coverage improved by {{interest_coverage.change@FY2026}} to {{interest_coverage@FY2026}}.
- Free cash flow was broadly unchanged at {{fcf@FY2026}}, so FCF to debt slipped by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}} as capex intensity rose by {{capex_intensity.change@FY2026}} to {{capex_intensity@FY2026}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2026}} to {{passengers@FY2026}} on capacity up {{ask.change@FY2026}} to {{ask@FY2026}} available seat kilometres, with RPK up {{rpk.change@FY2026}} to {{rpk@FY2026}} revenue passenger kilometres.
- The load factor slipped by {{load_factor.change@FY2026}} to {{load_factor@FY2026}} as capacity rose by {{ask.change@FY2026}} and traffic by {{rpk.change@FY2026}}.
- Unit revenue was stable, with passenger yield at {{passenger_yield@FY2026}} and RASK at {{rask@FY2026}}, while CASK was broadly unchanged at {{cask@FY2026}} but CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2026}} to {{fuel_share_of_costs@FY2026}}, and the fleet grew by {{fleet.change@FY2026}} to {{fleet@FY2026}} aircraft with an average age of {{fleet_age@FY2026}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2026}} to {{cash_like@FY2026}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2026}} to {{cash_liquidity_to_revenue@FY2026}}.
- Customer prepayments grew: contract liabilities rose by {{contract_liabilities.change@FY2026}} to {{contract_liabilities@FY2026}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2026}} to {{advance_ticket_cover@FY2026}}.
- The company repaid its eurobond out of free cash and renewed its Euro Medium Term Note programme, while Fitch and Moody's issued ratings with stable and negative outlooks respectively.

`peer_positioning`

- Wizz Air has the highest EBITDA margin of the low-cost group ({{ebitda_margin.peer_rank@FY2026}}), at {{ebitda_margin@FY2026}} against a median of {{ebitda_margin.peer_median@FY2026}}.
- Leverage is the weakest part of the profile: net leverage ranks {{net_leverage.peer_rank@FY2026}} and gross leverage {{gross_leverage.peer_rank@FY2026}}, with FFO to debt ranking {{ffo_to_debt.peer_rank@FY2026}} against a peer median of {{ffo_to_debt.peer_median@FY2026}}.
- Cash liquidity to revenue sits in the middle of the group, and capex intensity is below the peer median of {{capex_intensity.peer_median@FY2026}}.

`watch_items`

- Leverage: net leverage of {{net_leverage@FY2026}} and gross leverage of {{gross_leverage@FY2026}} remain well above the peer medians of {{net_leverage.peer_median@FY2026}} and {{gross_leverage.peer_median@FY2026}}, the weakest position in the group ({{net_leverage.peer_rank@FY2026}}).
- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}}, below the peer median of {{fcf_to_debt.peer_median@FY2026}}, as capex intensity rose to {{capex_intensity@FY2026}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2026}} is above the peer median of {{advance_ticket_cover.peer_median@FY2026}} and ranks {{advance_ticket_cover.peer_rank@FY2026}}, so a larger share of cash is refundable if bookings slow.
- Costs: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}} while RASK was broadly unchanged at {{rask@FY2026}}, and the GTF engine groundings continued to affect capacity, utilisation and cost performance.
