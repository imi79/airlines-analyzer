# Wizz Air Holdings, FY2025 (Apr 2024 to Mar 2025): draft commentary

Status: **needs manual editing** (some sections still rejected after two retries). First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `6a904918485b` ([fact sheet](../factsheets/wizz_FY2025.md)). Tokens: 46,800 in, 7,437 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot (needs manual editing)

Wizz Air, the low-cost carrier operating an all-Airbus narrowbody fleet, saw its EBITDA margin narrow by 2.0 points to 21.5% in FY2025, a year in which a manufacturer engine recall forced a large part of the fleet to be grounded at any time.
Net leverage rose by 0.38x to 4.28x as EBITDA fell by 4.9% to EUR 1.1bn.
The point to watch is leverage against the peer group: net leverage of 4.28x compares with a peer median of 0.78x, and Fitch downgraded the company citing higher leverage and increased costs.

> Event `event:fleet_and_engines`: A manufacturer recall affecting some of the company's aircraft engines, together with a shortage of spare engines and limited maintenance shop capacity, forced a large number of aircraft to be grounded at any time during the fiscal year. Quote (page 6): "A year ago this time, Wizz Air faced an unprecedented situation due to a manufacturer recall affecting some of our aircraft engines. This shortage of spare engines and limited maintenance shop capacity forced between forty and fifty-five aircraft to be grounded at any time during this F25 fiscal year."

> Event `event:funding_and_rating`: Fitch Ratings downgraded the company with a stable outlook, citing slower capacity growth from the engine issues, higher leverage and increased costs. Quote (page 15): "In October 2024, Wizz Air was downgraded by Fitch Ratings to 'BB+' with a ‘Stable Outlook’ due to the slower capacity growth caused by the Pratt & Whitney engine issues, leading to higher leverage, above the 2.0x threshold for a 'BBB-' rating; and increased costs impacting profitability."

> verifier: [rule 4] snapshot, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

## Credit metrics

Revenue rose by 3.8% to EUR 5.3bn, but EBITDA fell by 4.9% to EUR 1.1bn as CASK rose by 10.1% to 4.19 euro cents.
Operating profit fell by 61.7% to EUR 168m as depreciation, amortisation and impairment rose by 28.0% to EUR 967m.
Total debt increased by 5.5% to EUR 6.6bn and net debt by 4.2% to EUR 4.9bn, taking gross leverage up by 0.58x to 5.81x.
Interest coverage fell by 1.93x to 5.08x as finance costs rose by 26.8% to EUR 250m.
FFO fell by 13.3% to EUR 872m, so FFO to debt declined by 2.9 points to 13.2%, while free cash flow rose by 139.9% to EUR 783m as cash from operations increased by 60.4% and capex fell by 16.4%.

## Operating performance

Passengers rose by 2.2% to 63.4m while capacity was broadly unchanged, with ASK broadly stable at 121.7bn available seat kilometres.
The load factor improved by 0.9 points to 91.2%, with RPK broadly stable at 111.1bn.
RASK rose by 3.9% to 4.33 euro cents, but CASK ex-fuel rose by 18.9% to 2.71 euro cents, so unit cost outpaced unit revenue.
Fuel cost fell by 3.1% to EUR 1.8bn, and the fuel share of costs declined by 4.8 points to 35.2%.
The fleet grew by 11.1% to 231 aircraft, with an average age of 4.5 years, as new A321neo aircraft were delivered and older A320ceo aircraft redelivered.

> Event `event:fleet_and_engines-4`: The company took delivery of new A321neo aircraft, secured former Wizz Air aircraft on dry leases and redelivered A320ceo aircraft, ending the fiscal year with a larger total fleet. Quote (page 8): "During F25 , Wizz Air took delivery of 26 new A321neo aircraft and also secured three former Wizz Air aircraft on dry leases, while six A320ceo aircraft were redelivered, ending the fiscal year with a total fleet of 231 aircraft: 37x A320ceo, 41x A321ceo, 6x A320neo and 147x A321neo."

## Liquidity and funding

Cash and cash-like investments rose by 9.3% to EUR 1.7bn, taking cash liquidity to revenue up by 1.7 points to 33.0%.
Advance ticket cover rose by 8.2 points to 58.4%, and contract liabilities increased by 27.1% to EUR 1.0bn, so a larger share of the cash balance is customers' prepayments.
Cash generation supported the balance sheet, with cash from operations of EUR 1.1bn against capex of EUR 283m and capex intensity down by 1.3 points to 5.4%.

## Peer positioning

Wizz Air has the highest EBITDA margin of the low-cost peer group (1st of 3), at 21.5% against a median of 18.9%.
Leverage is the weakest part of the comparison: net leverage of 4.28x ranks 3rd of 3 against a peer median of 0.78x, and FFO to debt ranks 3rd of 3 against a median of 35.6%.
Cash liquidity to revenue and capex intensity both sit in the middle of the group, with cash liquidity to revenue ranking 2nd of 3.

## Watch items

- Leverage: net leverage rose by 0.38x to 4.28x, well above the peer median of 0.78x, and Fitch downgraded the company citing higher leverage and increased costs.
- Cash flow: FFO to debt fell by 2.9 points to 13.2%, below the peer median of 35.6%, as FFO declined by 13.3%.
- Coverage: interest coverage fell by 1.93x to 5.08x, below the peer median of 5.89x, as finance costs rose by 26.8%.
- Customer prepayments: advance ticket cover rose by 8.2 points to 58.4%, above the peer median of 50.2%, a sensitivity if bookings slow.

> Event `event:funding_and_rating`: Fitch Ratings downgraded the company with a stable outlook, citing slower capacity growth from the engine issues, higher leverage and increased costs. Quote (page 15): "In October 2024, Wizz Air was downgraded by Fitch Ratings to 'BB+' with a ‘Stable Outlook’ due to the slower capacity growth caused by the Pratt & Whitney engine issues, leading to higher leverage, above the 2.0x threshold for a 'BBB-' rating; and increased costs impacting profitability."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 14,307 / 3,740 |
| 2 | snapshot, credit_metrics, operating_performance, peer_positioning | 2 errors | 16,993 / 2,578 |
| 3 | snapshot, operating_performance | 1 errors | 15,500 / 1,119 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 4] snapshot, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] snapshot, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the low-cost carrier operating an all-Airbus narrowbody fleet, saw its EBITDA margin narrow by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}} in FY2025, a year in which a manufacturer engine recall forced a large part of the fleet to be grounded at any time.
- Net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- The point to watch is leverage against the peer group: net leverage of {{net_leverage@FY2025}} compares with a peer median of {{net_leverage.peer_median@FY2025}}, and Fitch downgraded the company citing higher leverage and increased costs.

`credit_metrics`

- Revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, but EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} as CASK rose by {{cask.change@FY2025}} to {{cask@FY2025}}.
- Operating profit fell by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} as depreciation, amortisation and impairment rose by {{dda.change@FY2025}} to {{dda@FY2025}}.
- Total debt increased by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, taking gross leverage up by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- Interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as finance costs rose by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}.
- FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, so FFO to debt declined by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, while free cash flow rose by {{fcf.change@FY2025}} to {{fcf@FY2025}} as cash from operations increased by {{cfo.change@FY2025}} and capex fell by {{capex.change@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}} while capacity was broadly unchanged, with ASK broadly stable at {{ask@FY2025}} available seat kilometres.
- The load factor improved by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}, with RPK broadly stable at {{rpk@FY2025}}.
- RASK rose by {{rask.change@FY2025}} to {{rask@FY2025}}, but CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, so unit cost outpaced unit revenue.
- Fuel cost fell by {{fuel_cost.change@FY2025}} to {{fuel_cost@FY2025}}, and the fuel share of costs declined by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}}, as new A321neo aircraft were delivered and older A320ceo aircraft redelivered.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, and contract liabilities increased by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of the cash balance is customers' prepayments.
- Cash generation supported the balance sheet, with cash from operations of {{cfo@FY2025}} against capex of {{capex@FY2025}} and capex intensity down by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`peer_positioning`

- Wizz Air has the highest EBITDA margin of the low-cost peer group ({{ebitda_margin.peer_rank@FY2025}}), at {{ebitda_margin@FY2025}} against a median of {{ebitda_margin.peer_median@FY2025}}.
- Leverage is the weakest part of the comparison: net leverage of {{net_leverage@FY2025}} ranks {{net_leverage.peer_rank@FY2025}} against a peer median of {{net_leverage.peer_median@FY2025}}, and FFO to debt ranks {{ffo_to_debt.peer_rank@FY2025}} against a median of {{ffo_to_debt.peer_median@FY2025}}.
- Cash liquidity to revenue and capex intensity both sit in the middle of the group, with cash liquidity to revenue ranking {{cash_liquidity_to_revenue.peer_rank@FY2025}}.

`watch_items`

- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, well above the peer median of {{net_leverage.peer_median@FY2025}}, and Fitch downgraded the company citing higher leverage and increased costs.
- Cash flow: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, below the peer median of {{ffo_to_debt.peer_median@FY2025}}, as FFO declined by {{ffo.change@FY2025}}.
- Coverage: interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, below the peer median of {{interest_coverage.peer_median@FY2025}}, as finance costs rose by {{finance_costs.change@FY2025}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, above the peer median of {{advance_ticket_cover.peer_median@FY2025}}, a sensitivity if bookings slow.
