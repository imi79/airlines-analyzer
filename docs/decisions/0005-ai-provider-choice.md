# 0005 · Choice of AI provider (before M3)

Date: 2026-10-29 · Status: accepted (asked by Imane)

The app does not call one AI vendor directly. Every model call (extraction in M3, drafting in M4)
goes through one small layer, `src/tearsheet/llm/`, with two adapters:

- **Anthropic**, through its own API.
- **OpenAI-compatible**, which covers DeepSeek, OpenRouter, Mistral, Groq, Azure OpenAI and
  local models, by changing the address and the model name.

`config/models.yaml` names the provider, the model for each job (drafting, extraction) and the
name of the environment variable that holds the API key. Changing provider is a config edit,
not a code change.

The safety net doesn't depend on the provider. Whichever model is used, the grounding check
(M3) and the verifier (M4) check every figure in code before anything reaches the tearsheet.
Models differ in quality, so the M3 and M4 evaluation sets will be run for each provider that
Imane wants to use, and the scores recorded.

Open point for M3: adding the OpenAI-compatible client library is a new dependency, to be
confirmed with Imane when M3 starts.
