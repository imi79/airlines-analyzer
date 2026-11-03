# Air France-KLM, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `770ac499456b` ([fact sheet](../factsheets/afkl_FY2025.md)). Tokens: 23,578 in, 5,426 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Air France-KLM, a network airline in the European peer group, ended FY2025 with a stronger credit profile as revenue rose by 4.9% to EUR 33.0bn and EBITDA by 23.0% to EUR 5.1bn.
Net leverage fell by 0.17x to 1.71x and gross leverage by 0.49x to 3.07x, both in line with the peer median.
The main point to watch is liquidity: cash liquidity to revenue declined by 1.2 points to 20.8%, below the peer median of 25.0%.

## Credit metrics

EBITDA increased by 23.0% to EUR 5.1bn and operating profit by 36.6% to EUR 2.0bn, lifting the EBITDA margin by 2.2 points to 15.3%.
Total debt rose by 5.9% to EUR 15.5bn and net debt by 12.3% to EUR 8.7bn, yet gross leverage fell by 0.49x to 3.07x as EBITDA rose by 23.0%.
FFO rose by 24.1% to EUR 4.3bn, taking FFO to debt up by 4.0 points to 27.4%, in line with the peer median.
Free cash flow turned positive at EUR 606m, with FCF to debt up by 5.5 points to 3.9%, still below the peer median of 10.8%.
Interest coverage improved by 1.55x to 8.06x, in line with the peer median.

## Operating performance

Revenue grew by 4.9% to EUR 33.0bn, with operating profit up by 36.6% to EUR 2.0bn as the margin widened.
Capex intensity rose by 1.6 points to 13.5%, above the peer median of 10.4%, as the fleet investment programme absorbed more of revenue.
The fleet stood at 564 aircraft with an average age of 12.1 years at the last reported count, and carried 98.0m passengers.

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at EUR 6.9bn, a change of 1.1% on the prior year.
Cash liquidity to revenue fell by 1.2 points to 20.8%, below the peer median of 25.0%.
Customer prepayments rose: contract liabilities increased by 4.1% to EUR 4.3bn, and advance ticket cover rose by 3.1 points to 62.2%.

## Peer positioning

Air France-KLM sits at the peer median on EBITDA margin (15.3% against 15.3%, ranked 2nd of 3), net leverage (1.71x against 1.71x, ranked 2nd of 3) and FFO to debt (27.4% against 27.4%, ranked 2nd of 3).
Cash generation is the weak spot: FCF to debt of 3.9% is below the peer median of 10.8% and ranks 3rd of 3, the weakest of the group.
Cash liquidity to revenue of 20.8% is below the peer median of 25.0% and ranks 3rd of 3, the weakest of the group.
Advance ticket cover of 62.2% is below the peer median of 67.4% but ranks 1st of 3, the best of the group on this measure.

## Watch items

- Cash generation: FCF to debt of 3.9% remains below the peer median of 10.8% despite the improvement of 5.5 points over the year.
- Investment: capex intensity rose by 1.6 points to 13.5%, above the peer median of 10.4%, which keeps free cash flow thin relative to debt.
- Liquidity: cash liquidity to revenue declined by 1.2 points to 20.8%, the weakest of the group (3rd of 3), while cash and cash-like investments were stable at EUR 6.9bn.
- Customer prepayments: contract liabilities rose by 4.1% to EUR 4.3bn, so a larger share of liquidity is refundable ticket money.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 11,162 / 3,493 |
| 2 | snapshot, credit_metrics, watch_items | passed | 12,416 / 1,933 |

### Errors found, by try

Try 1:

- [rule 1] snapshot, sentence 1: word that states a number: 'three'
- [rule 4] credit_metrics, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 2] watch_items, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2025 is not in the fact sheet
- [rule 5] watch_items, sentence 3: cash_liquidity_to_revenue.peer_rank@2025 is in the text but not listed in the form
- [rule 5] watch_items, sentence 3: cash_liquidity_to_revenue.peer_rank@FY2025 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- Air France-KLM, a network airline in the European peer group, ended FY2025 with a stronger credit profile as revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}} and EBITDA by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}} and gross leverage by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}, both in line with the peer median.
- The main point to watch is liquidity: cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, lifting the EBITDA margin by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, yet gross leverage fell by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}} as EBITDA rose by {{ebitda.change@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, taking FFO to debt up by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, in line with the peer median.
- Free cash flow turned positive at {{fcf@FY2025}}, with FCF to debt up by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, still below the peer median of {{fcf_to_debt.peer_median@2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, in line with the peer median.

`operating_performance`

- Revenue grew by {{revenue.change@FY2025}} to {{revenue@FY2025}}, with operating profit up by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} as the margin widened.
- Capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@2025}}, as the fleet investment programme absorbed more of revenue.
- The fleet stood at {{fleet@FY2024}} aircraft with an average age of {{fleet_age@FY2024}} at the last reported count, and carried {{passengers@FY2024}} passengers.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2025}}, a change of {{cash_like.change@FY2025}} on the prior year.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}.

`peer_positioning`

- Air France-KLM sits at the peer median on EBITDA margin ({{ebitda_margin@FY2025}} against {{ebitda_margin.peer_median@2025}}, ranked {{ebitda_margin.peer_rank@2025}}), net leverage ({{net_leverage@FY2025}} against {{net_leverage.peer_median@2025}}, ranked {{net_leverage.peer_rank@2025}}) and FFO to debt ({{ffo_to_debt@FY2025}} against {{ffo_to_debt.peer_median@2025}}, ranked {{ffo_to_debt.peer_rank@2025}}).
- Cash generation is the weak spot: FCF to debt of {{fcf_to_debt@FY2025}} is below the peer median of {{fcf_to_debt.peer_median@2025}} and ranks {{fcf_to_debt.peer_rank@2025}}, the weakest of the group.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@2025}} and ranks {{cash_liquidity_to_revenue.peer_rank@2025}}, the weakest of the group.
- Advance ticket cover of {{advance_ticket_cover@FY2025}} is below the peer median of {{advance_ticket_cover.peer_median@2025}} but ranks {{advance_ticket_cover.peer_rank@2025}}, the best of the group on this measure.

`watch_items`

- Cash generation: FCF to debt of {{fcf_to_debt@FY2025}} remains below the peer median of {{fcf_to_debt.peer_median@2025}} despite the improvement of {{fcf_to_debt.change@FY2025}} over the year.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@2025}}, which keeps free cash flow thin relative to debt.
- Liquidity: cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}), while cash and cash-like investments were stable at {{cash_like@FY2025}}.
- Customer prepayments: contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of liquidity is refundable ticket money.
