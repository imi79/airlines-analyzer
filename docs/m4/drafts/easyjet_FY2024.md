# easyJet, FY2024 (Oct 2023 to Sep 2024): draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v6`, fact sheet `d39d1e9939d2` ([fact sheet](../factsheets/easyjet_FY2024.md)). Tokens: 28,824 in, 5,338 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, the UK low-cost carrier, grew revenue by 13.9% to GBP 9.3bn in FY2024, with EBITDA up 20.7% to GBP 1.4bn.
The EBITDA margin widened by 0.8 points to 14.6%, and the group held net cash of GBP 181m, so net leverage stayed at -0.13x in net cash terms.
The point to watch is cash generation: free cash flow fell by 32.7% to GBP 536m as capex intensity rose to 10.0%.

## Credit metrics

EBITDA rose by 20.7% to GBP 1.4bn and operating profit by 30.0% to GBP 589m, on revenue up 13.9%.
Total debt increased by 13.7% to GBP 3.3bn, yet gross leverage fell by 0.15x to 2.41x as EBITDA rose by 20.7%.
Interest coverage improved by 4.04x to 10.30x, and FFO to debt rose by 5.1 points to 38.1% on FFO up 31.3% to GBP 1.3bn.
Free cash flow declined by 32.7% to GBP 536m, taking FCF to debt down by 11.3 points to 16.3% as capex intensity rose by 0.8 points to 10.0%.

## Operating performance

Passengers rose by 8.3% to 89.7m on capacity up 8.4% to 122.9bn available seat kilometres, with revenue passenger kilometres up 8.4% to 111.6bn.
The load factor was stable at 89.3% and passenger yield broadly unchanged at 5.12 pence, while RASK rose by 5.1% to 7.58 pence.
CASK increased by 4.2% to 7.10 pence and CASK ex-fuel by 5.4% to 5.29 pence, so unit cost rose faster than unit revenue.
The fuel share of costs eased by 0.8 points to 25.5%, and the fleet grew by 3.3% to 347 aircraft with an average age of 10.2 years.

## Liquidity and funding

Cash and cash-like investments rose by 18.3% to GBP 3.5bn, and cash liquidity to revenue increased by 1.4 points to 37.2%.
Cash liquidity of GBP 3.5bn leaves net cash of GBP 181m, an increase of 341.5% over the year.
Advance ticket cover eased by 1.0 point to 50.2%, with contract liabilities up 16.0% to GBP 1.7bn.
Funding was extended with a euro-denominated guaranteed bond under the EMTN programme maturing in 2031, and the audit committee noted an upgrade of the credit rating.

> Event `event:funding_and_rating`: easyJet issued a euro-denominated guaranteed bond under its EMTN programme, maturing in 2031. Quote (page 148): "March 2024: Eurobonds consisting of €850 million guaranteed Notes paying 3.750% coupon and maturing in 2031."

> Event `event:funding_and_rating-2`: The audit committee reviewed easyJet's credit rating position and noted an upgrade of rating. Quote (page 119): "The Committee reviewed easyJet’s credit rating position and noted the upgrade of rating from"

## Peer positioning

easyJet has the lowest net leverage of the low-cost peer group (1st of 3), and leads on interest coverage (1st of 3) and FFO to debt (1st of 3).
The EBITDA margin of 14.6% is the weakest of the group (3rd of 3), below the peer median of 18.9%.
Gross leverage, FCF to debt and advance ticket cover all sit in the middle of the group, while cash liquidity to revenue is the strongest (1st of 3).

## Watch items

- Cash generation: free cash flow fell by 32.7% to GBP 536m and FCF to debt by 11.3 points to 16.3%, in line with the peer median.
- Unit cost: CASK rose by 4.2% to 7.10 pence and CASK ex-fuel by 5.4%, with significant investment in spares to limit aircraft grounding.
- Investment: capex intensity rose by 0.8 points to 10.0%, above the peer median of 5.4%, as NEO aircraft joined the fleet.
- Profitability: the EBITDA margin of 14.6% is below the peer median of 18.9%, the weakest of the group (3rd of 3).

> Event `event:costs`: easyJet invested significantly in spares because supply-chain delays made just-in-time spares unviable. Quote (page 21): "Significant investment in spares made during the year, continuing a trend started in 2023. Global supply-chain issues with spares means that it is no longer viable to run a just-in-time spares process due to delivery delays, and so we have made this investment to minimise the period of time when aircraft are grounded"

> Event `event:fleet_and_engines`: NEO aircraft joined the fleet during the year, with a large number still on order. Quote (page 41): "16 NEO aircraft joined the fleet, with a further 299 on order."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 13,478 / 3,394 |
| 2 | credit_metrics, liquidity_funding, watch_items | passed | 15,346 / 1,944 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 2: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, the UK low-cost carrier, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, with EBITDA up {{ebitda.change@FY2024}} to {{ebitda@FY2024}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, and the group held net cash of {{net_cash@FY2024}}, so net leverage stayed at {{net_leverage@FY2024}} in net cash terms.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose to {{capex_intensity@FY2024}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} and operating profit by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}, on revenue up {{revenue.change@FY2024}}.
- Total debt increased by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, yet gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} as EBITDA rose by {{ebitda.change@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, and FFO to debt rose by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} on FFO up {{ffo.change@FY2024}} to {{ffo@FY2024}}.
- Free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}}, taking FCF to debt down by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}} on capacity up {{ask.change@FY2024}} to {{ask@FY2024}} available seat kilometres, with revenue passenger kilometres up {{rpk.change@FY2024}} to {{rpk@FY2024}}.
- The load factor was stable at {{load_factor@FY2024}} and passenger yield broadly unchanged at {{passenger_yield@FY2024}}, while RASK rose by {{rask.change@FY2024}} to {{rask@FY2024}}.
- CASK increased by {{cask.change@FY2024}} to {{cask@FY2024}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, so unit cost rose faster than unit revenue.
- The fuel share of costs eased by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}, and the fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft with an average age of {{fleet_age@FY2024}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Cash liquidity of {{cash_liquidity@FY2024}} leaves net cash of {{net_cash@FY2024}}, an increase of {{net_cash.change@FY2024}} over the year.
- Advance ticket cover eased by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, with contract liabilities up {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}.
- Funding was extended with a euro-denominated guaranteed bond under the EMTN programme maturing in 2031, and the audit committee noted an upgrade of the credit rating.

`peer_positioning`

- easyJet has the lowest net leverage of the low-cost peer group ({{net_leverage.peer_rank@FY2024}}), and leads on interest coverage ({{interest_coverage.peer_rank@FY2024}}) and FFO to debt ({{ffo_to_debt.peer_rank@FY2024}}).
- The EBITDA margin of {{ebitda_margin@FY2024}} is the weakest of the group ({{ebitda_margin.peer_rank@FY2024}}), below the peer median of {{ebitda_margin.peer_median@FY2024}}.
- Gross leverage, FCF to debt and advance ticket cover all sit in the middle of the group, while cash liquidity to revenue is the strongest ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} and FCF to debt by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, in line with the peer median.
- Unit cost: CASK rose by {{cask.change@FY2024}} to {{cask@FY2024}} and CASK ex-fuel by {{cask_ex_fuel.change@FY2024}}, with significant investment in spares to limit aircraft grounding.
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the peer median of {{capex_intensity.peer_median@FY2024}}, as NEO aircraft joined the fleet.
- Profitability: the EBITDA margin of {{ebitda_margin@FY2024}} is below the peer median of {{ebitda_margin.peer_median@FY2024}}, the weakest of the group ({{ebitda_margin.peer_rank@FY2024}}).
