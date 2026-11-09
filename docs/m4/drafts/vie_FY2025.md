# Flughafen Wien, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `bf1ca38a3039` ([fact sheet](../factsheets/vie_FY2025.md)). Tokens: 37,698 in, 4,815 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport group, reported revenue up 7.2% to EUR 1.1bn in FY2025, a year in which the third runway project was abandoned and carrying amounts were written off.
The EBITDA margin fell by 5.5 points to 36.5%, with EBITDA down 6.7% to EUR 412m.
The point to watch is cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex intensity rose by 8.0 points to 24.1%, above the peer median.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

## Credit metrics

Total debt was stable at EUR 55.9m, so gross leverage held at 0.14x, a change of 0.01x.
FFO fell by 31.0% to EUR 247m, and free cash flow dropped by 77.5% to EUR 61.7m as capital spending absorbed more of the cash generated.
Capex intensity increased by 8.0 points to 24.1%, against 16.1% in FY2024.

> removed by the verifier (still broke a rule after two retries): "EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} and operating profit by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}, with write-offs on the abandoned third runway project and higher personnel expenses under collective wage agreements weighing on the result." ('higher' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Operating performance

Passengers rose by 2.8% to 32.6m, although traffic growth slowed by 4.5 points to 2.8% from 7.3% in FY2024.
Aeronautical revenue per passenger increased by 3.1% to EUR 16.05, helped by charge adjustments under the price-cap formula.
The loss of control over the Get2 security subsidiary means it is no longer fully consolidated, which affects the comparability of the group's cost base.

> Event `event:regulation_and_tariffs`: Passenger-related charges increased due to passenger growth and charge adjustments, while higher temporary incentives in the winter schedule had a dampening effect. Quote (part 10): "Die passagierbezogenen Entgelte legten in Folge der robusten Passagierentwicklung (+2,6%) sowie von Ent-geltanpassungen um 5.1% auf € 390,2 Mio. zu (2024: € 371,3 Mio.). Dämpfend wirkten im Vergleich zur Vorperiode höhere temporäre Incentives im Winterflugplan zu Beginn des Jahres."

> Event `event:acquisitions_and_disposals`: Contractual changes led to loss of control over the GetService subsidiary, which is no longer fully consolidated but accounted for using the equity method. Quote (part 14): "Ein Sondereffekt im Periodenvergleich ergibt sich aus dem Verlust der Beherrschung über die Tochtergesellschaft „GetService“ Flughafen-Sicherheits- und Servicedienst GmbH (Get2) durch vertragliche Anpassungen. Seit dem 1. Jänner 2025 wird diese Gesellschaft nicht mehr voll konsolidiert, sondern nach der at-Equity-Methode bilanziert."

## Liquidity and funding

The group's cash and committed facilities are not disclosed in the fact base for FY2025, so the liquidity buffer cannot be sized against revenue.
Customer prepayments are not disclosed for FY2025 either, so the share of the cash position that reflects advance ticket sales cannot be assessed.

## Peer positioning

Gross leverage is the lowest of the airport peers (1st of 3), well below the peer median of 2.00x.
The EBITDA margin of 36.5% places the company in the middle of the group (2nd of 3).
Capex intensity is above the peer median of 18.2%, the least favourable relative position in the comparison.

## Watch items

- Cash generation: free cash flow fell by 77.5% to EUR 61.7m and FFO by 31.0% to EUR 247m, so the buffer against the investment programme has narrowed.
- Investment: capex intensity rose by 8.0 points to 24.1%, above the peer median of 18.2%.
- Margins: the EBITDA margin fell by 5.5 points to 36.5%, with write-offs on the abandoned third runway project and personnel expenses rising under collective wage agreements in the base.
- Traffic: traffic growth slowed by 4.5 points to 2.8%, which limits the operating leverage behind the charge adjustments.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

> Event `event:costs`: Personnel expenses rose due to collective agreement increases and additions to personnel provisions, partly related to underutilisation. Quote (part 10): "Der Anstieg des Personalaufwands um € 11,2 Mio. auf € 66,1 Mio. ist auf kollektivvertragliche Erhöhungen (ab 1.5.2025 +3,3%) und Dotierungen von Personalrückstellungen unter anderem im Zusammenhang mit Unterauslastung zurückzuführen."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 11 errors | 11,747 / 2,462 |
| 2 | credit_metrics, liquidity_funding, peer_positioning, watch_items | 2 errors | 13,719 / 1,469 |
| 3 | credit_metrics, peer_positioning | 1 errors | 12,232 / 884 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 1: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 1: total_debt@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 1: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: fcf@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] peer_positioning, sentence 1: 'better' claimed on gross_leverage@FY2025, but it is neither better nor worse
- [rule style] peer_positioning, sentence 1: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] peer_positioning, sentence 3: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'increases' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 1: 'rising' needs a 'up' claim on a figure in the same clause
- [rule 4] peer_positioning, sentence 3: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause

Try 3:

- [rule 4] credit_metrics, sentence 1: 'higher' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport group, reported revenue up {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, a year in which the third runway project was abandoned and carrying amounts were written off.
- The EBITDA margin fell by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, with EBITDA down {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median.

`credit_metrics`

- Total debt was stable at {{total_debt@FY2025}}, so gross leverage held at {{gross_leverage@FY2025}}, a change of {{gross_leverage.change@FY2025}}.
- FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}}, and free cash flow dropped by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capital spending absorbed more of the cash generated.
- Capex intensity increased by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, against {{capex_intensity@FY2024}} in FY2024.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, although traffic growth slowed by {{traffic_growth.change@FY2025}} to {{traffic_growth@FY2025}} from {{traffic_growth@FY2024}} in FY2024.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2025}} to {{aero_revenue_per_passenger@FY2025}}, helped by charge adjustments under the price-cap formula.
- The loss of control over the Get2 security subsidiary means it is no longer fully consolidated, which affects the comparability of the group's cost base.

`liquidity_funding`

- The group's cash and committed facilities are not disclosed in the fact base for FY2025, so the liquidity buffer cannot be sized against revenue.
- Customer prepayments are not disclosed for FY2025 either, so the share of the cash position that reflects advance ticket sales cannot be assessed.

`peer_positioning`

- Gross leverage is the lowest of the airport peers ({{gross_leverage.peer_rank@FY2025}}), well below the peer median of {{gross_leverage.peer_median@FY2025}}.
- The EBITDA margin of {{ebitda_margin@FY2025}} places the company in the middle of the group ({{ebitda_margin.peer_rank@FY2025}}).
- Capex intensity is above the peer median of {{capex_intensity.peer_median@FY2025}}, the least favourable relative position in the comparison.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FFO by {{ffo.change@FY2025}} to {{ffo@FY2025}}, so the buffer against the investment programme has narrowed.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@FY2025}}.
- Margins: the EBITDA margin fell by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, with write-offs on the abandoned third runway project and personnel expenses rising under collective wage agreements in the base.
- Traffic: traffic growth slowed by {{traffic_growth.change@FY2025}} to {{traffic_growth@FY2025}}, which limits the operating leverage behind the charge adjustments.
