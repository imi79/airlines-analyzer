# Aena, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `22912fc68e11` ([fact sheet](../factsheets/aena_FY2024.md)). Tokens: 41,223 in, 6,921 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, ended FY2024 with revenue up 14.4% to EUR 5.8bn and EBITDA up 16.1% to EUR 3.5bn, while Fitch upgraded its long-term rating and Moody's moved its outlook to positive.
Net leverage fell by 0.49x to 1.57x, helped by total debt down 14.8% to EUR 7.3bn.
The point to watch is liquidity: cash liquidity to revenue fell by 15.3 points to 31.6% as cash and cash-like investments declined by 22.9% to EUR 1.8bn.

> Event `event:funding_and_rating`: Fitch raised Aena's long-term issuer and EMTN programme rating and its short-term rating, keeping the outlook stable. Quote (page 52): "El 7 de mayo, Fitch Ratings mejoró la calificación de largo plazo y del programa EMTN a “A” desde “A-“, así como la calificación a corto plazo a “F1” desde “F2”, manteniendo la perspectiva estable."

> Event `event:funding_and_rating-2`: Moody's changed Aena's outlook to positive from stable and confirmed the long-term rating and the EMTN programme rating. Quote (page 164): "El 19 de marzo, la agencia de rating Moody’s mejoró la perspectiva de Aena S.M.E., S.A. a positiva desde estable y confirmó la calificación de largo plazo “A3” y del programa EMTN."

## Credit metrics

EBITDA rose by 16.1% to EUR 3.5bn and operating profit by 20.9% to EUR 2.7bn, lifting the EBITDA margin by 0.9 points to 60.9%.
Gross leverage fell by 0.76x to 2.08x and net debt was reduced by 11.6% to EUR 5.5bn.
Cash generation strengthened: FFO rose by 20.3% to EUR 2.9bn, taking FFO to debt up by 11.3 points to 39.0%, and free cash flow rose by 129.9% to EUR 1.9bn.
FCF to debt rose by 16.6 points to 26.3%, while interest coverage eased by 0.27x to 12.34x.
Capex intensity fell by 13.1 points to 14.3%, which supported free cash flow of EUR 1.9bn.

## Operating performance

Passengers rose by 9.2% to 309.3m, although traffic growth slowed by 7.0 points to 9.2%.
Aeronautical revenue per passenger rose by 4.1% to EUR 10.18, while the CNMC set the maximum adjusted annual revenue per passenger for 2025 at the prior year's level.
The result for the year includes the disposal of ADI's stake in ESSP SAS, and the Cartagena concession ended during the year.

> Event `event:regulation_and_tariffs`: The CNMC issued its supervision resolution on airport tariffs for 2025, stating the applicable maximum adjusted annual revenue per passenger and that it stays unchanged versus the prior year. Quote (page 164): "En relación con el Documento de Regulación Aeroportuaria para el período 2022-2026 (DORA II), el 28 de noviembre de 2024, la CNMC emitió su resolución de supervisión de las tarifas aeroportuarias para 2025, declarando que el ingreso máximo anual ajustado por pasajero (IMAAJ) aplicable es de 10,35 euros, lo que supone una variación del 0% respecto a"

> Event `event:acquisitions_and_disposals`: The result for the year includes the gain on the sale of ADI's stake in European Satellite Services Provider SAS. Quote (page 193): "concesión en Brasil (23,2 millones de euros) así como, el resultado por la venta de la participación de ADI en la sociedad European Satellite Services Provider SAS (ESSP SAS) (8,6 millones de euros)."

> Event `event:acquisitions_and_disposals-2`: The concession of the Rafael Núñez International Airport in Cartagena de Indias, managed through SACSA, ended. Quote (page 189): "En relación con SACSA, según se indica en el apartado 2.2.2 (Sociedades asociadas y con control conjunto) el 29 febrero de 2024 finalizó la concesión del Aeropuerto Internacional Rafael Núñez (Cartagena de Indias-Colombia) gestionada a través de esta Sociedad."

## Liquidity and funding

Cash and cash-like investments fell by 22.9% to EUR 1.8bn, and cash liquidity declined by 22.9% to EUR 1.8bn.
In FY2023 liquidity was EUR 4.9bn, including EUR 2.6bn of undrawn committed credit facilities, and liquidity to revenue was 97.6%.
Funding conditions improved during the year, with Fitch upgrading Aena's long-term and short-term ratings and Moody's moving the outlook to positive.

> Event `event:funding_and_rating`: Fitch raised Aena's long-term issuer and EMTN programme rating and its short-term rating, keeping the outlook stable. Quote (page 52): "El 7 de mayo, Fitch Ratings mejoró la calificación de largo plazo y del programa EMTN a “A” desde “A-“, así como la calificación a corto plazo a “F1” desde “F2”, manteniendo la perspectiva estable."

> Event `event:funding_and_rating-2`: Moody's changed Aena's outlook to positive from stable and confirmed the long-term rating and the EMTN programme rating. Quote (page 164): "El 19 de marzo, la agencia de rating Moody’s mejoró la perspectiva de Aena S.M.E., S.A. a positiva desde estable y confirmó la calificación de largo plazo “A3” y del programa EMTN."

## Peer positioning

Aena has the highest EBITDA margin among the airport peers (1st of 3), against a median of 42.0%.
Gross leverage sits in the middle of the group (2nd of 3), with the company itself the median of the peer set at 2.08x.
Cash generation leads the group: FFO to debt ranks 1st of 2 and FCF to debt 1st of 2, against medians of 26.5% and 14.8%.
Interest coverage is the strongest of the group (1st of 2) against a median of 9.65x, and capex intensity is below the peer median of 16.1%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 15.3 points to 31.6% as cash and cash-like investments were drawn down by 22.9%.
- Coverage: interest coverage eased by 0.27x to 12.34x, a weaker move than the rest of the credit profile.
- Traffic: traffic growth slowed by 7.0 points to 9.2%, so the pace of passenger expansion is moderating.

> removed by the verifier (still broke a rule after two retries): "Regulation: the CNMC set the maximum adjusted annual revenue per passenger for 2025 at the prior year's level, which limits tariff-led revenue growth." ('growth' needs a 'up' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 13 errors | 12,354 / 3,180 |
| 2 | credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 15,538 / 2,493 |
| 3 | credit_metrics, watch_items | 1 errors | 13,331 / 1,248 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 5: 'rise' needs a 'up' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 2: 'unchanged' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule 4] operating_performance, sentence 3: 'gain' needs a 'up' claim on a figure in the same clause
- [rule 5] liquidity_funding, sentence 1: cash_liquidity.change@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2024 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 2: gross_leverage.peer_median@FY2024 is listed in the form but not used in the text
- [rule style] peer_positioning, sentence 3: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 4: interest_coverage@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 4: capex_intensity@FY2024 is already given in credit_metrics, sentence 5: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'unchanged' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] credit_metrics, sentence 5: 'increase' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, ended FY2024 with revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}} and EBITDA up {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, while Fitch upgraded its long-term rating and Moody's moved its outlook to positive.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}}, helped by total debt down {{total_debt.change@FY2024}} to {{total_debt@FY2024}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} as cash and cash-like investments declined by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}.

`credit_metrics`

- EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} and operating profit by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}, lifting the EBITDA margin by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Gross leverage fell by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}} and net debt was reduced by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, taking FFO to debt up by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}, and free cash flow rose by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- FCF to debt rose by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, while interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}.
- Capex intensity fell by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, which supported free cash flow of {{fcf@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, although traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}}.
- Aeronautical revenue per passenger rose by {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}, while the CNMC set the maximum adjusted annual revenue per passenger for 2025 at the prior year's level.
- The result for the year includes the disposal of ADI's stake in ESSP SAS, and the Cartagena concession ended during the year.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity declined by {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- In FY2023 liquidity was {{liquidity@FY2023}}, including {{undrawn_facilities@FY2023}} of undrawn committed credit facilities, and liquidity to revenue was {{liquidity_to_revenue@FY2023}}.
- Funding conditions improved during the year, with Fitch upgrading Aena's long-term and short-term ratings and Moody's moving the outlook to positive.

`peer_positioning`

- Aena has the highest EBITDA margin among the airport peers ({{ebitda_margin.peer_rank@FY2024}}), against a median of {{ebitda_margin.peer_median@FY2024}}.
- Gross leverage sits in the middle of the group ({{gross_leverage.peer_rank@FY2024}}), with the company itself the median of the peer set at {{gross_leverage.peer_median@FY2024}}.
- Cash generation leads the group: FFO to debt ranks {{ffo_to_debt.peer_rank@FY2024}} and FCF to debt {{fcf_to_debt.peer_rank@FY2024}}, against medians of {{ffo_to_debt.peer_median@FY2024}} and {{fcf_to_debt.peer_median@FY2024}}.
- Interest coverage is the strongest of the group ({{interest_coverage.peer_rank@FY2024}}) against a median of {{interest_coverage.peer_median@FY2024}}, and capex intensity is below the peer median of {{capex_intensity.peer_median@FY2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} as cash and cash-like investments were drawn down by {{cash_like.change@FY2024}}.
- Coverage: interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, a weaker move than the rest of the credit profile.
- Traffic: traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}}, so the pace of passenger expansion is moderating.
