"""Method page: definitions, data sources, limits and disclaimer (read only)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from tearsheet.app import state
from tearsheet.app.cards import safe
from tearsheet.metrics.engine import load_catalog

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

**Peers.** Network airlines, low-cost airlines and airports are compared separately, plus an
all-airlines view. Each company's fiscal year is placed in the peer year whose 31 December
falls within six months of its year end. Medians and ranks use verified figures only.

**Limits.** Annual figures only (no half-year or LTM). The tool's own definitions, applied
identically to every company: they differ from company-reported and rating-agency-adjusted
figures (no pension or hybrid adjustments). No ratings, prices or spreads.

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
