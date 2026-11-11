"""M6 checklist: the manifest lists filing hashes, model and prompt version."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from tearsheet.llm.client import RECORDS
from tearsheet.narrative.drafting import PROMPT_VERSION
from tearsheet.render import manifest, tearsheet
from tearsheet.render.library import Library

TEARSHEETS = tearsheet.available()


@pytest.fixture(scope="module")
def lib() -> Library:
    return Library.read()


@pytest.fixture(scope="module")
def recorded() -> set[tuple[str, str]]:
    """(model, prompt version) of every recorded AI answer."""
    out = set()
    for path in RECORDS.glob("*.json"):
        r = json.loads(path.read_text())
        out.add((r.get("served_model") or r["request"]["model"], r["request"]["prompt_version"]))
    return out


@pytest.mark.parametrize(("issuer", "year"), TEARSHEETS)
def test_manifest_lists_every_source_with_its_fingerprint(lib, recorded, issuer, year):
    ts = tearsheet.read(issuer, year)
    m = manifest.build(lib, ts, now=datetime(2026, 11, 10, tzinfo=UTC))
    keys = manifest.original_keys(lib, ts, tearsheet.page_refs(lib, ts))
    assert m["figures_traced"] == len(keys) > 30
    for k in keys:
        f = lib.figures[k]
        where = m["filings"] if f["source_type"] != "extracted" else m["documents"]
        doc = f["filing_id"] if f["source_type"] != "extracted" else f["source"]["document"]
        assert doc in where, f"{k}: {doc} missing from the manifest"
    for entry in list(m["filings"].values()) + list(m["documents"].values()):
        assert entry["sha256"] and len(entry["sha256"]) == 64
    d = m["ai"]["drafting"]
    # M8: four sections from draft-v7, liquidity and watch items from draft-v8 (decision 0022)
    assert d["prompt_version"].startswith(f"{PROMPT_VERSION} + draft-v8")
    assert (d["model"], "draft-v8") in recorded
    for e in m["ai"]["extraction"] + m["ai"]["events"]:
        assert (e["model"], e["prompt_version"]) in recorded
    assert m["commentary_matches_figures"] is True
    assert m["code_version"]


def test_manifest_counts_the_analyst_edits(lib):
    ts = tearsheet.read("afkl", 2025)
    note = {
        "analyst_view": "Stable.",
        "edits": {
            "snapshot": {
                1: {"text": "x", "untraced": []},
                2: {"text": "y 1.5x", "untraced": ["1.5x"]},
            }
        },
    }
    m = manifest.build(lib, ts, note)
    assert m["analyst"] == {"edited_sentences": 2, "sentences_with_untraced_figures": 1,
                            "analyst_view": True, "reviews_in_session_not_saved": 0}  # fmt: skip
    assert "prompt draft-v7" in manifest.summary_line(m)
