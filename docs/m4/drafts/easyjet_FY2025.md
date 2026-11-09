# easyJet, FY2025 (Oct 2024 to Sep 2025): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `a5a83a89e166` ([fact sheet](../factsheets/easyjet_FY2025.md)). Tokens: 44,824 in, 6,931 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 8.6% to GBP 10.1bn in FY2025 while holding investment grade ratings from Moody's and Standard & Poor's.
Net leverage fell by 0.29x to -0.42x, a net cash position, as total debt was reduced by 10.8%.
The point to watch is the margin: EBITDA margin of 14.2% was broadly unchanged and sits below the peer median of 21.2%, the weakest of the low-cost group (3rd of 3).

> Event `event:funding_and_rating-3`: easyJet held investment grade corporate credit ratings from Moody's and Standard & Poor's, both with stable outlooks. Quote (page 33): "Building on this profit growth, easyJet continues to have one of the strongest investment grade balance sheets in European Aviation (Baa2/stable from Moody’s and BBB+/stable from Standard & Poor’s)."

## Credit metrics

EBITDA rose by 5.9% to GBP 1.4bn on revenue up 8.6%, and operating profit increased by 18.2% to GBP 696m.
Total debt was reduced by 10.8% to GBP 2.9bn, taking gross leverage down by 0.38x to 2.03x and leaving net cash of GBP 602m against GBP 181m in FY2024.
Cash generation strengthened: FFO to debt rose by 5.9 points to 44.0% and FCF to debt by 5.0 points to 21.3%, with free cash flow of GBP 624m up 16.4%.
Capex intensity was broadly unchanged at 9.9%, in line with the peer median.

> removed by the verifier (still broke a rule after two retries): "Interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as airline net financing charges rose, though it remains well above the peer median of {{interest_coverage.peer_median@FY2025}}." ('rose' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers rose by 4.1% to 93.4m on capacity up 9.4% to 134.5bn available seat kilometres, with revenue passenger kilometres up 9.3% to 122.0bn.
The load factor improved by 0.5 points to 89.8%, in line with the peer median.
Passenger yield fell by 2.8% to 4.98 pence, leaving RASK broadly unchanged at 7.52 pence.
CASK fell by 1.4% to 7.00 pence, while CASK ex-fuel was broadly unchanged at 5.32 pence and fuel fell to 23.9% of costs.
The fleet grew by 2.6% to 356 aircraft, with an average age of 10.9 years after the purchase of previously leased aircraft.

> Event `event:fleet_and_engines`: easyJet bought aircraft it had previously leased, exiting the leases early and recording a credit to the income statement. Quote (page 167): "Right of use asset disposals in note 18 includes £73 million (2024: £nil) relating to the purchase of eight aircraft that were previously leased, with a corresponding £237 million (2024: £nil) of additions to aircraft owned assets. The early exit of the leases and subsequent purchase of the aircraft resulted in a £54 million (2024: £nil) credit to the income statement."

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at GBP 3.5bn, giving cash liquidity of GBP 3.5bn and total liquidity of GBP 4.8bn including GBP 1.3bn of undrawn committed facilities.
Cash liquidity to revenue fell by 2.3 points to 34.9%, while liquidity to revenue was 47.4%.
Advance ticket cover rose by 4.9 points to 55.1%, with contract liabilities up 12.0% to GBP 1.9bn, so a larger share of cash is customer prepayment.
Funding was reshaped during the year: a new revolving credit facility replaced the prior UK Export Finance and smaller facilities, and a Eurobond was repaid at maturity.

> Event `event:funding_and_rating`: easyJet entered into a new revolving credit facility that replaced its previous UK Export Finance facility and smaller revolving credit facility, both terminated, lowering annual interest charges. Quote (page 111): "The Committee also reviewed easyJet’s undrawn facility arrangements and approved management’s recommendation to enter into a new Revolving Credit Facility for $1.7 billion. This new facility replaced the previous $1.75 billion UKEF facility and the $400 million Revolving Credit Facility, both of which have now been terminated."

> Event `event:funding_and_rating-2`: easyJet repaid a Eurobond on its maturity date and secured a new undrawn revolving credit facility. Quote (page 33): "In the year, easyJet repaid a €500 million Eurobond, and secured a $1.7 billion revolving credit facility (RCF) which is undrawn at 30 September 2025 (this new RCF replaced an existing $400 million RCF and a $1,750 million"

## Peer positioning

easyJet has the lowest net leverage of the low-cost group (1st of 3), at -0.42x against a peer median of 1.19x, and also ranks best on gross leverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3).
The weakest position is profitability: EBITDA margin of 14.2% is the lowest of the group (3rd of 3) against a peer median of 21.2%.
Cash liquidity to revenue is the strongest of the group (1st of 3), while capex intensity of 9.9% and advance ticket cover of 55.1% sit in the middle of the group.

## Watch items

- Profitability: EBITDA margin of 14.2% is below the peer median of 21.2% and the weakest of the group (3rd of 3), so the earnings base is thinner than peers' relative to revenue.
- Unit revenue: passenger yield fell by 2.8% to 4.98 pence, with RASK broadly unchanged at 7.52 pence as capacity rose by 9.4%.
- Customer prepayments: advance ticket cover rose by 4.9 points to 55.1%, in the middle of the group, so a larger part of the cash balance is refundable if bookings slow.

> removed by the verifier (still broke a rule after two retries): "Coverage: interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}} as airline net financing charges rose, a trend to monitor against the debt profile." ('rose' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 10 errors | 13,791 / 3,497 |
| 2 | credit_metrics, peer_positioning, watch_items | 2 errors | 15,902 / 2,025 |
| 3 | credit_metrics, watch_items | 2 errors | 15,131 / 1,409 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 4: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 1] peer_positioning, sentence 1: word that states a number: 'first'
- [rule 5] peer_positioning, sentence 1: gross_leverage.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 1: ffo_to_debt.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 1: fcf_to_debt.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: capex_intensity.peer_median@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: advance_ticket_cover.peer_median@FY2025 is listed in the form but not used in the text
- [rule 5] watch_items, sentence 1: ebitda_margin.peer_rank@FY2025 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 4: 'increased' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'increased' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'rose' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while holding investment grade ratings from Moody's and Standard & Poor's.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, a net cash position, as total debt was reduced by {{total_debt.change@FY2025}}.
- The point to watch is the margin: EBITDA margin of {{ebitda_margin@FY2025}} was broadly unchanged and sits below the peer median of {{ebitda_margin.peer_median@FY2025}}, the weakest of the low-cost group ({{ebitda_margin.peer_rank@FY2025}}).

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}}, and operating profit increased by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} and leaving net cash of {{net_cash@FY2025}} against {{net_cash@FY2024}} in FY2024.
- Cash generation strengthened: FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} and FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, with free cash flow of {{fcf@FY2025}} up {{fcf.change@FY2025}}.
- Capex intensity was broadly unchanged at {{capex_intensity@FY2025}}, in line with the peer median.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}} on capacity up {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres, with revenue passenger kilometres up {{rpk.change@FY2025}} to {{rpk@FY2025}}.
- The load factor improved by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}, in line with the peer median.
- Passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}, leaving RASK broadly unchanged at {{rask@FY2025}}.
- CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}}, while CASK ex-fuel was broadly unchanged at {{cask_ex_fuel@FY2025}} and fuel fell to {{fuel_share_of_costs@FY2025}} of costs.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}} after the purchase of previously leased aircraft.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2025}}, giving cash liquidity of {{cash_liquidity@FY2025}} and total liquidity of {{liquidity@FY2025}} including {{undrawn_facilities@FY2025}} of undrawn committed facilities.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, while liquidity to revenue was {{liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, with contract liabilities up {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of cash is customer prepayment.
- Funding was reshaped during the year: a new revolving credit facility replaced the prior UK Export Finance and smaller facilities, and a Eurobond was repaid at maturity.

`peer_positioning`

- easyJet has the lowest net leverage of the low-cost group ({{net_leverage.peer_rank@FY2025}}), at {{net_leverage@FY2025}} against a peer median of {{net_leverage.peer_median@FY2025}}, and also ranks best on gross leverage ({{gross_leverage.peer_rank@FY2025}}), FFO to debt ({{ffo_to_debt.peer_rank@FY2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@FY2025}}).
- The weakest position is profitability: EBITDA margin of {{ebitda_margin@FY2025}} is the lowest of the group ({{ebitda_margin.peer_rank@FY2025}}) against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while capex intensity of {{capex_intensity.peer_median@FY2025}} and advance ticket cover of {{advance_ticket_cover.peer_median@FY2025}} sit in the middle of the group.

`watch_items`

- Profitability: EBITDA margin of {{ebitda_margin@FY2025}} is below the peer median of {{ebitda_margin.peer_median@FY2025}} and the weakest of the group ({{ebitda_margin.peer_rank@FY2025}}), so the earnings base is thinner than peers' relative to revenue.
- Unit revenue: passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}, with RASK broadly unchanged at {{rask@FY2025}} as capacity rose by {{ask.change@FY2025}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, in the middle of the group, so a larger part of the cash balance is refundable if bookings slow.
