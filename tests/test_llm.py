"""The AI layer, with no network: answers come from a stand-in server (httpx.MockTransport)."""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from tearsheet.llm import LLM, LLMError, MissingKey, NotRecorded, ProviderSettings, ToolSpec
from tearsheet.llm.settings import load_settings

TOOL = ToolSpec(
    "record_figures",
    "Record figures",
    {"type": "object", "properties": {"n": {"type": "integer"}}, "required": ["n"]},
)


def settings(kind: str) -> ProviderSettings:
    return ProviderSettings(
        name="test",
        kind=kind,
        base_url="https://llm.example",
        api_key_env="TEST_LLM_KEY",
        models={"extraction": "model-x"},
        price={"input": 1, "output": 2},
    )


def openai_answer(arguments: dict) -> dict:
    return {
        "model": "model-x",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_1",
                            "type": "function",
                            "function": {
                                "name": "record_figures",
                                "arguments": json.dumps(arguments),
                            },
                        }
                    ],
                }
            }
        ],
        "usage": {"prompt_tokens": 1000, "completion_tokens": 200},
    }


def anthropic_answer(arguments: dict) -> dict:
    return {
        "model": "model-x",
        "content": [{"type": "tool_use", "id": "t1", "name": "record_figures", "input": arguments}],
        "usage": {"input_tokens": 1000, "output_tokens": 200},
    }


class Server:
    """Stand-in provider: records each request and replies with a fixed answer."""

    def __init__(self, answer: dict, status: int = 200):
        self.answer, self.status, self.requests = answer, status, []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return httpx.Response(self.status, json=self.answer)

    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self))


@pytest.fixture
def key(monkeypatch):
    monkeypatch.setenv("TEST_LLM_KEY", "sk-test")


def test_openai_compatible_request_and_answer(tmp_path: Path, key):
    server = Server(openai_answer({"n": 3}))
    llm = LLM(settings("openai_compatible"), records=tmp_path, http=server.client())
    result = llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")
    assert result.arguments == {"n": 3}
    assert not result.cached
    sent = server.requests[0]
    assert str(sent.url) == "https://llm.example/chat/completions"
    assert sent.headers["authorization"] == "Bearer sk-test"
    body = json.loads(sent.content)
    assert body["model"] == "model-x"
    assert body["tool_choice"]["function"]["name"] == "record_figures"
    assert body["temperature"] == 0
    # cost: 1000 tokens at 1 USD/m + 200 at 2 USD/m
    assert float(result.cost_usd) == pytest.approx(0.0014)


def test_anthropic_request_and_answer(tmp_path: Path, key):
    server = Server(anthropic_answer({"n": 5}))
    llm = LLM(settings("anthropic"), records=tmp_path, http=server.client())
    result = llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")
    assert result.arguments == {"n": 5}
    sent = server.requests[0]
    assert str(sent.url) == "https://llm.example/v1/messages"
    assert sent.headers["x-api-key"] == "sk-test"
    assert json.loads(sent.content)["tool_choice"] == {"type": "tool", "name": "record_figures"}


def test_identical_request_is_served_from_the_record(tmp_path: Path, key):
    server = Server(openai_answer({"n": 3}))
    llm = LLM(settings("openai_compatible"), records=tmp_path, http=server.client())
    llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")
    again = LLM(settings("openai_compatible"), records=tmp_path, offline=True)
    result = again.call_tool("extraction", "system", "user text", TOOL, "extract-v1")
    assert result.cached and result.arguments == {"n": 3}
    assert len(server.requests) == 1
    record = json.loads(next(tmp_path.glob("*.json")).read_text())
    assert "sk-test" not in json.dumps(record)  # the key is never written down


def test_new_prompt_version_is_a_new_request(tmp_path: Path, key):
    server = Server(openai_answer({"n": 3}))
    llm = LLM(settings("openai_compatible"), records=tmp_path, http=server.client())
    llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")
    llm.call_tool("extraction", "system", "user text", TOOL, "extract-v2")
    assert len(server.requests) == 2


def test_offline_without_record_refuses(tmp_path: Path):
    llm = LLM(settings("openai_compatible"), records=tmp_path, offline=True)
    with pytest.raises(NotRecorded):
        llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")


def test_missing_key_is_explained(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("TEST_LLM_KEY", raising=False)
    llm = LLM(settings("openai_compatible"), records=tmp_path)
    with pytest.raises(MissingKey, match="TEST_LLM_KEY"):
        llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")


def test_answer_without_form_is_an_error(tmp_path: Path, key):
    answer = {"choices": [{"message": {"role": "assistant", "content": "Here you go: 42"}}]}
    llm = LLM(settings("openai_compatible"), records=tmp_path, http=Server(answer).client())
    with pytest.raises(LLMError, match="without filling in the form"):
        llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")
    assert not list(tmp_path.glob("*.json"))  # a failed answer is not recorded


def test_refused_key_is_explained(tmp_path: Path, key):
    server = Server({"error": "bad key"}, status=401)
    llm = LLM(settings("openai_compatible"), records=tmp_path, http=server.client())
    with pytest.raises(LLMError, match="refused the key"):
        llm.call_tool("extraction", "system", "user text", TOOL, "extract-v1")


def test_models_yaml_loads_every_provider():
    for name in ("deepseek", "openrouter", "anthropic"):
        s = load_settings(use=name)
        assert s.model("extraction") and s.model("drafting")
    assert load_settings().name == "deepseek"
