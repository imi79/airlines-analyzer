"""Method page: definitions, data sources, limits and disclaimer (read only)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tearsheet.app import state
from tearsheet.app.cards import safe
from tearsheet.metrics.engine import load_catalog
from tearsheet.narrative.factsheet import FactSheet
from tearsheet.render import verifier_demo

lib = state.get_library()
st.title("Method")

st.markdown(
    """
**What this is.** A two-page credit tearsheet for European listed airlines and airports, built
from their annual filings (ESEF and UKSEF). Code computes every number; an AI model reads what
the filings don't tag and drafts the commentary; a verifier checks every figure the model
touches. The analyst view is written by the analyst only.

**Data sources.**
- Annual filings from [filings.xbrl.org](https://filings.xbrl.org): the tagged statements, read
  figure by figure, and a link to each filing in the iXBRL viewer.
- The annual report text, for figures the filings don't tag (traffic, fleet, fuel hedging,
  undrawn credit lines, airport segments). Read by the AI with the exact sentence it came
  from; code checks the sentence is in the report, the figure is in the sentence and the year
  matches. A figure that fails a check stays off the tearsheet until the analyst reviews it.
- Where no electronic filing exists (Air France-KLM and Groupe ADP, FY2025), figures entered
  by hand from the published statements, with the page, and reviewed.

**How the commentary is written.** The AI writes sentences with blanks such as
`{{net_leverage@FY2025}}`; code fills each blank from the facts. The verifier rejects any
number written outside a blank, any blank that is not a checked figure, and any direction
("improved", "fell") that contradicts the computed change. A rejected section goes back to
the AI up to two times; a sentence still failing is removed.

**Watchlist.** Credit triggers set by the analyst (config/watchlist.yaml), such as net
leverage above 3.0x or EBITDA margin down more than 3 points on the year, checked by code for
every company and year from verified figures only. A trigger whose figure is missing, not
meaningful or awaiting review shows as "cannot assess" with the reason, never as clear
(decision 0023).

**Half-year and LTM (last twelve months).** For the latest view of a company, the tool reads
its half-year report: LTM earnings and cash flows = last full year + this first half − last
year's first half; debt and cash are taken at the half-year date. The AI only points to the
rows of the half-year statements; code reads the amounts and checks each row against the last
annual figures. Half-year statements are **unaudited**, and they give no undrawn credit lines
or maturity table, so some figures are missing at LTM, with the reason (decision 0025).

**Peers.** Network airlines, low-cost airlines and airports are compared separately, plus an
all-airlines view. Each company's fiscal year is placed in the peer year whose 31 December
falls within six months of its year end. Medians and ranks use verified figures only.

**Limits.** Annual figures only (no half-year or LTM). The tool's own definitions, applied
identically to every company: they differ from company-reported and rating-agency-adjusted
figures (no pension or hybrid adjustments). No prices or spreads. Ratings (from M8) are copied
from each company's own annual report, with the page and the date, and shown only after the
analyst's review; they are a record of a public rating, never ranked or compared.

**Cash flow after leases and refinancing (M8).** Lease payments sit in financing cash flows,
so free cash flow flatters companies that lease their aircraft: FCF after leases takes them
out, and interest paid where a company shows it in financing. The maturity wall is read from
the debt note by the AI and checked by code: quotes word for word, column labels read as time
spans by code, each row footed, and the table compared with the balance sheet; a table that
fails stays off the page until reviewed.

**Disclaimer.** Draft prepared with AI assistance. Figures computed from regulatory filings and
checked automatically. Not investment advice.
"""
)

st.subheader("Metric definitions")
catalog = load_catalog()
rows = []
for spec in catalog.values():
    applies = spec.get("applies_to")
    rows.append(
        {
            "Metric": spec["label"],
            "Definition": " ".join(str(spec["definition"]).split()),
            "Applies to": ", ".join(applies) if applies else "airlines and airports",
            "Higher is better": {True: "yes", False: "no", None: "–"}[spec["higher_is_better"]],
        }
    )
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", height=600)
st.caption(safe(f"{len(rows)} metrics, from src/tearsheet/metrics/catalog.yaml."))


# --- Try the verifier (M7) ---------------------------------------------------------------------
st.subheader("Try the verifier")
issuer, year = state.current()
ts = state.get_tearsheet(issuer, year)
sheet = FactSheet.from_dict(ts["factsheet"])
st.markdown(
    f"The AI writes sentences with blanks such as `{{{{net_leverage@FY{year}}}}}`; code fills "
    f"them from the checked figures. Put a sentence through the verifier on "
    f"**{safe(ts['name'])} {safe(ts['period_label'])}**: pick an example, or write your own."
)
demos = verifier_demo.examples(sheet)
choice = st.selectbox(
    "Example",
    range(len(demos)),
    format_func=lambda n: demos[n]["name"],
    key=f"verifier-example-{issuer}-{year}",
)
text = st.text_area(
    "Sentence, with figures as {{blanks}}",
    demos[choice]["text"] if demos else "",
    key=f"verifier-text-{issuer}-{year}-{choice}",
    height=80,
)
with st.expander("Figures this tearsheet's sentences may use"):
    usable = [i for i in sheet.items.values() if i.kind != "event"]
    st.dataframe(
        pd.DataFrame(
            [
                {"Blank": "{{" + i.id + "}}", "Prints as": i.rendered, "What it is": i.label}
                for i in usable
            ]  # fmt: skip
        ),
        hide_index=True,
        width="stretch",
        height=260,
    )
if st.button("Check with the verifier", key=f"verifier-check-{issuer}-{year}", type="primary"):
    verdict = verifier_demo.check(sheet, text)
    if not verdict:
        filled = verifier_demo.fill(text, {i.id: i.rendered for i in sheet.items.values()})
        st.success("Passes: this sentence would reach the tearsheet as")
        st.markdown(f"> {safe(filled)}")
    else:
        st.error(f"Rejected: {len(verdict)} problem(s). The AI would get this list back and "
                 "rewrite the sentence.")  # fmt: skip
        for v in verdict:
            st.markdown(f"- **Rule {v['rule']}: {safe(v['title'])}**: {safe(v['message'])}")
st.caption(
    "The form the AI fills in also states the direction it claims for each figure; here it "
    "is set to the direction computed by code, so only what the sentence says can be wrong."
)
