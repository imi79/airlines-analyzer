# 0021 · M7: portfolio packaging, deployment and the public repository

Date: 2026-11-11 · Status: plan approved by Imane with every recommendation ("approved with all
recommendations, go ahead on m7-portfolio"); history rewritten on her go-ahead ("rewrite, keep
PDFs"); deployed by Imane at https://airlines-analyzer.streamlit.app, gate 3 passed;
rehearsal held and M7 closed by Imane (2026-11-11)

**Choices approved with the plan** (`docs/m7/plan.md`):

1. **Public repository, MIT licence** (closes the spec's open question). The holder in `LICENSE`
   is "Imane"; she may add her full name.
2. **History tidied once before publishing**, with a separate go-ahead at that step: commit email
   switched to the GitHub noreply address; the two supplied company PDFs (see below).
3. **Imane writes the analyst views** of the three samples; in the end she asked for drafts
   and adopted them unchanged (see below).
4. **Samples:** Air France-KLM, easyJet and Aena FY2025 (`samples/pdf/`), one per peer group.
5. **Commentary in English only**, French later (closes the spec's open question).
6. **A rehearsal in the chat** for "can explain every stage without notes"
   (`docs/m7/pipeline_explained.md`).

**Choices made while building:**

- **Test the hosting before deploying.** `deploy/hosting-copy.Dockerfile` copies Streamlit
  Community Cloud's setup: Debian, Python 3.12, `packages.txt`, `uv.lock`, the repository as
  cloned (no database), started from the repository root. Built from a clean export and toured
  in a real browser on Debian 12 and Debian 11: every page, a source card followed down, the
  verifier demo, a PDF download, no key.
- **Debian 11 is end of life** (August 2026): its packages now come from Debian's archive, and a
  plain install fails. Streamlit's documentation still names Debian 11; the copy tests both, and
  `packages.txt` uses names valid on Debian 11, 12 and 13.
- **The PDF's font was not the bundled one on a clean machine.** WeasyPrint ignores `@font-face`
  without a font configuration; the development machine has Inter installed system-wide, which
  hid it. The hosting copy showed DejaVu Sans. Fixed, the bundled font renamed "Tearsheet Inter"
  so no installed font can stand in, and the PDF test now checks the embedded font family on all
  18 tearsheets. The M6 PDFs in `docs/m6/pdf/` were made with the system copy of the same font
  file, so they look the same.
- **Watch the verifier work** (spec use case 4). Data and audit shows each recorded try of the
  AI's draft with the sentences rejected and the rule; the Method page has "Try the verifier",
  with faulty examples built from each tearsheet's own figures (a number typed outside a blank,
  the wrong direction, a figure that does not exist or awaits review) and a correct one. The
  form's claims are set to the direction computed by code, so only what the sentence says can be
  wrong. The examples use a headline metric: the verifier reads "PP" in "PP&E" as percentage
  points, which is right for its job but makes a poor demo.
- **Dockerfile**: Debian 12, demo mode, a non-root user, a health check, no development
  dependencies; 1.16 GB, because it carries the whole pipeline's libraries (Arelle, LibreOffice
  is not included). Slimming is left for later.
- **Checks on GitHub** (`.github/workflows/ci.yml`): code style, the full test suite with
  LibreOffice for the Excel recalculation check, and gitleaks over the whole history, on every
  push. Gitleaks runs from its official Docker image (pinned version), which needs no licence
  key; the first run passed both jobs.
- **Secret scan before going public**: gitleaks 8.30.1 over all 51 commits on every branch, no
  leak; the real API key of this environment searched for across the history, not found
  (`docs/m7/secret_scan.md`).
- **A correction to the record.** `docs/progress.md` said gate 2 had "17 drafts in a row"; the
  recorded summary (`docs/m4/drafts.md`) shows 11, and 17 was impossible with 16 of 18 drafts
  passing. Gate 2 asks for ten, so it still passes. The checklist line and the README use 11.
- **README** at the repository root with the architecture as a Mermaid diagram (displayed by
  GitHub, no image to maintain) and every gate result, the misses included.
- **The history was rewritten once before publishing** (Imane: "rewrite, keep PDFs"). Every
  commit's author and committer address became the GitHub noreply address
  (`245598871+imi79@users.noreply.github.com`); names, dates, messages and files are unchanged.
  Done with git-filter-repo on a separate full copy; before replacing anything on GitHub, each of
  the 11 branches was checked to hold exactly the same files and number of commits as before.
  All 11 branches were then replaced on GitHub, and new commits use the noreply address.
  Side effects: every commit identifier changed, so identifiers quoted in earlier records (the
  M6 manifests and PDF footers name `6e7ed9559042`, the M6 plan commit, now `31df84e`) no
  longer resolve; the old commits stay reachable on GitHub by their exact identifier until GitHub's
  own clean-up, but the repository was private and nobody outside has them.
- **The two supplied company PDFs stay** in `documents/`: the full rebuild reads them (the
  recorded AI answers are keyed on their text), and they are public investor documents. Their
  SHA-256 fingerprints are in `config/report_documents.yaml` and `config/manual_figures.yaml`.
- **The sample analyst views were drafted at Imane's request** ("draft the three analyst views
  for me to rewrite"), from verified figures only, and adopted by her unchanged ("use the drafts
  as they are"). Each note in `notes/` records this in `view_origin`. The tool itself never
  drafts an analyst view; these three were written outside it, like the M4 example notes.
- **A test that broke when the notes were committed.** The M5 check that demo mode saves nothing
  assumed `notes/` was empty; once the three analyst views were committed, it failed (30 errors)
  and GitHub's checks were red on `main` for two pushes before it was noticed at closing. The
  check now compares the folder's files before and after each demo test, so it still catches any
  write.

