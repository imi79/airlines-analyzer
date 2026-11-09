# Flughafen Wien, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `fc44386045a8` ([fact sheet](../factsheets/vie_FY2025.md)). Tokens: 40,925 in, 4,414 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport group, grew revenue by 7.2% to EUR 1.1bn in FY2025, but EBITDA fell by 6.7% as write-offs on the abandoned third runway project and higher personnel costs weighed on the result.
The EBITDA margin narrowed by 5.5 points to 36.5%, and net leverage moved to net cash of EUR 414m from EUR 512m.
The point to watch is cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex rose by 59.9% to EUR 272m, leaving cash liquidity to revenue at 41.6%.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

> Event `event:costs`: Personnel expenses rose due to collective agreement increases and additions to personnel provisions, partly related to underutilisation. Quote (part 10): "Der Anstieg des Personalaufwands um € 11,2 Mio. auf € 66,1 Mio. ist auf kollektivvertragliche Erhöhungen (ab 1.5.2025 +3,3%) und Dotierungen von Personalrückstellungen unter anderem im Zusammenhang mit Unterauslastung zurückzuführen."

## Credit metrics

EBITDA fell by 6.7% to EUR 412m on revenue up 7.2%, with the write-offs on the third runway project and environmental measures in the neighbouring municipalities among the special items.
Operating profit declined by 8.7% to EUR 280m as depreciation, amortisation and impairment eased by 2.1% to EUR 133m.
Total debt was stable at EUR 55.9m, so gross leverage held at 0.14x and the group kept net cash of EUR 414m, down by 19.1%.
Cash generation weakened: FFO fell by 31.0% to EUR 247m and cash from operations by 24.9% to EUR 333m, while capex intensity rose by 8.0 points to 24.1%.
Finance costs rose by 52.7% to EUR 4.3m, a small charge against an EBITDA of EUR 412m given the minimal debt stock.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

> Event `event:costs-2`: The company incurred expenses for environmental measures in the surrounding municipalities. Quote (part 14): "Dabei sind mehrere Sondereffekte zu berücksichtigen: Einerseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio., andererseits Buchwertabgänge von insgesamt € 55,9 Mio. aufgrund der Nichtrealisierung des Projektes 3. Piste."

## Operating performance

Passengers rose by 2.8% to 32.6m, with traffic growth of 2.8% against 7.3% in FY2024.
Aeronautical revenue per passenger increased by 3.1% to EUR 16.05, helped by charge adjustments under the price-cap formula and dampened by higher temporary winter incentives.
Personnel expenses rose on collective wage increases and additions to personnel provisions, partly related to underutilisation, and the loss of control over the Get2 subsidiary removed it from full consolidation.

> Event `event:regulation_and_tariffs`: Passenger-related charges increased due to passenger growth and charge adjustments, while higher temporary incentives in the winter schedule had a dampening effect. Quote (part 10): "Die passagierbezogenen Entgelte legten in Folge der robusten Passagierentwicklung (+2,6%) sowie von Ent-geltanpassungen um 5.1% auf € 390,2 Mio. zu (2024: € 371,3 Mio.). Dämpfend wirkten im Vergleich zur Vorperiode höhere temporäre Incentives im Winterflugplan zu Beginn des Jahres."

> Event `event:costs`: Personnel expenses rose due to collective agreement increases and additions to personnel provisions, partly related to underutilisation. Quote (part 10): "Der Anstieg des Personalaufwands um € 11,2 Mio. auf € 66,1 Mio. ist auf kollektivvertragliche Erhöhungen (ab 1.5.2025 +3,3%) und Dotierungen von Personalrückstellungen unter anderem im Zusammenhang mit Unterauslastung zurückzuführen."

> Event `event:acquisitions_and_disposals`: Contractual changes led to loss of control over the GetService subsidiary, which is no longer fully consolidated but accounted for using the equity method. Quote (part 14): "Ein Sondereffekt im Periodenvergleich ergibt sich aus dem Verlust der Beherrschung über die Tochtergesellschaft „GetService“ Flughafen-Sicherheits- und Servicedienst GmbH (Get2) durch vertragliche Anpassungen. Seit dem 1. Jänner 2025 wird diese Gesellschaft nicht mehr voll konsolidiert, sondern nach der at-Equity-Methode bilanziert."

## Liquidity and funding

Cash liquidity to revenue declined by 12.3 points to 41.6%, as the capital programme absorbed cash.
The cash position covers the group's debt several times over, so refinancing needs are limited and the liquidity profile rests on the cash balance rather than on committed lines.

> removed by the verifier (still broke a rule after two retries): "Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, a buffer that still stands well above the group's small debt stock." ('above' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Peer positioning

Flughafen Wien has the lowest net leverage of the airport group (1st of 3), against a peer median of 1.46x, and the lowest gross leverage (1st of 3).
Cash liquidity to revenue is the strongest of the group (1st of 3), above the peer median of 32.6%.
The EBITDA margin sits in the middle of the group, in line with the peer median of 36.5%.

## Watch items

- Cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex rose by 59.9% to EUR 272m.
- Investment: capex intensity rose by 8.0 points to 24.1%, above the peer median of 18.2%.
- Margins: the EBITDA margin narrowed by 5.5 points to 36.5%, with write-offs on the abandoned third runway project and environmental payments to neighbouring municipalities among the special items.
- Liquidity: cash and cash-like investments fell by 17.2% to EUR 470m, taking cash liquidity to revenue down by 12.3 points to 41.6%.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

> Event `event:costs-2`: The company incurred expenses for environmental measures in the surrounding municipalities. Quote (part 14): "Dabei sind mehrere Sondereffekte zu berücksichtigen: Einerseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio., andererseits Buchwertabgänge von insgesamt € 55,9 Mio. aufgrund der Nichtrealisierung des Projektes 3. Piste."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 13,144 / 2,885 |
| 2 | snapshot, liquidity_funding | 2 errors | 14,035 / 746 |
| 3 | snapshot, liquidity_funding | 1 errors | 13,746 / 783 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'fell' needs a 'down' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 1: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 1: total_debt@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: net_cash@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: finance_costs@FY2025 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: ebitda@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule 4] snapshot, sentence 1: 'declined' needs a 'down' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 1: 'exceeds' needs a 'up' or 'above_peers' claim on a figure in the same clause

Try 3:

- [rule 4] liquidity_funding, sentence 1: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport group, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, but EBITDA fell by {{ebitda.change@FY2025}} as write-offs on the abandoned third runway project and higher personnel costs weighed on the result.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, and net leverage moved to net cash of {{net_cash@FY2025}} from {{net_cash@FY2024}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex rose by {{capex.change@FY2025}} to {{capex@FY2025}}, leaving cash liquidity to revenue at {{cash_liquidity_to_revenue@FY2025}}.

`credit_metrics`

- EBITDA fell by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}}, with the write-offs on the third runway project and environmental measures in the neighbouring municipalities among the special items.
- Operating profit declined by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} as depreciation, amortisation and impairment eased by {{dda.change@FY2025}} to {{dda@FY2025}}.
- Total debt was stable at {{total_debt@FY2025}}, so gross leverage held at {{gross_leverage@FY2025}} and the group kept net cash of {{net_cash@FY2025}}, down by {{net_cash.change@FY2025}}.
- Cash generation weakened: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}} and cash from operations by {{cfo.change@FY2025}} to {{cfo@FY2025}}, while capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Finance costs rose by {{finance_costs.change@FY2025}} to {{finance_costs@FY2025}}, a small charge against an EBITDA of {{ebitda@FY2025}} given the minimal debt stock.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, with traffic growth of {{traffic_growth@FY2025}} against {{traffic_growth@FY2024}} in FY2024.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2025}} to {{aero_revenue_per_passenger@FY2025}}, helped by charge adjustments under the price-cap formula and dampened by higher temporary winter incentives.
- Personnel expenses rose on collective wage increases and additions to personnel provisions, partly related to underutilisation, and the loss of control over the Get2 subsidiary removed it from full consolidation.

`liquidity_funding`

- Cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, as the capital programme absorbed cash.
- The cash position covers the group's debt several times over, so refinancing needs are limited and the liquidity profile rests on the cash balance rather than on committed lines.

`peer_positioning`

- Flughafen Wien has the lowest net leverage of the airport group ({{net_leverage.peer_rank@FY2025}}), against a peer median of {{net_leverage.peer_median@FY2025}}, and the lowest gross leverage ({{gross_leverage.peer_rank@FY2025}}).
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), above the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- The EBITDA margin sits in the middle of the group, in line with the peer median of {{ebitda_margin.peer_median@FY2025}}.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex rose by {{capex.change@FY2025}} to {{capex@FY2025}}.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@FY2025}}.
- Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, with write-offs on the abandoned third runway project and environmental payments to neighbouring municipalities among the special items.
- Liquidity: cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
