# International Airlines Group, FY2025: draft commentary

Status: passed the verifier. First try: rejected; tries: 3. Model deepseek-flash, prompt `draft-v6`, fact sheet `1bbd381c6a23` ([fact sheet](../factsheets/iag_FY2025.md)). Tokens: 43,450 in, 5,451 out.

Every figure below was written by code from the fact sheet; the AI wrote the words.

## Snapshot

International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2025 with a stronger credit profile as revenue rose by 3.5% to EUR 33.2bn.
The EBITDA margin widened by 2.3 points to 23.0% and net leverage fell by 0.35x to 0.78x.
The point to watch is liquidity: cash liquidity to revenue fell by 5.6 points to 25.0% as cash was returned to shareholders.

> Event `event:capital_returns`: The company announced a share buyback and a further return of excess cash to shareholders in the coming year. Quote (page 12): "Last February we announced a €1 billion share buyback and we are pleased to be announcing another return of excess cash of €1.5 billion today. This takes the total amount of excess cash returns announced in the last three years to €2.85 billion as we build a track record of cash returns to shareholders."

## Credit metrics

EBITDA increased by 15.1% to EUR 7.7bn, with operating profit up 17.3% to EUR 5.0bn.
Total debt was reduced by 17.7% to EUR 14.3bn and net debt by 20.9% to EUR 5.9bn, taking gross leverage down by 0.75x to 1.86x.
FFO rose by 15.3% to EUR 6.5bn, lifting FFO to debt by 13.0 points to 45.5%, and interest coverage improved by 2.79x to 11.49x.
Free cash flow declined by 11.5% to EUR 3.1bn as capex intensity rose by 1.6 points to 10.4%, although FCF to debt still improved to 22.1%.

## Operating performance

Capacity grew by 2.4% to 351.4bn available seat kilometres, while passengers were broadly unchanged at 121.6m and RPK were broadly unchanged at 300.8bn.
Unit revenue held up, with RASK up 1.1% to 9.45 euro cents and passenger yield up 1.1% to 9.63 euro cents.
CASK fell by 1.0% to 8.02 euro cents, but CASK ex-fuel rose by 2.0% to 6.01 euro cents and the fuel share of costs eased by 2.3 points to 25.1%.
The fleet grew by 4.3% to 627 aircraft at an average age of 12.6 years, with supply chain pressures and engine problems limiting availability during the year.

> Event `event:fleet_and_engines`: British Airways reduced frequencies to some Middle East destinations because of a lack of available aircraft following Rolls Royce engine problems, while Boeing and Airbus reported delivery shortfalls. Quote (page 44): "Supply chain pressures continued in 2025. British Airways reduced frequencies to some Middle East destinations due to a lack of available aircraft after experiencing Rolls Royce engine problems, and Boeing and Airbus reported delivery shortfalls."

## Liquidity and funding

Liquidity fell by 17.2% to EUR 10.9bn, of which EUR 2.6bn in undrawn committed facilities, down 22.7%.
Cash and cash-like investments declined by 15.4% to EUR 8.3bn, taking cash liquidity to revenue down by 5.6 points to 25.0%.
Advance ticket cover rose by 11.8 points to 96.6%, while contract liabilities fell by 3.6% to EUR 8.0bn, so a larger share of the cash base is customers' prepayments.

## Peer positioning

IAG leads the network airlines on EBITDA margin (1st of 3), net leverage (1st of 3) and FFO to debt (1st of 3).
Gross leverage is below the peer median of 3.07x, and interest coverage exceeds the median of 8.06x.
The weakest position is advance ticket cover, the highest of the group (3rd of 3), while cash liquidity to revenue of 25.0% sits in the middle of the group.

> verifier: [rule style] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2025 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)

## Watch items

- Liquidity: cash liquidity to revenue fell by 5.6 points to 25.0%, and undrawn committed facilities were reduced by 22.7% to EUR 2.6bn.
- Customer prepayments: advance ticket cover of 96.6% is above the peer median of 67.4% and the highest of the group (3rd of 3), a sensitivity if bookings slow.
- Cash generation: free cash flow declined by 11.5% to EUR 3.1bn as capex intensity rose by 1.6 points to 10.4%.
- Cost base: CASK ex-fuel rose by 2.0% to 6.01 euro cents, and disruption from air traffic control strikes added direct costs during the year.

> Event `event:one_offs`: A July strike by air traffic control in France led to large daily cancellations and direct costs for the group. Quote (page 45): "ATC strikes caused significant disruption, especially in France, where a July strike resulted in 1,400 daily cancellations and over €120 million in direct costs for the"

## Analyst view

_Left for the analyst: never drafted._

## How each try went

| Try | Sections asked | Verifier | Tokens |
| --- | --- | --- | --- |
| 1 | snapshot, credit_metrics, operating_performance, liquidity_funding, peer_positioning, watch_items | 6 errors | 13,729 / 3,345 |
| 2 | operating_performance, peer_positioning, watch_items | 3 errors | 15,579 / 1,684 |
| 3 | peer_positioning | passed | 14,142 / 422 |

### Errors found, by try

Try 1:

- [rule 4] operating_performance, sentence 1: 'rose' needs a 'up' claim on a figure in the same clause
- [rule style] peer_positioning, sentence 2: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: interest_coverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: capex_intensity@FY2025 is listed in the form but not used in the text
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2025 is listed in the form but not used in the text
- [rule 5] watch_items, sentence 2: advance_ticket_cover.peer_rank@FY2025 is listed in the form but not used in the text

Try 2:

- [rule style] peer_positioning, sentence 2: gross_leverage@FY2025 is already given in credit_metrics, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule style] peer_positioning, sentence 2: interest_coverage@FY2025 is already given in credit_metrics, sentence 3: give each figure in one body section only (the snapshot and watch items may restate it)
- [rule 5] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2025 is listed in the form but not used in the text

Try 3:

- [rule style] peer_positioning, sentence 3: cash_liquidity_to_revenue@FY2025 is already given in liquidity_funding, sentence 2: give each figure in one body section only (the snapshot and watch items may restate it)

### Text with blanks (as the AI wrote it)

`snapshot`

- International Airlines Group, the owner of British Airways, Iberia and Aer Lingus, ended FY2025 with a stronger credit profile as revenue rose by {{revenue.change@FY2025}} to {{revenue@FY2025}}.
- The EBITDA margin widened by {{ebitda_margin.change@FY2025}} to {{ebitda_margin@FY2025}} and net leverage fell by {{net_leverage.change@FY2025}} to {{net_leverage@FY2025}}.
- The point to watch is liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}} as cash was returned to shareholders.

`credit_metrics`

- EBITDA increased by {{ebitda.change@FY2025}} to {{ebitda@FY2025}}, with operating profit up {{operating_profit.change@FY2025}} to {{operating_profit@FY2025}}.
- Total debt was reduced by {{total_debt.change@FY2025}} to {{total_debt@FY2025}} and net debt by {{net_debt.change@FY2025}} to {{net_debt@FY2025}}, taking gross leverage down by {{gross_leverage.change@FY2025}} to {{gross_leverage@FY2025}}.
- FFO rose by {{ffo.change@FY2025}} to {{ffo@FY2025}}, lifting FFO to debt by {{ffo_to_debt.change@FY2025}} to {{ffo_to_debt@FY2025}}, and interest coverage improved by {{interest_coverage.change@FY2025}} to {{interest_coverage@FY2025}}.
- Free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}, although FCF to debt still improved to {{fcf_to_debt@FY2025}}.

`operating_performance`

- Capacity grew by {{ask.change@FY2025}} to {{ask@FY2025}} available seat kilometres, while passengers were broadly unchanged at {{passengers@FY2025}} and RPK were broadly unchanged at {{rpk@FY2025}}.
- Unit revenue held up, with RASK up {{rask.change@FY2025}} to {{rask@FY2025}} and passenger yield up {{passenger_yield.change@FY2025}} to {{passenger_yield@FY2025}}.
- CASK fell by {{cask.change@FY2025}} to {{cask@FY2025}}, but CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}} and the fuel share of costs eased by {{fuel_share_of_costs.change@FY2025}} to {{fuel_share_of_costs@FY2025}}.
- The fleet grew by {{fleet.change@FY2025}} to {{fleet@FY2025}} aircraft at an average age of {{fleet_age@FY2025}}, with supply chain pressures and engine problems limiting availability during the year.

`liquidity_funding`

- Liquidity fell by {{liquidity.change@FY2025}} to {{liquidity@FY2025}}, of which {{undrawn_facilities@FY2025}} in undrawn committed facilities, down {{undrawn_facilities.change@FY2025}}.
- Cash and cash-like investments declined by {{cash_like.change@FY2025}} to {{cash_like@FY2025}}, taking cash liquidity to revenue down by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}.
- Advance ticket cover rose by {{advance_ticket_cover.change@FY2025}} to {{advance_ticket_cover@FY2025}}, while contract liabilities fell by {{contract_liabilities.change@FY2025}} to {{contract_liabilities@FY2025}}, so a larger share of the cash base is customers' prepayments.

`peer_positioning`

- IAG leads the network airlines on EBITDA margin ({{ebitda_margin.peer_rank@FY2025}}), net leverage ({{net_leverage.peer_rank@FY2025}}) and FFO to debt ({{ffo_to_debt.peer_rank@FY2025}}).
- Gross leverage is below the peer median of {{gross_leverage.peer_median@FY2025}}, and interest coverage exceeds the median of {{interest_coverage.peer_median@FY2025}}.
- The weakest position is advance ticket cover, the highest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), while cash liquidity to revenue of {{cash_liquidity_to_revenue@FY2025}} sits in the middle of the group.

`watch_items`

- Liquidity: cash liquidity to revenue fell by {{cash_liquidity_to_revenue.change@FY2025}} to {{cash_liquidity_to_revenue@FY2025}}, and undrawn committed facilities were reduced by {{undrawn_facilities.change@FY2025}} to {{undrawn_facilities@FY2025}}.
- Customer prepayments: advance ticket cover of {{advance_ticket_cover@FY2025}} is above the peer median of {{advance_ticket_cover.peer_median@FY2025}} and the highest of the group ({{advance_ticket_cover.peer_rank@FY2025}}), a sensitivity if bookings slow.
- Cash generation: free cash flow declined by {{fcf.change@FY2025}} to {{fcf@FY2025}} as capex intensity rose by {{capex_intensity.change@FY2025}} to {{capex_intensity@FY2025}}.
- Cost base: CASK ex-fuel rose by {{cask_ex_fuel.change@FY2025}} to {{cask_ex_fuel@FY2025}}, and disruption from air traffic control strikes added direct costs during the year.
