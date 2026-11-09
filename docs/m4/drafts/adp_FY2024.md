# Groupe ADP, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v7`, fact sheet `cb4254fb604c` ([fact sheet](../factsheets/adp_FY2024.md)). Tokens: 41,612 in, 5,964 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Groupe ADP, the Paris airport operator, grew revenue by 12.1% to EUR 6.2bn in FY2024, while the EBITDA margin narrowed by 2.0 points to 33.7%.
Net leverage was broadly unchanged at 4.13x, as net debt rose by 8.2% to EUR 8.6bn and EBITDA grew by 6.0%.
The point to watch is cash generation: free cash flow fell by 50.3% to EUR 355m as capex rose by 34.1%, and cash liquidity to revenue declined by 10.8 points to 34.0%.

## Credit metrics

EBITDA increased by 6.0% to EUR 2.1bn on revenue up 12.1% to EUR 6.2bn, but operating profit fell by 20.0% to EUR 994m as depreciation, amortisation and impairment were stable at EUR 791m and finance costs declined by 46.6% to EUR 595m.
Total debt rose by 2.7% to EUR 10.7bn and net debt by 8.2% to EUR 8.6bn, so gross leverage eased to 5.14x while net leverage was broadly unchanged at 4.13x.
Interest coverage improved to 6.97x as finance costs declined by 46.6%, and FFO was stable at EUR 1.5bn, leaving FFO to debt broadly unchanged at 14.0%.
Cash from operations declined by 4.0% to EUR 1.5bn while capex rose by 34.1% to EUR 1.2bn, cutting free cash flow by 50.3% to EUR 355m and FCF to debt to 3.3%.

## Operating performance

The Paris airports handled 103.4m passengers in FY2024.
In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond the Paris airports.
Capex intensity rose by 3.1 points to 19.0%, reflecting the investment programme across the airport network.
DIAL filed its tariff proposal for the next regulatory period in May 2024, with final tariffs published in March 2025 and effective from April 2025.

> Event `event:acquisitions_and_disposals`: In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond Paris airports. Quote (page 17): "En octobre 2024, le Groupe ADP a acquis, d’une part, Paris Expérience Group et, d’autre part, P/S, élargissant ainsi l'offre d'Extime au-delà des aéroports parisiens et renforçant ses perspectives de croissance à l'international ;"

> Event `event:regulation_and_tariffs`: DIAL filed its tariff proposal for the upcoming regulatory period, with final tariffs published later and effective in April 2025. Quote (page 86): "DIAL a déposé en mai 2024 sa proposition tarifaire pour la quatrième période de régulation. Les tarifs finaux ont été publiés le 28 mars 2025 et entreront en vigueur le 16 avril 2025, marquant une hausse notable par rapport à la période de régulation précédente et, pour la première fois en Inde, l’introduction d’une structure tarifaire différenciée."

## Liquidity and funding

Cash and cash-like investments fell by 14.8% to EUR 2.1bn, taking cash liquidity to revenue down by 10.8 points to 34.0%.
The group issued a bond in May 2024, whose proceeds are reported among the year's cash flows.
Cash liquidity to revenue of 34.0% leaves a thinner buffer against the debt stock than a year earlier, when it stood at 44.8%.

> Event `event:funding_and_rating`: The report mentions the proceeds of the bond issue among the group's cash flows. Quote (page 530): "Les flux de trésorerie opérationnels s'établissent à 1 524 millions d'euros et les produits de l'émission obligataire du 7 mai 2024 par"

## Peer positioning

Groupe ADP has the weakest EBITDA margin of the airport group (3rd of 3), at 33.7% against a peer median of 42.0%.
Leverage is the weakest in the group on both measures (3rd of 3 on net leverage and 3rd of 3 on gross leverage), against peer medians of 1.57x and 2.08x.
Cash liquidity to revenue sits in the middle of the group (2nd of 3), while capex intensity is above the peer median of 16.1%.

## Watch items

- Cash generation: FCF to debt fell by 3.6 points to 3.3%, below the peer median of 14.8%, as capex intensity rose to 19.0%.
- Leverage: net leverage of 4.13x is above the peer median of 1.57x, and FFO to debt of 14.0% is below the peer median of 26.5%.
- Liquidity: cash liquidity to revenue fell by 10.8 points to 34.0%, with cash and cash-like investments down by 14.8% to EUR 2.1bn.
- Coverage: interest coverage of 6.97x remains below the peer median of 9.65x, and impairment tests on equity-accounted holdings led to a charge in the year.

> Event `event:one_offs`: Impairment tests on equity-accounted holdings and related loans led the group to book an impairment. Quote (page 577): "Les tests menés sur les titres mis en équivalence et les prêts consentis aux sociétés testées ont conclu à la nécessité de constater une dépréciation de 47 millions d’euros."

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 11 errors | 12,741 / 3,194 |
| 2 | credit_metrics, operating_performance, liquidity_funding, peer_positioning | 4 errors | 15,239 / 1,962 |
| 3 | liquidity_funding, peer_positioning | passed | 13,632 / 808 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 3: 'fell' needs a 'down' claim on a figure in the same clause
- [rule style] operating_performance, sentence 2: revenue.change@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 2: revenue@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 2: cfo@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: total_debt.change@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] peer_positioning, sentence 2: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: net_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2024 is already given in operating_performance, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule style] liquidity_funding, sentence 3: total_debt.change@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] liquidity_funding, sentence 3: total_debt@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: capex_intensity@FY2024 is already given in operating_performance, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Groupe ADP, the Paris airport operator, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, while the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Net leverage was broadly unchanged at {{net_leverage@FY2024}}, as net debt rose by {{net_debt.change@FY2024}} to {{net_debt@FY2024}} and EBITDA grew by {{ebitda.change@FY2024}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2024}} to {{fcf@FY2024}} as capex rose by {{capex.change@FY2024}}, and cash liquidity to revenue declined by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}, but operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation, amortisation and impairment were stable at {{dda@FY2024}} and finance costs declined by {{finance_costs.change@FY2024}} to {{finance_costs@FY2024}}.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, so gross leverage eased to {{gross_leverage@FY2024}} while net leverage was broadly unchanged at {{net_leverage@FY2024}}.
- Interest coverage improved to {{interest_coverage@FY2024}} as finance costs declined by {{finance_costs.change@FY2024}}, and FFO was stable at {{ffo@FY2024}}, leaving FFO to debt broadly unchanged at {{ffo_to_debt@FY2024}}.
- Cash from operations declined by {{cfo.change@FY2024}} to {{cfo@FY2024}} while capex rose by {{capex.change@FY2024}} to {{capex@FY2024}}, cutting free cash flow by {{fcf.change@FY2024}} to {{fcf@FY2024}} and FCF to debt to {{fcf_to_debt@FY2024}}.

`operating_performance`

- The Paris airports handled {{passengers@FY2024}} passengers in FY2024.
- In October 2024 the group acquired Paris Experience Group and P/S, extending the Extime offering beyond the Paris airports.
- Capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, reflecting the investment programme across the airport network.
- DIAL filed its tariff proposal for the next regulatory period in May 2024, with final tariffs published in March 2025 and effective from April 2025.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- The group issued a bond in May 2024, whose proceeds are reported among the year's cash flows.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} leaves a thinner buffer against the debt stock than a year earlier, when it stood at {{cash_liquidity_to_revenue@FY2023}}.

`peer_positioning`

- Groupe ADP has the weakest EBITDA margin of the airport group ({{ebitda_margin.peer_rank@FY2024}}), at {{ebitda_margin@FY2024}} against a peer median of {{ebitda_margin.peer_median@FY2024}}.
- Leverage is the weakest in the group on both measures ({{net_leverage.peer_rank@FY2024}} on net leverage and {{gross_leverage.peer_rank@FY2024}} on gross leverage), against peer medians of {{net_leverage.peer_median@FY2024}} and {{gross_leverage.peer_median@FY2024}}.
- Cash liquidity to revenue sits in the middle of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}), while capex intensity is above the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, below the peer median of {{fcf_to_debt.peer_median@FY2024}}, as capex intensity rose to {{capex_intensity@FY2024}}.
- Leverage: net leverage of {{net_leverage@FY2024}} is above the peer median of {{net_leverage.peer_median@FY2024}}, and FFO to debt of {{ffo_to_debt@FY2024}} is below the peer median of {{ffo_to_debt.peer_median@FY2024}}.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, with cash and cash-like investments down by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.
- Coverage: interest coverage of {{interest_coverage@FY2024}} remains below the peer median of {{interest_coverage.peer_median@FY2024}}, and impairment tests on equity-accounted holdings led to a charge in the year.
