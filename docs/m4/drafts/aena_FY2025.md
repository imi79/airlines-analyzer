# Aena, FY2025: draft commentary

Status: passed the verifier. First try: passed; tries: 1. Model deepseek-flash, prompt `draft-v3`, fact sheet `5b69c67bac5b` ([fact sheet](../factsheets/aena_FY2025.md)). Tokens: 10,843 in, 2,949 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, ended FY2025 with revenue up 8.9% to EUR 6.3bn and net leverage down to 1.46x.
The EBITDA margin eased by 0.6 points to 60.3%, still the highest of the airport peers (1st of 3).
The main point to watch is cash generation: free cash flow fell by 10.2% to EUR 1.7bn as capex intensity rose to 16.9%.

## Credit metrics

EBITDA increased by 7.8% to EUR 3.8bn, with operating profit up 12.2% to EUR 3.0bn.
Total debt rose by 3.2% to EUR 7.6bn, while net debt was stable at EUR 5.5bn.
Gross leverage was broadly unchanged at 2.00x, in line with the peer median, and net leverage fell by 0.11x to 1.46x.
Interest coverage improved to 14.72x, up 2.38x, and FFO to debt rose by 0.6 points to 39.6%.
FCF to debt declined by 3.4 points to 22.9%, in line with the peer median, as capex intensity increased by 2.6 points to 16.9%.

## Operating performance

Revenue rose by 8.9% to EUR 6.3bn, with non-aeronautical activities making up 47.5% of the total, up 2.1 points.
The commercial mix therefore carries more of the revenue base, which is less directly exposed to the regulated aeronautical tariff.
Capex intensity of 16.9% compares with a peer median of 18.2%, so investment spending remains below the airport group.

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, and total liquidity stood at EUR 4.3bn.
Undrawn committed facilities of EUR 2.2bn supplement the cash position, taking liquidity to revenue to 68.4%.
Cash liquidity to revenue increased by 1.0 point to 32.6%, above the peer median of 30.1%.

## Peer positioning

Aena has the highest EBITDA margin in the airport group (1st of 3), at 60.3% against a peer median of 36.5%.
Net leverage of 1.46x and gross leverage of 2.00x both sit in line with the peer medians of 1.46x and 2.00x, ranking 2nd of 3 and 2nd of 3 respectively.
Cash generation and coverage are in line with the group: FFO to debt of 39.6% and interest coverage of 14.72x match the peer medians of 39.6% and 14.72x.
Cash liquidity to revenue is the strongest of the group (1st of 3).

## Watch items

- Cash generation: FCF to debt fell by 3.4 points to 22.9%, in line with the peer median, as free cash flow declined by 10.2%.
- Investment: capex intensity rose by 2.6 points to 16.9%, below the peer median of 18.2%, so the investment cycle is the main swing factor for free cash flow.
- Margins: the EBITDA margin eased by 0.6 points to 60.3%, though it remains above the peer median of 36.5%.
- Debt: total debt rose by 3.2% to EUR 7.6bn while net debt was stable at EUR 5.5bn, so leverage depends on EBITDA holding at current levels.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | passed | 10,843 / 2,949 |

### Errors found, by try

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, ended FY2025 with revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}} and net leverage down to {{net_leverage@FY2025}}.
- The EBITDA margin eased by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, still the highest of the airport peers ({{ebitda_margin.peer_rank@2025}}).
- The main point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose to {{capex_intensity@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, with operating profit up {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, while net debt was stable at {{net_debt@FY2025}}.
- Gross leverage was broadly unchanged at {{gross_leverage@FY2025}}, in line with the peer median, and net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- Interest coverage improved to {{interest_coverage@FY2025}}, up {{interest_coverage.change@FY2025}}, and FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}.
- FCF to debt declined by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, in line with the peer median, as capex intensity increased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, with non-aeronautical activities making up {{non_aero_share@FY2025}} of the total, up {{non_aero_share.change@FY2025}}.
- The commercial mix therefore carries more of the revenue base, which is less directly exposed to the regulated aeronautical tariff.
- Capex intensity of {{capex_intensity@FY2025}} compares with a peer median of {{capex_intensity.peer_median@2025}}, so investment spending remains below the airport group.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and total liquidity stood at {{liquidity@FY2025}}.
- Undrawn committed facilities of {{undrawn_facilities@FY2025}} supplement the cash position, taking liquidity to revenue to {{liquidity_to_revenue@FY2025}}.
- Cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, above the peer median of {{cash_liquidity_to_revenue.peer_median@2025}}.

`peer_positioning`

- Aena has the highest EBITDA margin in the airport group ({{ebitda_margin.peer_rank@2025}}), at {{ebitda_margin@FY2025}} against a peer median of {{ebitda_margin.peer_median@2025}}.
- Net leverage of {{net_leverage@FY2025}} and gross leverage of {{gross_leverage@FY2025}} both sit in line with the peer medians of {{net_leverage.peer_median@2025}} and {{gross_leverage.peer_median@2025}}, ranking {{net_leverage.peer_rank@2025}} and {{gross_leverage.peer_rank@2025}} respectively.
- Cash generation and coverage are in line with the group: FFO to debt of {{ffo_to_debt@FY2025}} and interest coverage of {{interest_coverage@FY2025}} match the peer medians of {{ffo_to_debt.peer_median@2025}} and {{interest_coverage.peer_median@2025}}.
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@2025}}).

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, in line with the peer median, as free cash flow declined by {{fcf.change@FY2025}}.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, below the peer median of {{capex_intensity.peer_median@2025}}, so the investment cycle is the main swing factor for free cash flow.
- Margins: the EBITDA margin eased by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, though it remains above the peer median of {{ebitda_margin.peer_median@2025}}.
- Debt: total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} while net debt was stable at {{net_debt@FY2025}}, so leverage depends on EBITDA holding at current levels.
