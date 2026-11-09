# Norwegian Air Shuttle, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `0bf7d0477264` ([fact sheet](../factsheets/norwegian_FY2025.md)). Tokens: 39,875 in, 4,550 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, a low-cost carrier operating a Boeing 737 fleet on Nordic and European leisure routes, grew revenue by 6.6% to NOK 37.6bn in FY2025 while paying an initial dividend to shareholders.
The EBITDA margin widened by 2.3 points to 21.2%, but net leverage rose by 0.41x to 1.19x as debt increased faster than earnings.
The point to watch is liquidity: cash liquidity to revenue fell by 4.1 points to 26.7%, the weakest of the low-cost peer group (3rd of 3).

> Event `event:capital_returns`: The company paid an initial dividend to its shareholders in August. Quote (page 6): "In 2025, the company paid its first-ever dividend, distributing NOK 0.90 per share to its nearly 75,000 shareholders in August."

## Credit metrics

EBITDA increased by 19.2% to NOK 8.0bn and operating profit by 99.3% to NOK 3.7bn, on revenue up 6.6%.
Total debt rose by 21.6% to NOK 19.6bn and net debt by 82.6% to NOK 9.5bn, so net leverage increased to 1.19x from 0.78x.
Gross leverage was stable at 2.46x, and interest coverage improved to 6.27x from 5.89x.
FFO rose by 21.1% to NOK 6.9bn, leaving FFO to debt broadly unchanged at 35.4%, but free cash flow fell by 49.9% to NOK 2.9bn as capex intensity climbed by 9.7 points to 13.2%.
FCF to debt fell by 20.8 points to 14.6%, a weaker cash buffer against debt than in FY2024.

## Operating performance

Passengers rose by 3.4% to 27.3m, supported by a summer programme with a large number of routes including new leisure destinations.
Fuel made up 28.2% of costs, broadly unchanged on the prior year, so the cost base remains exposed to jet fuel prices.

> Event `event:capacity_and_network`: The summer programme featured a large number of routes, including new routes to leisure destinations, and the winter season operated routes to many destinations. Quote (page 3): "Norwegian’s summer 2025 programme featured nearly 350 routes, including 17 new routes to attractive leisure destinations."

> removed by the verifier (still broke a rule after two retries): "The acquisition of previously leased Boeing 737-800 aircraft brought accounting gains and recurring cost savings, and the group exercised its option for additional 737 MAX 8 aircraft." (number written outside a blank: '0')

## Liquidity and funding

Cash and cash-like investments fell by 7.5% to NOK 10.1bn, and cash liquidity to revenue declined by 4.1 points to 26.7%.
Customer prepayments rose: contract liabilities increased by 6.1% to NOK 4.4bn, and advance ticket cover rose by 5.6 points to 43.7%.
The group redeemed its New Capital Perpetual Bonds in full during the year, removing that instrument from the capital structure.

> Event `event:funding_and_rating`: Norwegian announced it would redeem all outstanding New Capital Perpetual Bonds and launched an offer to repurchase part of them, after which the bonds were redeemed in full. Quote (page 20): "During the second quarter of 2025, Norwegian announced that it would exercise its call option to redeem all outstanding New Capital Perpetual Bonds bonds, totalling NOK 1,501 million, and that the company would launch an offer to repurchase up to 50 percent of these bonds. Following these transactions, the convertible bonds were redeemed in full."

## Peer positioning

Norwegian sits in the middle of the low-cost group on EBITDA margin (2nd of 3), net leverage (2nd of 3) and gross leverage (2nd of 3).
Cash generation is also mid-group, with FFO to debt ranking 2nd of 3 and FCF to debt 2nd of 3.
Cash liquidity to revenue is the weakest of the group (3rd of 3), while advance ticket cover is the strongest (1st of 3).

## Watch items

- Liquidity: cash liquidity to revenue of 26.7% is below the peer median of 34.3% and the weakest in the group (3rd of 3), leaving less headroom against near-term maturities.
- Leverage: net leverage rose by 0.41x to 1.19x as net debt increased by 82.6%, so further debt-funded investment would extend the trend.
- Investment: capex intensity of 13.2% is above the peer median of 9.9%, and free cash flow fell by 49.9% to NOK 2.9bn.
- Customer prepayments: advance ticket cover of 43.7% is below the peer median of 55.1%, so a slower booking cycle would reduce the float funding the cash position.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 12,761 / 3,024 |
| 2 | operating_performance, peer_positioning, watch_items | 1 errors | 14,256 / 1,238 |
| 3 | operating_performance | 1 errors | 12,858 / 288 |

### Errors found, by try

Try 1:

- [rule 1] operating_performance, sentence 1: number written outside a blank: '350'
- [rule 5] operating_performance, sentence 2: passengers.change@FY2025 is listed in the form but not used in the text
- [rule style] operating_performance, sentence 2: revenue.change@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 1] operating_performance, sentence 4: number written outside a blank: '0'
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause

Try 2:

- [rule 1] operating_performance, sentence 3: number written outside a blank: '0'

Try 3:

- [rule 1] operating_performance, sentence 3: number written outside a blank: '0'

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, a low-cost carrier operating a Boeing 737 fleet on Nordic and European leisure routes, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while paying an initial dividend to shareholders.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, but net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as debt increased faster than earnings.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the low-cost peer group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, on revenue up {{revenue.change@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, so net leverage increased to {{net_leverage@FY2025}} from {{net_leverage@FY2024}}.
- Gross leverage was stable at {{gross_leverage@FY2025}}, and interest coverage improved to {{interest_coverage@FY2025}} from {{interest_coverage@FY2024}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, leaving FFO to debt broadly unchanged at {{ffo_to_debt@FY2025}}, but free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity climbed by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, a weaker cash buffer against debt than in FY2024.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, supported by a summer programme with a large number of routes including new leisure destinations.
- Fuel made up {{fuel_share_of_costs@FY2025}} of costs, broadly unchanged on the prior year, so the cost base remains exposed to jet fuel prices.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.
- The group redeemed its New Capital Perpetual Bonds in full during the year, removing that instrument from the capital structure.

`peer_positioning`

- Norwegian sits in the middle of the low-cost group on EBITDA margin ({{ebitda_margin.peer_rank@FY2025}}), net leverage ({{net_leverage.peer_rank@FY2025}}) and gross leverage ({{gross_leverage.peer_rank@FY2025}}).
- Cash generation is also mid-group, with FFO to debt ranking {{ffo_to_debt.peer_rank@FY2025}} and FCF to debt {{fcf_to_debt.peer_rank@FY2025}}.
- Cash liquidity to revenue is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while advance ticket cover is the strongest ({{advance_ticket_cover.peer_rank@FY2025}}).

`watch_items`

- Liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}} and the weakest in the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), leaving less headroom against near-term maturities.
- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}}, so further debt-funded investment would extend the trend.
- Investment: capex intensity of {{capex_intensity@FY2025}} is above the peer median of {{capex_intensity.peer_median@FY2025}}, and free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is below the peer median of {{advance_ticket_cover.peer_median@FY2025}}, so a slower booking cycle would reduce the float funding the cash position.
