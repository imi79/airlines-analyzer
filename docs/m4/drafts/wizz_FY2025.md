# Wizz Air Holdings, FY2025 (Apr 2024 to Mar 2025): draft commentary

Status: **needs manual editing** (some sections still rejected after two retries). First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `e824efb7a4e7` ([fact sheet](../factsheets/wizz_FY2025.md)). Tokens: 44,995 in, 6,541 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot (needs manual editing)

Wizz Air, the low-cost carrier operating an all-Airbus narrowbody fleet, saw its credit profile weaken in FY2025 as grounded aircraft from the Pratt & Whitney engine recall held capacity broadly unchanged while revenue rose 3.8% to EUR 5.3bn.
Net leverage rose by 0.38x to 4.28x as EBITDA fell 4.9% and net debt increased 4.2% to EUR 4.9bn.
The point to watch is the cost base: CASK ex-fuel rose 18.9% to 2.71 euro cents, leaving interest coverage at 5.08x and FFO to debt at 13.2%, both below the peer median.

> Event `event:fleet_and_engines`: A manufacturer recall affecting some of the company's aircraft engines, together with a shortage of spare engines and limited maintenance shop capacity, forced a large number of aircraft to be grounded at any time during the fiscal year. Quote (page 6): "A year ago this time, Wizz Air faced an unprecedented situation due to a manufacturer recall affecting some of our aircraft engines. This shortage of spare engines and limited maintenance shop capacity forced between forty and fifty-five aircraft to be grounded at any time during this F25 fiscal year."

> verifier: [rule 5] snapshot, sentence 1: ask.change@FY2025 is listed in the form but not used in the text

> verifier: [rule 4] snapshot, sentence 1: 'weaken' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

## Credit metrics

EBITDA fell by 4.9% to EUR 1.1bn on revenue up 3.8%, and the EBITDA margin narrowed by 2.0 points to 21.5%.
Operating profit fell by 61.7% to EUR 168m, with depreciation between EBITDA and the operating line absorbing the fleet expansion.
Total debt rose by 5.5% to EUR 6.6bn and net debt by 4.2% to EUR 4.9bn, taking gross leverage up by 0.58x to 5.81x and net leverage to 4.28x.
FFO fell by 13.3% to EUR 872m, so FFO to debt declined by 2.9 points to 13.2%, while interest coverage weakened by 1.93x to 5.08x.
Free cash flow rose by 139.9% to EUR 783m, lifting FCF to debt by 6.7 points to 11.9%, helped by capex intensity easing by 1.3 points to 5.4%.

## Operating performance

Passengers rose by 2.2% to 63.4m while capacity was broadly unchanged, with ASK at 121.7bn and RPK at 111.1bn.
The load factor improved by 0.9 points to 91.2%, and RASK rose by 3.9% to 4.33 euro cents on a passenger yield of 2.62 euro cents.
Unit cost moved against the revenue line: CASK rose by 10.1% to 4.19 euro cents and CASK ex-fuel by 18.9% to 2.71 euro cents, with the fuel share of costs down 4.8 points to 35.2%.
The fleet grew by 11.1% to 231 aircraft, with an average age of 4.5 years, as new A321neo deliveries were partly offset by redeliveries of older aircraft.

> Event `event:fleet_and_engines-4`: The company took delivery of new A321neo aircraft, secured former Wizz Air aircraft on dry leases and redelivered A320ceo aircraft, ending the fiscal year with a larger total fleet. Quote (page 8): "During F25 , Wizz Air took delivery of 26 new A321neo aircraft and also secured three former Wizz Air aircraft on dry leases, while six A320ceo aircraft were redelivered, ending the fiscal year with a total fleet of 231 aircraft: 37x A320ceo, 41x A321ceo, 6x A320neo and 147x A321neo."

## Liquidity and funding

Cash and cash-like investments rose by 9.3% to EUR 1.7bn, and cash liquidity to revenue improved by 1.7 points to 33.0%.
Customer prepayments grew faster than the cash balance: contract liabilities rose by 27.1% to EUR 1.0bn, and advance ticket cover increased by 8.2 points to 58.4%, above the peer median.

> removed by the verifier (still broke a rule after two retries): "The rating trajectory reflects the leverage path: Fitch downgraded the company to BB+ with a stable outlook, citing slower capacity growth from the engine issues and higher leverage." ('growth' needs a 'up' claim on a figure in the same clause; 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Peer positioning

Wizz Air has the highest EBITDA margin in the low-cost peer group (1st of 3), against a median of 18.9%.
Leverage and cash generation are the weak spots: net leverage and gross leverage are the highest of the group (3rd of 3 and 3rd of 3), and FFO to debt and FCF to debt are the lowest (3rd of 3 and 3rd of 3).
Capex intensity and cash liquidity to revenue sit in the middle of the group, with cash liquidity to revenue ranking 2nd of 3.

## Watch items

- Leverage: net leverage rose to 4.28x, the highest of the peer group (3rd of 3), and gross leverage to 5.81x against a peer median of 2.41x.
- Cash generation: FFO to debt fell by 2.9 points to 13.2%, the weakest of the group (3rd of 3), and interest coverage declined by 1.93x to 5.08x.
- Cost base: CASK ex-fuel rose by 18.9% to 2.71 euro cents, outpacing the RASK increase of 3.9%.
- Customer prepayments: advance ticket cover of 58.4% is the highest of the group (3rd of 3), so a larger share of the cash balance is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 10 errors | 13,709 / 3,853 |
| 2 | snapshot, liquidity_funding, peer_positioning | 5 errors | 15,882 / 1,334 |
| 3 | snapshot, liquidity_funding, peer_positioning | 4 errors | 15,404 / 1,354 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'flat' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule 4] snapshot, sentence 1: 'weaken' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: net_leverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: fcf_to_debt@FY2025 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 4] snapshot, sentence 1: 'unchanged' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule 4] snapshot, sentence 1: 'weaken' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 3:

- [rule 5] snapshot, sentence 1: ask.change@FY2025 is listed in the form but not used in the text
- [rule 4] snapshot, sentence 1: 'weaken' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the low-cost carrier operating an all-Airbus narrowbody fleet, saw its credit profile weaken in FY2025 as grounded aircraft from the Pratt & Whitney engine recall held capacity broadly unchanged while revenue rose {{revenue.change@FY2025}} to {{revenue@FY2025}}.
- Net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as EBITDA fell {{ebitda.change@FY2025}} and net debt increased {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- The point to watch is the cost base: CASK ex-fuel rose {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, leaving interest coverage at {{interest_coverage@FY2025}} and FFO to debt at {{ffo_to_debt@FY2025}}, both below the peer median.

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}}, and the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Operating profit fell by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, with depreciation between EBITDA and the operating line absorbing the fleet expansion.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, taking gross leverage up by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} and net leverage to {{net_leverage@FY2025}}.
- FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, so FFO to debt declined by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, while interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- Free cash flow rose by {{fcf.change@FY2025}} to {{fcf@FY2025}}, lifting FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, helped by capex intensity easing by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}} while capacity was broadly unchanged, with ASK at {{ask@FY2025}} and RPK at {{rpk@FY2025}}.
- The load factor improved by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}, and RASK rose by {{rask.change@FY2025}} to {{rask@FY2025}} on a passenger yield of {{passenger_yield@FY2025}}.
- Unit cost moved against the revenue line: CASK rose by {{cask.change@FY2025}} to {{cask@FY2025}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, with the fuel share of costs down {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}}, as new A321neo deliveries were partly offset by redeliveries of older aircraft.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue improved by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments grew faster than the cash balance: contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, above the peer median.

`peer_positioning`

- Wizz Air has the highest EBITDA margin in the low-cost peer group ({{ebitda_margin.peer_rank@FY2025}}), against a median of {{ebitda_margin.peer_median@FY2025}}.
- Leverage and cash generation are the weak spots: net leverage and gross leverage are the highest of the group ({{net_leverage.peer_rank@FY2025}} and {{gross_leverage.peer_rank@FY2025}}), and FFO to debt and FCF to debt are the lowest ({{ffo_to_debt.peer_rank@FY2025}} and {{fcf_to_debt.peer_rank@FY2025}}).
- Capex intensity and cash liquidity to revenue sit in the middle of the group, with cash liquidity to revenue ranking {{cash_liquidity_to_revenue.peer_rank@FY2025}}.

`watch_items`

- Leverage: net leverage rose to {{net_leverage@FY2025}}, the highest of the peer group ({{net_leverage.peer_rank@FY2025}}), and gross leverage to {{gross_leverage@FY2025}} against a peer median of {{gross_leverage.peer_median@FY2025}}.
- Cash generation: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, the weakest of the group ({{ffo_to_debt.peer_rank@FY2025}}), and interest coverage declined by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- Cost base: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, outpacing the RASK increase of {{rask.change@FY2025}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is the highest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), so a larger share of the cash balance is refundable if bookings slow.
