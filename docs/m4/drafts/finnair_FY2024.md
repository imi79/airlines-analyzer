# Finnair, FY2024: draft commentary

Status: **needs manual editing** (some sections still rejected after two retries). First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `1c2a5682d833` ([fact sheet](../factsheets/finnair_FY2024.md)). Tokens: 46,758 in, 8,308 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot (needs manual editing)

Finnair, the Finnish network carrier, ended FY2024 with revenue up 2.0% to EUR 3.0bn but a lower earnings base, as industrial action in Finland led to the cancellation of a large number of flights in the early and late parts of the year.
The EBITDA margin narrowed by 3.4 points to 14.6%, and net leverage rose by 0.16x to 2.21x.
The point to watch is leverage against the network peers: net leverage of 2.21x is above the peer median of 1.88x and the weakest of the group (3rd of 3).

> Event `event:labour`: Industrial action in Finland led to the cancellation of a large number of flights in the early part of the year and again in the late part of the year. Quote (page 7): "Industrial action in Finland had an impact on Finnair’s operations, leading to the cancellation of approximately 550 flights in the first quarter and more than 500 flights in the fourth quarter."

> verifier: [rule 4] snapshot, sentence 1: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause

## Credit metrics

EBITDA fell by 17.3% to EUR 445m, and operating profit declined by 40.3% to EUR 114m as depreciation, amortisation and impairment eased by 4.6% to EUR 330m.
Total debt was reduced by 7.9% to EUR 1.9bn and net debt by 11.1% to EUR 981m, yet gross leverage rose by 0.43x to 4.20x as EBITDA fell by 17.3%.
Interest coverage improved to 4.15x as finance costs fell by 24.6% to EUR 107m.
FFO declined by 7.4% to EUR 406m, leaving FFO to debt broadly unchanged at 21.8%, while free cash flow rose by 456.7% to EUR 379m as capex fell by 42.2% to EUR 234m.
FCF to debt rose by 16.9 points to 20.3%, and capex intensity fell by 5.8 points to 7.7%.

## Operating performance

Passengers rose by 6.1% to 11.7m, while revenue grew by 2.0% to EUR 3.0bn.
Fuel cost was broadly unchanged at EUR 894m, with the fuel share of costs easing by 1.6 points to 30.5%.
The fleet was stable at 80 aircraft, with a new A350 delivered and leased A350 and A321 aircraft purchased during the year.

> Event `event:fleet_and_engines`: A new A350 aircraft was delivered during the year and Finnair purchased a leased A350 and a leased A321 aircraft. Quote (page 169): "During the financial year, a new A350 aircraft was delivered and additionally, Finnair purchased one leased A350 and one leased A321 aircraft. All aircraft were in operative use as at the balance sheet date."

## Liquidity and funding

Cash and cash-like investments fell by 4.1% to EUR 884m, and cash liquidity to revenue declined by 1.8 points to 29.0%.
Liquidity of EUR 1.1bn includes EUR 200m of undrawn committed facilities, and liquidity to revenue stood at 35.6%.
Advance ticket cover rose by 19.5 points to 74.5%, with contract liabilities up by 30.0% to EUR 659m, so a larger share of the cash is customers' prepayments.
Funding was refinanced during the year: a new unsecured senior bond was issued to replace the old bond, and a new secured revolving credit facility was agreed and left unused at year-end.

> Event `event:funding_and_rating-2`: Finnair issued a new unsecured senior bond to refinance the old unsecured senior bond, and the new bond matures later with a fixed annual interest. Quote (page 22): "As a testament to this, Finnair signed a binding secured revolving credit facility of 200 million euros for general corporate purposes and successfully issued a new 500-million-euro unsecured senior bond to refinance the old 400-million-euro unsecured senior bond. The new bond will mature in 2029 and carries a fixed annual interest of 4.750 per cent."

> Event `event:funding_and_rating-3`: Finnair agreed a new secured revolving credit facility for general corporate purposes, unused at year-end with a multi-year tenor and an extension option. Quote (page 15): "Further, in April, Finnair agreed on a new secured revolving credit facility 3 of 200 million euros for general corporate purposes. The arrangement was unused at the end of the year and carries a three-year tenor with a one-year extension option."

## Peer positioning

Finnair sits in the middle of the network group on EBITDA margin (2nd of 3), FCF to debt (2nd of 3) and cash liquidity to revenue (2nd of 3).
Leverage is the weakest part of the profile: net leverage and gross leverage are both the highest of the group (3rd of 3 and 3rd of 3).
Coverage and cash generation also trail the group, with interest coverage of 4.15x against a peer median of 6.51x and FFO to debt of 21.8% against 23.4%.

> verifier: [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

> verifier: [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Earnings: the EBITDA margin narrowed by 3.4 points to 14.6%, with EBITDA down 17.3% to EUR 445m.
- Customer prepayments: advance ticket cover rose by 19.5 points to 74.5%, in line with the peer median, so a larger part of the cash balance is refundable if bookings slow.
- Liquidity: cash liquidity to revenue fell by 1.8 points to 29.0%, with cash and cash-like investments down 4.1% to EUR 884m.

> removed by the verifier (still broke a rule after two retries): "Leverage: net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, above the peer median of {{net_leverage.peer_median@FY2024}}, so the earnings base needs to recover to bring it down." ('down' needs a 'down' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 7 errors | 13,754 / 3,389 |
| 2 | snapshot, credit_metrics, liquidity_funding, peer_positioning, watch_items | 5 errors | 16,995 / 2,933 |
| 3 | snapshot, liquidity_funding, peer_positioning, watch_items | 4 errors | 16,009 / 1,986 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 2: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 1] liquidity_funding, sentence 4: word that states a number: 'one'
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'down' needs a 'down' claim on a figure in the same clause

Try 2:

- [rule 4] snapshot, sentence 1: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 1] liquidity_funding, sentence 4: word that states a number: 'one'
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'down' needs a 'down' claim on a figure in the same clause

Try 3:

- [rule 4] snapshot, sentence 1: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'down' needs a 'down' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, ended FY2024 with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}} but a lower earnings base, as industrial action in Finland led to the cancellation of a large number of flights in the early and late parts of the year.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, and net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}.
- The point to watch is leverage against the network peers: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@FY2024}} and the weakest of the group ({{net_leverage.peer_rank@FY2024}}).

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, and operating profit declined by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation, amortisation and impairment eased by {{dda.change@FY2024}} to {{dda@FY2024}}.
- Total debt was reduced by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, yet gross leverage rose by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} as EBITDA fell by {{ebitda.change@FY2024}}.
- Interest coverage improved to {{interest_coverage@FY2024}} as finance costs fell by {{finance_costs.change@FY2024}} to {{finance_costs@FY2024}}.
- FFO declined by {{ffo.change@FY2024}} to {{ffo@FY2024}}, leaving FFO to debt broadly unchanged at {{ffo_to_debt@FY2024}}, while free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex fell by {{capex.change@FY2024}} to {{capex@FY2024}}.
- FCF to debt rose by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, and capex intensity fell by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, while revenue grew by {{revenue.change@FY2024}} to {{revenue@FY2024}}.
- Fuel cost was broadly unchanged at {{fuel_cost@FY2024}}, with the fuel share of costs easing by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}.
- The fleet was stable at {{fleet@FY2024}} aircraft, with a new A350 delivered and leased A350 and A321 aircraft purchased during the year.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Liquidity of {{liquidity@FY2024}} includes {{undrawn_facilities@FY2024}} of undrawn committed facilities, and liquidity to revenue stood at {{liquidity_to_revenue@FY2024}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, with contract liabilities up by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, so a larger share of the cash is customers' prepayments.
- Funding was refinanced during the year: a new unsecured senior bond was issued to replace the old bond, and a new secured revolving credit facility was agreed and left unused at year-end.

`peer_positioning`

- Finnair sits in the middle of the network group on EBITDA margin ({{ebitda_margin.peer_rank@FY2024}}), FCF to debt ({{fcf_to_debt.peer_rank@FY2024}}) and cash liquidity to revenue ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).
- Leverage is the weakest part of the profile: net leverage and gross leverage are both the highest of the group ({{net_leverage.peer_rank@FY2024}} and {{gross_leverage.peer_rank@FY2024}}).
- Coverage and cash generation also trail the group, with interest coverage of {{interest_coverage@FY2024}} against a peer median of {{interest_coverage.peer_median@FY2024}} and FFO to debt of {{ffo_to_debt@FY2024}} against {{ffo_to_debt.peer_median@FY2024}}.

`watch_items`

- Earnings: the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, with EBITDA down {{ebitda.change@FY2024}} to {{ebitda@FY2024}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, in line with the peer median, so a larger part of the cash balance is refundable if bookings slow.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, with cash and cash-like investments down {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.
