# International Airlines Group, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `0a1c12bdfde1` ([fact sheet](../factsheets/iag_FY2024.md)). Tokens: 43,640 in, 6,260 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia, Aer Lingus and Vueling, ended FY2024 with revenue up 9.0% to EUR 32.1bn and both Moody's and S&P upgrading the group to investment grade during the year.
The EBITDA margin widened by 1.8 points to 20.7% and net leverage fell by 0.53x to 1.13x, the lowest of the network peers (1st of 3).
The point to watch is customer prepayments: advance ticket cover fell by 28.8 points to 84.8%, the weakest of the group (3rd of 3), while undrawn committed facilities declined by 22.9% to EUR 3.4bn.

> Event `event:funding_and_rating-2`: The Group states it is investment grade with Moody's and S&P, both of which upgraded IAG during the year. Quote (page 115): "We are investment grade with Moody’s and S&P, both of which upgraded IAG during the year."

## Credit metrics

EBITDA increased by 19.3% to EUR 6.6bn, and operating profit rose by 22.1% to EUR 4.3bn after depreciation.
Interest coverage improved by 3.16x to 8.70x, well above the peer median of 6.51x.
FFO rose by 31.9% to EUR 5.6bn, lifting FFO to debt by 5.9 points to 32.5%, and free cash flow increased by 169.4% to EUR 3.6bn as capex intensity eased by 2.3 points to 8.8%.

> removed by the verifier (still broke a rule after two retries): "Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, but net debt was reduced by {{net_debt.change@FY2024}} to {{net_debt@FY2024}} as cash built up, taking gross leverage down by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}." ('up' needs a 'up' claim on a figure in the same clause)

## Operating performance

Capacity grew by 6.2% to 343.3bn available seat kilometres, carrying 122.0m passengers.
RASK rose by 2.6% to 9.35 euro cents, while CASK was broadly unchanged at 8.10 euro cents as the fuel share of costs fell by 1.7 points to 27.4%.
CASK ex-fuel rose by 3.4% to 5.89 euro cents, so non-fuel unit costs absorbed part of the fuel benefit.
The fleet increased by 3.3% to 601 aircraft, with an average age of 12.4 years, as engine reliability issues and delivery delays continued to affect the group.

> Event `event:fleet_and_engines`: The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent and Pratt and Whitney GTF engines, mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers. Quote (page 161): "The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent 1000 and Pratt and Whitney GTF engines, which are mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers."

## Liquidity and funding

Liquidity rose by 17.6% to EUR 13.2bn, of which cash and cash-like investments of EUR 9.8bn were up 43.7%.
Cash liquidity to revenue rose by 7.4 points to 30.6%, and liquidity to revenue reached 41.2%.
Undrawn committed facilities fell by 22.9% to EUR 3.4bn, after the group replaced its previous secured facilities with a new sustainability-linked revolving credit facility that was undrawn at year end.
Contract liabilities rose by 7.3% to EUR 8.3bn, but advance ticket cover fell by 28.8 points to 84.8%.

> Event `event:funding_and_rating`: The Group entered into a new sustainability-linked secured revolving credit facility and extinguished its previous secured revolving credit facility and British Airways' export development guarantee facilities. Quote (page 30): "on 14 June 2024, the Group entered into a five-year $3.0 billion, sustainability-linked, secured Revolving Credit Facility, with two one-year extension options available subject to the approval of lenders, accessible by British Airways, Iberia and Aer Lingus, each of which has separate limits. At 31 December 2024 no amounts had been drawn under the facility."

## Peer positioning

IAG leads the network airlines on EBITDA margin (1st of 3), net leverage (1st of 3) and FFO to debt (1st of 3).
Advance ticket cover ranks 3rd of 3, the weakest of the group, against a peer median of 74.5%.
Capex intensity sits in the middle of the group, and FCF to debt of 20.5% is in line with the peer median of 20.3%.

## Watch items

- Customer prepayments: advance ticket cover fell by 28.8 points to 84.8%, the weakest of the group (3rd of 3), so the cash buffer rests more on the group's own balances than on bookings.
- Undrawn facilities: committed lines fell by 22.9% to EUR 3.4bn, a weaker backstop than a year earlier.
- Unit cost: CASK ex-fuel rose by 3.4% to 5.89 euro cents, so non-fuel costs are the pressure point even as the fuel share of costs declined by 1.7 points to 27.4%.
- Fleet: average age rose by 3.3% to 12.4 years years, with engine reliability issues and delivery delays still affecting operations.

> Event `event:fleet_and_engines`: The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent and Pratt and Whitney GTF engines, mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers. Quote (page 161): "The Group continues to be impacted by reliability and performance issues with Rolls-Royce Trent 1000 and Pratt and Whitney GTF engines, which are mitigated by using replacement aircraft and invoking remedy support from the engine manufacturers."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 13,589 / 3,218 |
| 2 | snapshot, credit_metrics, peer_positioning, watch_items | 1 errors | 15,887 / 2,257 |
| 3 | credit_metrics | 1 errors | 14,164 / 785 |

### Errors found, by try

Try 1:

- [rule 3] snapshot, sentence 2: 'best_in_group' needs the rank id (.peer_rank), not net_leverage@FY2024
- [rule 3] snapshot, sentence 3: 'worst_in_group' needs the rank id (.peer_rank), not advance_ticket_cover@FY2024
- [rule 4] credit_metrics, sentence 2: 'up' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: advance_ticket_cover@FY2024 is already given in liquidity_funding, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] watch_items, sentence 1: 'worst_in_group' needs the rank id (.peer_rank), not advance_ticket_cover@FY2024
- [rule 4] watch_items, sentence 3: 'fell' needs a 'down' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 2: 'up' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 2: 'up' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia, Aer Lingus and Vueling, ended FY2024 with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}} and both Moody's and S&P upgrading the group to investment grade during the year.
- The EBITDA margin widened by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}} and net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, the lowest of the network peers ({{net_leverage.peer_rank@FY2024}}).
- The point to watch is customer prepayments: advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, the weakest of the group ({{advance_ticket_cover.peer_rank@FY2024}}), while undrawn committed facilities declined by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, and operating profit rose by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} after depreciation.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, well above the peer median of {{interest_coverage.peer_median@FY2024}}.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, lifting FFO to debt by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}, and free cash flow increased by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity eased by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Capacity grew by {{ask.change@FY2024}} to {{ask@FY2024}} available seat kilometres, carrying {{passengers@FY2024}} passengers.
- RASK rose by {{rask.change@FY2024}} to {{rask@FY2024}}, while CASK was broadly unchanged at {{cask@FY2024}} as the fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}.
- CASK ex-fuel rose by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, so non-fuel unit costs absorbed part of the fuel benefit.
- The fleet increased by {{fleet.change@FY2024}} to {{fleet@FY2024}} aircraft, with an average age of {{fleet_age@FY2024}}, as engine reliability issues and delivery delays continued to affect the group.

`liquidity_funding`

- Liquidity rose by {{liquidity.change@FY2024}} to {{liquidity@FY2024}}, of which cash and cash-like investments of {{cash_like@FY2024}} were up {{cash_like.change@FY2024}}.
- Cash liquidity to revenue rose by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, and liquidity to revenue reached {{liquidity_to_revenue@FY2024}}.
- Undrawn committed facilities fell by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}, after the group replaced its previous secured facilities with a new sustainability-linked revolving credit facility that was undrawn at year end.
- Contract liabilities rose by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, but advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}.

`peer_positioning`

- IAG leads the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@FY2024}}), net leverage ({{net_leverage.peer_rank@FY2024}}) and FFO to debt ({{ffo_to_debt.peer_rank@FY2024}}).
- Advance ticket cover ranks {{advance_ticket_cover.peer_rank@FY2024}}, the weakest of the group, against a peer median of {{advance_ticket_cover.peer_median@FY2024}}.
- Capex intensity sits in the middle of the group, and FCF to debt of {{fcf_to_debt@FY2024}} is in line with the peer median of {{fcf_to_debt.peer_median@FY2024}}.

`watch_items`

- Customer prepayments: advance ticket cover fell by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, the weakest of the group ({{advance_ticket_cover.peer_rank@FY2024}}), so the cash buffer rests more on the group's own balances than on bookings.
- Undrawn facilities: committed lines fell by {{undrawn_facilities.change@FY2024}} to {{undrawn_facilities@FY2024}}, a weaker backstop than a year earlier.
- Unit cost: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2024}} to {{cask_ex_fuel@FY2024}}, so non-fuel costs are the pressure point even as the fuel share of costs declined by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}.
- Fleet: average age rose by {{fleet_age.change@FY2024}} to {{fleet_age@FY2024}} years, with engine reliability issues and delivery delays still affecting operations.
