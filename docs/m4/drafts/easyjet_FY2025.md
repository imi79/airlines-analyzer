# easyJet, FY2025 (Oct 2024 to Sep 2025): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `56f482cae4b2` ([fact sheet](../factsheets/easyjet_FY2025.md)). Tokens: 43,090 in, 5,322 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 8.6% to GBP 10.1bn in FY2025 while holding its EBITDA margin broadly unchanged at 14.2%.
The balance sheet strengthened: net leverage fell by 0.29x to -0.42x, a net cash position, and gross leverage came down to 2.03x.
The point to watch is the margin gap to peers, with EBITDA margin of 14.2% below the peer median of 21.2% and cash liquidity to revenue down by 2.3 points to 34.9%.

## Credit metrics

EBITDA rose by 5.9% to GBP 1.4bn on revenue up 8.6%, and operating profit increased by 18.2% to GBP 696m.
Total debt was reduced by 10.8% to GBP 2.9bn, taking gross leverage down by 0.38x to 2.03x and leaving net cash of GBP 602m.
Cash generation improved: FFO to debt rose by 5.9 points to 44.0% and FCF to debt by 5.0 points to 21.3%, with free cash flow of GBP 624m.
Interest coverage eased by 1.08x to 9.22x, still well above the peer median of 6.27x, as airline net financing charges increased.
Capex intensity was broadly unchanged at 9.9%, in line with the peer median.

> Event `event:costs`: Airline net financing charges rose due to lower interest income on cash and higher interest charges on borrowings. Quote (page 33): "Airline net financing charges increased due to reduced interest income from lower market interest rates on our cash and an increase in interest charges relating to borrowings."

## Operating performance

Passengers rose by 4.1% to 93.4m as capacity grew by 9.4% to 134.5bn available seat kilometres.
Traffic rose by 9.3% to 122.0bn revenue passenger kilometres, lifting the load factor by 0.5 points to 89.8%.
Passenger yield fell by 2.8% to 4.98 pence, leaving RASK broadly unchanged at 7.52 pence.
CASK declined by 1.4% to 7.00 pence, while CASK ex-fuel was broadly unchanged at 5.32 pence and the fuel share of costs fell by 1.6 points to 23.9%.
The fleet grew by 2.6% to 356 aircraft, with an average age of 10.9 years after the purchase of previously leased aircraft.

> Event `event:fleet_and_engines`: easyJet bought aircraft it had previously leased, exiting the leases early and recording a credit to the income statement. Quote (page 167): "Right of use asset disposals in note 18 includes £73 million (2024: £nil) relating to the purchase of eight aircraft that were previously leased, with a corresponding £237 million (2024: £nil) of additions to aircraft owned assets. The early exit of the leases and subsequent purchase of the aircraft resulted in a £54 million (2024: £nil) credit to the income statement."

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at GBP 3.5bn, and total liquidity stood at GBP 4.8bn, including GBP 1.3bn of undrawn committed facilities.
Cash liquidity to revenue fell by 2.3 points to 34.9%, while liquidity to revenue was 47.4%.
Customer prepayments rose: advance ticket cover increased by 4.9 points to 55.1%, with contract liabilities up 12.0% to GBP 1.9bn.
Funding was reshaped during the year: a new revolving credit facility replaced the previous UK Export Finance facility and smaller facility, and a Eurobond was repaid at maturity.

> Event `event:funding_and_rating`: easyJet entered into a new revolving credit facility that replaced its previous UK Export Finance facility and smaller revolving credit facility, both terminated, lowering annual interest charges. Quote (page 111): "The Committee also reviewed easyJet’s undrawn facility arrangements and approved management’s recommendation to enter into a new Revolving Credit Facility for $1.7 billion. This new facility replaced the previous $1.75 billion UKEF facility and the $400 million Revolving Credit Facility, both of which have now been terminated."

> Event `event:funding_and_rating-2`: easyJet repaid a Eurobond on its maturity date and secured a new undrawn revolving credit facility. Quote (page 33): "In the year, easyJet repaid a €500 million Eurobond, and secured a $1.7 billion revolving credit facility (RCF) which is undrawn at 30 September 2025 (this new RCF replaced an existing $400 million RCF and a $1,750 million"

## Peer positioning

easyJet has the lowest net leverage and gross leverage of the low-cost peer group (1st of 3 and 1st of 3), and leads on interest coverage, FFO to debt and FCF to debt (1st of 3, 1st of 3, 1st of 3).
The weakest point is profitability: EBITDA margin of 14.2% is the lowest of the group (3rd of 3) against a peer median of 21.2%.
Cash liquidity to revenue is the strongest of the group (1st of 3), while capex intensity and advance ticket cover sit in the middle of the group.

## Watch items

- Profitability: EBITDA margin of 14.2% is below the peer median of 21.2%, the weakest margin in the group (3rd of 3).
- Unit revenue: passenger yield fell by 2.8% to 4.98 pence, so RASK was broadly unchanged at 7.52 pence even as capacity rose by 9.4%.
- Liquidity: cash liquidity to revenue fell by 2.3 points to 34.9%, and advance ticket cover rose by 4.9 points to 55.1%, so more of the cash is customers' prepayments.
- Costs and fleet: interest coverage eased by 1.08x to 9.22x, and the average fleet age rose by 6.9% to 10.9 years.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 13,764 / 3,555 |
| 2 | peer_positioning, watch_items | passed | 14,972 / 1,242 |
| 3 | peer_positioning | passed | 14,354 / 525 |

### Errors found, by try

Try 1:

- [rule 5] peer_positioning, sentence 3: capex_intensity@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: advance_ticket_cover@FY2025 is listed in the form but not used in the text
- [rule 5] watch_items, sentence 1: ebitda_margin.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while holding its EBITDA margin broadly unchanged at {{ebitda_margin@FY2025}}.
- The balance sheet strengthened: net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, a net cash position, and gross leverage came down to {{gross_leverage@FY2025}}.
- The point to watch is the margin gap to peers, with EBITDA margin of {{ebitda_margin@FY2025}} below the peer median of {{ebitda_margin.peer_median@FY2025}} and cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}}, and operating profit increased by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} and leaving net cash of {{net_cash@FY2025}}.
- Cash generation improved: FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} and FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with free cash flow of {{fcf@FY2025}}.
- Interest coverage eased by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, still well above the peer median of {{interest_coverage.peer_median@FY2025}}, as airline net financing charges increased.
- Capex intensity was broadly unchanged at {{capex_intensity@FY2025}}, in line with the peer median.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}} as capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres.
- Traffic rose by {{rpk.change@FY2025}} to {{rpk@FY2025}} revenue passenger kilometres, lifting the load factor by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}.
- Passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}, leaving RASK broadly unchanged at {{rask@FY2025}}.
- CASK declined by {{cask.change@FY2025}} to {{cask@FY2025}}, while CASK ex-fuel was broadly unchanged at {{cask_ex_fuel@FY2025}} and the fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}} after the purchase of previously leased aircraft.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2025}}, and total liquidity stood at {{liquidity@FY2025}}, including {{undrawn_facilities@FY2025}} of undrawn committed facilities.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, while liquidity to revenue was {{liquidity_to_revenue@FY2025}}.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, with contract liabilities up {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}.
- Funding was reshaped during the year: a new revolving credit facility replaced the previous UK Export Finance facility and smaller facility, and a Eurobond was repaid at maturity.

`peer_positioning`

- easyJet has the lowest net leverage and gross leverage of the low-cost peer group ({{net_leverage.peer_rank@FY2025}} and {{gross_leverage.peer_rank@FY2025}}), and leads on interest coverage, FFO to debt and FCF to debt ({{interest_coverage.peer_rank@FY2025}}, {{ffo_to_debt.peer_rank@FY2025}}, {{fcf_to_debt.peer_rank@FY2025}}).
- The weakest point is profitability: EBITDA margin of {{ebitda_margin@FY2025}} is the lowest of the group ({{ebitda_margin.peer_rank@FY2025}}) against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while capex intensity and advance ticket cover sit in the middle of the group.

`watch_items`

- Profitability: EBITDA margin of {{ebitda_margin@FY2025}} is below the peer median of {{ebitda_margin.peer_median@FY2025}}, the weakest margin in the group ({{ebitda_margin.peer_rank@FY2025}}).
- Unit revenue: passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}, so RASK was broadly unchanged at {{rask@FY2025}} even as capacity rose by {{ask.change@FY2025}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, so more of the cash is customers' prepayments.
- Costs and fleet: interest coverage eased by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and the average fleet age rose by {{fleet_age.change@FY2025}} to {{fleet_age@FY2025}}.
