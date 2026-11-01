# 0010 · M3: how the AI reads the report, and what "verified" means

Date: 2026-11-01 · Status: accepted (M3 plan approved by Imane; provider DeepSeek)

**No AI vendor library.** Both connectors in `src/tearsheet/llm/` (Anthropic, and
"OpenAI-compatible" for DeepSeek, OpenRouter and the like) send plain web requests with `httpx`,
already in the stack. This settles the open point in decision 0005: no new dependency. Pydantic
(in the agreed stack) checks the shape of each answer.

**The AI answers through a form only.** One request per report. The model fills the form
`record_figures` (figure, year, number as printed, scale, currency, quote, table header,
scope), or marks a figure "not found". It never writes free text that reaches the tearsheet.
The instructions are a versioned file (`extract/prompts/extract_v1.md`, version `extract-v1`);
any change to the prompt, the form or the request bumps the version.

**It sees a few pages, not the whole report.** The section locator picks up to four passages
per figure around the figure's words (English, French, Spanish and German), at most
60,000 characters per report (about 15,000 tokens).

**Verified means code confirmed it against the report, not that the AI said so.** A figure is
verified only if every check passes:

1. the quote is in the report word for word (spaces ignored, because some converters split
   words);
2. the quote is about the figure (it contains one of the figure's words);
3. the number is printed in the quote, with its scale, % sign or currency;
4. the year is right: not the prior-year comparative printed beside it;
5. the value is plausible (range, and share of revenue for amounts);
6. across reports: the year's own report and the next year's comparative agree; RPK ÷ ASK
   matches the printed load factor; no implausible jump from the year before.

Anything else stays **unverified**, with each reason kept, and off the tearsheet until Imane
approves or corrects it in `config/extraction_reviews.yaml`.

**One value per figure and year.** Verified first; then the year's own report over a later
report's comparative; then the latest report.

**Every answer is recorded** under `records/llm/`, named by a fingerprint of the whole request.
A rerun replays the record: same result, no cost, works offline. The records are committed so
the audit trail travels with the repository. `tearsheet load` only replays; only
`tearsheet extract` calls the model.
