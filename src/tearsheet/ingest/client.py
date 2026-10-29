"""Cached client for the filings.xbrl.org JSON:API and the ECB data API.

Every response is kept on disk, so a rerun works offline and gives the same result."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urljoin

import httpx

from tearsheet.config import CACHE

FILINGS_BASE = "https://filings.xbrl.org"
ECB_BASE = "https://data-api.ecb.europa.eu/service/data"

PAUSE_SECONDS = 1.0  # between network calls, to stay under the API's rate limit
RETRIES = 6


class Client:
    def __init__(self, cache: Path = CACHE, offline: bool = False):
        self.cache = cache
        self.offline = offline
        self.http = httpx.Client(timeout=300, follow_redirects=True)
        self._last_call = 0.0

    def _wait_turn(self) -> None:
        delay = PAUSE_SECONDS - (time.monotonic() - self._last_call)
        if delay > 0:
            time.sleep(delay)
        self._last_call = time.monotonic()

    def _get(self, url: str, **kwargs) -> httpx.Response:
        """GET with a pause between calls and backoff on rate limits and server errors."""
        for attempt in range(RETRIES):
            self._wait_turn()
            try:
                response = self.http.get(url, **kwargs)
            except httpx.TransportError:
                if attempt == RETRIES - 1:
                    raise
                time.sleep(2**attempt)
                continue
            if response.status_code == 429 or response.status_code >= 500:
                if attempt == RETRIES - 1:
                    response.raise_for_status()
                retry_after = response.headers.get("Retry-After", "")
                time.sleep(float(retry_after) if retry_after.isdigit() else 2 ** (attempt + 1))
                continue
            response.raise_for_status()
            return response
        raise RuntimeError("unreachable")

    def _cache_path(self, kind: str, url: str, params: dict | None, suffix: str) -> Path:
        key = url + json.dumps(params or {}, sort_keys=True)
        digest = hashlib.sha256(key.encode()).hexdigest()[:16]
        return self.cache / kind / f"{digest}{suffix}"

    def get_json(self, path: str, params: dict | None = None) -> dict:
        url = urljoin(FILINGS_BASE, path)
        target = self._cache_path("api", url, params, ".json")
        if not target.exists():
            if self.offline:
                raise FileNotFoundError(f"not cached: {url} {params}")
            response = self._get(url, params=params, headers={"Accept": "application/json"})
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(response.text)
        return json.loads(target.read_text())

    def get_all(self, path: str, params: dict | None = None) -> list[dict]:
        """Follow JSON:API pagination and return every item in `data`."""
        params = {**(params or {}), "page[size]": 200}
        items, page = [], 1
        while True:
            body = self.get_json(path, {**params, "page[number]": page})
            items.extend(body.get("data", []))
            if not body.get("links", {}).get("next") or not body.get("data"):
                return items
            page += 1

    def download(self, url_or_path: str, kind: str) -> Path:
        url = urljoin(FILINGS_BASE, url_or_path)
        suffix = Path(url.split("?")[0]).suffix or ".bin"
        target = self._cache_path(kind, url, None, suffix)
        if not target.exists():
            if self.offline:
                raise FileNotFoundError(f"not cached: {url}")
            target.parent.mkdir(parents=True, exist_ok=True)
            partial = target.with_suffix(target.suffix + ".part")
            partial.write_bytes(self._get(url).content)
            partial.rename(target)
        return target

    def ecb_series(self, flow: str, key: str, start: str) -> str:
        url = f"{ECB_BASE}/{flow}/{key}"
        params = {"format": "csvdata", "startPeriod": start}
        target = self._cache_path("ecb", url, params, ".csv")
        if not target.exists():
            if self.offline:
                raise FileNotFoundError(f"not cached: {url}")
            response = self._get(url, params=params)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(response.text)
        return target.read_text()
