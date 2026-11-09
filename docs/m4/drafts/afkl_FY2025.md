# Air France-KLM, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `0723bc17f2df` ([fact sheet](../factsheets/afkl_FY2025.md)). Tokens: 41,009 in, 5,243 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

Air France-KLM, a network airline in the European peer group, grew revenue by 4.9% to EUR 33.0bn in FY2025 while EBITDA rose by 23.0% to EUR 5.1bn.
The EBITDA margin widened by 2.2 points to 15.3%, and net leverage fell by 0.17x to 1.71x.
The point to watch is cash liquidity, which fell by 1.2 points to 20.8% of revenue, below the peer median of 25.0%.

## Credit metrics

EBITDA increased by 23.0% to EUR 5.1bn, and operating profit rose by 36.6% to EUR 2.0bn.
Total debt rose by 5.9% to EUR 15.5bn and net debt by 12.3% to EUR 8.7bn, yet gross leverage fell by 0.49x to 3.07x.
FFO rose by 24.1% to EUR 4.3bn, lifting FFO to debt by 4.0 points to 27.4%, and interest coverage improved by 1.55x to 8.06x.
Free cash flow turned positive at EUR 606m from EUR -232m in FY2024, taking FCF to debt to 3.9% as capex intensity rose by 1.6 points to 13.5%.

## Operating performance

Revenue grew by 4.9% to EUR 33.0bn, with the EBITDA margin widening by 2.2 points to 15.3%.
In FY2024 the group carried 98.0m passengers with a fleet of 564 aircraft at an average age of 12.1 years.

## Liquidity and funding

Cash and cash-like investments were broadly unchanged at EUR 6.9bn, a change of 1.1%, so cash liquidity stood at EUR 6.9bn.
Cash liquidity to revenue fell by 1.2 points to 20.8%, below the peer median of 25.0%.
Contract liabilities rose by 4.1% to EUR 4.3bn, and advance ticket cover increased by 3.1 points to 62.2%, the lowest of the peer group (1st of 3).
The group placed senior unsecured bonds under its EMTN programme and redeemed its outstanding hybrid bonds from the hard call date, while the extension option on its credit facility pushed that maturity to 2029.

> Event `event:funding_and_rating`: The Group placed senior unsecured bonds under its EMTN programme, with the cash received in September 2025. Quote (page 18): "bonds on August 28, 2025, with a maturity of 5 years and a coupon of 3.75% (yield of 3.866%) under its EMTN program. The cash inflow occurred on September 4, 2025 (see Note 31 “Financial liabilities”)."

> Event `event:funding_and_rating-2`: The Group notified holders of its last-rank indefinite subordinated convertible bonds of its intention to redeem all outstanding hybrid bonds from the hard call date, and paid the nominal amount plus accrued interest in November 2025. Quote (page 18): "On October 15, Air France–KLM Group notified the holders of last-rank indefinite subordinated bond convertible into new shares and/or existing shares its intention to redeem all of the outstanding hybrid Bonds from the First Hard Call Date at a price per hybrid Bonds equal to par (€100,000) plus accrued interest of 1,625 euro."

> Event `event:funding_and_rating-3`: The Group exercised an extension option on the Air France-KLM and Air France credit facility, pushing its maturity date out. Quote (page 17): "This last extension option was exercised in June 2025, bringing the maturity date to 2029."

## Peer positioning

Air France-KLM sits in the middle of the network group on EBITDA margin, net leverage, gross leverage, interest coverage and FFO to debt, each ranking 2nd of 3.
It is weakest on cash generation and liquidity, with FCF to debt below the peer median of 10.8% and the lowest of the group (3rd of 3), and cash liquidity to revenue the lowest as well (3rd of 3).

## Watch items

- Cash generation: FCF to debt of 3.9% is below the peer median of 10.8% and the weakest of the group (3rd of 3), despite the improvement of 5.5 points over the year.
- Liquidity: cash liquidity to revenue fell by 1.2 points to 20.8%, the weakest of the group (3rd of 3).
- Investment: capex intensity rose by 1.6 points to 13.5%, above the peer median of 10.4%, which limits the room to rebuild free cash flow.
- Debt: total debt rose by 5.9% to EUR 15.5bn and net debt by 12.3% to EUR 8.7bn, so leverage depends on EBITDA holding at the FY2025 level.

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 8 errors | 12,743 / 3,366 |
| 2 | snapshot, operating_performance, peer_positioning | passed | 14,523 / 1,318 |
| 3 | operating_performance, peer_positioning | passed | 13,743 / 559 |

### Errors found, by try

Try 1:

- [rule 1] snapshot, sentence 1: word that states a number: 'one'
- [rule style] operating_performance, sentence 1: ebitda.change@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 1: ebitda@FY2025 is already given in credit_metrics, sentence 1: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 2: capex_intensity.change@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 2: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: advance_ticket_cover.peer_rank@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 3: fcf_to_debt@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)

Try 2:

- [rule style] operating_performance, sentence 2: capex_intensity.change@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] operating_performance, sentence 2: capex_intensity@FY2025 is already given in credit_metrics, sentence 4: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: advance_ticket_cover.peer_rank@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: advance_ticket_cover@FY2025 is already given in liquidity_funding, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- Air France-KLM, a network airline in the European peer group, grew revenue by {{revenue.change@FY2025}} to {{revenue@FY2025}} in FY2025 while EBITDA rose by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}, and net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- The point to watch is cash liquidity, which fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} of revenue, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, and operating profit rose by {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, yet gross leverage fell by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, and interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- Free cash flow turned positive at {{fcf@FY2025}} from {{fcf@FY2024}} in FY2024, taking FCF to debt to {{fcf_to_debt@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.

`operating_performance`

- Revenue grew by {{revenue.change@FY2025}} to {{revenue@FY2025}}, with the EBITDA margin widening by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}}.
- In FY2024 the group carried {{passengers@FY2024}} passengers with a fleet of {{fleet@FY2024}} aircraft at an average age of {{fleet_age@FY2024}}.

`liquidity_funding`

- Cash and cash-like investments were broadly unchanged at {{cash_like@FY2025}}, a change of {{cash_like.change@FY2025}}, so cash liquidity stood at {{cash_liquidity@FY2025}}.
- Cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, below the peer median of {{cash_liquidity_to_revenue.peer_median@FY2025}}.
- Contract liabilities rose by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, and advance ticket cover increased by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, the lowest of the peer group ({{advance_ticket_cover.peer_rank@FY2025}}).
- The group placed senior unsecured bonds under its EMTN programme and redeemed its outstanding hybrid bonds from the hard call date, while the extension option on its credit facility pushed that maturity to 2029.

`peer_positioning`

- Air France-KLM sits in the middle of the network group on EBITDA margin, net leverage, gross leverage, interest coverage and FFO to debt, each ranking {{net_leverage.peer_rank@FY2025}}.
- It is weakest on cash generation and liquidity, with FCF to debt below the peer median of {{fcf_to_debt.peer_median@FY2025}} and the lowest of the group ({{fcf_to_debt.peer_rank@FY2025}}), and cash liquidity to revenue the lowest as well ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).

`watch_items`

- Cash generation: FCF to debt of {{fcf_to_debt@FY2025}} is below the peer median of {{fcf_to_debt.peer_median@FY2025}} and the weakest of the group ({{fcf_to_debt.peer_rank@FY2025}}), despite the improvement of {{fcf_to_debt.change@FY2025}} over the year.
- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, the weakest of the group ({{cash_liquidity_to_revenue.peer_rank@FY2025}}).
- Investment: capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, above the peer median of {{capex_intensity.peer_median@FY2025}}, which limits the room to rebuild free cash flow.
- Debt: total debt rose by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, so leverage depends on EBITDA holding at the FY2025 level.
