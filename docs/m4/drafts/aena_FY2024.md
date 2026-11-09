# Aena, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v6`, fact sheet `213e6472a9c9` ([fact sheet](../factsheets/aena_FY2024.md)). Tokens: 27,084 in, 4,412 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, grew revenue by 14.4% to EUR 5.8bn in FY2024, with Fitch raising its long-term rating and Moody's moving its outlook to positive.
Net leverage fell by 0.49x to 1.57x as EBITDA rose by 16.1% to EUR 3.5bn.
The point to watch is cash liquidity, which fell by 15.3 points to 31.6% of revenue, below the peer median of 34.0%.

> Event `event:funding_and_rating`: Fitch raised Aena's long-term issuer and EMTN programme rating and its short-term rating, keeping the outlook stable. Quote (page 52): "El 7 de mayo, Fitch Ratings mejoró la calificación de largo plazo y del programa EMTN a “A” desde “A-“, así como la calificación a corto plazo a “F1” desde “F2”, manteniendo la perspectiva estable."

> Event `event:funding_and_rating-2`: Moody's changed Aena's outlook to positive from stable and confirmed the long-term rating and the EMTN programme rating. Quote (page 164): "El 19 de marzo, la agencia de rating Moody’s mejoró la perspectiva de Aena S.M.E., S.A. a positiva desde estable y confirmó la calificación de largo plazo “A3” y del programa EMTN."

## Credit metrics

EBITDA increased by 16.1% to EUR 3.5bn on revenue up 14.4% to EUR 5.8bn, and operating profit rose by 20.9% to EUR 2.7bn.
Total debt was reduced by 14.8% to EUR 7.3bn and net debt by 11.6% to EUR 5.5bn, taking gross leverage down by 0.76x to 2.08x.
Cash generation strengthened: FFO rose by 20.3% to EUR 2.9bn, lifting FFO to debt by 11.3 points to 39.0%, and free cash flow increased by 129.9% to EUR 1.9bn.
FCF to debt rose by 16.6 points to 26.3%, helped by capex intensity easing by 13.1 points to 14.3%.
Interest coverage eased by 0.27x to 12.34x, still well above the peer median of 9.65x.

## Operating performance

Passengers rose by 9.2% to 309.3m, with traffic growth of 9.2% below the 16.2% of FY2023.
Aeronautical revenue per passenger increased by 4.1% to EUR 10.18, with the CNMC setting the maximum adjusted annual revenue per passenger for 2025 at the prior year's level.
The EBITDA margin widened by 0.9 points to 60.9%, as revenue growth outpaced the rise in operating costs.

> Event `event:regulation_and_tariffs`: The CNMC issued its supervision resolution on airport tariffs for 2025, stating the applicable maximum adjusted annual revenue per passenger and that it stays unchanged versus the prior year. Quote (page 164): "En relación con el Documento de Regulación Aeroportuaria para el período 2022-2026 (DORA II), el 28 de noviembre de 2024, la CNMC emitió su resolución de supervisión de las tarifas aeroportuarias para 2025, declarando que el ingreso máximo anual ajustado por pasajero (IMAAJ) aplicable es de 10,35 euros, lo que supone una variación del 0% respecto a"

## Liquidity and funding

Cash and cash-like investments fell by 22.9% to EUR 1.8bn, taking cash liquidity to revenue down by 15.3 points to 31.6%.
In FY2023 the group held liquidity of EUR 4.9bn, including EUR 2.6bn of undrawn committed credit facilities, equal to 97.6% of revenue.
Funding conditions improved with the rating actions: Fitch upgraded the long-term and EMTN programme rating and Moody's moved the outlook to positive.

> Event `event:funding_and_rating`: Fitch raised Aena's long-term issuer and EMTN programme rating and its short-term rating, keeping the outlook stable. Quote (page 52): "El 7 de mayo, Fitch Ratings mejoró la calificación de largo plazo y del programa EMTN a “A” desde “A-“, así como la calificación a corto plazo a “F1” desde “F2”, manteniendo la perspectiva estable."

> Event `event:funding_and_rating-2`: Moody's changed Aena's outlook to positive from stable and confirmed the long-term rating and the EMTN programme rating. Quote (page 164): "El 19 de marzo, la agencia de rating Moody’s mejoró la perspectiva de Aena S.M.E., S.A. a positiva desde estable y confirmó la calificación de largo plazo “A3” y del programa EMTN."

## Peer positioning

Aena has the highest EBITDA margin of the airport peers (1st of 3), against a median of 42.0%, and the strongest interest coverage (1st of 2).
Cash generation also leads the group, with FFO to debt and FCF to debt both ranking 1st of 2.
Leverage sits in the middle of the group, with net leverage ranking 2nd of 3 and gross leverage 2nd of 3, while cash liquidity to revenue is the weakest of the peers (3rd of 3).

## Watch items

- Liquidity: cash liquidity to revenue fell by 15.3 points to 31.6%, below the peer median of 34.0% and the weakest of the group (3rd of 3).
- Cash: cash and cash-like investments declined by 22.9% to EUR 1.8bn as debt was repaid, so the buffer against maturities is thinner than a year earlier.
- Coverage: interest coverage eased by 0.27x to 12.34x, a move to monitor even though it remains above the peer median.
- Traffic: traffic growth slowed by 7.0 points to 9.2%, and the CNMC set the maximum adjusted annual revenue per passenger for 2025 at the prior year's level, limiting tariff-led revenue.

> Event `event:regulation_and_tariffs`: The CNMC issued its supervision resolution on airport tariffs for 2025, stating the applicable maximum adjusted annual revenue per passenger and that it stays unchanged versus the prior year. Quote (page 164): "En relación con el Documento de Regulación Aeroportuaria para el período 2022-2026 (DORA II), el 28 de noviembre de 2024, la CNMC emitió su resolución de supervisión de las tarifas aeroportuarias para 2025, declarando que el ingreso máximo anual ajustado por pasajero (IMAAJ) aplicable es de 10,35 euros, lo que supone una variación del 0% respecto a"

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 9 errors | 12,720 / 3,070 |
| 2 | operating_performance, peer_positioning, watch_items | passed | 14,364 / 1,342 |

### Errors found, by try

Try 1:

- [rule 4] operating_performance, sentence 2: 'unchanged' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2024 is already given in operating_performance, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: ffo_to_debt@FY2024 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: fcf_to_debt@FY2024 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: gross_leverage@FY2024 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 1: 'weakest' needs a 'worst_in_group' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'unchanged' needs a 'flat' or 'in_line_with_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'growth' needs a 'up' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, with Fitch raising its long-term rating and Moody's moving its outlook to positive.
- Net leverage fell by {{net_leverage.change@FY2024}} to {{net_leverage@FY2024}} as EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}} of revenue, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} on revenue up {{revenue.change@FY2024}} to {{revenue@FY2024}}, and operating profit rose by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}}.
- Total debt was reduced by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, taking gross leverage down by {{gross_leverage.change@FY2024}} to {{gross_leverage@FY2024}}.
- Cash generation strengthened: FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, lifting FFO to debt by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}}, and free cash flow increased by {{fcf.change@FY2024}} to {{fcf@FY2024}}.
- FCF to debt rose by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, helped by capex intensity easing by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}.
- Interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, still well above the peer median of {{interest_coverage.peer_median@FY2024}}.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, with traffic growth of {{traffic_growth@FY2024}} below the {{traffic_growth@FY2023}} of FY2023.
- Aeronautical revenue per passenger increased by {{aero_revenue_per_passenger.change@FY2024}} to {{aero_revenue_per_passenger@FY2024}}, with the CNMC setting the maximum adjusted annual revenue per passenger for 2025 at the prior year's level.
- The EBITDA margin widened by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}, as revenue growth outpaced the rise in operating costs.

`liquidity_funding`

- Cash and cash-like investments fell by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}.
- In FY2023 the group held liquidity of {{liquidity@FY2023}}, including {{undrawn_facilities@FY2023}} of undrawn committed credit facilities, equal to {{liquidity_to_revenue@FY2023}} of revenue.
- Funding conditions improved with the rating actions: Fitch upgraded the long-term and EMTN programme rating and Moody's moved the outlook to positive.

`peer_positioning`

- Aena has the highest EBITDA margin of the airport peers ({{ebitda_margin.peer_rank@FY2024}}), against a median of {{ebitda_margin.peer_median@FY2024}}, and the strongest interest coverage ({{interest_coverage.peer_rank@FY2024}}).
- Cash generation also leads the group, with FFO to debt and FCF to debt both ranking {{ffo_to_debt.peer_rank@FY2024}}.
- Leverage sits in the middle of the group, with net leverage ranking {{net_leverage.peer_rank@FY2024}} and gross leverage {{gross_leverage.peer_rank@FY2024}}, while cash liquidity to revenue is the weakest of the peers ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2024}} and the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2024}}).
- Cash: cash and cash-like investments declined by {{cash_like.change@FY2024}} to {{cash_like@FY2024}} as debt was repaid, so the buffer against maturities is thinner than a year earlier.
- Coverage: interest coverage eased by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, a move to monitor even though it remains above the peer median.
- Traffic: traffic growth slowed by {{traffic_growth.change@FY2024}} to {{traffic_growth@FY2024}}, and the CNMC set the maximum adjusted annual revenue per passenger for 2025 at the prior year's level, limiting tariff-led revenue.
