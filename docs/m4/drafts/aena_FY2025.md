# Aena, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `29a759dcc1f8` ([fact sheet](../factsheets/aena_FY2025.md)). Tokens: 38,147 in, 4,205 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, grew revenue by 8.9% to EUR 6.3bn in FY2025, and Moody's raised its long-term issuer and senior unsecured ratings during the year.
Net leverage fell by 0.11x to 1.46x, in line with the airport peer median, while the EBITDA margin narrowed by 0.6 points to 60.3%.
The point to watch is cash generation: free cash flow fell by 10.2% to EUR 1.7bn as capex intensity rose by 2.6 points to 16.9%.

> Event `event:funding_and_rating-2`: Moody's raised Aena's long-term issuer and senior unsecured debt ratings. Quote (page 231): "La agencia de calificación crediticia Moody's Investors Service ha mejorado la calificación de emisor a largo plazo y la calificación de deuda senior no garantizada de Aena S.M.E., S.A. a A2 desde A3."

## Credit metrics

EBITDA increased by 7.8% to EUR 3.8bn, and operating profit rose by 12.2% to EUR 3.0bn.
Total debt rose by 3.2% to EUR 7.6bn, but net debt was broadly unchanged at EUR 5.5bn, so gross leverage was stable at 2.00x.
Interest coverage improved by 2.38x to 14.72x, above the peer median.
FFO rose by 4.8% to EUR 3.0bn, lifting FFO to debt by 0.6 points to 39.6%, but FCF to debt fell by 3.4 points to 22.9%.

## Operating performance

In FY2024 the Spanish network carried 309.3m passengers, with traffic growth of 9.2%.
Aeronautical revenue per passenger was EUR 10.18 in FY2024, the base against which the regulator set the average airport charge for 2026 above the prior year's level.
Group revenue rose by 8.9% to EUR 6.3bn, while the EBITDA margin narrowed by 0.6 points to 60.3%, so cost growth outpaced revenue growth.

> Event `event:regulation_and_tariffs`: The competition regulator issued its supervision resolution setting the average airport charge per passenger for the following year, above the prior year's level. Quote (page 180): "En relación con el Documento de Regulación Aeroportuaria para el período 2022-2026 (DORA II), el 13 de noviembre de 2025, la CNMC emitió su resolución de supervisión de las tarifas aeroportuarias para 2026, estableciendo que el IMAAJ para 2026 sea de 11,00 euros por pasajero, lo que supone un incremento del 6,31% respecto al IMAAJ de 2025 (10,35 euros por"

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, and cash liquidity to revenue increased by 1.0 point to 32.6%.
Liquidity stood at EUR 4.3bn, including EUR 2.2bn of undrawn committed credit facilities, equal to 68.4% of revenue.
On the funding side, the Brazilian subsidiary BOAB issued secured debentures maturing in the long term, London Luton airport completed the refinancing of its bank debt, and Fitch affirmed the ratings with a stable long-term outlook.

> Event `event:funding_and_rating`: The Brazilian subsidiary BOAB issued secured, non-convertible debentures maturing in the long term, indexed to IPCA with a fixed coupon payable semi-annually. Quote (page 61): "El 30 de octubre de 2025, la filial BOAB realizó su primera emisión de bonos (debentures simples) por importe de 5.300 millones de BRL, no convertibles, con garantía real, con vencimiento en junio de 2048), indexadas a IPCA y con cupón fijo del 8,74% anual, pagadero semestralmente, siendo el primer pago el 15 de junio de 2026 (Nota 20)."

> Event `event:funding_and_rating-4`: London Luton airport completed the refinancing of its bank debt. Quote (page 216): "En junio de 2025, el Aeropuerto London Luton completó la refinanciación de su deuda bancaria."

> Event `event:funding_and_rating-3`: Fitch affirmed Aena's long-term and short-term ratings, with a stable long-term outlook. Quote (page 180): "El 22 de octubre, la agencia Fitch Ratings afirmó la calificación de largo plazo “A”, así como la calificación a corto plazo “F1” de Aena S.M.E., S.A. La perspectiva de largo plazo es estable."

## Peer positioning

Aena has the highest EBITDA margin in the airport group (1st of 3), against a peer median of 36.5%.
Cash generation also leads the group, with FFO to debt and FCF to debt both ranking 1st of 2 against peer medians of 27.7% and 13.4% respectively.
Leverage sits in the middle of the group, with net leverage ranking 2nd of 3 and gross leverage ranking 2nd of 3.

## Watch items

- Cash generation: free cash flow fell by 10.2% to EUR 1.7bn and FCF to debt by 3.4 points to 22.9%, as capex intensity rose by 2.6 points to 16.9%.
- Investment: capex intensity of 16.9% is below the peer median of 18.2%, but capital spending rose by 2.6 points and absorbs a larger share of cash generated.
- Regulation: the regulator set the average airport charge for 2026 above the prior year's level, so the tariff path under the next regulatory period remains the key revenue sensitivity.

> Event `event:regulation_and_tariffs`: The competition regulator issued its supervision resolution setting the average airport charge per passenger for the following year, above the prior year's level. Quote (page 180): "En relación con el Documento de Regulación Aeroportuaria para el período 2022-2026 (DORA II), el 13 de noviembre de 2025, la CNMC emitió su resolución de supervisión de las tarifas aeroportuarias para 2026, estableciendo que el IMAAJ para 2026 sea de 11,00 euros por pasajero, lo que supone un incremento del 6,31% respecto al IMAAJ de 2025 (10,35 euros por"

> removed by the verifier (still broke a rule after two retries): "Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, a worse outcome than the prior year even as revenue rose by {{revenue.change@FY2025}}." ('worse' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 5 errors | 12,371 / 2,707 |
| 2 | peer_positioning, watch_items | 2 errors | 13,196 / 917 |
| 3 | watch_items | 1 errors | 12,580 / 581 |

### Errors found, by try

Try 1:

- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2025 is already given in operating_performance, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: ffo_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: fcf_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'rise' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] watch_items, sentence 2: 'weaker' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'increase' needs a 'up' claim on a figure in the same clause

Try 3:

- [rule 4] watch_items, sentence 2: 'worse' needs a 'worse' or 'worse_than_peers' or 'worst_in_group' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, and Moody's raised its long-term issuer and senior unsecured ratings during the year.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, in line with the airport peer median, while the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, but net debt was broadly unchanged at {{net_debt@FY2025}}, so gross leverage was stable at {{gross_leverage@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, above the peer median.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, but FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}.

`operating_performance`

- In FY2024 the Spanish network carried {{passengers@FY2024}} passengers, with traffic growth of {{traffic_growth@FY2024}}.
- Aeronautical revenue per passenger was {{aero_revenue_per_passenger@FY2024}} in FY2024, the base against which the regulator set the average airport charge for 2026 above the prior year's level.
- Group revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, while the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, so cost growth outpaced revenue growth.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Liquidity stood at {{liquidity@FY2025}}, including {{undrawn_facilities@FY2025}} of undrawn committed credit facilities, equal to {{liquidity_to_revenue@FY2025}} of revenue.
- On the funding side, the Brazilian subsidiary BOAB issued secured debentures maturing in the long term, London Luton airport completed the refinancing of its bank debt, and Fitch affirmed the ratings with a stable long-term outlook.

`peer_positioning`

- Aena has the highest EBITDA margin in the airport group ({{ebitda_margin.peer_rank@FY2025}}), against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- Cash generation also leads the group, with FFO to debt and FCF to debt both ranking {{ffo_to_debt.peer_rank@FY2025}} against peer medians of {{ffo_to_debt.peer_median@FY2025}} and {{fcf_to_debt.peer_median@FY2025}} respectively.
- Leverage sits in the middle of the group, with net leverage ranking {{net_leverage.peer_rank@FY2025}} and gross leverage ranking {{gross_leverage.peer_rank@FY2025}}.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Investment: capex intensity of {{capex_intensity@FY2025}} is below the peer median of {{capex_intensity.peer_median@FY2025}}, but capital spending rose by {{capex_intensity.change@FY2025}} and absorbs a larger share of cash generated.
- Regulation: the regulator set the average airport charge for 2026 above the prior year's level, so the tariff path under the next regulatory period remains the key revenue sensitivity.
