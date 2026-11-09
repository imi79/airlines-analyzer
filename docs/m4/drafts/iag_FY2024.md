# International Airlines Group, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `0a1c12bdfde1` ([fact sheet](../factsheets/iag_FY2024.md)). Tokens: 41,464 in, 5,003 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia, Aer Lingus and Vueling, ended FY2024 with a stronger credit profile, both Moody's and S&P having upgraded the group to investment grade during the year.
Net leverage fell by 0.53x to 1.13x as EBITDA rose by 19.3% to EUR 6.6bn on revenue up 9.0% to EUR 32.1bn.
The point to watch is customer prepayments: advance ticket cover fell by 28.8 points to 84.8%, the weakest of the network peers (3rd of 3), while undrawn committed facilities declined by 22.9% to EUR 3.4bn.

> Event `event:funding_and_rating-2`: The Group states it is investment grade with Moody's and S&P, both of which upgraded IAG during the year. Quote (page 115): "We are investment grade with Moody’s and S&P, both of which upgraded IAG during the year."

## Credit metrics

EBITDA increased by 19.3% to EUR 6.6bn, with operating profit up 22.1% to EUR 4.3bn.
Total debt rose by 7.9% to EUR 17.3bn, but net debt was reduced by 18.7% to EUR 7.5bn, taking gross leverage down by 0.28x to 2.61x.
Cash generation strengthened: FFO rose by 31.9% to EUR 5.6bn, lifting FFO to debt by 5.9 points to 32.5%, and free cash flow increased by 169.4% to EUR 3.6bn.
Interest coverage improved by 3.16x to 8.70x, and capex intensity eased by 2.3 points to 8.8%.

## Operating performance

Capacity grew by 6.2% to 343.3bn available seat kilometres, carrying 122.0m passengers.
Unit revenue outpaced unit cost: RASK rose by 2.6% to 9.35 euro cents, while CASK was broadly unchanged at 8.10 euro cents.
CASK ex-fuel rose by 3.4% to 5.89 euro cents, a weaker outcome than the headline unit cost, while the fuel share of costs fell by 1.7 points to 27.4%.
The fleet grew by 3.3% to 601 aircraft, with an average age of 12.4 years, as engine reliability issues and delivery delays continued to affect the group.

> Event `event:fleet_and_engines`: The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent and Pratt and Whitney GTF engines, mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers. Quote (page 161): "The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent 1000 and Pratt and Whitney GTF engines, which are mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers."

## Liquidity and funding

Liquidity rose by 17.6% to EUR 13.2bn, of which EUR 3.4bn in undrawn committed facilities.
Cash and cash-like investments increased by 43.7% to EUR 9.8bn, lifting cash liquidity to revenue by 7.4 points to 30.6%.
Advance ticket cover fell by 28.8 points to 84.8%, even as contract liabilities rose by 7.3% to EUR 8.3bn.
The group replaced its previous secured revolving credit facility and British Airways' export development guarantee facilities with a new sustainability-linked secured facility, undrawn at year end.

> Event `event:funding_and_rating`: The Group entered into a new sustainability-linked secured revolving credit facility and extinguished its previous secured revolving credit facility and British Airways' export development guarantee facilities. Quote (page 30): "on 14 June 2024, the Group entered into a five-year $3.0 billion, sustainability-linked, secured Revolving Credit Facility, with two one-year extension options available subject to the approval of lenders, accessible by British Airways, Iberia and Aer Lingus, each of which has separate limits. At 31 December 2024 no amounts had been drawn under the facility."

## Peer positioning

IAG leads the network airlines on EBITDA margin (1st of 3), net leverage (1st of 3) and gross leverage (1st of 3).
It also ranks at the top on interest coverage (1st of 3), FFO to debt (1st of 3) and FCF to debt (1st of 3), against a peer median FFO to debt of 23.4%.
Capex intensity sits in the middle of the group, and cash liquidity to revenue is the strongest of the peers (1st of 3).
Advance ticket cover is the weakest of the group (3rd of 3), above the peer median of 74.5% but a worse position for credit.

## Watch items

- Customer prepayments: advance ticket cover fell by 28.8 points to 84.8%, the weakest of the network peers (3rd of 3), so the cushion from bookings is thinner than at the group's rivals.
- Committed backstops: undrawn committed facilities fell by 22.9% to EUR 3.4bn, so liquidity of EUR 13.2bn relies more on cash than on committed lines.
- Fleet: average fleet age rose by 3.3% to 12.4 years years, with engine reliability issues and delivery delays still affecting operations.

> Event `event:fleet_and_engines`: The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent and Pratt and Whitney GTF engines, mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers. Quote (page 161): "The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent 1000 and Pratt and Whitney GTF engines, which are mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers."

> removed by the verifier (still broke a rule after two retries): "Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, a weaker trend than the stable headline CASK of {{cask@FY2024}}." ('weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 13,317 / 3,320 |
| 2 | peer_positioning, watch_items | 1 errors | 14,384 / 1,127 |
| 3 | watch_items | 1 errors | 13,763 / 556 |

### Errors found, by try

Try 1:

- [rule 1] peer_positioning, sentence 2: word that states a number: 'first'
- [rule 5] watch_items, sentence 1: advance_ticket_cover.peer_rank@FY2024 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 3: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

Try 2:

- [rule 4] watch_items, sentence 3: 'worse' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 3: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia, Aer Lingus and Vueling, ended FY2024 with a stronger credit profile, both Moody's and S&P having upgraded the group to investment grade during the year.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} as EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}.
- The point to watch is customer prepayments: advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, the weakest of the network peers ({{advance_ticket_cover.peer_rank@FY2024}}), while undrawn committed facilities declined by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, with operating profit up {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, but net debt was reduced by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, taking gross leverage down by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, lifting FFO to debt by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}, and free cash flow increased by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, and capex intensity eased by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Capacity grew by {{ask.change@FY2024}} to {{ask@FY2024}} available seat kilometres, carrying {{passengers@FY2024}} passengers.
- Unit revenue outpaced unit cost: RASK rose by {{rask.change@FY2024}} to {{rask@FY2024}}, while CASK was broadly unchanged at {{cask@FY2024}}.
- CASK ex-fuel rose by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, a weaker outcome than the headline unit cost, while the fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}.
- The fleet grew by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft, with an average age of {{fleet_age@FY2024}}, as engine reliability issues and delivery delays continued to affect the group.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2024}} to {{liquidity@FY2024}}, of which {{undrawn_facilities@FY2024}} in undrawn committed facilities.
- Cash and cash-like investments increased by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, lifting cash liquidity to revenue by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, even as contract liabilities rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}.
- The group replaced its previous secured revolving credit facility and British Airways' export development guarantee facilities with a new sustainability-linked secured facility, undrawn at year end.

`peer_positioning`

- IAG leads the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@FY2024}}), net leverage ({{net_leverage.peer_rank@FY2024}}) and gross leverage ({{gross_leverage.peer_rank@FY2024}}).
- It also ranks at the top on interest coverage ({{interest_coverage.peer_rank@FY2024}}), FFO to debt ({{ffo_to_debt.peer_rank@FY2024}}) and FCF to debt ({{fcf_to_debt.peer_rank@FY2024}}), against a peer median FFO to debt of {{ffo_to_debt.peer_median@FY2024}}.
- Capex intensity sits in the middle of the group, and cash liquidity to revenue is the strongest of the peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).
- Advance ticket cover is the weakest of the group ({{advance_ticket_cover.peer_rank@FY2024}}), above the peer median of {{advance_ticket_cover.peer_median@FY2024}} but a worse position for credit.

`watch_items`

- Customer prepayments: advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, the weakest of the network peers ({{advance_ticket_cover.peer_rank@FY2024}}), so the cushion from bookings is thinner than at the group's rivals.
- Committed backstops: undrawn committed facilities fell by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}, so liquidity of {{liquidity@FY2024}} relies more on cash than on committed lines.
- Fleet: average fleet age rose by {{fleet_age.change@FY2024}} to {{fleet_age@FY2024}} years, with engine reliability issues and delivery delays still affecting operations.
