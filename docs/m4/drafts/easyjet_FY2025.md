# easyJet, FY2025 (Oct 2024 to Sep 2025): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `a5a83a89e166` ([fact sheet](../factsheets/easyjet_FY2025.md)). Tokens: 42,780 in, 5,799 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 8.6% to GBP 10.1bn in FY2025 while holding investment grade ratings from Moody's and Standard & Poor's.
Net leverage fell by 0.29x to -0.42x, a net cash position, as total debt was reduced by 10.8%.
The point to watch is profitability against peers: the EBITDA margin was stable at 14.2%, below the peer median of 21.2% and the weakest of the group (3rd of 3).

> Event `event:funding_and_rating-3`: easyJet held investment grade corporate credit ratings from Moody's and Standard & Poor's, both with stable outlooks. Quote (page 33): "Building on this profit growth, easyJet continues to have one of the strongest investment grade balance sheets in European Aviation (Baa2/stable from Moody’s and BBB+/stable from Standard & Poor’s)."

## Credit metrics

EBITDA rose by 5.9% to GBP 1.4bn and operating profit by 18.2% to GBP 696m, so the EBITDA margin was broadly unchanged at 14.2%.
Total debt was reduced by 10.8% to GBP 2.9bn, taking gross leverage down by 0.38x to 2.03x and leaving net cash of GBP 602m.
Cash generation strengthened: FFO to debt rose by 5.9 points to 44.0% and FCF to debt by 5.0 points to 21.3%, with free cash flow of GBP 624m.
Interest coverage weakened by 1.08x to 9.22x, as airline net financing charges increased, though coverage remains well above the peer median of 6.27x.
Capex intensity was stable at 9.9%, in line with the peer median.

> Event `event:costs`: Airline net financing charges rose due to lower interest income on cash and higher interest charges on borrowings. Quote (page 33): "Airline net financing charges increased due to reduced interest income from lower market interest rates on our cash and an increase in interest charges relating to borrowings."

## Operating performance

Capacity grew by 9.4% to 134.5bn available seat kilometres and traffic by 9.3% to 122.0bn revenue passenger kilometres, lifting the load factor by 0.5 points to 89.8%.
Passengers rose by 4.1% to 93.4m, but passenger yield fell by 2.8% to 4.98 pence and RASK was broadly unchanged at 7.52 pence.
CASK fell by 1.4% to 7.00 pence, while CASK ex-fuel was stable at 5.32 pence, so the fuel share of costs declined by 1.6 points to 23.9%.
The fleet grew by 2.6% to 356 aircraft, with the average age rising by 6.9% to 10.9 years.

## Liquidity and funding

Cash and cash-like investments were stable at GBP 3.5bn, and total liquidity stood at GBP 4.8bn, including GBP 1.3bn of undrawn committed facilities.
Liquidity to revenue was 47.4%, while cash liquidity to revenue fell by 2.3 points to 34.9%.
Customer prepayments rose: advance ticket cover increased by 4.9 points to 55.1% and contract liabilities by 12.0% to GBP 1.9bn.
Funding was reshaped during the year: a new revolving credit facility replaced the previous UK Export Finance facility and smaller facility, and a Eurobond was repaid at maturity.

> Event `event:funding_and_rating`: easyJet entered into a new revolving credit facility that replaced its previous UK Export Finance facility and smaller revolving credit facility, both terminated, lowering annual interest charges. Quote (page 111): "The Committee also reviewed easyJet’s undrawn facility arrangements and approved management’s recommendation to enter into a new Revolving Credit Facility for $1.7 billion. This new facility replaced the previous $1.75 billion UKEF facility and the $400 million Revolving Credit Facility, both of which have now been terminated."

> Event `event:funding_and_rating-2`: easyJet repaid a Eurobond on its maturity date and secured a new undrawn revolving credit facility. Quote (page 33): "In the year, easyJet repaid a €500 million Eurobond, and secured a $1.7 billion revolving credit facility (RCF) which is undrawn at 30 September 2025 (this new RCF replaced an existing $400 million RCF and a $1,750 million"

## Peer positioning

easyJet has the lowest net leverage and gross leverage in the low-cost group (1st of 3 and 1st of 3), against a net leverage median of 1.19x and a gross leverage median of 2.46x.
It also leads the group on cash flow: FFO to debt and FCF to debt both rank 1st of 3 and 1st of 3, against medians of 35.4% and 14.6% respectively.
Profitability is the weak spot: the EBITDA margin ranks 3rd of 3 against a peer median of 21.2%, and the load factor ranks 2nd of 2 against a median of 90.3%.
Cash liquidity to revenue is the strongest of the group (1st of 3), while capex intensity and advance ticket cover sit in the middle of the group, at 9.9% and 55.1% respectively.

## Watch items

- Profitability: the EBITDA margin of 14.2% is below the peer median of 21.2% and the weakest in the group (3rd of 3), with passenger yield down 2.8% to 4.98 pence.
- Liquidity: cash liquidity to revenue declined by 2.3 points to 34.9%, and cash and cash-like investments were stable at GBP 3.5bn.
- Customer prepayments: advance ticket cover rose by 4.9 points to 55.1%, in the middle of the group at a median of 55.1%, so a larger share of liquidity is refundable if bookings slow.

> removed by the verifier (still broke a rule after two retries): "Coverage: interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as airline net financing charges increased, leaving less headroom than a year earlier." ('increased' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 13,519 / 3,713 |
| 2 | peer_positioning, watch_items | 1 errors | 15,085 / 1,420 |
| 3 | watch_items | 1 errors | 14,176 / 666 |

### Errors found, by try

Try 1:

- [rule 5] peer_positioning, sentence 2: fcf_to_debt.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 2: interest_coverage.peer_rank@FY2025 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 2: interest_coverage.peer_median@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 4: capex_intensity.peer_median@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 4: advance_ticket_cover.peer_median@FY2025 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 1: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause
- [rule 4] watch_items, sentence 2: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 5] watch_items, sentence 4: advance_ticket_cover.peer_median@FY2025 is listed in the form but not used in the text

Try 2:

- [rule 4] watch_items, sentence 2: 'rose' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 2: 'increased' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while holding investment grade ratings from Moody's and Standard & Poor's.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, a net cash position, as total debt was reduced by {{total_debt.change@FY2025}}.
- The point to watch is profitability against peers: the EBITDA margin was stable at {{ebitda_margin@FY2025}}, below the peer median of {{ebitda_margin.peer_median@FY2025}} and the weakest of the group ({{ebitda_margin.peer_rank@FY2025}}).

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, so the EBITDA margin was broadly unchanged at {{ebitda_margin@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} and leaving net cash of {{net_cash@FY2025}}.
- Cash generation strengthened: FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} and FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with free cash flow of {{fcf@FY2025}}.
- Interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, as airline net financing charges increased, though coverage remains well above the peer median of {{interest_coverage.peer_median@FY2025}}.
- Capex intensity was stable at {{capex_intensity@FY2025}}, in line with the peer median.

`operating_performance`

- Capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres and traffic by {{rpk.change@FY2025}} to {{rpk@FY2025}} revenue passenger kilometres, lifting the load factor by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}.
- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, but passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}} and RASK was broadly unchanged at {{rask@FY2025}}.
- CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}}, while CASK ex-fuel was stable at {{cask_ex_fuel@FY2025}}, so the fuel share of costs declined by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with the average age rising by {{fleet_age.change@FY2025}} to {{fleet_age@FY2025}}.

`liquidity_funding`

- Cash and cash-like investments were stable at {{cash_like@FY2025}}, and total liquidity stood at {{liquidity@FY2025}}, including {{undrawn_facilities@FY2025}} of undrawn committed facilities.
- Liquidity to revenue was {{liquidity_to_revenue@FY2025}}, while cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}} and contract liabilities by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}.
- Funding was reshaped during the year: a new revolving credit facility replaced the previous UK Export Finance facility and smaller facility, and a Eurobond was repaid at maturity.

`peer_positioning`

- easyJet has the lowest net leverage and gross leverage in the low-cost group ({{net_leverage.peer_rank@FY2025}} and {{gross_leverage.peer_rank@FY2025}}), against a net leverage median of {{net_leverage.peer_median@FY2025}} and a gross leverage median of {{gross_leverage.peer_median@FY2025}}.
- It also leads the group on cash flow: FFO to debt and FCF to debt both rank {{ffo_to_debt.peer_rank@FY2025}} and {{fcf_to_debt.peer_rank@FY2025}}, against medians of {{ffo_to_debt.peer_median@FY2025}} and {{fcf_to_debt.peer_median@FY2025}} respectively.
- Profitability is the weak spot: the EBITDA margin ranks {{ebitda_margin.peer_rank@FY2025}} against a peer median of {{ebitda_margin.peer_median@FY2025}}, and the load factor ranks {{load_factor.peer_rank@FY2025}} against a median of {{load_factor.peer_median@FY2025}}.
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while capex intensity and advance ticket cover sit in the middle of the group, at {{capex_intensity.peer_median@FY2025}} and {{advance_ticket_cover.peer_median@FY2025}} respectively.

`watch_items`

- Profitability: the EBITDA margin of {{ebitda_margin@FY2025}} is below the peer median of {{ebitda_margin.peer_median@FY2025}} and the weakest in the group ({{ebitda_margin.peer_rank@FY2025}}), with passenger yield down {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}.
- Liquidity: cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, and cash and cash-like investments were stable at {{cash_like@FY2025}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, in the middle of the group at a median of {{advance_ticket_cover.peer_median@FY2025}}, so a larger share of liquidity is refundable if bookings slow.
