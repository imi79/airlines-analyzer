# M10 answer key score

The answer key (`answer_key.csv`, three companies, written before the AI read anything) against the figures loaded. Written by `uv run tearsheet all`.

| Outcome | Lines |
| --- | ---: |
| Verified and correct | 56 |
| **Verified but wrong** (must be zero) | **0** |
| Flagged for review, figure correct | 1 |
| Flagged for review, figure wrong | 1 |
| Not read | 0 |
| Total | 58 |

These counts are the machine's own reading and checks, before any review. After Imane's reviews: 58 on the page and correct, **0 on the page and wrong**, 0 kept off the page.

Lines not verified automatically:

- adp, Capex (purchases of PP&E and intangibles): flagged and wrong; after review: on the page, correct
- adp, Lease payments (principal): flagged and correct; after review: on the page, correct
