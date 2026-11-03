# Air France-KLM, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `ac0301c846c5` ([fact sheet](../factsheets/afkl_FY2024.md)). Tokens: 22,894 in, 4,691 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Air France-KLM, a network airline group, ended FY2024 with a weaker credit profile as net leverage rose by 0.59x to 1.88x on revenue up 4.8% to EUR 31.5bn.
The EBITDA margin narrowed by 0.8 points to 13.1%, and free cash flow turned negative at EUR -232m as net debt rose by 43.5% to EUR 7.7bn.
The main point to watch is liquidity: cash liquidity to revenue fell by 5.5 points to 22.0%, the weakest of the network peers (3rd of 3).

## Credit metrics

EBITDA was broadly unchanged at EUR 4.1bn, a change of 1.5%, while operating profit fell by 12.6% to EUR 1.5bn.
Total debt rose by 7.4% to EUR 14.6bn, taking gross leverage up by 0.29x to 3.56x.
Interest coverage weakened by 0.45x to 6.51x.
FFO rose by 2.1% to EUR 3.4bn, but FFO to debt fell by 1.2 points to 23.4% as total debt rose by 7.4%.
FCF to debt fell by 2.0 points to -1.6%, with capex intensity broadly unchanged at 11.9%.

## Operating performance

Passengers rose by 4.7% to 98.0m, and the fleet grew by 4.3% to 564 aircraft.
The average fleet age was broadly stable at 12.1 years, a change of 0.8%.
Revenue rose by 4.8% to EUR 31.5bn, while EBITDA was broadly unchanged at EUR 4.1bn, so the margin narrowed by 0.8 points to 13.1%.

## Liquidity and funding

Cash and cash-like investments fell by 16.0% to EUR 6.9bn, and cash liquidity to revenue declined by 5.5 points to 22.0%.
Customer prepayments rose: advance ticket cover increased by 12.4 points to 59.1%, with contract liabilities up by 6.2% to EUR 4.1bn.
Cash liquidity of EUR 6.9bn covers a smaller share of revenue than the peer median of 29.0%, leaving less headroom against the debt taken on during the year.

## Peer positioning

Air France-KLM has the weakest EBITDA margin of the network peers (3rd of 3), at 13.1% against a median of 14.6%.
Leverage is in line with the group: net leverage of 1.88x ranks 2nd of 3 against a median of 1.88x, and gross leverage of 3.56x also sits at the median.
Interest coverage of 6.51x is the weakest of the group (3rd of 3) against a median of 8.70x, and FCF to debt of -1.6% also ranks 3rd of 3.
Advance ticket cover of 59.1% is the lowest of the group (1st of 3) against a median of 74.5%, and capex intensity of 11.9% is above the peer median of 8.8%.

## Watch items

- Cash generation: free cash flow turned negative at EUR -232m and FCF to debt declined to -1.6%, the weakest of the network peers (3rd of 3).
- Leverage: net debt rose by 43.5% to EUR 7.7bn, lifting net leverage by 0.59x to 1.88x.
- Liquidity: cash and cash-like investments fell by 16.0% to EUR 6.9bn, and cash liquidity to revenue of 22.0% is below the peer median of 29.0%.
- Coverage: interest coverage fell by 0.45x to 6.51x, below the peer median of 8.70x, as total debt rose to EUR 14.6bn.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 11,315 / 3,366 |
| 2 | credit_metrics, watch_items | passed | 11,579 / 1,325 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 4: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 1: 'fell' needs a 'down' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Air France-KLM, a network airline group, ended FY2024 with a weaker credit profile as net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, and free cash flow turned negative at {{fcf@FY2024}} as net debt rose by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the network peers ({{cash_liquidity_to_revenue.peer_rank@2024}}).

`credit_metrics`

- EBITDA was broadly unchanged at {{ebitda@FY2024}}, a change of {{ebitda.change@FY2024}}, while operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, taking gross leverage up by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- Interest coverage weakened by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but FFO to debt fell by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} as total debt rose by {{total_debt.change@FY2024}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, with capex intensity broadly unchanged at {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, and the fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft.
- The average fleet age was broadly stable at {{fleet_age@FY2024}}, a change of {{fleet_age.change@FY2024}}.
- Revenue rose by {{revenue.change@FY2024}} to {{revenue@FY2024}}, while EBITDA was broadly unchanged at {{ebitda@FY2024}}, so the margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, with contract liabilities up by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}.
- Cash liquidity of {{cash_liquidity@FY2024}} covers a smaller share of revenue than the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}, leaving less headroom against the debt taken on during the year.

`peer_positioning`

- Air France-KLM has the weakest EBITDA margin of the network peers ({{ebitda_margin.peer_rank@2024}}), at {{ebitda_margin@FY2024}} against a median of {{ebitda_margin.peer_median@2024}}.
- Leverage is in line with the group: net leverage of {{net_leverage@FY2024}} ranks {{net_leverage.peer_rank@2024}} against a median of {{net_leverage.peer_median@2024}}, and gross leverage of {{gross_leverage@FY2024}} also sits at the median.
- Interest coverage of {{interest_coverage@FY2024}} is the weakest of the group ({{interest_coverage.peer_rank@2024}}) against a median of {{interest_coverage.peer_median@2024}}, and FCF to debt of {{fcf_to_debt@FY2024}} also ranks {{fcf_to_debt.peer_rank@2024}}.
- Advance ticket cover of {{advance_ticket_cover@FY2024}} is the lowest of the group ({{advance_ticket_cover.peer_rank@2024}}) against a median of {{advance_ticket_cover.peer_median@2024}}, and capex intensity of {{capex_intensity@FY2024}} is above the peer median of {{capex_intensity.peer_median@2024}}.

`watch_items`

- Cash generation: free cash flow turned negative at {{fcf@FY2024}} and FCF to debt declined to {{fcf_to_debt@FY2024}}, the weakest of the network peers ({{fcf_to_debt.peer_rank@2024}}).
- Leverage: net debt rose by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, lifting net leverage by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}.
- Liquidity: cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} is below the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.
- Coverage: interest coverage fell by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, below the peer median of {{interest_coverage.peer_median@2024}}, as total debt rose to {{total_debt@FY2024}}.
