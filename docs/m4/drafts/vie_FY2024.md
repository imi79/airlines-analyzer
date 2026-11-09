# Flughafen Wien, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v7`, fact sheet `45e8063a379c` ([fact sheet](../factsheets/vie_FY2024.md)). Tokens: 27,754 in, 4,049 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Flughafen Wien, the Vienna airport group, closed FY2024 with revenue up 13.0% to EUR 1.1bn and EBITDA up 12.3% to EUR 442m, while the complete repayment of interest-bearing financial liabilities left the balance sheet in net cash.
Net leverage fell by 0.24x to -1.16x, a net cash position, with the EBITDA margin broadly unchanged at 42.0%.
The point to watch is capital spending: capex intensity rose by 5.6 points to 16.1% and free cash flow fell by 4.6% to EUR 274m.

> Event `event:funding_and_rating`: The report states that the complete elimination of interest-bearing financial liabilities has greatly reduced the potential effects of interest rate changes on the company. Quote (part 24): "Der vollständige Abbau zinstragender Finanzverbindlichkeiten hat die potenziellen Auswirkungen einer Zinsänderung auf die FWAG massiv reduziert."

## Credit metrics

EBITDA increased by 12.3% to EUR 442m on revenue up 13.0% to EUR 1.1bn, and operating profit rose by 16.9% to EUR 306m as depreciation rose by 3.1% to EUR 136m.
Total debt was stable at EUR 55.6m, so gross leverage held at 0.13x and net cash rose by 41.4% to EUR 512m.
Cash generation improved: FFO rose by 3.4% to EUR 358m and cash from operations by 15.3% to EUR 444m, while finance costs fell by 76.3% to EUR 2.8m.
Free cash flow declined by 4.6% to EUR 274m as capex rose by 73.6% to EUR 170m.

## Operating performance

Passengers rose by 7.3% to 31.7m, although traffic growth of 7.3% was below the prior year's 24.7%.
Aeronautical revenue per passenger increased by 7.6% to EUR 15.57, supported by the temporary inflation-linked adjustment of airport charges.

> Event `event:regulation_and_tariffs`: Airport charges at Vienna Airport are temporarily adjusted by average inflation under the amended airport charges act, with this rule ending at the end of 2026. Quote (part 9): "Die Flughafenentgelte am Flughafen Wien werden gemäß § 17a FEG vorübergehend um die durchschnittliche Inflation (gerechnet von 1.8. bis 31.7.) angepasst. Diese Regelung endet mit 31. Dezember 2026, wodurch die Flughäfen im Entgeltantrag 2026 zur bestehenden Formel zurückkehren und diese mit 1. Jänner 2027 wieder anwenden."

## Liquidity and funding

Cash and cash-like investments rose by 36.0% to EUR 567m, taking cash liquidity to revenue up by 9.1 points to 53.9%.
The complete repayment of interest-bearing financial liabilities has greatly reduced the potential effects of interest rate changes on the group, leaving the cash balance unencumbered by debt service.
A financing commitment was given for the City Air Terminal joint venture's new train sets, part of which was drawn as a loan in the year.

> Event `event:funding_and_rating`: The report states that the complete elimination of interest-bearing financial liabilities has greatly reduced the potential effects of interest rate changes on the company. Quote (part 24): "Der vollständige Abbau zinstragender Finanzverbindlichkeiten hat die potenziellen Auswirkungen einer Zinsänderung auf die FWAG massiv reduziert."

> Event `event:funding_and_rating-2`: A financing commitment was given for the joint venture City Air Terminal for the procurement of new train sets, part of which was drawn as a loan in the reporting year. Quote (part 77): "Es gibt für das Gemeinschaftsunternehmen City Air Terminal Betriebsgesellschaft m.b.H. eine Finanzierungszusage für die Beschaffung neuer Zuggarnituren in Höhe von rund € 30,0 Mio., im laufenden Geschäftsjahr wurden davon T€ 1.002,0 als Darlehen in Anspruch genommen."

## Peer positioning

Flughafen Wien has the lowest net leverage of the airport group (1st of 3), at -1.16x against a peer median of 1.57x, and the lowest gross leverage (1st of 3).
Cash liquidity to revenue is the strongest of the group (1st of 3), against a peer median of 34.0%.
The EBITDA margin sits in the middle of the group at 42.0%, as does capex intensity at 16.1%, while traffic growth is the weakest of the group (2nd of 2).

## Watch items

- Investment: capex intensity rose by 5.6 points to 16.1%, in line with the peer median, and free cash flow fell by 4.6% to EUR 274m as capital spending absorbed more cash.
- Traffic: traffic growth of 7.3% was below the peer median of 8.3% and the weakest of the group (2nd of 2).
- Regulation: airport charges are temporarily adjusted by average inflation, a rule that ends at the end of 2026, so aeronautical revenue per passenger of EUR 15.57 depends on the tariff framework that follows.
- Litigation: disputes with the Maltese government and employee claims concerning Malta International Airport remain outstanding, which the group considers unfounded.

> Event `event:regulation_and_tariffs`: Airport charges at Vienna Airport are temporarily adjusted by average inflation under the amended airport charges act, with this rule ending at the end of 2026. Quote (part 9): "Die Flughafenentgelte am Flughafen Wien werden gemäß § 17a FEG vorübergehend um die durchschnittliche Inflation (gerechnet von 1.8. bis 31.7.) angepasst. Diese Regelung endet mit 31. Dezember 2026, wodurch die Flughäfen im Entgeltantrag 2026 zur bestehenden Formel zurückkehren und diese mit 1. Jänner 2027 wieder anwenden."

> Event `event:other`: At the balance sheet date there were disputes with the Maltese government and claims by individual employees concerning Malta International Airport, which the group considers unfounded. Quote (part 77): "Zum Bilanzstichtag bestanden betreffend Malta International Airport p.l.c. Streitigkeiten mit der maltesischen Regierung (Streitwert: rund € 8,3 Mio., VJ: rund € 7,5 Mio.) sowie Forderungen einzelner Arbeitnehmer. Aus Sicht des FWAG-Konzerns sind sämtliche Ansprüche unbegründet."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 13,185 / 2,816 |
| 2 | liquidity_funding, peer_positioning, watch_items | passed | 14,569 / 1,233 |

### Errors found, by try

Try 1:

- [rule style] liquidity_funding, sentence 2: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: net_cash@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: cash_liquidity_to_revenue@FY2024 is already given in liquidity_funding, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: traffic_growth@FY2024 is already given in operating_performance, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Flughafen Wien, the Vienna airport group, closed FY2024 with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}} and EBITDA up {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, while the complete repayment of interest-bearing financial liabilities left the balance sheet in net cash.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, a net cash position, with the EBITDA margin broadly unchanged at {{ebitda_margin@FY2024}}.
- The point to watch is capital spending: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}} and free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}, and operating profit rose by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation rose by {{dda.change@FY2024}} to {{dda@FY2024}}.
- Total debt was stable at {{total_debt@FY2024}}, so gross leverage held at {{gross_leverage@FY2024}} and net cash rose by {{net_cash.change@FY2024}} to {{net_cash@FY2024}}.
- Cash generation improved: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}} and cash from operations by {{cfo.change@FY2024}} to {{cfo@FY2024}}, while finance costs fell by {{finance_costs.change@FY2024}} to {{finance_costs@FY2024}}.
- Free cash flow declined by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex rose by {{capex.change@FY2024}} to {{capex@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, although traffic growth of {{traffic_growth@FY2024}} was below the prior year's {{traffic_growth@FY2023}}.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}, supported by the temporary inflation-linked adjustment of airport charges.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue up by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- The complete repayment of interest-bearing financial liabilities has greatly reduced the potential effects of interest rate changes on the group, leaving the cash balance unencumbered by debt service.
- A financing commitment was given for the City Air Terminal joint venture's new train sets, part of which was drawn as a loan in the year.

`peer_positioning`

- Flughafen Wien has the lowest net leverage of the airport group ({{net_leverage.peer_rank@FY2024}}), at {{net_leverage@FY2024}} against a peer median of {{net_leverage.peer_median@FY2024}}, and the lowest gross leverage ({{gross_leverage.peer_rank@FY2024}}).
- Cash liquidity to revenue is the strongest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), against a peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.
- The EBITDA margin sits in the middle of the group at {{ebitda_margin@FY2024}}, as does capex intensity at {{capex_intensity@FY2024}}, while traffic growth is the weakest of the group ({{traffic_growth.peer_rank@FY2024}}).

`watch_items`

- Investment: capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, in line with the peer median, and free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capital spending absorbed more cash.
- Traffic: traffic growth of {{traffic_growth@FY2024}} was below the peer median of {{traffic_growth.peer_median@FY2024}} and the weakest of the group ({{traffic_growth.peer_rank@FY2024}}).
- Regulation: airport charges are temporarily adjusted by average inflation, a rule that ends at the end of 2026, so aeronautical revenue per passenger of {{aero_revenue_per_passenger@FY2024}} depends on the tariff framework that follows.
- Litigation: disputes with the Maltese government and employee claims concerning Malta International Airport remain outstanding, which the group considers unfounded.
