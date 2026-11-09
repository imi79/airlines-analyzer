# Wizz Air Holdings, FY2026 (Apr 2025 to Mar 2026): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `88d9ba71e1c5` ([fact sheet](../factsheets/wizz_FY2026.md)). Tokens: 45,983 in, 7,845 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Wizz Air, the Central and Eastern European low-cost carrier, grew revenue by 8.0% to EUR 5.7bn in FY2026 while the Pratt & Whitney GTF engine issue continued to ground aircraft and weigh on capacity, utilisation and cost performance.
The EBITDA margin widened by 1.7 points to 23.2% and net leverage fell by 0.49x to 3.79x, still well above the peer median.
The point to watch is leverage: net debt rose by 3.1% to EUR 5.0bn as the fleet expanded to 262 aircraft, leaving net leverage at the weakest level of the low-cost group (3rd of 3).

> Event `event:fleet_and_engines`: The Pratt & Whitney GTF engine issue continued to ground aircraft, affecting capacity, utilisation and cost performance, though fewer aircraft were grounded on average than in the prior year. Quote (page 4): "As in the previous year, the Pratt & Whitney Geared Turbofan (GTF) engine issue was a defining challenge for the Company in F26, although we saw improving trends with fewer aircraft grounded on average this year and slightly better turnaround times on our engines. With that said, fleet groundings have continued to affect capacity, utilisation and cost performance, creating structural headwinds largely beyond management’s direct control."

## Credit metrics

Total debt rose by 5.6% to EUR 7.0bn, yet gross leverage fell by 0.53x to 5.28x on the stronger earnings base.
FFO increased by 20.9% to EUR 1.1bn, lifting FFO to debt by 2.0 points to 15.2%, and interest coverage improved by 0.31x to 5.39x.
Free cash flow was broadly unchanged at EUR 772m, so FCF to debt fell by 0.8 points to 11.1% as capex intensity rose by 1.8 points to 7.2%.

> removed by the verifier (still broke a rule after two retries): "EBITDA increased by {{ebitda.change@FY2026}} to {{ebitda@FY2026}}, but operating profit fell by {{operating_profit.change@FY2026}} to {{operating_profit@FY2026}} as depreciation rose with the larger fleet." ('rose' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers rose by 10.0% to 69.7m on capacity up 8.5% to 132.0bn available seat kilometres, with RPK up 7.9% to 119.9bn revenue passenger kilometres.
The load factor slipped by 0.5 points to 90.7%, in line with the peer median.
Unit revenue was stable, with RASK at 4.31 euro cents and passenger yield at 2.64 euro cents, while CASK was broadly unchanged at 4.20 euro cents.
CASK ex-fuel rose by 5.7% to 2.87 euro cents, while the fuel share of costs fell by 3.4 points to 31.8%.
The fleet grew by 13.4% to 262 aircraft with an average age of 4.6 years, and the company renegotiated its Airbus order book to defer deliveries and support lifting the grounded fleet.

> Event `event:fleet_and_engines-2`: Wizz Air renegotiated its remaining Airbus order book, deferring deliveries and taking fewer aircraft than usual to support lifting the grounded fleet. Quote (page 23): "Wizz Air has re-negotiated the remaining order book of 254 aircraft with Airbus, deferring deliveries from 2030 to 2032, reshaping the long-term fleet plan, with the renegotiation finalised in November 2025. Due to the Pratt & Whitney GTF engine inspections in F28, Wizz Air negotiated to take 20-25% fewer deliveries than usual to support the main strategy of lifting the grounded fleet and to maintain balanced operational fleet growth following the initial plans of annual 13-15%."

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, taking cash liquidity to revenue up by 1.3 points to 34.3%.
Customer prepayments grew: contract liabilities rose by 16.5% to EUR 1.2bn, and advance ticket cover rose by 2.1 points to 60.5%, above the peer median.
The company repaid its eurobond out of free cash and renewed its Euro Medium Term Note programme, with Fitch and Moody's issuing ratings with stable and negative outlooks respectively.

> Event `event:funding_and_rating`: The company repaid its eurobond out of free cash, and Fitch and Moody's issued credit ratings with stable and negative outlooks respectively. Quote (page 96): "None of these borrowings contain any financial covenants and the €500.0 million, 1.00 per cent Eurobond was repaid in January 2026 out of free cash. Two ratings agencies, Fitch and Moody’s, issued updates during the fourth quarter with Fitch updating Wizz Air’s credit rating to BB with a stable outlook, while Moody’s issued a Ba2 rating with a negative outlook."

> Event `event:funding_and_rating-2`: The company renewed its Euro Medium Term Note programme for possible future euro bond issuance. Quote (page 64): "The Company renewed the Euro Medium Term Note Program with the total amount of EUR 3bn, for the possibility of future EUR Bond issuance in December 2025."

## Peer positioning

Wizz Air has the highest EBITDA margin of the low-cost group (1st of 3), at 23.2% against a median of 21.2%.
Leverage is the weakest in the group, with net leverage ranking 3rd of 3 against a peer median of 1.19x and gross leverage ranking 3rd of 3 against 2.46x.

> removed by the verifier (still broke a rule after two retries): "Cash generation and coverage are also below the group, with FFO to debt ranking {{ffo_to_debt.peer_rank@FY2026}} against a median of {{ffo_to_debt.peer_median@FY2026}} and interest coverage ranking {{interest_coverage.peer_rank@FY2026}} against {{interest_coverage.peer_median@FY2026}}, while cash liquidity to revenue sits in the middle of the group at {{cash_liquidity_to_revenue.peer_median@FY2026}}." ('below' needs a 'down' or 'below_peers' claim on a figure in the same clause)

## Watch items

- Leverage: net leverage of 3.79x is the highest of the low-cost group (3rd of 3) and gross leverage of 5.28x is above the peer median of 2.46x.
- Cash flow: FCF to debt fell by 0.8 points to 11.1%, below the peer median of 14.6%, as capex intensity rose to 7.2%.
- Unit cost: CASK ex-fuel rose by 5.7% to 2.87 euro cents, and the GTF engine issue continued to affect capacity, utilisation and cost performance.
- Customer prepayments: advance ticket cover of 60.5% is the highest of the group (3rd of 3), so a larger share of cash depends on forward bookings.

> Event `event:fleet_and_engines`: The Pratt & Whitney GTF engine issue continued to ground aircraft, affecting capacity, utilisation and cost performance, though fewer aircraft were grounded on average than in the prior year. Quote (page 4): "As in the previous year, the Pratt & Whitney Geared Turbofan (GTF) engine issue was a defining challenge for the Company in F26, although we saw improving trends with fewer aircraft grounded on average this year and slightly better turnaround times on our engines. With that said, fleet groundings have continued to affect capacity, utilisation and cost performance, creating structural headwinds largely beyond management’s direct control."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 13 errors | 13,747 / 3,491 |
| 2 | snapshot, credit_metrics, operating_performance, peer_positioning, watch_items | 3 errors | 17,239 / 3,041 |
| 3 | credit_metrics, peer_positioning | 2 errors | 14,997 / 1,313 |

### Errors found, by try

Try 1:

- [rule 3] snapshot, sentence 2: 'worse' claimed on net_leverage@FY2026, but it is better
- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 1] operating_performance, sentence 1: word that states a number: 'billion'
- [rule 3] peer_positioning, sentence 2: 'worse' claimed on net_leverage@FY2026, but it is better
- [rule 3] peer_positioning, sentence 2: 'worse' claimed on gross_leverage@FY2026, but it is better
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2026 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2026 is listed in the form but not used in the text
- [rule 3] peer_positioning, sentence 3: 'worse' claimed on ffo_to_debt@FY2026, but it is better
- [rule 3] peer_positioning, sentence 3: 'worse' claimed on interest_coverage@FY2026, but it is better
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2026 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2026 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] watch_items, sentence 1: 'worse' claimed on net_leverage@FY2026, but it is better
- [rule 3] watch_items, sentence 1: 'worse' claimed on gross_leverage@FY2026, but it is better

Try 2:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue.peer_median@FY2026 is listed in the form but not used in the text
- [rule 4] peer_positioning, sentence 3: 'trail' needs a 'down' or 'below_peers' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] peer_positioning, sentence 3: 'below' needs a 'down' or 'below_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the Central and Eastern European low-cost carrier, grew revenue by {{revenue.change@FY2026}} to {{revenue@FY2026}} in FY2026 while the Pratt & Whitney GTF engine issue continued to ground aircraft and weigh on capacity, utilisation and cost performance.
- The EBITDA margin widened by {{ebitda_margin.change@FY2026}} to {{ebitda_margin@FY2026}} and net leverage fell by {{net_leverage.change@FY2026}} to {{net_leverage@FY2026}}, still well above the peer median.
- The point to watch is leverage: net debt rose by {{net_debt.change@FY2026}} to {{net_debt@FY2026}} as the fleet expanded to {{fleet@FY2026}} aircraft, leaving net leverage at the weakest level of the low-cost group ({{net_leverage.peer_rank@FY2026}}).

`credit_metrics`

- Total debt rose by {{total_debt.change@FY2026}} to {{total_debt@FY2026}}, yet gross leverage fell by {{gross_leverage.change@FY2026}} to {{gross_leverage@FY2026}} on the stronger earnings base.
- FFO increased by {{ffo.change@FY2026}} to {{ffo@FY2026}}, lifting FFO to debt by {{ffo_to_debt.change@FY2026}} to {{ffo_to_debt@FY2026}}, and interest coverage improved by {{interest_coverage.change@FY2026}} to {{interest_coverage@FY2026}}.
- Free cash flow was broadly unchanged at {{fcf@FY2026}}, so FCF to debt fell by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}} as capex intensity rose by {{capex_intensity.change@FY2026}} to {{capex_intensity@FY2026}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2026}} to {{passengers@FY2026}} on capacity up {{ask.change@FY2026}} to {{ask@FY2026}} available seat kilometres, with RPK up {{rpk.change@FY2026}} to {{rpk@FY2026}} revenue passenger kilometres.
- The load factor slipped by {{load_factor.change@FY2026}} to {{load_factor@FY2026}}, in line with the peer median.
- Unit revenue was stable, with RASK at {{rask@FY2026}} and passenger yield at {{passenger_yield@FY2026}}, while CASK was broadly unchanged at {{cask@FY2026}}.
- CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}}, while the fuel share of costs fell by {{fuel_share_of_costs.change@FY2026}} to {{fuel_share_of_costs@FY2026}}.
- The fleet grew by {{fleet.change@FY2026}} to {{fleet@FY2026}} aircraft with an average age of {{fleet_age@FY2026}}, and the company renegotiated its Airbus order book to defer deliveries and support lifting the grounded fleet.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2026}} to {{cash_like@FY2026}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2026}} to {{cash_liquidity_to_revenue@FY2026}}.
- Customer prepayments grew: contract liabilities rose by {{contract_liabilities.change@FY2026}} to {{contract_liabilities@FY2026}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2026}} to {{advance_ticket_cover@FY2026}}, above the peer median.
- The company repaid its eurobond out of free cash and renewed its Euro Medium Term Note programme, with Fitch and Moody's issuing ratings with stable and negative outlooks respectively.

`peer_positioning`

- Wizz Air has the highest EBITDA margin of the low-cost group ({{ebitda_margin.peer_rank@FY2026}}), at {{ebitda_margin@FY2026}} against a median of {{ebitda_margin.peer_median@FY2026}}.
- Leverage is the weakest in the group, with net leverage ranking {{net_leverage.peer_rank@FY2026}} against a peer median of {{net_leverage.peer_median@FY2026}} and gross leverage ranking {{gross_leverage.peer_rank@FY2026}} against {{gross_leverage.peer_median@FY2026}}.

`watch_items`

- Leverage: net leverage of {{net_leverage@FY2026}} is the highest of the low-cost group ({{net_leverage.peer_rank@FY2026}}) and gross leverage of {{gross_leverage@FY2026}} is above the peer median of {{gross_leverage.peer_median@FY2026}}.
- Cash flow: FCF to debt fell by {{fcf_to_debt.change@FY2026}} to {{fcf_to_debt@FY2026}}, below the peer median of {{fcf_to_debt.peer_median@FY2026}}, as capex intensity rose to {{capex_intensity@FY2026}}.
- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2026}} to {{cask_ex_fuel@FY2026}}, and the GTF engine issue continued to affect capacity, utilisation and cost performance.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2026}} is the highest of the group ({{advance_ticket_cover.peer_rank@FY2026}}), so a larger share of cash depends on forward bookings.
