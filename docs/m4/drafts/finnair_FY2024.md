# Finnair, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `420d40064147` ([fact sheet](../factsheets/finnair_FY2024.md)). Tokens: 44,620 in, 8,304 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Finnair, the Finnish network carrier, ended FY2024 with revenue up 2.0% to EUR 3.0bn, but EBITDA declined by 17.3% as industrial action in Finland led to the cancellation of a large number of flights in the early and late parts of the year.
The EBITDA margin narrowed by 3.4 points to 14.6%, and net leverage rose by 0.16x to 2.21x despite lower net debt of EUR 981m.
The point to watch is leverage against the network peers: net leverage of 2.21x is above the peer median of 1.88x and the weakest of the group (3rd of 3).

> Event `event:labour`: Industrial action in Finland led to the cancellation of a large number of flights in the early part of the year and again in the late part of the year. Quote (page 7): "Industrial action in Finland had an impact on Finnair’s operations, leading to the cancellation of approximately 550 flights in the first quarter and more than 500 flights in the fourth quarter."

## Credit metrics

EBITDA fell by 17.3% to EUR 445m on revenue up 2.0%, and operating profit declined by 40.3% to EUR 114m.
Total debt was reduced by 7.9% to EUR 1.9bn and net debt by 11.1% to EUR 981m, yet gross leverage rose by 0.43x to 4.20x as EBITDA fell by 17.3%.
Interest coverage improved by 0.37x to 4.15x, while FFO fell by 7.4% to EUR 406m and FFO to debt was broadly unchanged at 21.8%.
Free cash flow rose by 456.7% to EUR 379m, lifting FCF to debt by 16.9 points to 20.3%, helped by capex intensity easing by 5.8 points to 7.7%.

## Operating performance

Passengers rose by 6.1% to 11.7m, while the fleet was broadly unchanged at 80 aircraft, with a new A350 delivered and leased A350 and A321 aircraft purchased during the year.
The fuel share of costs fell by 1.6 points to 30.5%, above the peer median of 28.9%.
The fleet averaged 12.5 years in age in FY2023.

> Event `event:fleet_and_engines`: A new A350 aircraft was delivered during the year and Finnair purchased a leased A350 and a leased A321 aircraft. Quote (page 169): "During the financial year, a new A350 aircraft was delivered and additionally, Finnair purchased one leased A350 and one leased A321 aircraft. All aircraft were in operative use as at the balance sheet date."

## Liquidity and funding

Cash and cash-like investments fell by 4.1% to EUR 884m, and cash liquidity to revenue declined by 1.8 points to 29.0%.
Total liquidity was EUR 1.1bn, including EUR 200m of undrawn committed facilities under a new secured revolving credit facility agreed in April and unused at year-end.
Advance ticket cover rose by 19.5 points to 74.5%, with contract liabilities up 30.0% to EUR 659m, so a larger share of cash is customers' prepayments.
Funding was refinanced during the year, with a new unsecured senior bond issued to repay the old bond, and S&P assigned Finnair an issuer credit rating with a stable outlook.

> Event `event:funding_and_rating-3`: Finnair agreed a new secured revolving credit facility for general corporate purposes, unused at year-end with a multi-year tenor and an extension option. Quote (page 15): "Further, in April, Finnair agreed on a new secured revolving credit facility 3 of 200 million euros for general corporate purposes. The arrangement was unused at the end of the year and carries a three-year tenor with a one-year extension option."

> Event `event:funding_and_rating-2`: Finnair issued a new unsecured senior bond to refinance the old unsecured senior bond, and the new bond matures later with a fixed annual interest. Quote (page 22): "As a testament to this, Finnair signed a binding secured revolving credit facility of 200 million euros for general corporate purposes and successfully issued a new 500-million-euro unsecured senior bond to refinance the old 400-million-euro unsecured senior bond. The new bond will mature in 2029 and carries a fixed annual interest of 4.750 per cent."

> Event `event:funding_and_rating`: S&P Global Ratings assigned Finnair a long-term issuer credit rating with a stable outlook, the company's inaugural credit rating. Quote (page 22): "Furthemore, S&P Global Ratings assigned a long-term issuer credit rating of BB+ to Finnair Plc with a stable outlook. It is the first credit rating for Finnair."

## Peer positioning

Finnair's EBITDA margin of 14.6% puts it in the middle of the network group (2nd of 3), and FCF to debt ranks 2nd of 3, also in the middle of the group.
Leverage is the weakest part of the profile: net leverage of 2.21x is above the peer median of 1.88x and ranks 3rd of 3, and gross leverage is also the highest of the group (3rd of 3).
Coverage and cash generation lag the group: interest coverage of 4.15x is below the peer median of 6.51x and ranks 3rd of 3, and FFO to debt is also the weakest (3rd of 3).

> verifier: [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Leverage: net leverage rose by 0.16x to 2.21x and gross leverage by 0.43x to 4.20x, both above the peer median, as EBITDA fell by 17.3%.
- Earnings: the EBITDA margin narrowed by 3.4 points to 14.6%, with industrial action in Finland leading to the cancellation of a large number of flights in the early and late parts of the year.
- Cash generation: FFO fell by 7.4% to EUR 406m, leaving FFO to debt at 21.8%, below the peer median of 23.4%.
- Customer prepayments: advance ticket cover rose by 19.5 points to 74.5%, a sensitivity if bookings slow.

> Event `event:labour`: Industrial action in Finland led to the cancellation of a large number of flights in the early part of the year and again in the late part of the year. Quote (page 7): "Industrial action in Finland had an impact on Finnair’s operations, leading to the cancellation of approximately 550 flights in the first quarter and more than 500 flights in the fourth quarter."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 9 errors | 13,158 / 3,365 |
| 2 | snapshot, credit_metrics, liquidity_funding, peer_positioning, watch_items | 3 errors | 16,459 / 2,967 |
| 3 | credit_metrics, peer_positioning, watch_items | passed | 15,003 / 1,972 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 4] credit_metrics, sentence 2: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 1] liquidity_funding, sentence 4: word that states a number: 'one'
- [rule 5] peer_positioning, sentence 1: fcf_to_debt.peer_rank@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 1: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'fell' needs a 'down' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 2: 'declined' needs a 'down' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'declined' needs a 'down' claim on a figure in the same clause

Try 3:

- [rule style] peer_positioning, sentence 3: interest_coverage@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Finnair, the Finnish network carrier, ended FY2024 with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}, but EBITDA declined by {{ebitda.change@FY2024}} as industrial action in Finland led to the cancellation of a large number of flights in the early and late parts of the year.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, and net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} despite lower net debt of {{net_debt@FY2024}}.
- The point to watch is leverage against the network peers: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@FY2024}} and the weakest of the group ({{net_leverage.peer_rank@FY2024}}).

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}}, and operating profit declined by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt was reduced by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, yet gross leverage rose by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} as EBITDA fell by {{ebitda.change@FY2024}}.
- Interest coverage improved by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, while FFO fell by {{ffo.change@FY2024}} to {{ffo@FY2024}} and FFO to debt was broadly unchanged at {{ffo_to_debt@FY2024}}.
- Free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}}, lifting FCF to debt by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, helped by capex intensity easing by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, while the fleet was broadly unchanged at {{fleet@FY2024}} aircraft, with a new A350 delivered and leased A350 and A321 aircraft purchased during the year.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}, above the peer median of {{fuel_share_of_costs.peer_median@FY2024}}.
- The fleet averaged {{fleet_age@FY2023}} in age in FY2023.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Total liquidity was {{liquidity@FY2024}}, including {{undrawn_facilities@FY2024}} of undrawn committed facilities under a new secured revolving credit facility agreed in April and unused at year-end.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, with contract liabilities up {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}, so a larger share of cash is customers' prepayments.
- Funding was refinanced during the year, with a new unsecured senior bond issued to repay the old bond, and S&P assigned Finnair an issuer credit rating with a stable outlook.

`peer_positioning`

- Finnair's EBITDA margin of {{ebitda_margin@FY2024}} puts it in the middle of the network group ({{ebitda_margin.peer_rank@FY2024}}), and FCF to debt ranks {{fcf_to_debt.peer_rank@FY2024}}, also in the middle of the group.
- Leverage is the weakest part of the profile: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@FY2024}} and ranks {{net_leverage.peer_rank@FY2024}}, and gross leverage is also the highest of the group ({{gross_leverage.peer_rank@FY2024}}).
- Coverage and cash generation lag the group: interest coverage of {{interest_coverage@FY2024}} is below the peer median of {{interest_coverage.peer_median@FY2024}} and ranks {{interest_coverage.peer_rank@FY2024}}, and FFO to debt is also the weakest ({{ffo_to_debt.peer_rank@FY2024}}).

`watch_items`

- Leverage: net leverage rose by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} and gross leverage by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}, both above the peer median, as EBITDA fell by {{ebitda.change@FY2024}}.
- Earnings: the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, with industrial action in Finland leading to the cancellation of a large number of flights in the early and late parts of the year.
- Cash generation: FFO fell by {{ffo.change@FY2024}} to {{ffo@FY2024}}, leaving FFO to debt at {{ffo_to_debt@FY2024}}, below the peer median of {{ffo_to_debt.peer_median@FY2024}}.
- Customer prepayments: advance ticket cover rose by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}}, a sensitivity if bookings slow.
