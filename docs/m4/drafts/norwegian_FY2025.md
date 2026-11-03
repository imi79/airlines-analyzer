# Norwegian Air Shuttle, FY2025: draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `9896d975dcd1` ([fact sheet](../factsheets/norwegian_FY2025.md)). Tokens: 11,390 in, 3,396 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, a low-cost carrier in the Nordic market, grew revenue by 6.6% to NOK 37.6bn in FY2025 while its EBITDA margin widened by 2.3 points to 21.2%.
The earnings gain did not translate into deleveraging: net leverage rose by 0.41x to 1.19x as net debt increased by 82.6% to NOK 9.5bn.
The main point to watch is liquidity: cash liquidity to revenue fell by 4.1 points to 26.7%, the weakest of the low-cost peer group (3rd of 3).

## Credit metrics

EBITDA increased by 19.2% to NOK 8.0bn and operating profit by 99.3% to NOK 3.7bn, on revenue up 6.6% to NOK 37.6bn.
Total debt rose by 21.6% to NOK 19.6bn, so gross leverage was broadly unchanged at 2.46x while net leverage climbed to 1.19x.
Interest coverage improved to 6.27x, up 0.38x, and FFO rose by 21.1% to NOK 6.9bn, leaving FFO to debt stable at 35.4%.
Free cash flow fell by 49.9% to NOK 2.9bn as capex intensity rose by 9.7 points to 13.2%, taking FCF to debt down by 20.8 points to 14.6%.

## Operating performance

Passengers rose by 3.4% to 27.3m, supporting revenue of NOK 37.6bn, up 6.6%.
The EBITDA margin widened by 2.3 points to 21.2%, with EBITDA of NOK 8.0bn against NOK 6.7bn the year before.
Fuel made up 28.2% of costs, broadly unchanged on the prior year and in line with the peer median of 28.2%.

## Liquidity and funding

Cash and cash-like investments fell by 7.5% to NOK 10.1bn, and cash liquidity to revenue declined by 4.1 points to 26.7%.
Customer prepayments grew: contract liabilities rose by 6.1% to NOK 4.4bn, and advance ticket cover increased by 5.6 points to 43.7%.
Cash liquidity to revenue of 26.7% sits below the peer median of 34.3%, so the buffer against near-term maturities is thinner than at the peers.

## Peer positioning

Norwegian sits at the peer median on EBITDA margin (21.2% against 21.2%), ranking 2nd of 3.
Leverage is in line with the group: net leverage of 1.19x against a median of 1.19x (2nd of 3) and gross leverage of 2.46x against 2.46x.
Cash generation and coverage are also at the median, with FFO to debt of 35.4% (2nd of 3), FCF to debt of 14.6% and interest coverage of 6.27x.
The clear outlier is liquidity: cash liquidity to revenue of 26.7% is the weakest of the group (3rd of 3) against a median of 34.3%.

## Watch items

- Leverage: net leverage rose by 0.41x to 1.19x as net debt increased by 82.6%, so further debt-funded investment would leave less room at the current rating level.
- Cash flow: FCF to debt fell by 20.8 points to 14.6% as capex intensity rose by 9.7 points to 13.2%, above the peer median of 9.9%.
- Liquidity: cash liquidity to revenue fell by 4.1 points to 26.7%, the weakest of the group (3rd of 3), with no undrawn committed facilities disclosed for the year.
- Customer prepayments: advance ticket cover of 43.7% is below the peer median of 55.1%, so a larger share of the cash balance is customers' money rather than own liquidity.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 11,390 / 3,396 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, a low-cost carrier in the Nordic market, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while its EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The earnings gain did not translate into deleveraging: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the low-cost peer group ({{cash_liquidity_to_revenue.peer_rank@2025}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, on revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, so gross leverage was broadly unchanged at {{gross_leverage@FY2025}} while net leverage climbed to {{net_leverage@FY2025}}.
- Interest coverage improved to {{interest_coverage@FY2025}}, up {{interest_coverage.change@FY2025}}, and FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, leaving FFO to debt stable at {{ffo_to_debt@FY2025}}.
- Free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, taking FCF to debt down by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, supporting revenue of {{revenue@FY2025}}, up {{revenue.change@FY2025}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, with EBITDA of {{ebitda@FY2025}} against {{ebitda@FY2024}} the year before.
- Fuel made up {{fuel_share_of_costs@FY2025}} of costs, broadly unchanged on the prior year and in line with the peer median of {{fuel_share_of_costs.peer_median@2025}}.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments grew: contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} sits below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}, so the buffer against near-term maturities is thinner than at the peers.

`peer_positioning`

- Norwegian sits at the peer median on EBITDA margin ({{ebitda_margin@FY2025}} against {{ebitda_margin.peer_median@2025}}), ranking {{ebitda_margin.peer_rank@2025}}.
- Leverage is in line with the group: net leverage of {{net_leverage@FY2025}} against a median of {{net_leverage.peer_median@2025}} ({{net_leverage.peer_rank@2025}}) and gross leverage of {{gross_leverage@FY2025}} against {{gross_leverage.peer_median@2025}}.
- Cash generation and coverage are also at the median, with FFO to debt of {{ffo_to_debt@FY2025}} ({{ffo_to_debt.peer_rank@2025}}), FCF to debt of {{fcf_to_debt@FY2025}} and interest coverage of {{interest_coverage@FY2025}}.
- The clear outlier is liquidity: cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}) against a median of {{cash_liquidity_to_revenue.peer_median@2025}}.

`watch_items`

- Leverage: net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as net debt increased by {{net_debt.change@FY2025}}, so further debt-funded investment would leave less room at the current rating level.
- Cash flow: FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@2025}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), with no undrawn committed facilities disclosed for the year.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is below the peer median of {{advance_ticket_cover.peer_median@2025}}, so a larger share of the cash balance is customers' money rather than own liquidity.
