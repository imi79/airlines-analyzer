# easyJet, FY2025 (Oct 2024 to Sep 2025): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `8dc5bbbf7004` ([fact sheet](../factsheets/easyjet_FY2025.md)). Tokens: 45,898 in, 6,039 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 8.6% to GBP 10.1bn in FY2025 while holding its EBITDA margin broadly unchanged at 14.2%.
The balance sheet strengthened: net leverage fell by 0.29x to -0.42x, a net cash position, as total debt was reduced by 10.8%.
The point to watch is liquidity: cash liquidity to revenue fell by 2.3 points to 34.9%, and the EBITDA margin of 14.2% is the weakest of the low-cost peers (3rd of 3).

## Credit metrics

EBITDA rose by 5.9% to GBP 1.4bn on revenue up 8.6%, and operating profit increased by 18.2% to GBP 696m as depreciation fell by 3.5%.
Total debt was cut by 10.8% to GBP 2.9bn, taking gross leverage down by 0.38x to 2.03x and leaving net cash of GBP 602m against GBP 181m in FY2024.
Cash generation improved: FFO rose by 3.0% to GBP 1.3bn, lifting FFO to debt by 5.9 points to 44.0%, and free cash flow rose by 16.4% to GBP 624m despite capex up 7.8% to GBP 1.0bn.
Interest coverage eased by 1.08x to 9.22x as finance costs rose by 18.2% to GBP 156m, with airline net financing charges up on lower interest income on cash and higher charges on borrowings.

> Event `event:costs`: Airline net financing charges rose due to lower interest income on cash and higher interest charges on borrowings. Quote (page 33): "Airline net financing charges increased due to reduced interest income from lower market interest rates on our cash and an increase in interest charges relating to borrowings."

## Operating performance

Capacity grew by 9.4% to 134.5bn available seat kilometres and traffic by 9.3% to 122.0bn revenue passenger kilometres, with passengers up 4.1% to 93.4m.
The load factor rose by 0.5 points to 89.8%, but passenger yield fell by 2.8% to 4.98 pence, leaving RASK broadly unchanged at 7.52 pence.
CASK fell by 1.4% to 7.00 pence while CASK ex-fuel was stable at 5.32 pence, and fuel cost was broadly unchanged at GBP 2.3bn, taking the fuel share of costs down by 1.6 points to 23.9%.
The fleet rose by 2.6% to 356 aircraft, with an average age of 10.9 years after the purchase of aircraft previously held on lease.

> Event `event:fleet_and_engines`: easyJet bought aircraft it had previously leased, exiting the leases early and recording a credit to the income statement. Quote (page 167): "Right of use asset disposals in note 18 includes £73 million (2024: £nil) relating to the purchase of eight aircraft that were previously leased, with a corresponding £237 million (2024: £nil) of additions to aircraft owned assets. The early exit of the leases and subsequent purchase of the aircraft resulted in a £54 million (2024: £nil) credit to the income statement."

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at GBP 3.5bn, and total liquidity stood at GBP 4.8bn, including GBP 1.3bn of undrawn committed facilities.
Liquidity to revenue was 47.4%, while cash liquidity to revenue fell by 2.3 points to 34.9%.
Customer prepayments rose: advance ticket cover increased by 4.9 points to 55.1%, with contract liabilities up 12.0% to GBP 1.9bn.
Funding was reshaped during the year: a new revolving credit facility replaced the previous UK Export Finance facility and smaller facility, a Eurobond was repaid at maturity, and the EMTN programme was refreshed.

> Event `event:funding_and_rating`: easyJet entered into a new revolving credit facility that replaced its previous UK Export Finance facility and smaller revolving credit facility, both terminated, lowering annual interest charges. Quote (page 111): "The Committee also reviewed easyJet’s undrawn facility arrangements and approved management’s recommendation to enter into a new Revolving Credit Facility for $1.7 billion. This new facility replaced the previous $1.75 billion UKEF facility and the $400 million Revolving Credit Facility, both of which have now been terminated."

> Event `event:funding_and_rating-2`: easyJet repaid a Eurobond on its maturity date and secured a new undrawn revolving credit facility. Quote (page 33): "In the year, easyJet repaid a €500 million Eurobond, and secured a $1.7 billion revolving credit facility (RCF) which is undrawn at 30 September 2025 (this new RCF replaced an existing $400 million RCF and a $1,750 million"

> Event `event:funding_and_rating-4`: The Committee reviewed and recommended a refresh of the Company's Euro Medium Term Note programme to access a diverse range of funding alternatives. Quote (page 111): "During the year the Committee reviewed and recommended to the Board the refresh of the Company’s EMTN Programme, which had originally been established in January 2016. The refresh of the EMTN Programme allows easyJet to access a diverse range of funding alternatives."

## Peer positioning

easyJet has the lowest net leverage of the low-cost group (1st of 3), at -0.42x against a peer median of 1.19x, and also leads on gross leverage (1st of 3), interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3).
The weakest point is profitability: the EBITDA margin of 14.2% is the lowest of the group (3rd of 3) against a peer median of 21.2%.
Capex intensity sits in the middle of the group at 9.9%, advance ticket cover is in the middle of the group at 55.1%, and cash liquidity to revenue is the highest of the group (1st of 3).

## Watch items

- Profitability: the EBITDA margin of 14.2% is below the peer median of 21.2% and the weakest of the group (3rd of 3).
- Liquidity: cash liquidity to revenue fell by 2.3 points to 34.9%, a thinner buffer even though it remains the highest of the group (1st of 3).
- Coverage: interest coverage fell by 1.08x to 9.22x as finance costs rose by 18.2% to GBP 156m.
- Customer prepayments: advance ticket cover rose by 4.9 points to 55.1%, so a larger share of the cash balance is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 10 errors | 14,397 / 3,689 |
| 2 | snapshot, peer_positioning, watch_items | 3 errors | 16,415 / 1,661 |
| 3 | peer_positioning | passed | 15,086 / 689 |

### Errors found, by try

Try 1:

- [rule 3] snapshot, sentence 3: 'worse' claimed on ebitda_margin@FY2025, but it is neither better nor worse
- [rule 5] peer_positioning, sentence 1: gross_leverage.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 1: interest_coverage.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 1: ffo_to_debt.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 1: fcf_to_debt.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 3] peer_positioning, sentence 2: 'worse' claimed on ebitda_margin@FY2025, but it is neither better nor worse
- [rule 5] peer_positioning, sentence 3: capex_intensity.peer_median@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: advance_ticket_cover.peer_median@FY2025 is listed in the form but not used in the text
- [rule 3] watch_items, sentence 1: 'worse' claimed on ebitda_margin@FY2025, but it is neither better nor worse
- [rule 5] watch_items, sentence 2: cash_liquidity_to_revenue.peer_rank@FY2025 is listed in the form but not used in the text

Try 2:

- [rule 1] peer_positioning, sentence 1: word that states a number: 'first'
- [rule 5] peer_positioning, sentence 3: capex_intensity.peer_median@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: advance_ticket_cover.peer_median@FY2025 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while holding its EBITDA margin broadly unchanged at {{ebitda_margin@FY2025}}.
- The balance sheet strengthened: net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, a net cash position, as total debt was reduced by {{total_debt.change@FY2025}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, and the EBITDA margin of {{ebitda_margin@FY2025}} is the weakest of the low-cost peers ({{ebitda_margin.peer_rank@FY2025}}).

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}}, and operating profit increased by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} as depreciation fell by {{dda.change@FY2025}}.
- Total debt was cut by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} and leaving net cash of {{net_cash@FY2025}} against {{net_cash@FY2024}} in FY2024.
- Cash generation improved: FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, and free cash flow rose by {{fcf.change@FY2025}} to {{fcf@FY2025}} despite capex up {{capex.change@FY2025}} to {{capex@FY2025}}.
- Interest coverage eased by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as finance costs rose by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}, with airline net financing charges up on lower interest income on cash and higher charges on borrowings.

`operating_performance`

- Capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres and traffic by {{rpk.change@FY2025}} to {{rpk@FY2025}} revenue passenger kilometres, with passengers up {{passengers.change@FY2025}} to {{passengers@FY2025}}.
- The load factor rose by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}, but passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}, leaving RASK broadly unchanged at {{rask@FY2025}}.
- CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}} while CASK ex-fuel was stable at {{cask_ex_fuel@FY2025}}, and fuel cost was broadly unchanged at {{fuel_cost@FY2025}}, taking the fuel share of costs down by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet rose by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}} after the purchase of aircraft previously held on lease.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2025}}, and total liquidity stood at {{liquidity@FY2025}}, including {{undrawn_facilities@FY2025}} of undrawn committed facilities.
- Liquidity to revenue was {{liquidity_to_revenue@FY2025}}, while cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, with contract liabilities up {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}.
- Funding was reshaped during the year: a new revolving credit facility replaced the previous UK Export Finance facility and smaller facility, a Eurobond was repaid at maturity, and the EMTN programme was refreshed.

`peer_positioning`

- easyJet has the lowest net leverage of the low-cost group ({{net_leverage.peer_rank@FY2025}}), at {{net_leverage@FY2025}} against a peer median of {{net_leverage.peer_median@FY2025}}, and also leads on gross leverage ({{gross_leverage.peer_rank@FY2025}}), interest coverage ({{interest_coverage.peer_rank@FY2025}}), FFO to debt ({{ffo_to_debt.peer_rank@FY2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@FY2025}}).
- The weakest point is profitability: the EBITDA margin of {{ebitda_margin@FY2025}} is the lowest of the group ({{ebitda_margin.peer_rank@FY2025}}) against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- Capex intensity sits in the middle of the group at {{capex_intensity.peer_median@FY2025}}, advance ticket cover is in the middle of the group at {{advance_ticket_cover.peer_median@FY2025}}, and cash liquidity to revenue is the highest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).

`watch_items`

- Profitability: the EBITDA margin of {{ebitda_margin@FY2025}} is below the peer median of {{ebitda_margin.peer_median@FY2025}} and the weakest of the group ({{ebitda_margin.peer_rank@FY2025}}).
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, a thinner buffer even though it remains the highest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).
- Coverage: interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as finance costs rose by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, so a larger share of the cash balance is refundable if bookings slow.
