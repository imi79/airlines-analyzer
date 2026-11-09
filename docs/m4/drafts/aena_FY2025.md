# Aena, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `7cd238123854` ([fact sheet](../factsheets/aena_FY2025.md)). Tokens: 39,035 in, 4,689 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Aena, the Spanish airport operator, grew revenue by 8.9% to EUR 6.3bn in FY2025, with Moody's raising its long-term issuer rating during the year.
Net leverage fell by 0.11x to 1.46x, in line with the airport peer median, as EBITDA rose by 7.8%.
The point to watch is cash generation: free cash flow fell by 10.2% to EUR 1.7bn as capex intensity rose by 2.6 points to 16.9%.

> Event `event:funding_and_rating-2`: Moody's raised Aena's long-term issuer and senior unsecured debt ratings. Quote (page 231): "La agencia de calificación crediticia Moody's Investors Service ha mejorado la calificación de emisor a largo plazo y la calificación de deuda senior no garantizada de Aena S.M.E., S.A. a A2 desde A3."

## Credit metrics

EBITDA increased by 7.8% to EUR 3.8bn, and operating profit rose by 12.2% to EUR 3.0bn.
Total debt rose by 3.2% to EUR 7.6bn, while net debt was broadly unchanged at EUR 5.5bn, so gross leverage was stable at 2.00x.
Interest coverage improved by 2.38x to 14.72x, and FFO to debt rose by 0.6 points to 39.6% on FFO up 4.8% to EUR 3.0bn.
Free cash flow declined by 10.2% to EUR 1.7bn, taking FCF to debt down by 3.4 points to 22.9% as capex intensity rose by 2.6 points to 16.9%.

## Operating performance

Revenue rose by 8.9% to EUR 6.3bn, with the EBITDA margin easing by 0.6 points to 60.3%.
In FY2024 the Spanish network carried 309.3m passengers, with traffic growth of 9.2% and aeronautical revenue per passenger of EUR 10.18.

> removed by the verifier (still broke a rule after two retries): "The regulator set the average airport charge per passenger for 2026 above the prior year's level, which supports the aeronautical revenue base." ('above' needs a 'up' or 'above_peers' claim on a figure in the same clause)

## Liquidity and funding

Cash and cash-like investments rose by 12.4% to EUR 2.0bn, and cash liquidity to revenue increased by 1.0 point to 32.6%.
Total liquidity of EUR 4.3bn includes EUR 2.2bn of undrawn committed credit facilities, and liquidity to revenue reached 68.4%.
On the funding side, Fitch affirmed Aena's long-term rating with a stable outlook, and the Brazilian subsidiary BOAB issued secured debentures maturing in the long term.

> Event `event:funding_and_rating-3`: Fitch affirmed Aena's long-term and short-term ratings, with a stable long-term outlook. Quote (page 180): "El 22 de octubre, la agencia Fitch Ratings afirmó la calificación de largo plazo “A”, así como la calificación a corto plazo “F1” de Aena S.M.E., S.A. La perspectiva de largo plazo es estable."

> Event `event:funding_and_rating`: The Brazilian subsidiary BOAB issued secured, non-convertible debentures maturing in the long term, indexed to IPCA with a fixed coupon payable semi-annually. Quote (page 61): "El 30 de octubre de 2025, la filial BOAB realizó su primera emisión de bonos (debentures simples) por importe de 5.300 millones de BRL, no convertibles, con garantía real, con vencimiento en junio de 2048), indexadas a IPCA y con cupón fijo del 8,74% anual, pagadero semestralmente, siendo el primer pago el 15 de junio de 2026 (Nota 20)."

## Peer positioning

Aena has the highest EBITDA margin in the airport group (1st of 3), against a peer median of 36.5%.
It also leads the group on interest coverage (1st of 2), FFO to debt (1st of 2) and FCF to debt (1st of 2).
Leverage sits in the middle of the group, with net leverage ranking 2nd of 3 and gross leverage 2nd of 3, and capex intensity is below the peer median of 18.2%.

## Watch items

- Cash generation: free cash flow fell by 10.2% to EUR 1.7bn and FCF to debt by 3.4 points to 22.9%, as capex intensity rose by 2.6 points to 16.9%.
- Margins: the EBITDA margin eased by 0.6 points to 60.3%, a weaker result than the prior year.
- Debt: total debt rose by 3.2% to EUR 7.6bn, so gross leverage of 2.00x leaves limited headroom if EBITDA stalls.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 12,402 / 2,733 |
| 2 | snapshot, operating_performance, peer_positioning, watch_items | 1 errors | 14,183 / 1,598 |
| 3 | operating_performance | 1 errors | 12,450 / 358 |

### Errors found, by try

Try 1:

- [rule 1] snapshot, sentence 1: number written outside a blank: 'A2'
- [rule 1] snapshot, sentence 1: number written outside a blank: 'A3'
- [rule 4] operating_performance, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 1: ebitda_margin@FY2025 is already given in operating_performance, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 4] watch_items, sentence 2: 'growth' needs a 'up' claim on a figure in the same clause
- [rule 4] watch_items, sentence 3: 'growth' needs a 'up' claim on a figure in the same clause

Try 2:

- [rule 4] operating_performance, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

Try 3:

- [rule 4] operating_performance, sentence 3: 'above' needs a 'up' or 'above_peers' claim on a figure in the same clause

### Text with blanks (as the AI wrote it)

`snapshot`

- Aena, the Spanish airport operator, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025, with Moody's raising its long-term issuer rating during the year.
- Net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}, in line with the airport peer median, as EBITDA rose by {{ebitda.change@FY2025}}.
- The point to watch is cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, while net debt was broadly unchanged at {{net_debt@FY2025}}, so gross leverage was stable at {{gross_leverage@FY2025}}.
- Interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}, and FFO to debt rose by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}} on FFO up {{ffo.change@FY2025}} to {{ffo@FY2025}}.
- Free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}}, taking FCF to debt down by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}, with the EBITDA margin easing by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- In FY2024 the Spanish network carried {{passengers@FY2024}} passengers, with traffic growth of {{traffic_growth@FY2024}} and aeronautical revenue per passenger of {{aero_revenue_per_passenger@FY2024}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, and cash liquidity to revenue increased by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Total liquidity of {{liquidity@FY2025}} includes {{undrawn_facilities@FY2025}} of undrawn committed credit facilities, and liquidity to revenue reached {{liquidity_to_revenue@FY2025}}.
- On the funding side, Fitch affirmed Aena's long-term rating with a stable outlook, and the Brazilian subsidiary BOAB issued secured debentures maturing in the long term.

`peer_positioning`

- Aena has the highest EBITDA margin in the airport group ({{ebitda_margin.peer_rank@FY2025}}), against a peer median of {{ebitda_margin.peer_median@FY2025}}.
- It also leads the group on interest coverage ({{interest_coverage.peer_rank@FY2025}}), FFO to debt ({{ffo_to_debt.peer_rank@FY2025}}) and FCF to debt ({{fcf_to_debt.peer_rank@FY2025}}).
- Leverage sits in the middle of the group, with net leverage ranking {{net_leverage.peer_rank@FY2025}} and gross leverage {{gross_leverage.peer_rank@FY2025}}, and capex intensity is below the peer median of {{capex_intensity.peer_median@FY2025}}.

`watch_items`

- Cash generation: free cash flow fell by {{fcf.change@FY2025}} to {{fcf@FY2025}} and FCF to debt by {{fcf_to_debt.change@FY2025}} to {{fcf_to_debt@FY2025}}, as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Margins: the EBITDA margin eased by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, a weaker result than the prior year.
- Debt: total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}}, so gross leverage of {{gross_leverage@FY2025}} leaves limited headroom if EBITDA stalls.
