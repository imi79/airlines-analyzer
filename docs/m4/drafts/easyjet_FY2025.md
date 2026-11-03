# easyJet, FY2025 (Oct 2024 to Sep 2025): draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v3`, fact sheet `fbfece2e3c16` ([fact sheet](../factsheets/easyjet_FY2025.md)). Tokens: 35,661 in, 5,361 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

easyJet, a low-cost airline operating a European short-haul network, ended FY2025 with revenue up 8.6% to GBP 10.1bn and a net cash position, as net leverage fell by 0.29x to -0.42x.
The EBITDA margin was broadly unchanged at 14.2%, a change of 0.4 points versus the prior year, as RASK held flat at 7.52 pence while CASK declined by 1.4% to 7.00 pence.
The main point to watch is liquidity: cash liquidity to revenue fell by 2.3 points to 34.9%, even though it remains above the peer median of 34.3%.

## Credit metrics

EBITDA rose by 5.9% to GBP 1.4bn and operating profit by 18.2% to GBP 696m, so the margin held at 14.2%.
Total debt was reduced by 10.8% to GBP 2.9bn, taking gross leverage down by 0.38x to 2.03x and net debt to GBP -602m.
Cash generation strengthened: FFO rose by 3.0% to GBP 1.3bn and FFO to debt by 5.9 points to 44.0%, while free cash flow increased by 16.4% to GBP 624m.
Interest coverage weakened by 1.08x to 9.22x, and capex intensity was stable at 9.9%.

## Operating performance

Passengers rose by 4.1% to 93.4m on capacity up 9.4% to 134.5bn available seat kilometres.
RPK grew by 9.3% to 122.0bn, lifting the load factor by 1.5 points to 90.8%.
Passenger yield fell by 2.8% to 4.98 pence, leaving RASK broadly unchanged at 7.52 pence.
CASK declined by 1.4% to 7.00 pence, with CASK ex-fuel stable at 5.32 pence and the fuel share of costs down by 1.6 points to 23.9%.
The fleet grew by 2.6% to 356 aircraft, with an average age of 10.9 years.

## Liquidity and funding

Cash and cash-like investments were stable at GBP 3.5bn, and total liquidity stood at GBP 4.8bn, including GBP 1.3bn of undrawn committed facilities.
Liquidity to revenue was 47.4%, and cash liquidity to revenue fell by 2.3 points to 34.9%.
Customer prepayments rose: advance ticket cover increased by 4.9 points to 55.1%, with contract liabilities up 12.0% to GBP 1.9bn.

## Peer positioning

easyJet has the lowest net leverage in the low-cost peer group (1st of 3), at -0.42x against a median of 1.19x, and the lowest gross leverage (1st of 3) at 2.03x.
It leads the group on cash generation, with FFO to debt of 44.0% (1st of 3) and FCF to debt of 21.3% (1st of 3), and on interest coverage at 9.22x (1st of 3).
Profitability is the weak point: the EBITDA margin of 14.2% is below the peer median of 21.2% and ranks 3rd of 3.
Cash liquidity to revenue of 34.9% is the strongest of the group (1st of 3), while capex intensity of 9.9% is in line with the peer median of 9.9%.

## Watch items

- Profitability: the EBITDA margin of 14.2% is the weakest in the peer group (3rd of 3) and below the median of 21.2%, so the earnings buffer against a softer demand environment is thinner than at peers.
- Unit revenue: passenger yield fell by 2.8% to 4.98 pence while RASK was broadly unchanged at 7.52 pence, so revenue rose 8.6% on capacity growth of 9.4% rather than on pricing.
- Liquidity: cash liquidity to revenue fell by 2.3 points to 34.9%, and undrawn committed facilities of GBP 1.3bn are the buffer to monitor.
- Customer prepayments: advance ticket cover of 55.1% is in line with the peer median of 55.1%, and contract liabilities of GBP 1.9bn are a refund exposure if schedules change.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 12,122 / 3,533 |
| 2 | snapshot, watch_items | 1 errors | 12,074 / 1,167 |
| 3 | watch_items | passed | 11,465 / 661 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 2: 'eased' needs a 'down' claim on a figure in the same clause
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 2] watch_items, sentence 1: ebitda_margin.peer_rank@FY2025 is not in the fact sheet

### Text with blanks (as the AI wrote it)

`snapshot`

- easyJet, a low-cost airline operating a European short-haul network, ended FY2025 with revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}} and a net cash position, as net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- The EBITDA margin was broadly unchanged at {{ebitda_margin@FY2025}}, a change of {{ebitda_margin.change@FY2025}} versus the prior year, as RASK held flat at {{rask@FY2025}} while CASK declined by {{cask.change@FY2025}} to {{cask@FY2025}}.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, even though it remains above the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, so the margin held at {{ebitda_margin@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} and net debt to {{net_debt@FY2025}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}} and FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, while free cash flow increased by {{fcf.change@FY2025}} to {{fcf@FY2025}}.
- Interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and capex intensity was stable at {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}} on capacity up {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres.
- RPK grew by {{rpk.change@FY2025}} to {{rpk@FY2025}}, lifting the load factor by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}.
- Passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}, leaving RASK broadly unchanged at {{rask@FY2025}}.
- CASK declined by {{cask.change@FY2025}} to {{cask@FY2025}}, with CASK ex-fuel stable at {{cask_ex_fuel@FY2025}} and the fuel share of costs down by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}}.

`liquidity_funding`

- Cash and cash-like investments were stable at {{cash_like@FY2025}}, and total liquidity stood at {{liquidity@FY2025}}, including {{undrawn_facilities@FY2025}} of undrawn committed facilities.
- Liquidity to revenue was {{liquidity_to_revenue@FY2025}}, and cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, with contract liabilities up {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}.

`peer_positioning`

- easyJet has the lowest net leverage in the low-cost peer group ({{net_leverage.peer_rank@2025}}), at {{net_leverage@FY2025}} against a median of {{net_leverage.peer_median@2025}}, and the lowest gross leverage ({{gross_leverage.peer_rank@2025}}) at {{gross_leverage@FY2025}}.
- It leads the group on cash generation, with FFO to debt of {{ffo_to_debt@FY2025}} ({{ffo_to_debt.peer_rank@2025}}) and FCF to debt of {{fcf_to_debt@FY2025}} ({{fcf_to_debt.peer_rank@2025}}), and on interest coverage at {{interest_coverage@FY2025}} ({{interest_coverage.peer_rank@2025}}).
- Profitability is the weak point: the EBITDA margin of {{ebitda_margin@FY2025}} is below the peer median of {{ebitda_margin.peer_median@2025}} and ranks {{ebitda_margin.peer_rank@2025}}.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), while capex intensity of {{capex_intensity@FY2025}} is in line with the peer median of {{capex_intensity.peer_median@2025}}.

`watch_items`

- Profitability: the EBITDA margin of {{ebitda_margin@FY2025}} is the weakest in the peer group ({{ebitda_margin.peer_rank@2025}}) and below the median of {{ebitda_margin.peer_median@2025}}, so the earnings buffer against a softer demand environment is thinner than at peers.
- Unit revenue: passenger yield fell by {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}} while RASK was broadly unchanged at {{rask@FY2025}}, so revenue rose {{revenue.change@FY2025}} on capacity growth of {{ask.change@FY2025}} rather than on pricing.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, and undrawn committed facilities of {{undrawn_facilities@FY2025}} are the buffer to monitor.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is in line with the peer median of {{advance_ticket_cover.peer_median@2025}}, and contract liabilities of {{contract_liabilities@FY2025}} are a refund exposure if schedules change.
