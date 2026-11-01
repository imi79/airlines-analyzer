"""Shared types for the AI layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


class LLMError(Exception):
    """The provider failed, or the model did not fill in the form."""


class MissingKey(LLMError):
    """The environment variable named in config/models.yaml is not set."""


class NotRecorded(LLMError):
    """Offline mode: no recorded answer exists for this exact request."""


@dataclass(frozen=True)
class ToolSpec:
    """The form the model must fill: a name, what it is for, and a JSON schema."""

    name: str
    description: str
    schema: dict


@dataclass(frozen=True)
class Usage:
    input_tokens: int
    output_tokens: int

    def cost(self, price: dict | None) -> Decimal | None:
        """USD cost if prices per million tokens are configured, else None."""
        if not price or price.get("input") is None or price.get("output") is None:
            return None
        million = Decimal(1_000_000)
        return (
            Decimal(str(price["input"])) * self.input_tokens
            + Decimal(str(price["output"])) * self.output_tokens
        ) / million


@dataclass(frozen=True)
class ToolResult:
    arguments: dict  # the form as filled by the model
    provider: str  # entry name in models.yaml, e.g. "deepseek"
    model: str
    prompt_version: str
    request_hash: str  # fingerprint of everything sent; identical requests share it
    usage: Usage
    cached: bool  # served from the record of an earlier identical request
    cost_usd: Decimal | None = None
    extra: dict = field(default_factory=dict, compare=False)
