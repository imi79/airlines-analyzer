# Wizz Air Holdings, FY2025 (Apr 2024 to Mar 2025): draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `99b331c5e0fd` ([fact sheet](../factsheets/wizz_FY2025.md)). Tokens: 25,187 in, 6,028 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Wizz Air Holdings, a low-cost carrier with a fleet of 231 aircraft, grew revenue by 3.8% to EUR 5.3bn in FY2025, but EBITDA declined by 4.9% to EUR 1.1bn.
Net leverage rose by 0.38x to 4.28x as the EBITDA margin narrowed by 2.0 points to 21.5%.
The main point to watch is unit cost: CASK rose by 10.1% to 4.19 euro cents while capacity was broadly unchanged, with ASK moving by 0.1% to 121.7bn available seat kilometres.

## Credit metrics

EBITDA fell by 4.9% to EUR 1.1bn on revenue of EUR 5.3bn, which rose by 3.8%, so the EBITDA margin narrowed by 2.0 points to 21.5%.
Total debt increased by 5.5% to EUR 6.6bn and net debt by 4.2% to EUR 4.9bn, taking gross leverage up by 0.58x to 5.81x.
Interest coverage weakened by 1.93x to 5.08x, and FFO to debt fell by 2.9 points to 13.2% as FFO declined by 13.3% to EUR 872m.
Free cash flow improved by 139.9% to EUR 783m, lifting FCF to debt by 6.7 points to 11.9%, helped by capex intensity easing by 1.3 points to 5.4%.

## Operating performance

Passengers rose by 2.2% to 63.4m, while capacity was stable, with ASK of 121.7bn available seat kilometres and RPK of 111.1bn revenue passenger kilometres.
The load factor improved by 0.9 points to 91.2%, above the peer median of 90.3%.
Unit revenue rose by 3.9% to 4.33 euro cents, but unit cost rose faster, with CASK up by 10.1% to 4.19 euro cents and CASK ex-fuel up by 18.9% to 2.71 euro cents.
The fuel share of costs fell by 4.8 points to 35.2%, still above the peer median of 28.0%.
The fleet grew by 11.1% to 231 aircraft, with an average age of 4.5 years.

## Liquidity and funding

Cash and cash-like investments rose by 9.3% to EUR 1.7bn, and cash liquidity to revenue improved by 1.7 points to 33.0%, in line with the peer median of 33.0%.
Customer prepayments rose: contract liabilities increased by 27.1% to EUR 1.0bn, and advance ticket cover rose by 8.2 points to 58.4%, above the peer median of 50.2%.
Cash liquidity of EUR 1.7bn is the only committed buffer disclosed, so the funding mix rests on a debt stack of EUR 6.6bn against net debt of EUR 4.9bn.

## Peer positioning

Wizz Air has the highest EBITDA margin in the low-cost peer group (1st of 3), at 21.5% against a median of 18.9%.
Leverage is the weakest in the group: net leverage of 4.28x ranks 3rd of 3 against a peer median of 0.78x, and gross leverage of 5.81x ranks 3rd of 3 against 2.41x.
Cash generation also trails: FFO to debt of 13.2% ranks 3rd of 3 against a median of 35.6%, and FCF to debt of 11.9% ranks 3rd of 3 against 16.3%.
Interest coverage of 5.08x is below the peer median of 5.89x and ranks 3rd of 3, while cash liquidity to revenue ranks 2nd of 3.

## Watch items

- Unit cost: CASK ex-fuel rose by 18.9% to 2.71 euro cents while ASK was broadly unchanged at 121.7bn available seat kilometres, so the cost base is not being spread over more flying.
- Leverage: net leverage of 4.28x is above the peer median of 0.78x and ranks 3rd of 3, with total debt up by 5.5% to EUR 6.6bn.
- Cash generation: FFO to debt of 13.2% is below the peer median of 35.6%, and interest coverage fell by 1.93x to 5.08x.
- Customer prepayments: advance ticket cover of 58.4% is above the peer median of 50.2%, so a larger share of liquidity is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 12,001 / 4,046 |
| 2 | snapshot, credit_metrics, watch_items | passed | 13,186 / 1,982 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 1: 'narrowed' needs a 'down' claim on a figure in the same clause
- [rule 5] watch_items, sentence 1: ask@FY2025 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- Wizz Air Holdings, a low-cost carrier with a fleet of {{fleet@FY2025}} aircraft, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, but EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- Net leverage rose by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} as the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The main point to watch is unit cost: CASK rose by {{cask.change@FY2025}} to {{cask@FY2025}} while capacity was broadly unchanged, with ASK moving by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres.

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue of {{revenue@FY2025}}, which rose by {{revenue.change@FY2025}}, so the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Total debt increased by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, taking gross leverage up by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- Interest coverage weakened by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO to debt fell by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} as FFO declined by {{ffo.change@FY2025}} to {{ffo@FY2025}}.
- Free cash flow improved by {{fcf.change@FY2025}} to {{fcf@FY2025}}, lifting FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, helped by capex intensity easing by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, while capacity was stable, with ASK of {{ask@FY2025}} available seat kilometres and RPK of {{rpk@FY2025}} revenue passenger kilometres.
- The load factor improved by {{load_factor.change@FY2025}} to {{load_factor@FY2025}}, above the peer median of {{load_factor.peer_median@2024}}.
- Unit revenue rose by {{rask.change@FY2025}} to {{rask@FY2025}}, but unit cost rose faster, with CASK up by {{cask.change@FY2025}} to {{cask@FY2025}} and CASK ex-fuel up by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}, still above the peer median of {{fuel_share_of_costs.peer_median@2024}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft, with an average age of {{fleet_age@FY2025}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue improved by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, in line with the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, above the peer median of {{advance_ticket_cover.peer_median@2024}}.
- Cash liquidity of {{cash_liquidity@FY2025}} is the only committed buffer disclosed, so the funding mix rests on a debt stack of {{total_debt@FY2025}} against net debt of {{net_debt@FY2025}}.

`peer_positioning`

- Wizz Air has the highest EBITDA margin in the low-cost peer group ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2025}} against a median of {{ebitda_margin.peer_median@2024}}.
- Leverage is the weakest in the group: net leverage of {{net_leverage@FY2025}} ranks {{net_leverage.peer_rank@2024}} against a peer median of {{net_leverage.peer_median@2024}}, and gross leverage of {{gross_leverage@FY2025}} ranks {{gross_leverage.peer_rank@2024}} against {{gross_leverage.peer_median@2024}}.
- Cash generation also trails: FFO to debt of {{ffo_to_debt@FY2025}} ranks {{ffo_to_debt.peer_rank@2024}} against a median of {{ffo_to_debt.peer_median@2024}}, and FCF to debt of {{fcf_to_debt@FY2025}} ranks {{fcf_to_debt.peer_rank@2024}} against {{fcf_to_debt.peer_median@2024}}.
- Interest coverage of {{interest_coverage@FY2025}} is below the peer median of {{interest_coverage.peer_median@2024}} and ranks {{interest_coverage.peer_rank@2024}}, while cash liquidity to revenue ranks {{cash_liquidity_to_revenue.peer_rank@2024}}.

`watch_items`

- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}} while ASK was broadly unchanged at {{ask@FY2025}} available seat kilometres, so the cost base is not being spread over more flying.
- Leverage: net leverage of {{net_leverage@FY2025}} is above the peer median of {{net_leverage.peer_median@2024}} and ranks {{net_leverage.peer_rank@2024}}, with total debt up by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}.
- Cash generation: FFO to debt of {{ffo_to_debt@FY2025}} is below the peer median of {{ffo_to_debt.peer_median@2024}}, and interest coverage fell by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is above the peer median of {{advance_ticket_cover.peer_median@2024}}, so a larger share of liquidity is refundable if bookings slow.
