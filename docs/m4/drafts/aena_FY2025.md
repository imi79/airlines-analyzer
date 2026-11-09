# Aena, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v5`, fact sheet `f53221167e21` ([fact sheet](../factsheets/aena_FY2025.md)). Tokens: 38,277 in, 4,979 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, grew revenue by 8.9% to EUR 6.3bn in FY2025, and Moody's raised its long-term issuer and senior unsecured ratings during the year.
Net leverage fell by 0.11x to 1.46x, helped by EBITDA up 7.8%.
The point to watch is cash generation: free cash flow fell by 10.2% to EUR 1.7bn as capex intensity rose by 2.6 points to 16.9%.

> Event `event:funding_and_rating-2`: Moody's raised Aena's long-term issuer and senior unsecured debt ratings. Quote (page 231): "La agencia de calificación crediticia Moody's Investors Service ha mejorado la calificación de emisor a largo plazo y la calificación de deuda senior no garantizada de Aena S.M.E., S.A. a A2 desde A3."

## Credit metrics

EBITDA increased by 7.8% to EUR 3.8bn, with operating profit up 12.2% to EUR 3.0bn.
Total debt rose by 3.2% to EUR 7.6bn, while net debt was stable at EUR 5.5bn and gross leverage broadly unchanged at 2.00x.
Interest coverage improved by 2.38x to 14.72x, and FFO to debt rose by 0.6 points to 39.6% on FFO up 4.8% to EUR 3.0bn.
FCF to debt fell by 3.4 points to 22.9%, as free cash flow declined by 10.2% to EUR 1.7bn with capex intensity up 2.6 points to 16.9%.

## Operating performance

In FY2024 the Spanish network carried 309.3m passengers, with traffic growth of 9.2%.
Aeronautical revenue per passenger was EUR 10.18 in FY2024, the base on which the regulator's charge decision builds.
Group revenue rose by 8.9% to EUR 6.3bn, reflecting both the Spanish network and the group's other airports.

> removed by the verifier (still broke a rule after two retries): "The CNMC set the average airport charge per passenger for 2026 at a level above the prior year's, which supports the aeronautical revenue base." ('above' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, and cash liquidity to revenue increased by 1.0 point to 32.6%.
Total liquidity was EUR 4.3bn, including EUR 2.2bn of undrawn committed credit facilities, equal to 68.4% of revenue.
Funding access was supported by the Brazilian subsidiary's debenture issue and by the refinancing of London Luton's bank debt.

> Event `event:funding_and_rating`: The Brazilian subsidiary BOAB issued secured, non-convertible debentures maturing in the long term, indexed to IPCA with a fixed coupon payable semi-annually. Quote (page 61): "El 30 de octubre de 2025, la filial BOAB realizó su primera emisión de bonos (debentures simples) por importe de 5.300 millones de BRL, no convertibles, con garantía real, con vencimiento en junio de 2048), indexadas a IPCA y con cupón fijo del 8,74% anual, pagadero semestralmente, siendo el primer pago el 15 de junio de 2026 (Nota 20)."

> Event `event:funding_and_rating-4`: London Luton airport completed the refinancing of its bank debt. Quote (page 216): "En junio de 2025, el Aeropuerto London Luton completó la refinanciación de su deuda bancaria."

## Peer positioning

Aena has the highest EBITDA margin among the airport peers (1st of 3), at 60.3% against a median of 36.5%.
Gross leverage sits in the middle of the group (2nd of 3), and capex intensity is below the peer median of 18.2%.
Interest coverage, FFO to debt and FCF to debt all rank best in the group (1st of 2, 1st of 2 and 1st of 2).

## Watch items

- Cash generation: FCF to debt fell by 3.4 points to 22.9% as capex intensity rose to 16.9%.
- Margin: the EBITDA margin narrowed by 0.6 points to 60.3%, though it remains above the peer median of 36.5%.
- Debt: total debt rose by 3.2% to EUR 7.6bn, leaving gross leverage broadly unchanged at 2.00x.

> removed by the verifier (still broke a rule after two retries): "Regulation: the CNMC set the average airport charge per passenger for 2026 at a level above the prior year's, so the next DORA review governs the aeronautical revenue base." ('above' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 11,978 / 2,695 |
| 2 | operating_performance, liquidity_funding, peer_positioning, watch_items | 2 errors | 13,766 / 1,519 |
| 3 | operating_performance, watch_items | 2 errors | 12,533 / 765 |

### Errors found, by try

Try 1:

- [rule 4] operating_performance, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] operating_performance, sentence 4: ebitda.change@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 4: ebitda@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 1] liquidity_funding, sentence 3: word that states a number: 'first'
- [rule style] peer_positioning, sentence 2: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 4: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

Try 2:

- [rule 4] operating_performance, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

Try 3:

- [rule 4] operating_performance, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule 4] watch_items, sentence 4: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, and Moody's raised its long-term issuer and senior unsecured ratings during the year.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, helped by EBITDA up {{ebitda.change@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, with operating profit up {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, while net debt was stable at {{net_debt@FY2025}} and gross leverage broadly unchanged at {{gross_leverage@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} on FFO up {{ffo.change@FY2025}} to {{ffo@FY2025}}.
- FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, as free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} with capex intensity up {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- In FY2024 the Spanish network carried {{passengers@FY2024}} passengers, with traffic growth of {{traffic_growth@FY2024}}.
- Aeronautical revenue per passenger was {{aero_revenue_per_passenger@FY2024}} in FY2024, the base on which the regulator's charge decision builds.
- Group revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, reflecting both the Spanish network and the group's other airports.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Total liquidity was {{liquidity@FY2025}}, including {{undrawn_facilities@FY2025}} of undrawn committed credit facilities, equal to {{liquidity_to_revenue@FY2025}} of revenue.
- Funding access was supported by the Brazilian subsidiary's debenture issue and by the refinancing of London Luton's bank debt.

`peer_positioning`

- Aena has the highest EBITDA margin among the airport peers ({{ebitda_margin.peer_rank@FY2025}}), at {{ebitda_margin@FY2025}} against a median of {{ebitda_margin.peer_median@FY2025}}.
- Gross leverage sits in the middle of the group ({{gross_leverage.peer_rank@FY2025}}), and capex intensity is below the peer median of {{capex_intensity.peer_median@FY2025}}.
- Interest coverage, FFO to debt and FCF to debt all rank best in the group ({{interest_coverage.peer_rank@FY2025}}, {{ffo_to_debt.peer_rank@FY2025}} and {{fcf_to_debt.peer_rank@FY2025}}).

`watch_items`

- Cash generation: FCF to debt fell by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} as capex intensity rose to {{capex_intensity@FY2025}}.
- Margin: the EBITDA margin narrowed by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, though it remains above the peer median of {{ebitda_margin.peer_median@FY2025}}.
- Debt: total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, leaving gross leverage broadly unchanged at {{gross_leverage@FY2025}}.
