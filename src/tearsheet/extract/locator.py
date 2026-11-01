"""Section locator: find the few passages of a report worth sending to the AI.

For each figure, it looks for the terms in items.yaml (report language, plus English), takes a
window of text around each hit, scores windows (more numbers, the fiscal year mentioned and
several of the figure's terms score higher), and keeps the best few. Matching ignores spaces,
because some reports split words ('tr affic'). The AI sees a few pages, not the whole report.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from tearsheet.extract.documents import Document
from tearsheet.extract.numbers import number_tokens, year_marks

ITEMS = Path(__file__).with_name("items.yaml")

BEFORE, AFTER = 600, 900  # characters kept around a hit
PER_ITEM = 4  # best windows kept per figure
MAX_CHARS = 60_000  # total sent per report (about 15,000 tokens)


def load_items(path: Path = ITEMS) -> dict[str, dict]:
    return yaml.safe_load(path.read_text())["items"]


def items_for(issuer_type: str, items: dict[str, dict] | None = None) -> dict[str, dict]:
    items = items or load_items()
    return {k: v for k, v in items.items() if issuer_type in v["applies_to"]}


def terms_for(item: dict, language: str | None) -> list[str]:
    terms = list(item["terms"].get(language or "en", []))
    for t in item["terms"].get("en", []):
        if t not in terms:
            terms.append(t)
    return terms


def _squashed(text: str) -> tuple[str, list[int]]:
    """Lower-case text without whitespace, and for each kept character its original index."""
    chars, index = [], []
    for i, ch in enumerate(text):
        if not ch.isspace():
            chars.append(ch.lower())
            index.append(i)
    return "".join(chars), index


def find_terms(page: str, terms: list[str]) -> list[tuple[int, str]]:
    """(position, term) of every hit. Acronyms match case-sensitively as whole words."""
    hits = []
    flat, index = None, None
    for term in terms:
        if term.isupper() and len(term) <= 5:
            for m in re.finditer(rf"(?<![A-Za-z]){re.escape(term)}s?(?![A-Za-z])", page):
                hits.append((m.start(), term))
            continue
        if flat is None:
            flat, index = _squashed(page)
        needle = re.sub(r"\s+", "", term.lower())
        start = flat.find(needle)
        while start >= 0:
            hits.append((index[start], term))
            start = flat.find(needle, start + 1)
    return sorted(hits)


@dataclass
class Window:
    page: int
    start: int
    end: int
    score: float
    items: set[str] = field(default_factory=set)


def _score(text: str, item_terms: list[str], fiscal_year: int, language: str | None) -> float:
    numbers = len(number_tokens(text, language))
    years = {m.year for m in year_marks(text)}
    distinct_terms = len({t for _, t in find_terms(text, item_terms)})
    score = min(numbers, 25) / 5 + 2 * distinct_terms
    if fiscal_year in years:
        score += 3
    if fiscal_year - 1 in years:
        score += 1
    if numbers == 0:
        score -= 5
    return score


def locate(doc: Document, items: dict[str, dict], fiscal_year: int | None = None) -> list[Window]:
    """The windows to send for these items, in page order, within MAX_CHARS."""
    fiscal_year = fiscal_year or doc.fiscal_year
    chosen: list[Window] = []
    for item_id, item in items.items():
        terms = terms_for(item, doc.language)
        candidates = []
        for p, page in enumerate(doc.pages):
            for pos, _ in find_terms(page, terms):
                start = page.rfind("\n", 0, max(0, pos - BEFORE)) + 1
                end = page.find("\n", min(len(page), pos + AFTER))
                end = len(page) if end < 0 else end
                text = page[start:end]
                score = _score(text, terms, fiscal_year, doc.language)
                candidates.append(Window(p, start, end, score, {item_id}))
        candidates.sort(key=lambda w: -w.score)
        kept: list[Window] = []
        for w in candidates:
            if len(kept) == PER_ITEM:
                break
            if any(k.page == w.page and k.start < w.end and w.start < k.end for k in kept):
                continue
            kept.append(w)
        chosen.extend(kept)
    return _merge_and_cap(chosen)


def _merge_and_cap(windows: list[Window]) -> list[Window]:
    windows = sorted(windows, key=lambda w: (w.page, w.start))
    merged: list[Window] = []
    for w in windows:
        last = merged[-1] if merged else None
        if last and last.page == w.page and w.start <= last.end:
            last.end = max(last.end, w.end)
            last.score = max(last.score, w.score)
            last.items |= w.items
        else:
            merged.append(Window(w.page, w.start, w.end, w.score, set(w.items)))
    total = sum(w.end - w.start for w in merged)
    if total <= MAX_CHARS:
        return merged
    # Drop the weakest windows, but keep at least one window per item.
    keep = sorted(merged, key=lambda w: -w.score)
    result, size, covered = [], 0, set()
    for w in keep:
        length = w.end - w.start
        if size + length <= MAX_CHARS or not (w.items <= covered):
            result.append(w)
            size += length
            covered |= w.items
    return sorted(result, key=lambda w: (w.page, w.start))


def render(doc: Document, windows: list[Window]) -> str:
    """The passages as sent to the AI, each headed with its location."""
    blocks = []
    for w in windows:
        text = doc.pages[w.page][w.start : w.end].strip()
        blocks.append(f"=== {doc.location(w.page)} ===\n{text}")
    return "\n\n".join(blocks)
