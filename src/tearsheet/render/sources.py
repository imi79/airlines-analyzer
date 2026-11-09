"""Source cards: the audit trail of one figure, as the app shows it on click.

A card says what the figure is and where it came from, in plain words, and lists the figures
it was built from as links to their own cards, down to the filing fact, the quote from the
report or the hand entry. Cards are built from the library and the tearsheet record only, so
demo mode and live mode show the same trail.

Figures on the page are referred to in two ways:

    library key    afkl:net_leverage@FY2025         a stored figure (any company, any year)
    fact sheet id  net_leverage.change@FY2025       a figure of the commentary: a level, a change,
                                                    a peer median or rank, or an event
"""

from __future__ import annotations

from decimal import Decimal
from functools import cache

from tearsheet.narrative.factsheet import load_narrative as _load_narrative
from tearsheet.render.library import Library, key, members_year, small_debt, split


@cache
def load_narrative() -> dict:
    return _load_narrative()


SOURCE_WORDS = {
    "tagged": "Tagged in the filing",
    "computed": "Computed by code",
    "extracted": "Read from the report text by the AI, then checked by code",
    "manual": "Entered by hand from the published statements",
}
STATUS_WORDS = {
    "verified": "verified",
    "overridden": "approved by Imane",
    "unverified": "not verified yet: waiting for Imane's review, kept off the tearsheet",
}
ENDPOINTS = ("tagged", "extracted", "manual")


def ref_of_key(figure_key: str) -> dict:
    return {"key": figure_key}


def ref_of_id(fid: str) -> dict:
    return {"fid": fid}


# --- Cards for stored figures ------------------------------------------------------------------


def figure_card(lib: Library, figure_key: str) -> dict:
    f = lib.figure(figure_key)
    issuer, concept, year = split(figure_key)
    name = lib.issuers.get(issuer, {}).get("name", issuer)
    if f is None:
        return {
            "kind": "missing",
            "title": f"{lib.label.get(concept, concept)}, {name} FY{year}",
            "rendered": "n.a.",
            "lines": [f"No figure: {lib.why_missing(figure_key)}"],
            "inputs": [],
        }
    card = {
        "kind": f["source_type"],
        "title": f"{f['label']}, {name} {lib.period_label(issuer, year)}",
        "rendered": f["rendered"],
        "value": f["value"],
        "status": f["status"],
        "how": SOURCE_WORDS.get(f["source_type"], f["source_type"]),
        "status_text": STATUS_WORDS.get(f["status"], f["status"]),
        "definition": lib.definition.get(concept) or None,
        "lines": [],
        "inputs": [],
        "link": None,
    }
    src = f["source"]
    filing = lib.filings.get(f["filing_id"] or "", {})
    if f["source_type"] == "tagged":
        concepts = ", ".join(src.get("concepts") or [])
        card["lines"] += [
            f"Filing: {f['filing_id']} ({filing.get('origin', 'filing')})",
            f"Tagged as: {concepts}",
            f"Value as tagged: {_plain(f['value_tagged'])} {f['currency']}"
            + (f", decimals {f['decimals']}" if f["decimals"] is not None else ""),
            f"Period end: {f['period_end']}",
        ]
        if src.get("sha256"):
            card["lines"].append(f"Filing fingerprint (SHA-256): {src['sha256']}")
        card["link"] = filing.get("viewer_url") or filing.get("report_url")
    elif f["source_type"] == "manual":
        page = ", ".join(src.get("fact_ids") or [])
        label = ", ".join(src.get("concepts") or [])
        card["lines"] += [
            f"Document: {filing.get('choice_reason') or f['filing_id']}",
            f"Line: “{label}”, {page}",
            f"Entered on {filing.get('date_added', 'n.a.')}; prior-year column checked against "
            "the database (decision 0007)",
        ]
    elif f["source_type"] == "extracted":
        quotes = src.get("quotes") or []
        locations = src.get("locations") or []
        card["lines"].append(f"Document: {src.get('document')}")
        for q, loc in zip(quotes, locations, strict=False):
            card["lines"].append(f"Quote ({loc or 'location not found'}): “{q.strip()}”")
        if src.get("printed"):
            card["lines"].append(f"Printed as: {src['printed']}")
        if src.get("scope"):
            card["lines"].append(f"Scope: {src['scope']}")
        if src.get("model"):
            card["lines"].append(
                f"Read by {src.get('provider', '')} {src['model']}, prompt "
                f"{src.get('prompt_version', '')}"
            )
        for why in src.get("checks_failed") or []:
            card["lines"].append(f"Check failed: {why}")
        review = src.get("review")
        if review:
            card["lines"].append(f"Review: {review}")
        card["quotes"] = [q.strip() for q in quotes if q and q.strip()]
        card["link"] = filing.get("report_url") or filing.get("viewer_url")
    elif f["source_type"] == "computed":
        if f.get("note"):
            card["lines"].append(f"Calculation: {f['note']}")
        for inp, link in zip(src.get("inputs") or [], f.get("input_keys") or [], strict=False):
            if link:
                card["inputs"].append(ref_of_key(link))
            else:
                card["lines"].append(f"Input {inp['name']}: {_plain(inp['value'])} (not linked)")
    tiny = small_debt(lib, issuer, concept, year)
    if tiny:
        card["lines"].append(f"Shown as {tiny}; left out of peer medians and ranks")
    if f.get("footnote"):
        card["lines"].append(f"Note: {f['footnote']}")
    if f.get("restated"):
        card["lines"].append("Restated: a later filing gives a different value; the latest is used")
    if f.get("comparative"):
        card["lines"].append("Read from the prior-year column of the next year's filing")
    return card


def _plain(value) -> str:
    v = Decimal(str(value))
    return f"{v:,.0f}" if v == v.to_integral() else f"{v:,f}".rstrip("0")


# --- Cards for the commentary's figures --------------------------------------------------------


def item_card(lib: Library, ts: dict, fid: str) -> dict:
    """The card of a fact sheet id (a figure used in the commentary)."""
    sheet = ts["factsheet"]
    issuer = ts["issuer"]
    item = sheet["items"].get(fid)
    if item is None:
        reason = sheet["unavailable"].get(fid, "not in the fact sheet")
        return {"kind": "missing", "title": fid, "rendered": "n.a.", "lines": [reason],
                "inputs": []}  # fmt: skip
    kind = item["kind"]
    if kind == "value":
        year = int(item["period"].removeprefix("FY"))
        k = key(issuer, item["metric"], year)
        if k in lib.figures:
            return figure_card(lib, k)
        return _derived(lib, ts, item, year)
    if kind == "change":
        prior, current = item["period"].split(" to ")
        refs = [ref_of_id(f"{item['metric']}@{prior}"), ref_of_id(f"{item['metric']}@{current}")]
        words = {"up": "up", "down": "down", "flat": "stable"}
        return {
            "kind": "change",
            "title": item["label"][:1].upper() + item["label"][1:],
            "rendered": item["rendered"],
            "how": "Computed by code from the two years below",
            "lines": [
                f"Direction: {words.get(item['direction'], item['direction'])}"
                + (f", {item['assessment']}" if item["assessment"] != "neutral" else ""),
                "Changes in percentages are in points; changes in amounts and traffic are a "
                "share of the prior year; flat below the threshold in catalog.yaml",
            ],
            "inputs": refs,
        }
    if kind in ("peer_median", "peer_rank"):
        return _peer_card(lib, ts, item)
    if kind == "event":
        summary, _, quote = item["note"].partition(" Quote ")
        return {
            "kind": "event",
            "title": item["label"],
            "rendered": "",
            "how": "Read from the report by the AI; the quote was found in the report by code",
            "lines": [summary, f"Quote {quote}"],
            "quotes": [quote],
            "inputs": [],
        }
    return {"kind": kind, "title": item["label"], "rendered": item["rendered"], "lines": [],
            "inputs": []}  # fmt: skip


def _derived(lib: Library, ts: dict, item: dict, year: int) -> dict:
    """A fact sheet level not stored as such: net cash (net debt with the sign reversed)."""
    narrative = load_narrative()
    source = (narrative.get("net_cash") or {}).get("from")
    if item["metric"] == "net_cash" and source:
        return {
            "kind": "derived",
            "title": item["label"],
            "rendered": item["rendered"],
            "how": "Net debt below zero, shown as net cash (a positive figure)",
            "lines": [],
            "inputs": [ref_of_key(key(ts["issuer"], source, year))],
        }
    return {"kind": "missing", "title": item["label"], "rendered": item["rendered"],
            "lines": ["not found in the figure library"], "inputs": []}  # fmt: skip


def peer_members(lib: Library, ts: dict, metric: str) -> tuple[list[str], list[tuple[str, str]]]:
    """The library keys behind a fact sheet's peer median and rank, as M4 computed them, and
    the companies left out with the reason."""
    narrative = load_narrative()
    rule = narrative.get("small_debt") or {}
    debt_ratios = set(rule.get("metrics") or ())
    limit = Decimal(str(rule["gross_leverage_below"])) if rule else None
    used, left_out = [], []
    for member in ts["peer_members"]:
        fy = members_year(lib, member, ts["peer_year"])
        if fy is None:
            continue
        k = key(member, metric, fy)
        if k not in lib.figures:
            continue
        gross = lib.figures.get(key(member, "gross_leverage", fy))
        if metric in debt_ratios and limit is not None and gross is not None:
            if Decimal(gross["value"]) < limit:
                left_out.append((member, "debt is very small, so ratios to debt say little"))
                continue
        used.append(k)
    return used, left_out


def _peer_card(lib: Library, ts: dict, item: dict) -> dict:
    used, left_out = peer_members(lib, ts, item["metric"])
    lines = [
        f"Peer group: {ts['peer_group']}, peer year {ts['peer_year']} (each company's fiscal "
        "year whose 31 December falls within six months of its year end, decision 0008)",
    ]
    if item["kind"] == "peer_median":
        lines.append(f"Median of the {len(used)} companies below")
    else:
        better = lib.higher_is_better.get(item["metric"])
        lines.append(
            f"Rank among the {len(used)} companies below; 1st is the "
            f"{'highest' if better else 'lowest'} value"
        )
    for member, why in left_out:
        lines.append(f"Left out: {lib.issuers[member]['name']} ({why})")
    return {
        "kind": item["kind"],
        "title": item["label"],
        "rendered": item["rendered"],
        "how": "Computed by code from the peers' figures",
        "lines": lines,
        "inputs": [ref_of_key(k) for k in used],
    }


def peer_median_card(lib: Library, table: dict, row: dict) -> dict:
    """The card of a median on the Peers page."""
    used = [c["key"] for c in row["cells"].values() if c.get("rendered")]
    return {
        "kind": "peer_median",
        "title": f"{row['label']}, median of {table['label'].lower()}, peer year "
        f"{table['peer_year']}",
        "rendered": row["median_rendered"] or "n.a.",
        "how": "Computed by code from the verified figures below",
        "lines": [f"Median of {len(used)} companies; figures awaiting review are left out"],
        "inputs": [ref_of_key(k) for k in used],
    }


# --- Following a card down to its sources --------------------------------------------------------


def ref_of_peer_median(group: str, peer_year: int, metric: str) -> dict:
    return {"peer": group, "year": peer_year, "metric": metric}


def card(lib: Library, ts: dict | None, ref: dict) -> dict:
    if "key" in ref:
        return figure_card(lib, ref["key"])
    if "peer" in ref:
        from tearsheet.render.library import peer_table

        table = peer_table(lib, ref["peer"], ref["year"])
        row = next(r for r in table["rows"] if r["metric"] == ref["metric"])
        return peer_median_card(lib, table, row)
    if ts is None:
        raise ValueError("a fact sheet id needs its tearsheet")
    return item_card(lib, ts, ref["fid"])


def endpoints(lib: Library, ts: dict | None, ref: dict, seen: set | None = None) -> list[dict]:
    """Follow a card's inputs down to the cards with no inputs (the original sources)."""
    seen = set() if seen is None else seen
    label = ref.get("key") or ref.get("fid") or repr(sorted(ref.items()))
    if label in seen:
        return []
    seen.add(label)
    c = card(lib, ts, ref)
    if not c["inputs"]:
        return [c]
    out = []
    for inp in c["inputs"]:
        out += endpoints(lib, ts, inp, seen)
    return out


def traced(c: dict) -> bool:
    """An original source a reader can check: a filing fact, a quote, a hand entry, an event."""
    if c["kind"] in ENDPOINTS:
        if c["kind"] == "extracted":
            return bool(c.get("quotes"))
        return bool(c["lines"])
    return c["kind"] == "event" and bool(c.get("quotes"))
