# Flughafen Wien, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `443b1098442d` ([fact sheet](../factsheets/vie_FY2025.md)). Tokens: 39,869 in, 4,995 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport group, grew revenue by 7.2% to EUR 1.1bn in FY2025, but write-offs on the abandoned third runway project and higher personnel costs weighed on EBITDA.
The EBITDA margin narrowed by 5.5 points to 36.5%, while net leverage moved to net cash of EUR 414m and gross leverage stayed at 0.14x.
The point to watch is cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex intensity rose by 8.0 points to 24.1%, above the peer median.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

> Event `event:costs`: Personnel expenses rose due to collective agreement increases and additions to personnel provisions, partly related to underutilisation. Quote (part 10): "Der Anstieg des Personalaufwands um € 11,2 Mio. auf € 66,1 Mio. ist auf kollektivvertragliche Erhöhungen (ab 1.5.2025 +3,3%) und Dotierungen von Personalrückstellungen unter anderem im Zusammenhang mit Unterauslastung zurückzuführen."

## Credit metrics

EBITDA declined by 6.7% to EUR 412m, and operating profit fell by 8.7% to EUR 280m after depreciation.
Total debt was stable at EUR 55.9m, so gross leverage held at 0.14x and net cash of EUR 414m covers the debt several times over.
FFO fell by 31.0% to EUR 247m, and free cash flow dropped by 77.5% to EUR 61.7m as capex intensity climbed by 8.0 points to 24.1%.
Profit for the year fell by 12.3% to EUR 210m, with the loss of control over the Get2 subsidiary also changing the consolidation scope.

> Event `event:acquisitions_and_disposals`: Contractual changes led to loss of control over the GetService subsidiary, which is no longer fully consolidated but accounted for using the equity method. Quote (part 14): "Ein Sondereffekt im Periodenvergleich ergibt sich aus dem Verlust der Beherrschung über die Tochtergesellschaft „GetService“ Flughafen-Sicherheits- und Servicedienst GmbH (Get2) durch vertragliche Anpassungen. Seit dem 1. Jänner 2025 wird diese Gesellschaft nicht mehr voll konsolidiert, sondern nach der at-Equity-Methode bilanziert."

## Operating performance

Passengers rose by 2.8% to 32.6m, though traffic growth slowed by 4.5 points to 2.8%.
Aeronautical revenue per passenger increased by 3.1% to EUR 16.05, helped by charge adjustments under the price-cap formula.
Costs moved against the top line: personnel expenses rose on collective wage increases and additions to personnel provisions, and the group also booked expenses for environmental measures in the surrounding municipalities.

> Event `event:regulation_and_tariffs`: Passenger-related charges increased due to passenger growth and charge adjustments, while higher temporary incentives in the winter schedule had a dampening effect. Quote (part 10): "Die passagierbezogenen Entgelte legten in Folge der robusten Passagierentwicklung (+2,6%) sowie von Ent-geltanpassungen um 5.1% auf € 390,2 Mio. zu (2024: € 371,3 Mio.). Dämpfend wirkten im Vergleich zur Vorperiode höhere temporäre Incentives im Winterflugplan zu Beginn des Jahres."

> Event `event:costs`: Personnel expenses rose due to collective agreement increases and additions to personnel provisions, partly related to underutilisation. Quote (part 10): "Der Anstieg des Personalaufwands um € 11,2 Mio. auf € 66,1 Mio. ist auf kollektivvertragliche Erhöhungen (ab 1.5.2025 +3,3%) und Dotierungen von Personalrückstellungen unter anderem im Zusammenhang mit Unterauslastung zurückzuführen."

> Event `event:costs-2`: The company incurred expenses for environmental measures in the surrounding municipalities. Quote (part 14): "Dabei sind mehrere Sondereffekte zu berücksichtigen: Einerseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio., andererseits Buchwertabgänge von insgesamt € 55,9 Mio. aufgrund der Nichtrealisierung des Projektes 3. Piste."

## Liquidity and funding

Cash and cash-like investments fell by 17.2% to EUR 470m, so cash liquidity declined by 17.2% to EUR 470m.
Cash liquidity to revenue fell by 12.3 points to 41.6%, still a sizeable buffer against the group's small debt stock.
The group's funding position rests on its own cash rather than drawn facilities, and the loss of control over the Get2 subsidiary changed the consolidation scope from the start of the year.

> Event `event:acquisitions_and_disposals`: Contractual changes led to loss of control over the GetService subsidiary, which is no longer fully consolidated but accounted for using the equity method. Quote (part 14): "Ein Sondereffekt im Periodenvergleich ergibt sich aus dem Verlust der Beherrschung über die Tochtergesellschaft „GetService“ Flughafen-Sicherheits- und Servicedienst GmbH (Get2) durch vertragliche Anpassungen. Seit dem 1. Jänner 2025 wird diese Gesellschaft nicht mehr voll konsolidiert, sondern nach der at-Equity-Methode bilanziert."

## Peer positioning

Flughafen Wien has the lowest net leverage of the airport group (1st of 3), against a peer median of 1.46x, and the lowest gross leverage (1st of 3).
Cash liquidity to revenue is the strongest of the group (1st of 3), well above the peer median of 32.6%.
On profitability the company sits in the middle of the group on EBITDA margin, while capex intensity is above the peer median of 18.2%.

## Watch items

- Cash generation: free cash flow fell by 77.5% to EUR 61.7m and FFO by 31.0% to EUR 247m, so the buffer that funds investment is thinner.
- Investment: capex intensity rose by 8.0 points to 24.1%, above the peer median of 18.2%, which keeps pressure on free cash flow.
- Liquidity: cash liquidity to revenue fell by 12.3 points to 41.6% as cash and cash-like investments were drawn down by 17.2%.

> removed by the verifier (still broke a rule after two retries): "Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, with write-offs on the abandoned third runway project and higher personnel expenses on collective wage increases weighing on the result." ('increases' needs a 'up' claim on a figure in the same clause; 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 12,607 / 2,683 |
| 2 | snapshot, liquidity_funding, peer_positioning, watch_items | 2 errors | 14,460 / 1,720 |
| 3 | watch_items | 2 errors | 12,802 / 592 |

### Errors found, by try

Try 1:

- [rule 4] snapshot, sentence 1: 'lower' needs a 'down' or 'below_peers' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 2: total_debt@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: net_cash@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause

Try 2:

- [rule 4] watch_items, sentence 4: 'rising' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'increases' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 4: 'increases' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport group, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, but write-offs on the abandoned third runway project and higher personnel costs weighed on EBITDA.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, while net leverage moved to net cash of {{net_cash@FY2025}} and gross leverage stayed at {{gross_leverage@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median.

`credit_metrics`

- EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit fell by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} after depreciation.
- Total debt was stable at {{total_debt@FY2025}}, so gross leverage held at {{gross_leverage@FY2025}} and net cash of {{net_cash@FY2025}} covers the debt several times over.
- FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, and free cash flow dropped by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity climbed by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Profit for the year fell by {{profit.change@FY2025}} to {{profit@FY2025}}, with the loss of control over the Get2 subsidiary also changing the consolidation scope.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, though traffic growth slowed by {{traffic_growth.change@FY2025}} to {{traffic_growth@FY2025}}.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2025}} to {{aero_revenue_per_passenger@FY2025}}, helped by charge adjustments under the price-cap formula.
- Costs moved against the top line: personnel expenses rose on collective wage increases and additions to personnel provisions, and the group also booked expenses for environmental measures in the surrounding municipalities.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, so cash liquidity declined by {{cash_liquidity.change@FY2025}} to {{cash_liquidity@FY2025}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, still a sizeable buffer against the group's small debt stock.
- The group's funding position rests on its own cash rather than drawn facilities, and the loss of control over the Get2 subsidiary changed the consolidation scope from the start of the year.

`peer_positioning`

- Flughafen Wien has the lowest net leverage of the airport group ({{net_leverage.peer_rank@FY2025}}), against a peer median of {{net_leverage.peer_median@FY2025}}, and the lowest gross leverage ({{gross_leverage.peer_rank@FY2025}}).
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), well above the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- On profitability the company sits in the middle of the group on EBITDA margin, while capex intensity is above the peer median of {{capex_intensity.peer_median@FY2025}}.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FFO by {{ffo.change@FY2025}} to {{ffo@FY2025}}, so the buffer that funds investment is thinner.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@FY2025}}, which keeps pressure on free cash flow.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} as cash and cash-like investments were drawn down by {{cash_like.change@FY2025}}.
