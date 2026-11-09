# Flughafen Wien, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `efe2c9281df2` ([fact sheet](../factsheets/vie_FY2025.md)). Tokens: 41,515 in, 5,997 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport group, grew revenue by 7.2% to EUR 1.1bn in FY2025, but the year carried one-off write-offs from the abandoned third runway project and the deconsolidation of the Get2 security subsidiary.
The EBITDA margin narrowed by 5.5 points to 36.5%, and net leverage moved to net cash of EUR 414m from EUR 512m in FY2024.
The point to watch is cash generation: free cash flow fell by 77.5% to EUR 61.7m as capex intensity rose by 8.0 points to 24.1%, above the peer median.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

> Event `event:acquisitions_and_disposals`: Contractual changes led to loss of control over the GetService subsidiary, which is no longer fully consolidated but accounted for using the equity method. Quote (part 14): "Ein Sondereffekt im Periodenvergleich ergibt sich aus dem Verlust der Beherrschung über die Tochtergesellschaft „GetService“ Flughafen-Sicherheits- und Servicedienst GmbH (Get2) durch vertragliche Anpassungen. Seit dem 1. Jänner 2025 wird diese Gesellschaft nicht mehr voll konsolidiert, sondern nach der at-Equity-Methode bilanziert."

## Credit metrics

EBITDA declined by 6.7% to EUR 412m on revenue up 7.2%, with operating profit down 8.7% to EUR 280m after the write-offs on the third runway project.
Total debt was stable at EUR 55.9m, so gross leverage held at 0.14x and the group retains net cash of EUR 414m, down 19.1% as cash was spent on the investment programme.
Cash generation weakened: FFO fell by 31.0% to EUR 247m and free cash flow by 77.5% to EUR 61.7m, with capex intensity up 8.0 points to 24.1%.

> Event `event:one_offs`: The company recorded write-offs of carrying amounts because the third runway project was not realised. Quote (part 10): "Dabei waren mehrere Sondereffekte zu berücksichtigen: Einerseits Buchwertabgänge von insgesamt € 55,9 Mio. betreffend die Nichtrealisierung des Projektes 3. Piste, andererseits Aufwendungen für Umweltmaßnahmen in den Umlandgemeinden in Höhe von € 6,5 Mio."

## Operating performance

Passengers rose by 2.8% to 32.6m, a slower rate than the 7.3% traffic growth of FY2024, with traffic growth of 2.8% in FY2025.
Aeronautical revenue per passenger increased by 3.1% to EUR 16.05, supported by charge adjustments under the price-cap formula and partly offset by higher temporary winter incentives.
Personnel expenses rose on collective wage increases and additions to personnel provisions, which weighed on the cost base.

> Event `event:regulation_and_tariffs`: Passenger-related charges increased due to passenger growth and charge adjustments, while higher temporary incentives in the winter schedule had a dampening effect. Quote (part 10): "Die passagierbezogenen Entgelte legten in Folge der robusten Passagierentwicklung (+2,6%) sowie von Ent-geltanpassungen um 5.1% auf € 390,2 Mio. zu (2024: € 371,3 Mio.). Dämpfend wirkten im Vergleich zur Vorperiode höhere temporäre Incentives im Winterflugplan zu Beginn des Jahres."

> Event `event:costs`: Personnel expenses rose due to collective agreement increases and additions to personnel provisions, partly related to underutilisation. Quote (part 10): "Der Anstieg des Personalaufwands um € 11,2 Mio. auf € 66,1 Mio. ist auf kollektivvertragliche Erhöhungen (ab 1.5.2025 +3,3%) und Dotierungen von Personalrückstellungen unter anderem im Zusammenhang mit Unterauslastung zurückzuführen."

## Liquidity and funding

Cash liquidity to revenue declined by 12.3 points to 41.6%, a buffer that remains above the airport peer median of 32.6%.
Funding needs are modest given the group's very low gross leverage, so the investment programme is largely met from internal cash rather than new borrowing.

> removed by the verifier (still broke a rule after two retries): "Cash and cash-like investments fell by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, still comfortably above the group's total debt of {{total_debt@FY2025}}." ('above' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Peer positioning

Flughafen Wien has the lowest net leverage of the airport group (1st of 3), at -1.00x against a peer median of 1.46x, and the lowest gross leverage (1st of 3).
Cash liquidity to revenue is the strongest of the group (1st of 3), while the EBITDA margin sits in the middle of the group at 36.5%.
Capex intensity is above the peer median of 18.2%, the main offset to the balance-sheet strength.

## Watch items

- Cash generation: free cash flow fell by 77.5% to EUR 61.7m and FFO by 31.0% to EUR 247m, so the investment programme absorbs most of the cash the group generates.
- Investment: capex intensity rose by 8.0 points to 24.1%, above the peer median of 18.2%, which keeps pressure on free cash flow.
- Liquidity: cash liquidity to revenue fell by 12.3 points to 41.6% as cash and cash-like investments declined by 17.2% to EUR 470m.

> removed by the verifier (still broke a rule after two retries): "Costs: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}} as personnel expenses rose on collective wage increases and provisions, and the abandoned third runway project left write-offs in the result." ('rose' needs a 'up' claim on a figure in the same clause; 'increases' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 10 errors | 12,580 / 2,712 |
| 2 | operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 14,575 / 1,638 |
| 3 | operating_performance, liquidity_funding, peer_positioning, watch_items | 4 errors | 14,360 / 1,647 |

### Errors found, by try

Try 1:

- [rule 4] operating_performance, sentence 1: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 1: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 1: total_debt@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 3] peer_positioning, sentence 1: 'better' claimed on net_leverage@FY2025, but it is worse
- [rule 5] peer_positioning, sentence 2: ebitda_margin.peer_median@FY2025 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'increases' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] operating_performance, sentence 1: 'growth' needs a 'up' claim on a figure in the same clause
- [rule style] operating_performance, sentence 3: revenue.change@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] liquidity_funding, sentence 1: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 5] peer_positioning, sentence 2: ebitda_margin.peer_median@FY2025 is listed in the form but not used in the text
- [rule 4] watch_items, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'increases' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] liquidity_funding, sentence 1: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] liquidity_funding, sentence 1: total_debt@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'rose' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'increases' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport group, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, but the year carried one-off write-offs from the abandoned third runway project and the deconsolidation of the Get2 security subsidiary.
- The EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, and net leverage moved to net cash of {{net_cash@FY2025}} from {{net_cash@FY2024}} in FY2024.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median.

`credit_metrics`

- EBITDA declined by {{ebitda.change@FY2025}} to {{ebitda@FY2025}} on revenue up {{revenue.change@FY2025}}, with operating profit down {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}} after the write-offs on the third runway project.
- Total debt was stable at {{total_debt@FY2025}}, so gross leverage held at {{gross_leverage@FY2025}} and the group retains net cash of {{net_cash@FY2025}}, down {{net_cash.change@FY2025}} as cash was spent on the investment programme.
- Cash generation weakened: FFO fell by {{ffo.change@FY2025}} to {{ffo@FY2025}} and free cash flow by {{fcf.change@FY2025}} to {{fcf@FY2025}}, with capex intensity up {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2025}} to {{passengers@FY2025}}, a slower rate than the {{traffic_growth@FY2024}} traffic growth of FY2024, with traffic growth of {{traffic_growth@FY2025}} in FY2025.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2025}} to {{aero_revenue_per_passenger@FY2025}}, supported by charge adjustments under the price-cap formula and partly offset by higher temporary winter incentives.
- Personnel expenses rose on collective wage increases and additions to personnel provisions, which weighed on the cost base.

`liquidity_funding`

- Cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, a buffer that remains above the airport peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- Funding needs are modest given the group's very low gross leverage, so the investment programme is largely met from internal cash rather than new borrowing.

`peer_positioning`

- Flughafen Wien has the lowest net leverage of the airport group ({{net_leverage.peer_rank@FY2025}}), at {{net_leverage@FY2025}} against a peer median of {{net_leverage.peer_median@FY2025}}, and the lowest gross leverage ({{gross_leverage.peer_rank@FY2025}}).
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}), while the EBITDA margin sits in the middle of the group at {{ebitda_margin.peer_median@FY2025}}.
- Capex intensity is above the peer median of {{capex_intensity.peer_median@FY2025}}, the main offset to the balance-sheet strength.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FFO by {{ffo.change@FY2025}} to {{ffo@FY2025}}, so the investment programme absorbs most of the cash the group generates.
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@FY2025}}, which keeps pressure on free cash flow.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} as cash and cash-like investments declined by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}.
