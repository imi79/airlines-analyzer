"""The run manifest (M6): the audit stamp of one exported tearsheet.

It lists every filing and document behind a figure on the tearsheet (with its SHA-256
fingerprint), the AI models and prompt versions that touched it (drafting, extraction,
events), the fact sheet fingerprint and the draft's AI usage, the code version, the time of
the export, and whether the analyst's edits and view are included.
"""

from __future__ import annotations

import json
import os
import subprocess
from datetime import UTC, datetime
from functools import cache
from pathlib import Path

import yaml

from tearsheet.config import CONFIG, ROOT
from tearsheet.render import sources
from tearsheet.render.library import Library
from tearsheet.render.tearsheet import page_refs

ORIGINALS = ("tagged", "manual", "extracted")


@cache
def code_version() -> str:
    """The commit the export was made from (or TEARSHEET_COMMIT where git is unavailable)."""
    if os.environ.get("TEARSHEET_COMMIT"):
        return os.environ["TEARSHEET_COMMIT"]
    try:
        out = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, check=True, timeout=5)  # fmt: skip
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


@cache
def supplied_documents() -> dict[str, dict]:
    """Report PDFs supplied by Imane (config/report_documents.yaml), by document id."""
    path = CONFIG / "report_documents.yaml"
    docs = yaml.safe_load(path.read_text()).get("documents") or []
    return {d["id"]: d for d in docs}


def original_keys(lib: Library, ts: dict, refs: list[dict]) -> set[str]:
    """The stored figures at the bottom of every trail: filing facts, quotes, hand entries."""
    found: set[str] = set()
    seen: set[str] = set()
    todo = list(refs)
    while todo:
        ref = todo.pop()
        label = ref.get("key") or ref.get("fid") or repr(sorted(ref.items()))
        if label in seen:
            continue
        seen.add(label)
        if "key" in ref:
            f = lib.figures.get(ref["key"])
            if f is None:
                continue
            if f["source_type"] in ORIGINALS:
                found.add(ref["key"])
            todo += [{"key": k} for k in f.get("input_keys") or [] if k]
        else:
            todo += sources.card(lib, ts, ref)["inputs"]
    return found


def build(lib: Library, ts: dict, note: dict | None = None, mode: str = "demo",
          now: datetime | None = None, session_reviews: int = 0) -> dict:  # fmt: skip
    keys = original_keys(lib, ts, page_refs(lib, ts))
    filings: dict[str, dict] = {}
    documents: dict[str, dict] = {}
    extraction: dict[tuple, int] = {}
    for k in sorted(keys):
        f = lib.figures[k]
        if f["source_type"] in ("tagged", "manual"):
            rec = lib.filings.get(f["filing_id"] or "", {})
            entry = filings.setdefault(
                f["filing_id"],
                {
                    "company": rec.get("issuer"),
                    "fiscal_year": rec.get("fiscal_year"),
                    "origin": rec.get("origin"),
                    "sha256": rec.get("sha256"),
                    "link": rec.get("viewer_url") or rec.get("report_url"),
                    "figures": 0,
                },
            )
            entry["figures"] += 1
        else:
            src = f["source"]
            doc = src.get("document")
            entry = documents.setdefault(doc, _document(lib, doc, src.get("document_sha256")))
            entry["figures"] += 1
            model = (src.get("provider"), src.get("model"), src.get("prompt_version"))
            extraction[model] = extraction.get(model, 0) + 1
    for e in ts.get("events") or []:
        if e["status"] == "verified":
            documents.setdefault(e["document"], _document(lib, e["document"], None))
    run = ts.get("run") or {}
    events_ai = sorted({(e.get("model"), e.get("prompt_version")) for e in ts.get("events") or []
                        if e["status"] == "verified" and e.get("model")})  # fmt: skip
    edits = (note or {}).get("edits") or {}
    edited = sum(len(v) for v in edits.values())
    untraced = sum(1 for v in edits.values() for e in v.values() if e.get("untraced"))
    return {
        "tearsheet": {
            "company": ts["issuer"],
            "name": ts["name"],
            "fiscal_year": ts["fiscal_year"],
            "period": ts["period_label"],
            "currency": ts["currency"],
            "peer_group": ts["peer_group"],
            "peer_year": ts["peer_year"],
        },
        "exported_at": (now or datetime.now(UTC)).isoformat(timespec="seconds"),
        "code_version": code_version(),
        "mode": mode,
        "filings": filings,
        "documents": documents,
        "ai": {
            "drafting": {
                "provider": run.get("provider"),
                "model": run.get("model"),
                "prompt_version": run.get("prompt_version"),
                "calls": run.get("calls"),
                "input_tokens": run.get("input_tokens"),
                "output_tokens": run.get("output_tokens"),
                "cost_usd": run.get("cost_usd"),
                "recorded_at": run.get("recorded_at"),
            },
            "extraction": [
                {"provider": p, "model": m, "prompt_version": v, "figures": n}
                for (p, m, v), n in sorted(extraction.items(), key=lambda t: str(t[0]))
            ],
            "events": [{"model": m, "prompt_version": v} for m, v in events_ai],
        },
        "fact_sheet_fingerprint": run.get("input_hash"),
        "commentary_matches_figures": run.get("matches_figures"),
        "analyst": {
            "edited_sentences": edited,
            "sentences_with_untraced_figures": untraced,
            "analyst_view": bool((note or {}).get("analyst_view", "").strip()),
            "reviews_in_session_not_saved": session_reviews,
        },
        "figures_traced": len(keys),
    }


def _document(lib: Library, doc_id: str, sha: str | None) -> dict:
    if doc_id in lib.filings:
        rec = lib.filings[doc_id]
        return {"kind": "filing report", "sha256": sha or rec.get("sha256"),
                "link": rec.get("report_url") or rec.get("viewer_url"), "figures": 0}  # fmt: skip
    supplied = supplied_documents().get(doc_id, {})
    return {"kind": "report supplied by Imane", "file": supplied.get("file"),
            "sha256": sha or supplied.get("sha256"), "figures": 0}  # fmt: skip


def summary_line(m: dict) -> str:
    """One line for the PDF footnotes."""
    d = m["ai"]["drafting"]
    sources_count = len(m["filings"]) + len(m["documents"])
    return (
        f"Manifest: {m['figures_traced']} source figures from {sources_count} filings and "
        f"documents (SHA-256 in the Excel backup); commentary drafted by {d['model']}, "
        f"prompt {d['prompt_version']}, fact sheet {str(m['fact_sheet_fingerprint'])[:12]}; "
        f"code {m['code_version']}; exported {m['exported_at'][:16].replace('T', ' ')} UTC."
    )


def write(m: dict, folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    t = m["tearsheet"]
    path = folder / f"{t['company']}_FY{t['fiscal_year']}_manifest.json"
    path.write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    return path
