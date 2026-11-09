# Wizz Air Holdings, FY2025 (Apr 2024 to Mar 2025): draft commentary

Status: **needs manual editing** (some sections still rejected after two retries). First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `8693f4452711` ([fact sheet](../factsheets/wizz_FY2025.md)). Tokens: 44,408 in, 6,266 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot (needs manual editing)

Wizz Air, the low-cost carrier operating an all-Airbus narrowbody fleet, closed FY2025 with revenue up 3.8% to EUR 5.3bn while a manufacturer engine recall kept a large part of the fleet grounded through the year.
The EBITDA margin narrowed by 2.0 points to 21.5%, and net leverage rose by 0.38x to 4.28x.
The point to watch is leverage: net leverage of 4.28x sits well above the peer median of 0.78x, and Fitch downgraded the company during the year, citing slower capacity growth from the engine issues.

> Event `event:fleet_and_engines`: A manufacturer recall affecting some of the company's aircraft engines, together with a shortage of spare engines and limited maintenance shop capacity, forced a large number of aircraft to be grounded at any time during the fiscal year. Quote (page 6): "A year ago this time, Wizz Air faced an unprecedented situation due to a manufacturer recall affecting some of our aircraft engines. This shortage of spare engines and limited maintenance shop capacity forced between forty and fifty-five aircraft to be grounded at any time during this F25 fiscal year."

> Event `event:funding_and_rating`: Fitch Ratings downgraded the company with a stable outlook, citing slower capacity growth from the engine issues, higher leverage and increased costs. Quote (page 15): "In October 2024, Wizz Air was downgraded by Fitch Ratings to 'BB+' with a ‘Stable Outlook’ due to the slower capacity growth caused by the Pratt & Whitney engine issues, leading to higher leverage, above the 2.0x threshold for a 'BBB-' rating; and increased costs impacting profitability."

> verifier: [rule 4] snapshot, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause

## Credit metrics

EBITDA fell by 4.9% to EUR 1.1bn on revenue of EUR 5.3bn, and operating profit declined by 61.7% to EUR 168m after depreciation.
Total debt rose by 5.5% to EUR 6.6bn and net debt by 4.2% to EUR 4.9bn, so gross leverage increased by 0.58x to 5.81x.
Interest coverage weakened by 1.93x to 5.08x, and FFO to debt fell by 2.9 points to 13.2% as FFO declined by 13.3% to EUR 872m.
Free cash flow rose by 139.9% to EUR 783m, lifting FCF to debt by 6.7 points to 11.9%, helped by capex intensity easing by 1.3 points to 5.4%.

## Operating performance

Passengers rose by 2.2% to 63.4m while capacity was broadly unchanged, with ASK stable at 121.7bn available seat kilometres.
The load factor improved by 0.9 points to 91.2%, and RASK rose by 3.9% to 4.33 euro cents.
Unit cost moved against the revenue line: CASK rose by 10.1% to 4.19 euro cents and CASK ex-fuel by 18.9% to 2.71 euro cents, with the fuel share of costs down 4.8 points to 35.2%.
The fleet grew by 11.1% to 231 aircraft with an average age of 4.5 years, as new A321neo deliveries were partly offset by redeliveries and the delivery schedule with Airbus was smoothed.

> Event `event:fleet_and_engines-2`: The company renegotiated its delivery pipeline with Airbus so that the delivery schedule was smoothed and extended, while the total number of aircraft deliveries stayed the same. Quote (page 4): "During the year, we renegotiated our delivery pipeline with Airbus. Delays in aircraft deliveries this year risked creating unsustainable growth spikes in the coming years, which would have strained both the business and the industry. While the total number of aircraft deliveries remains unchanged, the delivery schedule has been smoothed and now extends into 2030."

## Liquidity and funding

Cash and cash-like investments rose by 9.3% to EUR 1.7bn, taking cash liquidity to revenue up by 1.7 points to 33.0%.
Customer prepayments grew: contract liabilities rose by 27.1% to EUR 1.0bn, and advance ticket cover increased by 8.2 points to 58.4%.

> removed by the verifier (still broke a rule after two retries): "The funding profile carries a downgrade: Fitch cut the company to a lower rating with a stable outlook during the year, citing slower capacity growth from the engine issues, leverage above the threshold for an investment-grade rating and higher costs." ('growth' needs a 'up' claim on a figure in the same clause; 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause; 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Peer positioning

Wizz Air has the highest EBITDA margin of the low-cost peer group (1st of 3), at 21.5% against a median of 18.9%.
Leverage is the weak spot: net leverage ranks 3rd of 3 and gross leverage 3rd of 3, with gross leverage above the peer median of 2.41x.
Cash generation also trails the group, with FFO to debt and FCF to debt both below the peer medians of 35.6% and 16.3%, while cash liquidity to revenue sits in the middle of the group (2nd of 3).

## Watch items

- Leverage: net leverage rose by 0.38x to 4.28x, above the peer median of 0.78x, and the rating was downgraded during the year.
- Unit cost: CASK ex-fuel rose by 18.9% to 2.71 euro cents, outpacing the RASK increase, so the margin narrowed by 2.0 points to 21.5%.
- Cash generation: FFO to debt fell by 2.9 points to 13.2%, below the peer median of 35.6%, leaving less internal cover for a debt stock of EUR 6.6bn.
- Customer prepayments: advance ticket cover of 58.4% is above the peer median of 50.2%, so a larger share of cash is refundable if bookings slow.

> Event `event:funding_and_rating`: Fitch Ratings downgraded the company with a stable outlook, citing slower capacity growth from the engine issues, higher leverage and increased costs. Quote (page 15): "In October 2024, Wizz Air was downgraded by Fitch Ratings to 'BB+' with a ‘Stable Outlook’ due to the slower capacity growth caused by the Pratt & Whitney engine issues, leading to higher leverage, above the 2.0x threshold for a 'BBB-' rating; and increased costs impacting profitability."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 13,678 / 3,469 |
| 2 | snapshot, operating_performance, liquidity_funding, peer_positioning | 4 errors | 16,078 / 1,946 |
| 3 | snapshot, liquidity_funding | 4 errors | 14,652 / 851 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 1: 'up' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2025 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: fcf_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 4] snapshot, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] snapshot, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 3: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air, the low-cost carrier operating an all-Airbus narrowbody fleet, closed FY2025 with revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}} while a manufacturer engine recall kept a large part of the fleet grounded through the year.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, and net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- The point to watch is leverage: net leverage of {{net_leverage@FY2025}} sits well above the peer median of {{net_leverage.peer_median@FY2025}}, and Fitch downgraded the company during the year, citing slower capacity growth from the engine issues.

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue of {{revenue@FY2025}}, and operating profit declined by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} after depreciation.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, so gross leverage increased by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- Interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} as FFO declined by {{ffo.change@FY2025}} to {{ffo@FY2025}}.
- Free cash flow rose by {{fcf.change@FY2025}} to {{fcf@FY2025}}, lifting FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, helped by capex intensity easing by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}} while capacity was broadly unchanged, with ASK stable at {{ask@FY2025}} available seat kilometres.
- The load factor improved by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}, and RASK rose by {{rask.change@FY2025}} to {{rask@FY2025}}.
- Unit cost moved against the revenue line: CASK rose by {{cask.change@FY2025}} to {{cask@FY2025}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, with the fuel share of costs down {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft with an average age of {{fleet_age@FY2025}}, as new A321neo deliveries were partly offset by redeliveries and the delivery schedule with Airbus was smoothed.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments grew: contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.

`peer_positioning`

- Wizz Air has the highest EBITDA margin of the low-cost peer group ({{ebitda_margin.peer_rank@FY2025}}), at {{ebitda_margin@FY2025}} against a median of {{ebitda_margin.peer_median@FY2025}}.
- Leverage is the weak spot: net leverage ranks {{net_leverage.peer_rank@FY2025}} and gross leverage {{gross_leverage.peer_rank@FY2025}}, with gross leverage above the peer median of {{gross_leverage.peer_median@FY2025}}.
- Cash generation also trails the group, with FFO to debt and FCF to debt both below the peer medians of {{ffo_to_debt.peer_median@FY2025}} and {{fcf_to_debt.peer_median@FY2025}}, while cash liquidity to revenue sits in the middle of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).

`watch_items`

- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, above the peer median of {{net_leverage.peer_median@FY2025}}, and the rating was downgraded during the year.
- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, outpacing the RASK increase, so the margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Cash generation: FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, below the peer median of {{ffo_to_debt.peer_median@FY2025}}, leaving less internal cover for a debt stock of {{total_debt@FY2025}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is above the peer median of {{advance_ticket_cover.peer_median@FY2025}}, so a larger share of cash is refundable if bookings slow.
