# Groupe ADP, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `638893d593b5` ([fact sheet](../factsheets/adp_FY2024.md)). Tokens: 40,712 in, 6,693 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport group with international operations through TAV Airports and GMR Airports, grew revenue by 12.1% to EUR 6.2bn in FY2024, while the EBITDA margin narrowed by 2.0 points to 33.7%.
Net leverage was broadly unchanged at 4.13x, as net debt rose by 8.2% to EUR 8.6bn and gross leverage eased to 5.14x.
The point to watch is cash generation: free cash flow fell by 50.3% to EUR 355m as capex intensity rose by 3.1 points to 19.0%, leaving cash liquidity to revenue down by 10.8 points to 34.0%.

## Credit metrics

Total debt rose by 2.7% to EUR 10.7bn, so gross leverage fell only to 5.14x and net leverage held at 4.13x.
Interest coverage improved to 6.97x, up 0.23x on the prior year.
FFO was stable at EUR 1.5bn, so FFO to debt held at 14.0%, while FCF to debt fell by 3.6 points to 3.3%.

> removed by the verifier (still broke a rule after two retries): "EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation rose and impairment tests on equity-accounted holdings led to a charge." ('rose' needs a 'up' claim on a figure in the same clause)

## Operating performance

Passengers at the Paris airports reached 103.4m in FY2024.
Revenue grew by 12.1% to EUR 6.2bn, faster than EBITDA, so the EBITDA margin narrowed by 2.0 points to 33.7%.
Capex intensity rose by 3.1 points to 19.0%, reflecting the investment programme across the Paris platform and the international portfolio.
In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond the Paris airports, and since July 2024 it holds a lower economic interest in GMR Airports after the merger of the Indian entities.

> Event `event:acquisitions_and_disposals`: In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond Paris airports. Quote (page 17): "En octobre 2024, le Groupe ADP a acquis, d’une part, Paris Expérience Group et, d’autre part, P/S, élargissant ainsi l'offre d'Extime au-delà des aéroports parisiens et renforçant ses perspectives de croissance à l'international ;"

> Event `event:acquisitions_and_disposals-3`: Following the merger of GMR Airports Infrastructures Ltd and GMR Airports Ltd, the group holds a lower economic interest in GMR Airports. Quote (page 17): "Depuis le 25 juillet 2024, suite à la fusion de GMR Airports Infrastructures Ltd et de GMR Airports Ltd, le Groupe ADP détient un intérêt économique de 45,7 % dans GMR Airports (contre 49,0 % précédemment)."

## Liquidity and funding

Cash and cash-like investments fell by 14.8% to EUR 2.1bn, so cash liquidity to revenue declined by 10.8 points to 34.0%.
The group issued a bond in May 2024, whose proceeds are reported among the year's cash flows, alongside operating cash flow of the year.
With the cash buffer smaller, the group's funding relies more on the bond market and on the cash flow it generates.

> Event `event:funding_and_rating`: The report mentions the proceeds of the bond issue among the group's cash flows. Quote (page 530): "Les flux de trésorerie opérationnels s'établissent à 1 524 millions d'euros et les produits de l'émission obligataire du 7 mai 2024 par"

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport peers (3rd of 3), against a median of 42.0%.
Leverage is the weakest in the group, with net leverage against a median of 1.57x (3rd of 3) and gross leverage against 2.08x (3rd of 3).
Cash generation also lags, with FFO to debt and FCF to debt below peer medians of 26.5% and 14.8%, while cash liquidity to revenue of 34.0% sits in the middle of the group.

> verifier: [rule style] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is already given in liquidity_funding, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Cash generation: free cash flow fell by 50.3% to EUR 355m and FCF to debt dropped by 3.6 points to 3.3%, well below the peer median of 14.8%.
- Investment: capex intensity rose by 3.1 points to 19.0%, above the peer median of 16.1%, which keeps pressure on free cash flow.
- Liquidity: cash and cash-like investments fell by 14.8% to EUR 2.1bn, taking cash liquidity to revenue down by 10.8 points to 34.0%.
- Leverage: net leverage of 4.13x is above the peer median of 1.57x and the weakest of the group (3rd of 3), with net debt up 8.2% to EUR 8.6bn.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 12 errors | 12,173 / 3,215 |
| 2 | credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 15,415 / 2,409 |
| 3 | credit_metrics, peer_positioning | 2 errors | 13,124 / 1,069 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule style] operating_performance, sentence 2: ebitda.change@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 2: ebitda@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: total_debt.change@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2024 is already given in operating_performance, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: net_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is listed in the form but not used in the text
- [rule 4] peer_positioning, sentence 3: 'lags' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule 4] peer_positioning, sentence 3: 'below' needs a 'down' or 'below_peers' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is already given in liquidity_funding, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport group with international operations through TAV Airports and GMR Airports, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, while the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Net leverage was broadly unchanged at {{net_leverage@FY2024}}, as net debt rose by {{net_debt.change@FY2024}} to {{net_debt@FY2024}} and gross leverage eased to {{gross_leverage@FY2024}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, leaving cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.

`credit_metrics`

- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}}, so gross leverage fell only to {{gross_leverage@FY2024}} and net leverage held at {{net_leverage@FY2024}}.
- Interest coverage improved to {{interest_coverage@FY2024}}, up {{interest_coverage.change@FY2024}} on the prior year.
- FFO was stable at {{ffo@FY2024}}, so FFO to debt held at {{ffo_to_debt@FY2024}}, while FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}.

`operating_performance`

- Passengers at the Paris airports reached {{passengers@FY2024}} in FY2024.
- Revenue grew by {{revenue.change@FY2024}} to {{revenue@FY2024}}, faster than EBITDA, so the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, reflecting the investment programme across the Paris platform and the international portfolio.
- In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond the Paris airports, and since July 2024 it holds a lower economic interest in GMR Airports after the merger of the Indian entities.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, so cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- The group issued a bond in May 2024, whose proceeds are reported among the year's cash flows, alongside operating cash flow of the year.
- With the cash buffer smaller, the group's funding relies more on the bond market and on the cash flow it generates.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport peers ({{ebitda_margin.peer_rank@FY2024}}), against a median of {{ebitda_margin.peer_median@FY2024}}.
- Leverage is the weakest in the group, with net leverage against a median of {{net_leverage.peer_median@FY2024}} ({{net_leverage.peer_rank@FY2024}}) and gross leverage against {{gross_leverage.peer_median@FY2024}} ({{gross_leverage.peer_rank@FY2024}}).
- Cash generation also lags, with FFO to debt and FCF to debt below peer medians of {{ffo_to_debt.peer_median@FY2024}} and {{fcf_to_debt.peer_median@FY2024}}, while cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} sits in the middle of the group.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} and FCF to debt dropped by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, well below the peer median of {{fcf_to_debt.peer_median@FY2024}}.
- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, above the peer median of {{capex_intensity.peer_median@FY2024}}, which keeps pressure on free cash flow.
- Liquidity: cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- Leverage: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@FY2024}} and the weakest of the group ({{net_leverage.peer_rank@FY2024}}), with net debt up {{net_debt.change@FY2024}} to {{net_debt@FY2024}}.
