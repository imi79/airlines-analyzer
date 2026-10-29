"""Small cached client for the filings.xbrl.org JSON:API and the ECB data API."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin

import httpx

FILINGS_BASE = "https://filings.xbrl.org"
ECB_BASE = "https://data-api.ecb.europa.eu/service/data"
CACHE = Path("data/raw")


class Client:
    """Every response is stored on disk, so a rerun works offline and gives the same result."""

    def __init__(self, cache: Path = CACHE, offline: bool = False):
        self.cache = cache
        self.offline = offline
        self.http = httpx.Client(timeout=120, follow_redirects=True)

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
            response = self.http.get(url, params=params, headers={"Accept": "application/json"})
            response.raise_for_status()
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
            with self.http.stream("GET", url) as response:
                response.raise_for_status()
                with partial.open("wb") as out:
                    for chunk in response.iter_bytes():
                        out.write(chunk)
            partial.rename(target)
        return target

    def ecb_series(self, flow: str, key: str, start: str) -> str:
        url = f"{ECB_BASE}/{flow}/{key}"
        params = {"format": "csvdata", "startPeriod": start}
        target = self._cache_path("ecb", url, params, ".csv")
        if not target.exists():
            if self.offline:
                raise FileNotFoundError(f"not cached: {url}")
            response = self.http.get(url, params=params)
            response.raise_for_status()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(response.text)
        return target.read_text()
