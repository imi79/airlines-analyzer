# Norwegian Air Shuttle, FY2024: draft commentary

Status: passed the verifier. First try: rejected; tries: 2. Model deepseek-flash, prompt `draft-v3`, fact sheet `08455c6c44ad` ([fact sheet](../factsheets/norwegian_FY2024.md)). Tokens: 24,131 in, 5,508 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Norwegian Air Shuttle, the Norwegian low-cost carrier, grew revenue by 38.3% to NOK 35.3bn in FY2024, but the EBITDA margin narrowed by 3.7 points to 18.9%.
Net leverage was stable at 0.78x as EBITDA rose by 15.9% to NOK 6.7bn alongside higher debt.
The main point to watch is liquidity: cash liquidity to revenue fell by 6.3 points to 30.8%, the weakest of the low-cost peer group (3rd of 3).

## Credit metrics

EBITDA increased by 15.9% to NOK 6.7bn, while operating profit fell by 16.1% to NOK 1.9bn as depreciation and interest charges absorbed more of the earnings.
Total debt rose by 14.6% to NOK 16.1bn and net debt by 14.3% to NOK 5.2bn, leaving gross leverage broadly unchanged at 2.41x.
Interest coverage weakened by 0.91x to 5.89x, in line with the peer median.
FFO rose by 11.1% to NOK 5.7bn, but FFO to debt fell by 1.1 points to 35.6% as total debt rose by 14.6%.
Free cash flow increased by 20.9% to NOK 5.7bn, lifting FCF to debt by 1.8 points to 35.4%, above the peer median.

## Operating performance

Passengers rose by 28.2% to 26.4m, well ahead of the revenue increase of 38.3%.
Unit economics for FY2023, the last year with capacity data, showed RASK of 79.07 øre against CASK of 72.16 øre and CASK ex-fuel of 48.27 øre.
The fuel share of costs fell by 5.1 points to 28.0%, in line with the peer median.
Capex intensity rose by 1.4 points to 3.5%, still below the peer median of 5.4%.

## Liquidity and funding

Cash and cash-like investments rose by 14.8% to NOK 10.9bn, and cash liquidity increased by the same 14.8% to NOK 10.9bn.
Cash liquidity to revenue fell by 6.3 points to 30.8%, below the peer median of 33.0%, as revenue rose by 38.3% faster than the cash balance.
Customer prepayments rose: advance ticket cover increased by 4.3 points to 38.1% and contract liabilities by 29.4% to NOK 4.1bn.

## Peer positioning

Norwegian has the lowest gross leverage in the low-cost peer group (1st of 3), at 2.41x against a median of 2.41x.
FCF to debt of 35.4% is the strongest of the group (1st of 3), well above the peer median of 16.3%.
The EBITDA margin of 18.9% and net leverage of 0.78x both sit at the peer median, ranking 2nd of 3 and 2nd of 3 respectively.
Cash liquidity to revenue of 30.8% is the weakest of the group (3rd of 3), below the peer median of 33.0%.

## Watch items

- Liquidity: cash liquidity to revenue fell by 6.3 points to 30.8%, the weakest of the peer group (3rd of 3), so the buffer against near-term maturities is thinner than at the other low-cost carriers.
- Debt: total debt rose by 14.6% to NOK 16.1bn and net debt by 14.3% to NOK 5.2bn, so leverage now depends on EBITDA holding at NOK 6.7bn.
- Margins: the EBITDA margin narrowed by 3.7 points to 18.9% and interest coverage fell by 0.91x to 5.89x, both now only in line with the peer median.
- Customer prepayments: contract liabilities of NOK 4.1bn rose by 29.4%, and advance ticket cover of 38.1% remains below the peer median of 50.2%, a sensitivity if bookings slow.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 3 errors | 11,445 / 3,477 |
| 2 | credit_metrics, liquidity_funding, watch_items | passed | 12,686 / 2,031 |

### Errors found, by try

Try 1:

- [rule 4] credit_metrics, sentence 4: 'expanded' needs a 'up' claim on a figure in the same clause
- [rule 4] liquidity_funding, sentence 2: 'grew' needs a 'up' claim on a figure in the same clause
- [rule 5] watch_items, sentence 1: cash_liquidity_to_revenue.peer_rank@2024 is listed in the form but not used in the text

### Text with blanks (as the AI wrote it)

`snapshot`

- Norwegian Air Shuttle, the Norwegian low-cost carrier, grew revenue by {{revenue.change@FY2024}} to {{revenue@FY2024}} in FY2024, but the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}}.
- Net leverage was stable at {{net_leverage@FY2024}} as EBITDA rose by {{ebitda.change@FY2024}} to {{ebitda@FY2024}} alongside higher debt.
- The main point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the low-cost peer group ({{cash_liquidity_to_revenue.peer_rank@2024}}).

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2024}} to {{ebitda@FY2024}}, while operating profit fell by {{operating_profit.change@FY2024}} to {{operating_profit@FY2024}} as depreciation and interest charges absorbed more of the earnings.
- Total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, leaving gross leverage broadly unchanged at {{gross_leverage@FY2024}}.
- Interest coverage weakened by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, in line with the peer median.
- FFO rose by {{ffo.change@FY2024}} to {{ffo@FY2024}}, but FFO to debt fell by {{ffo_to_debt.change@FY2024}} to {{ffo_to_debt@FY2024}} as total debt rose by {{total_debt.change@FY2024}}.
- Free cash flow increased by {{fcf.change@FY2024}} to {{fcf@FY2024}}, lifting FCF to debt by {{fcf_to_debt.change@FY2024}} to {{fcf_to_debt@FY2024}}, above the peer median.

`operating_performance`

- Passengers rose by {{passengers.change@FY2024}} to {{passengers@FY2024}}, well ahead of the revenue increase of {{revenue.change@FY2024}}.
- Unit economics for FY2023, the last year with capacity data, showed RASK of {{rask@FY2023}} against CASK of {{cask@FY2023}} and CASK ex-fuel of {{cask_ex_fuel@FY2023}}.
- The fuel share of costs fell by {{fuel_share_of_costs.change@FY2024}} to {{fuel_share_of_costs@FY2024}}, in line with the peer median.
- Capex intensity rose by {{capex_intensity.change@FY2024}} to {{capex_intensity@FY2024}}, still below the peer median of {{capex_intensity.peer_median@2024}}.

`liquidity_funding`

- Cash and cash-like investments rose by {{cash_like.change@FY2024}} to {{cash_like@FY2024}}, and cash liquidity increased by the same {{cash_liquidity.change@FY2024}} to {{cash_liquidity@FY2024}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}, as revenue rose by {{revenue.change@FY2024}} faster than the cash balance.
- Customer prepayments rose: advance ticket cover increased by {{advance_ticket_cover.change@FY2024}} to {{advance_ticket_cover@FY2024}} and contract liabilities by {{contract_liabilities.change@FY2024}} to {{contract_liabilities@FY2024}}.

`peer_positioning`

- Norwegian has the lowest gross leverage in the low-cost peer group ({{gross_leverage.peer_rank@2024}}), at {{gross_leverage@FY2024}} against a median of {{gross_leverage.peer_median@2024}}.
- FCF to debt of {{fcf_to_debt@FY2024}} is the strongest of the group ({{fcf_to_debt.peer_rank@2024}}), well above the peer median of {{fcf_to_debt.peer_median@2024}}.
- The EBITDA margin of {{ebitda_margin@FY2024}} and net leverage of {{net_leverage@FY2024}} both sit at the peer median, ranking {{ebitda_margin.peer_rank@2024}} and {{net_leverage.peer_rank@2024}} respectively.
- Cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2024}} is the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@2024}}), below the peer median of {{cash_liquidity_to_revenue.peer_median@2024}}.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2024}} to {{cash_liquidity_to_revenue@FY2024}}, the weakest of the peer group ({{cash_liquidity_to_revenue.peer_rank@2024}}), so the buffer against near-term maturities is thinner than at the other low-cost carriers.
- Debt: total debt rose by {{total_debt.change@FY2024}} to {{total_debt@FY2024}} and net debt by {{net_debt.change@FY2024}} to {{net_debt@FY2024}}, so leverage now depends on EBITDA holding at {{ebitda@FY2024}}.
- Margins: the EBITDA margin narrowed by {{ebitda_margin.change@FY2024}} to {{ebitda_margin@FY2024}} and interest coverage fell by {{interest_coverage.change@FY2024}} to {{interest_coverage@FY2024}}, both now only in line with the peer median.
- Customer prepayments: contract liabilities of {{contract_liabilities@FY2024}} rose by {{contract_liabilities.change@FY2024}}, and advance ticket cover of {{advance_ticket_cover@FY2024}} remains below the peer median of {{advance_ticket_cover.peer_median@2024}}, a sensitivity if bookings slow.
