"""One entry point for every model call, with a record of each answer.

Every answer is saved under `records/llm/`, named by a fingerprint of the full request
(provider, model, prompt version, instructions, text sent and form). An identical request is
answered from that record: a rerun costs nothing, gives the same result, and works offline.
The records are committed, so the audit trail of what the model said travels with the repo.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path

import httpx

from tearsheet.config import ROOT
from tearsheet.llm.adapters import ADAPTERS
from tearsheet.llm.base import LLMError, MissingKey, NotRecorded, ToolResult, ToolSpec, Usage
from tearsheet.llm.settings import ProviderSettings, load_settings

RECORDS = ROOT / "records" / "llm"
RETRIES = 4
TIMEOUT_SECONDS = 300


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class LLM:
    def __init__(
        self,
        settings: ProviderSettings | None = None,
        records: Path = RECORDS,
        offline: bool = False,
        http: httpx.Client | None = None,
    ):
        self.settings = settings or load_settings()
        self.records = records
        self.offline = offline
        self._http = http

    @property
    def http(self) -> httpx.Client:
        if self._http is None:
            self._http = httpx.Client(timeout=TIMEOUT_SECONDS)
        return self._http

    def fingerprint(
        self, job: str, system: str, user: str, tool: ToolSpec, prompt_version: str
    ) -> tuple[str, dict]:
        s = self.settings
        request = {
            "provider": s.name,
            "kind": s.kind,
            "model": s.model(job),
            "job": job,
            "prompt_version": prompt_version,
            "system_sha256": _sha(system),
            "user_sha256": _sha(user),
            "tool_sha256": _sha(json.dumps([tool.name, tool.description, tool.schema])),
        }
        return _sha(json.dumps(request, sort_keys=True)), request

    def call_tool(
        self,
        job: str,
        system: str,
        user: str,
        tool: ToolSpec,
        prompt_version: str,
        label: str = "",
    ) -> ToolResult:
        """Ask the model for `job` to fill in `tool`. Raises LLMError if it can't."""
        digest, request = self.fingerprint(job, system, user, tool, prompt_version)
        path = self.records / f"{digest[:24]}.json"
        if path.exists():
            record = json.loads(path.read_text())
            return self._result(record, digest, cached=True)
        if self.offline:
            raise NotRecorded(f"no recorded answer for {label or digest[:12]} (offline mode)")

        s = self.settings
        key = os.environ.get(s.api_key_env)
        if not key:
            raise MissingKey(
                f"the environment variable {s.api_key_env} is not set "
                f"(config/models.yaml, provider {s.name})"
            )
        build, parse = ADAPTERS[s.kind]
        url, headers, body = build(s.base_url, key, s.model(job), system, user, tool)
        data = self._post(url, headers, body)
        arguments, usage = parse(data, tool)
        record = {
            "label": label,
            "request": request,
            "answer": arguments,
            "usage": {"input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens},
            "served_model": data.get("model", s.model(job)),
            "recorded_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        self.records.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, indent=1, ensure_ascii=False, sort_keys=True) + "\n")
        return self._result(record, digest, cached=False)

    def _result(self, record: dict, digest: str, cached: bool) -> ToolResult:
        usage = Usage(**record["usage"])
        req = record["request"]
        return ToolResult(
            arguments=record["answer"],
            provider=req["provider"],
            model=record.get("served_model") or req["model"],
            prompt_version=req["prompt_version"],
            request_hash=digest,
            usage=usage,
            cached=cached,
            cost_usd=usage.cost(self.settings.price),
        )

    def _post(self, url: str, headers: dict, body: dict) -> dict:
        for attempt in range(RETRIES):
            try:
                response = self.http.post(url, headers=headers, json=body)
            except httpx.TransportError as exc:
                if attempt == RETRIES - 1:
                    raise LLMError(f"could not reach {url}: {exc}") from exc
                time.sleep(2 ** (attempt + 1))
                continue
            if response.status_code == 429 or response.status_code >= 500:
                if attempt == RETRIES - 1:
                    raise LLMError(f"{url} answered {response.status_code}: {response.text[:300]}")
                time.sleep(2 ** (attempt + 1))
                continue
            if response.status_code in (401, 403):
                raise LLMError(
                    f"{url} refused the key ({response.status_code}). Check the key stored in "
                    f"{self.settings.api_key_env} and base_url in config/models.yaml."
                )
            if response.status_code >= 400:
                raise LLMError(f"{url} answered {response.status_code}: {response.text[:500]}")
            return response.json()
        raise RuntimeError("unreachable")
