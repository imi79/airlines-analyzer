# Airline Credit Tearsheet

Turns a European airline's or airport's annual ESEF/UKSEF filing into a two-page credit tearsheet, with every figure traced to its source and verified. The full spec is in `docs/SPEC.md`; read it before starting any milestone.

## Working rules

- Build one milestone per session, never two at once.
- Start each milestone with a written plan and wait for approval before coding.
- End each milestone with tests green, its checklist ticked in `docs/progress.md`, and a short walkthrough Imane can follow.
- Never hardcode a financial figure. Every metric lives in `catalog.yaml` and has a unit test.
- Store values as reported with their decimals; round only when rendering.
- No network calls in unit tests; use recorded fixtures.
- No LLM output reaches the tearsheet without the verifier. Any prompt change bumps the prompt version.
- Secrets only from the environment. Ask before adding a dependency that isn't in the stack table.
- Record every non-obvious choice as a short note in `docs/decisions/`.

## Talking to Imane

- Imane has a finance and credit background and very little technical knowledge. Explain in plain language, use finance analogies, avoid jargon, and define any technical term that can't be avoided.
- Say what is being built and why before building it; report results as findings, not as code.

## Commits

- Never add Claude as a contributor: no `Co-Authored-By: Claude` trailer, no `Claude-Session` trailer, no "Generated with Claude Code" line in commit messages.
- Commits are authored by the repository owner (`imi79`), never by a Claude identity.
