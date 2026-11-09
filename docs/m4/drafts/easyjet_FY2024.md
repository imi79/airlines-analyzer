# easyJet, FY2024 (Oct 2023 to Sep 2024): draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v5`, fact sheet `d39d1e9939d2` ([fact sheet](../factsheets/easyjet_FY2024.md)). Tokens: 29,323 in, 6,473 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 13.9% to GBP 9.3bn in FY2024, with EBITDA up 20.7% and an EBITDA margin of 14.6%.
The balance sheet stayed in net cash, with net cash of GBP 181m and net leverage of -0.13x, broadly unchanged on the year at 0.09x.
The point to watch is cash generation: free cash flow fell by 32.7% to GBP 536m as capex intensity rose to 10.0%, and the EBITDA margin of 14.6% is the weakest of the low-cost peers (3rd of 3).

## Credit metrics

EBITDA increased by 20.7% to GBP 1.4bn, lifting the EBITDA margin by 0.8 points to 14.6%.
Total debt rose by 13.7% to GBP 3.3bn, but gross leverage fell by 0.15x to 2.41x as EBITDA rose by 20.7%.
Interest coverage improved by 4.04x to 10.30x, and FFO to debt rose by 5.1 points to 38.1% on FFO up 31.3% to GBP 1.3bn.
Free cash flow declined by 32.7% to GBP 536m, taking FCF to debt down by 11.3 points to 16.3% as capex intensity increased by 0.8 points to 10.0%.

## Operating performance

Passengers rose by 8.3% to 89.7m on capacity up 8.4% to 122.9bn available seat kilometres, with RPK up 8.4% to 111.6bn.
The load factor was stable at 89.3% and passenger yield broadly unchanged at 5.12 pence, so unit revenue rose by 5.1% to 7.58 pence without a pricing tailwind.
CASK rose by 4.2% to 7.10 pence and CASK ex-fuel by 5.4% to 5.29 pence, so the unit cost base moved against the airline.
The fuel share of costs eased by 0.8 points to 25.5%, while the fleet grew by 3.3% to 347 aircraft and the average age rose to 10.2 years.
The airline invested significantly in spares to limit the time aircraft are grounded, and NEO aircraft joined the fleet during the year.

> Event `event:costs`: easyJet invested significantly in spares because supply-chain delays made just-in-time spares unviable. Quote (page 21): "Significant investment in spares made during the year, continuing a trend started in 2023. Global supply-chain issues with spares means that it is no longer viable to run a just-in-time spares process due to delivery delays, and so we have made this investment to minimise the period of time when aircraft are grounded"

> Event `event:fleet_and_engines`: NEO aircraft joined the fleet during the year, with a large number still on order. Quote (page 41): "16 NEO aircraft joined the fleet, with a further 299 on order."

## Liquidity and funding

Cash and cash-like investments rose by 18.3% to GBP 3.5bn, taking cash liquidity to revenue up by 1.4 points to 37.2%.
Net cash rose by 341.5% to GBP 181m, so cash and cash-like investments now exceed total debt.
Customer prepayments remain a large part of the funding base: contract liabilities rose by 16.0% to GBP 1.7bn, while advance ticket cover eased by 1.0 point to 50.2%.
The group issued a euro-denominated guaranteed bond under its EMTN programme maturing in 2031, and the audit committee noted an upgrade of the credit rating.

> Event `event:funding_and_rating`: easyJet issued a euro-denominated guaranteed bond under its EMTN programme, maturing in 2031. Quote (page 148): "March 2024: Eurobonds consisting of €850 million guaranteed Notes paying 3.750% coupon and maturing in 2031."

> Event `event:funding_and_rating-2`: The audit committee reviewed easyJet's credit rating position and noted an upgrade of rating. Quote (page 119): "The Committee reviewed easyJet’s credit rating position and noted the upgrade of rating from"

## Peer positioning

easyJet has the lowest net leverage of the low-cost peers (1st of 3), against a peer median of 0.78x.
It leads the group on interest coverage (1st of 3) and FFO to debt (1st of 3), and its cash liquidity to revenue is the strongest of the peers (1st of 3).
Gross leverage, FCF to debt and advance ticket cover all sit in the middle of the group, with ranks of 2nd of 3, 2nd of 3 and 2nd of 3 respectively.
Profitability is the weak spot: the EBITDA margin is the lowest of the peers (3rd of 3) against a peer median of 18.9%, and capex intensity is above the peer median of 5.4%.

## Watch items

- Cash generation: free cash flow fell by 32.7% to GBP 536m and FCF to debt by 11.3 points to 16.3%, with capex intensity of 10.0% above the peer median of 5.4%.
- Unit costs: CASK rose by 4.2% to 7.10 pence and CASK ex-fuel by 5.4% to 5.29 pence, outpacing the RASK increase of 5.1%.
- Profitability: the EBITDA margin of 14.6% is below the peer median of 18.9% and the weakest of the group (3rd of 3).
- Customer prepayments: contract liabilities rose by 16.0% to GBP 1.7bn, so a slower booking cycle would reduce the cash held on behalf of passengers.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 13,206 / 3,851 |
| 2 | credit_metrics, operating_performance, liquidity_funding, peer_positioning | passed | 16,117 / 2,622 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 2: 'exceeding' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 2: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] peer_positioning, sentence 4: 'above_peers' claimed on ebitda_margin.peer_median@FY2024, but it is below
- [rule style] peer_positioning, sentence 4: capex_intensity@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, with EBITDA up {{ebitda.change@FY2024}} and an EBITDA margin of {{ebitda_margin@FY2024}}.
- The balance sheet stayed in net cash, with net cash of {{net_cash@FY2024}} and net leverage of {{net_leverage@FY2024}}, broadly unchanged on the year at {{net_leverage.change@FY2024}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose to {{capex_intensity@FY2024}}, and the EBITDA margin of {{ebitda_margin@FY2024}} is the weakest of the low-cost peers ({{ebitda_margin.peer_rank@FY2024}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, lifting the EBITDA margin by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, but gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} as EBITDA rose by {{ebitda.change@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, and FFO to debt rose by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} on FFO up {{ffo.change@FY2024}} to {{ffo@FY2024}}.
- Free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}}, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}} as capex intensity increased by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}} on capacity up {{ask.change@FY2024}} to {{ask@FY2024}} available seat kilometres, with RPK up {{rpk.change@FY2024}} to {{rpk@FY2024}}.
- The load factor was stable at {{load_factor@FY2024}} and passenger yield broadly unchanged at {{passenger_yield@FY2024}}, so unit revenue rose by {{rask.change@FY2024}} to {{rask@FY2024}} without a pricing tailwind.
- CASK rose by {{cask.change@FY2024}} to {{cask@FY2024}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, so the unit cost base moved against the airline.
- The fuel share of costs eased by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}, while the fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft and the average age rose to {{fleet_age@FY2024}}.
- The airline invested significantly in spares to limit the time aircraft are grounded, and NEO aircraft joined the fleet during the year.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Net cash rose by {{net_cash.change@FY2024}} to {{net_cash@FY2024}}, so cash and cash-like investments now exceed total debt.
- Customer prepayments remain a large part of the funding base: contract liabilities rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, while advance ticket cover eased by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}.
- The group issued a euro-denominated guaranteed bond under its EMTN programme maturing in 2031, and the audit committee noted an upgrade of the credit rating.

`peer_positioning`

- easyJet has the lowest net leverage of the low-cost peers ({{net_leverage.peer_rank@FY2024}}), against a peer median of {{net_leverage.peer_median@FY2024}}.
- It leads the group on interest coverage ({{interest_coverage.peer_rank@FY2024}}) and FFO to debt ({{ffo_to_debt.peer_rank@FY2024}}), and its cash liquidity to revenue is the strongest of the peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).
- Gross leverage, FCF to debt and advance ticket cover all sit in the middle of the group, with ranks of {{gross_leverage.peer_rank@FY2024}}, {{fcf_to_debt.peer_rank@FY2024}} and {{advance_ticket_cover.peer_rank@FY2024}} respectively.
- Profitability is the weak spot: the EBITDA margin is the lowest of the peers ({{ebitda_margin.peer_rank@FY2024}}) against a peer median of {{ebitda_margin.peer_median@FY2024}}, and capex intensity is above the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} and FCF to debt by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, with capex intensity of {{capex_intensity@FY2024}} above the peer median of {{capex_intensity.peer_median@FY2024}}.
- Unit costs: CASK rose by {{cask.change@FY2024}} to {{cask@FY2024}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, outpacing the RASK increase of {{rask.change@FY2024}}.
- Profitability: the EBITDA margin of {{ebitda_margin@FY2024}} is below the peer median of {{ebitda_margin.peer_median@FY2024}} and the weakest of the group ({{ebitda_margin.peer_rank@FY2024}}).
- Customer prepayments: contract liabilities rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, so a slower booking cycle would reduce the cash held on behalf of passengers.
