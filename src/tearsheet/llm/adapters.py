"""The two connectors: how a request is written, and how the answer is read back.

Both work over plain HTTPS with httpx, so no vendor library is needed (decision 0010).
Each connector has two pure functions, so tests can check them on recorded answers:
`request(...)` gives the URL, headers and body; `parse(...)` gives the filled form and usage.
"""

from __future__ import annotations

import json

from tearsheet.llm.base import LLMError, ToolSpec, Usage

MAX_OUTPUT_TOKENS = 8192
ANTHROPIC_VERSION = "2023-06-01"


# --- OpenAI-compatible (DeepSeek, OpenRouter, Mistral, Azure, local models...) ---------------


def openai_request(
    base_url: str, key: str, model: str, system: str, user: str, tool: ToolSpec
) -> tuple[str, dict, dict]:
    url = f"{base_url}/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.schema,
                },
            }
        ],
        "tool_choice": {"type": "function", "function": {"name": tool.name}},
        "temperature": 0,
        "max_tokens": MAX_OUTPUT_TOKENS,
    }
    return url, headers, body


def openai_parse(data: dict, tool: ToolSpec) -> tuple[dict, Usage]:
    try:
        message = data["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"unexpected answer shape: {str(data)[:300]}") from exc
    calls = [c for c in message.get("tool_calls") or [] if c["function"]["name"] == tool.name]
    if not calls:
        raise LLMError("the model answered without filling in the form")
    try:
        arguments = json.loads(calls[0]["function"]["arguments"])
    except json.JSONDecodeError as exc:
        raise LLMError(f"the form the model returned is not valid JSON: {exc}") from exc
    usage = data.get("usage") or {}
    return arguments, Usage(usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))


# --- Anthropic ---------------------------------------------------------------------------------


def anthropic_request(
    base_url: str, key: str, model: str, system: str, user: str, tool: ToolSpec
) -> tuple[str, dict, dict]:
    url = f"{base_url}/v1/messages"
    headers = {
        "x-api-key": key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }
    body = {
        "model": model,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "tools": [
            {"name": tool.name, "description": tool.description, "input_schema": tool.schema}
        ],
        "tool_choice": {"type": "tool", "name": tool.name},
        "temperature": 0,
    }
    return url, headers, body


def anthropic_parse(data: dict, tool: ToolSpec) -> tuple[dict, Usage]:
    blocks = [
        b
        for b in data.get("content") or []
        if b.get("type") == "tool_use" and b.get("name") == tool.name
    ]
    if not blocks:
        raise LLMError("the model answered without filling in the form")
    usage = data.get("usage") or {}
    return blocks[0]["input"], Usage(usage.get("input_tokens", 0), usage.get("output_tokens", 0))


ADAPTERS = {
    "openai_compatible": (openai_request, openai_parse),
    "anthropic": (anthropic_request, anthropic_parse),
}
