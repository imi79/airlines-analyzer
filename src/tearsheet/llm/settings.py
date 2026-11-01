"""Read config/models.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from tearsheet.config import CONFIG

MODELS = CONFIG / "models.yaml"
KINDS = ("openai_compatible", "anthropic")
JOBS = ("extraction", "drafting")


@dataclass(frozen=True)
class ProviderSettings:
    name: str  # entry name, e.g. "deepseek"
    kind: str  # openai_compatible | anthropic
    base_url: str
    api_key_env: str
    models: dict[str, str]  # job -> model name
    price: dict | None  # USD per million tokens: {"input": .., "output": ..}

    def model(self, job: str) -> str:
        if job not in self.models:
            raise KeyError(f"config/models.yaml: no model set for job '{job}' under {self.name}")
        return self.models[job]


def load_settings(path: Path = MODELS, use: str | None = None) -> ProviderSettings:
    raw = yaml.safe_load(path.read_text())
    name = use or raw["use"]
    if name not in raw["providers"]:
        raise KeyError(f"config/models.yaml: `use: {name}` but no provider entry has that name")
    entry = raw["providers"][name]
    if entry["kind"] not in KINDS:
        raise ValueError(f"config/models.yaml: kind must be one of {KINDS}, got {entry['kind']}")
    return ProviderSettings(
        name=name,
        kind=entry["kind"],
        base_url=entry["base_url"].rstrip("/"),
        api_key_env=entry["api_key_env"],
        models=dict(entry["models"]),
        price=entry.get("price_per_million_tokens"),
    )
