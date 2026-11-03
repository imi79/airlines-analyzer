# Norwegian Air Shuttle, FY2025: draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `446603cacef8` ([fact sheet](../factsheets/norwegian_FY2025.md)). Tokens: 11,393 in, 3,497 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, a low-cost carrier in the Nordic market, grew revenue by 6.6% to NOK 37.6bn in FY2025 while its EBITDA margin widened by 2.3 points to 21.2%.
The earnings gain did not translate into deleveraging: net leverage rose by 0.41x to 1.19x as net debt increased by 82.6% to NOK 9.5bn.
The main point to watch is liquidity: cash liquidity to revenue fell by 4.1 points to 26.7%, the weakest of the low-cost peer group (3rd of 3).

## Credit metrics

EBITDA increased by 19.2% to NOK 8.0bn and operating profit by 99.3% to NOK 3.7bn, on revenue up 6.6% to NOK 37.6bn.
Total debt rose by 21.6% to NOK 19.6bn, so gross leverage was broadly unchanged at 2.46x while net leverage climbed by 0.41x to 1.19x.
Interest coverage improved by 0.38x to 6.27x, and FFO rose by 21.1% to NOK 6.9bn, leaving FFO to debt stable at 35.4%.
Free cash flow fell by 49.9% to NOK 2.9bn as capex intensity rose by 9.7 points to 13.2%, taking FCF to debt down by 20.8 points to 14.6%.

## Operating performance

Passengers rose by 3.4% to 27.3m, supporting revenue growth of 6.6% to NOK 37.6bn.
The fuel share of costs was broadly unchanged at 28.2%, in line with the peer median of 28.2%.
The EBITDA margin widened by 2.3 points to 21.2%, so the revenue gain carried through to earnings.

## Liquidity and funding

Cash and cash-like investments fell by 7.5% to NOK 10.1bn, and cash liquidity to revenue declined by 4.1 points to 26.7%.
Customer prepayments rose: contract liabilities increased by 6.1% to NOK 4.4bn, and advance ticket cover rose by 5.6 points to 43.7%.
Cash liquidity to revenue of 26.7% sits below the peer median of 34.3%, so the buffer against near-term maturities is thinner than at the peers.

## Peer positioning

Norwegian sits at the peer median on EBITDA margin (21.2% against 21.2%), ranking 2nd of 3.
Leverage is in line with the group, with net leverage of 1.19x against a median of 1.19x and gross leverage of 2.46x against 2.46x.
Cash generation is in line with peers, with FFO to debt of 35.4% and FCF to debt of 14.6% both at the median, while capex intensity of 13.2% is above the peer median of 9.9%.
Liquidity is the weak spot: cash liquidity to revenue of 26.7% is below the peer median of 34.3% and ranks 3rd of 3, although advance ticket cover of 43.7% is the best in the group (1st of 3).

## Watch items

- Leverage: net leverage rose by 0.41x to 1.19x as net debt grew by 82.6% to NOK 9.5bn, so further debt-funded investment would leave less headroom.
- Cash flow: free cash flow fell by 49.9% to NOK 2.9bn as capex intensity rose by 9.7 points to 13.2%, above the peer median of 9.9%.
- Liquidity: cash liquidity to revenue fell by 4.1 points to 26.7%, below the peer median of 34.3% and the weakest of the group (3rd of 3).
- Customer prepayments: advance ticket cover rose by 5.6 points to 43.7%, with contract liabilities of NOK 4.4bn, so a larger share of the cash balance is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 11,393 / 3,497 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, a low-cost carrier in the Nordic market, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while its EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The earnings gain did not translate into deleveraging: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the low-cost peer group ({{cash_liquidity_to_revenue.peer_rank@2025}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, on revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, so gross leverage was broadly unchanged at {{gross_leverage@FY2025}} while net leverage climbed by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, leaving FFO to debt stable at {{ffo_to_debt@FY2025}}.
- Free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, taking FCF to debt down by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, supporting revenue growth of {{revenue.change@FY2025}} to {{revenue@FY2025}}.
- The fuel share of costs was broadly unchanged at {{fuel_share_of_costs@FY2025}}, in line with the peer median of {{fuel_share_of_costs.peer_median@2025}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, so the revenue gain carried through to earnings.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} sits below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}, so the buffer against near-term maturities is thinner than at the peers.

`peer_positioning`

- Norwegian sits at the peer median on EBITDA margin ({{ebitda_margin@FY2025}} against {{ebitda_margin.peer_median@2025}}), ranking {{ebitda_margin.peer_rank@2025}}.
- Leverage is in line with the group, with net leverage of {{net_leverage@FY2025}} against a median of {{net_leverage.peer_median@2025}} and gross leverage of {{gross_leverage@FY2025}} against {{gross_leverage.peer_median@2025}}.
- Cash generation is in line with peers, with FFO to debt of {{ffo_to_debt@FY2025}} and FCF to debt of {{fcf_to_debt@FY2025}} both at the median, while capex intensity of {{capex_intensity@FY2025}} is above the peer median of {{capex_intensity.peer_median@2025}}.
- Liquidity is the weak spot: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}} and ranks {{cash_liquidity_to_revenue.peer_rank@2025}}, although advance ticket cover of {{advance_ticket_cover@FY2025}} is the best in the group ({{advance_ticket_cover.peer_rank@2025}}).

`watch_items`

- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt grew by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, so further debt-funded investment would leave less headroom.
- Cash flow: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@2025}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}} and the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}).
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, with contract liabilities of {{contract_liabilities@FY2025}}, so a larger share of the cash balance is refundable if bookings slow.
