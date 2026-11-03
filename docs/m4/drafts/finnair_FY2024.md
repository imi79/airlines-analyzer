# Finnair, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `e2c7735e4566` ([fact sheet](../factsheets/finnair_FY2024.md)). Tokens: 23,450 in, 4,902 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Finnair, the Finnish network carrier, ended FY2024 with a weaker credit profile as EBITDA fell by 17.3% to EUR 445m on revenue up 2.0% to EUR 3.0bn.
Net leverage rose by 0.16x to 2.21x and gross leverage by 0.43x to 4.20x, both above the peer median.
The main point to watch is liquidity: cash liquidity to revenue fell by 1.8 points to 29.0% as cash and cash-like investments declined by 4.1% to EUR 884m.

## Credit metrics

EBITDA declined by 17.3% to EUR 445m, taking the EBITDA margin down by 3.4 points to 14.6%.
Total debt was reduced by 7.9% to EUR 1.9bn and net debt by 11.1% to EUR 981m, but net leverage still rose to 2.21x.
Interest coverage improved by 6.25x to 11.70x, above the peer median of 8.70x.
FFO fell by 7.4% to EUR 406m, leaving FFO to debt broadly unchanged at 21.8% and below the peer median of 23.4%.
Free cash flow rose by 456.7% to EUR 379m as capex intensity eased by 5.8 points to 7.7%, lifting FCF to debt to 20.3%.

## Operating performance

Passengers rose by 6.1% to 11.7m, while the fleet was stable at 80 aircraft.
Revenue grew by 2.0% to EUR 3.0bn, but operating profit fell by 40.3% to EUR 114m.
Fuel made up 30.5% of costs, down 1.6 points and above the peer median of 28.9%, so the cost base remains sensitive to jet fuel prices.

## Liquidity and funding

Cash and cash-like investments fell by 4.1% to EUR 884m, and total liquidity stood at EUR 1.1bn, including EUR 200m of undrawn committed facilities.
Liquidity to revenue was 35.6%, with cash liquidity to revenue down by 1.8 points to 29.0%, in line with the peer median.
Customer prepayments rose: contract liabilities increased by 30.0% to EUR 659m, and advance ticket cover rose by 19.5 points to 74.5%, in line with the peer median.

## Peer positioning

Finnair has the weakest net leverage of the network airlines (3rd of 3), at 2.21x against a peer median of 1.88x.
Gross leverage of 4.20x is also the highest of the group (3rd of 3), above the peer median of 3.56x.
Interest coverage is the strongest in the group (1st of 3) at 11.70x, while FFO to debt ranks 3rd of 3 at 21.8%.
The EBITDA margin of 14.6% is in line with the peer median of 14.6%, ranking 2nd of 3.

## Watch items

- Leverage: net leverage rose to 2.21x and gross leverage to 4.20x, ranking 3rd of 3 and 3rd of 3 respectively, so further EBITDA erosion would leave little headroom.
- Cash generation: FFO to debt of 21.8% is below the peer median of 23.4%, and FFO fell by 7.4% to EUR 406m.
- Liquidity: cash liquidity to revenue fell by 1.8 points to 29.0%, with undrawn committed facilities of EUR 200m against total liquidity of EUR 1.1bn.
- Customer prepayments: advance ticket cover rose by 19.5 points to 74.5%, in line with the peer median, so a larger share of liquidity is refundable if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 11,502 / 3,413 |
| 2 | credit_metrics, watch_items | passed | 11,948 / 1,489 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 2: 'decline' needs a 'down' claim on a figure in the same clause
- [rule 3] watch_items, sentence 1: 'worst_in_group' needs the rank id (.peer_rank), not net_leverage@FY2024
- [rule 3] watch_items, sentence 1: 'worst_in_group' needs the rank id (.peer_rank), not gross_leverage@FY2024

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, ended FY2024 with a weaker credit profile as EBITDA fell by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}.
- Net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} and gross leverage by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}, both above the peer median.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} as cash and cash-like investments declined by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.

`credit_metrics`

- EBITDA declined by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, taking the EBITDA margin down by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Total debt was reduced by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, but net leverage still rose to {{net_leverage@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, above the peer median of {{interest_coverage.peer_median@2024}}.
- FFO fell by {{ffo.change@FY2024}} to {{ffo@FY2024}}, leaving FFO to debt broadly unchanged at {{ffo_to_debt@FY2024}} and below the peer median of {{ffo_to_debt.peer_median@2024}}.
- Free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity eased by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, lifting FCF to debt to {{fcf_to_debt@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, while the fleet was stable at {{fleet@FY2024}} aircraft.
- Revenue grew by {{revenue.change@FY2024}} to {{revenue@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Fuel made up {{fuel_share_of_costs@FY2024}} of costs, down {{fuel_share_of_costs.change@FY2024}} and above the peer median of {{fuel_share_of_costs.peer_median@2024}}, so the cost base remains sensitive to jet fuel prices.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and total liquidity stood at {{liquidity@FY2024}}, including {{undrawn_facilities@FY2024}} of undrawn committed facilities.
- Liquidity to revenue was {{liquidity_to_revenue@FY2024}}, with cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, in line with the peer median.
- Customer prepayments rose: contract liabilities increased by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, and advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, in line with the peer median.

`peer_positioning`

- Finnair has the weakest net leverage of the network airlines ({{net_leverage.peer_rank@2024}}), at {{net_leverage@FY2024}} against a peer median of {{net_leverage.peer_median@2024}}.
- Gross leverage of {{gross_leverage@FY2024}} is also the highest of the group ({{gross_leverage.peer_rank@2024}}), above the peer median of {{gross_leverage.peer_median@2024}}.
- Interest coverage is the strongest in the group ({{interest_coverage.peer_rank@2024}}) at {{interest_coverage@FY2024}}, while FFO to debt ranks {{ffo_to_debt.peer_rank@2024}} at {{ffo_to_debt@FY2024}}.
- The EBITDA margin of {{ebitda_margin@FY2024}} is in line with the peer median of {{ebitda_margin.peer_median@2024}}, ranking {{ebitda_margin.peer_rank@2024}}.

`watch_items`

- Leverage: net leverage rose to {{net_leverage@FY2024}} and gross leverage to {{gross_leverage@FY2024}}, ranking {{net_leverage.peer_rank@2024}} and {{gross_leverage.peer_rank@2024}} respectively, so further EBITDA erosion would leave little headroom.
- Cash generation: FFO to debt of {{ffo_to_debt@FY2024}} is below the peer median of {{ffo_to_debt.peer_median@2024}}, and FFO fell by {{ffo.change@FY2024}} to {{ffo@FY2024}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, with undrawn committed facilities of {{undrawn_facilities@FY2024}} against total liquidity of {{liquidity@FY2024}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, in line with the peer median, so a larger share of liquidity is refundable if bookings slow.
