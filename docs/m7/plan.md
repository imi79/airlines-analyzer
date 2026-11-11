# M7 plan: the portfolio piece, live on a public link

Status: **approved by Imane** (2026-11-11) with every recommendation: 1. public repository,
MIT licence; 2. history tidied once before publishing, with a go-ahead at that step; 3. Imane
writes the three analyst views; 4. Air France-KLM, easyJet and Aena FY2025 as samples; 5.
commentary in English only, French later; 6. a rehearsal in the chat for the second checklist
item. Built in the same session, on `m7-portfolio`.

## What M7 is for

M1 to M6 built a working tool. M7 makes it something a recruiter can open and an interviewer
can follow: a **public link** that works in any browser without a key, a **README** that
explains the design in two minutes, **three sample PDFs**, a **three-minute demo script**, and
the words you'll use about it: a **LinkedIn post** and a **CV line**. Gate 3 closes v1.

Think of it as moving from the finished deal to the pitch book: same substance, packaged for
someone who has two minutes and no context.

## What gets built

1. **Public deployment** on Streamlit Community Cloud (free), from the GitHub repository,
   demo mode only. I prepare everything in the repository; the deployment itself needs your
   GitHub login, so you click "Deploy" (about five minutes, steps below).
   - `packages.txt`: the system libraries the PDF needs on the host (Pango).
   - Before you deploy, I test a **copy of the hosting setup** here (Debian 11, Python 3.12,
     the same install from `uv.lock`) in a container: every page, a source card, and a PDF and
     Excel export, in a real browser, with no key and no database.
2. **Dockerfile**, so the app can run on any host later (spec). Built and tested here the same
   way: start the container, open the app, export a PDF.
3. **"Watch the verifier work"**, the demo's third beat (spec use case 4: "the verifier
   rejecting a bad draft"). Today the app shows only the final, clean draft. Two small
   additions:
   - on Data and audit, **the AI's first attempt and the verifier's verdict on it**, from the
     recorded drafts (for example easyJet FY2025: "'worse' claimed on EBITDA margin, but it is
     neither better nor worse"), so a visitor sees real rejections;
   - on Method, **"Try the verifier"**: pick a faulty sentence (a number typed outside a blank,
     "improved" on a figure that worsened, a made-up figure) or type your own, and see which
     rule rejects it, in plain words.
4. **README** at the repository root: what the tool does and why it is different, the public
   link, screenshots, an **architecture diagram** of the seven stages around the facts store
   (drawn as a Mermaid diagram, which GitHub displays without any tool), the design choices
   (code computes, the AI only references figures by id, a verifier checks every sentence,
   any AI provider), the results of every gate in plain numbers (including the misses: the
   commentary score of 3.78 and the extraction goal), how to run it, and the limits.
5. **Three sample PDFs** in `samples/pdf/`, one per peer group (question 4), each with an
   analyst view (question 3).
6. **Continuous checks on GitHub** (spec: GitHub Actions and gitleaks): on every push, the tests,
   the code style check, and a **secret scan** of the whole history (gitleaks), so no key can
   reach the public repository unnoticed. Run once over the full history before going public.
7. **Demo script** (`docs/m7/demo_script.md`): three minutes, timed beat by beat: the problem
   (0:00), the tearsheet (0:30), one figure audited down to the filing (1:15), the verifier
   rejecting a bad draft (1:45), the PDF and the Excel backup (2:30), close (2:50). With the
   clicks, the words, and what to do if the app is asleep.
8. **LinkedIn post draft and CV line** (`docs/m7/`), in English, for you to put in your own
   words.
9. **"The pipeline in seven stages"** (`docs/m7/pipeline_explained.md`): one page per stage in
   plain language (what goes in, what comes out, what can go wrong, what checks it), plus ten
   interview-style questions with model answers, for the second checklist item.

## How we know it works (the M7 checklist)

- [ ] **Public link works in a fresh browser with no key (gate 3).** I open the public link
      from here in a fresh browser (no cookies, no key): all four pages, a source card down to
      the filing, the verifier demo, a PDF download. You open it on your phone in a private
      window. Recorded with screenshots in `docs/m7/gate3.md`.
- [ ] **Imane can explain every stage of the pipeline without notes.** Your call, not a test:
      I suggest a rehearsal here in the chat, where you explain each stage in your words and I
      tell you what an interviewer might push on (question 6).

Other checks: the Docker image and the hosting copy pass the same browser tour; the secret scan
finds nothing in the history; the README's numbers match the milestone records; tests green.

## What you do (about 15 minutes in all)

1. **Deploy** (5 min): sign in at share.streamlit.io with GitHub, "Create app", repository
   `imi79/airlines-analyzer`, branch `main`, main file `src/tearsheet/app/main.py`, Python 3.12,
   then Deploy. Send me the link.
2. **Make the app public** if the repository stays private (app settings, "Who can view this
   app"): a private repository gives a private app by default.
3. **Delete the two leftover `claude/...` branches** on GitHub (Branches page), so the public
   repository holds only the work-named branches.
4. **Write or rewrite** the three analyst views, the LinkedIn post and the CV line.

## Order of work

1. Secret scan of the full history, and the history clean-up if you choose it (question 2).
2. "Watch the verifier work": the first attempts on Data and audit, "Try the verifier" on Method.
3. `packages.txt`, the hosting copy test; the Dockerfile and its test.
4. GitHub Actions: tests, style, secret scan.
5. Three sample PDFs (after your analyst views).
6. README, demo script, LinkedIn post, CV line, the seven-stage explainer.
7. You deploy; gate 3 check on the public link; walkthrough, decision note, checklist.

No AI tokens are needed.

## New software

- **gitleaks** (secret scanner), named in the spec's security section; run by GitHub Actions
  and once here. Not a Python dependency.
- The Dockerfile uses the official Python 3.12 image and `uv`, both already the project's tools.
- Nothing added to the app itself.

## Known difficulties

- **Sleep.** A free app sleeps after 12 hours without visitors; the first visitor then waits
  about half a minute and clicks "Yes, get this app back up!". The demo script covers it: open
  the link a few minutes before an interview.
- **Resources.** The free host gives about 0.7 to 2.7 GB of memory; the app uses well under
  that (the demo files are 3.6 MB), and a PDF takes about four seconds.
- **Debian 11 on the host.** It is older than the system here; the hosting copy test is there to
  catch any library that behaves differently before you deploy.
- **Private by default.** One private app is allowed per account; a public repository avoids
  the question entirely (question 1).

## Questions for Imane

1. **Public or private repository, and the licence** (open question in the spec). (a) Public
   repository with the MIT licence: recruiters can read the code, the tests and the decision
   notes, which is most of the portfolio value; anyone may reuse the code, but the value of a
   commercial version lies in coverage, data and verification, not in this code. (b) Public with
   a "source-available" licence (for example PolyForm Noncommercial): readable, but no
   commercial reuse without your permission. (c) Private repository, public app only:
   recruiters see the app, not the code. Recommendation: (a).
2. **Before going public: tidy the history once?** Today every commit carries your personal
   email address, and the history holds the two company PDFs you supplied (Air France-KLM's and
   ADP's 2025 statements, 9 MB, which are the companies' copyright even if published). (a) Publish
   as is; or (b) rewrite the history once before publishing: commits switched to your GitHub
   "noreply" address, the two PDFs removed (their SHA-256 fingerprints and the companies' links
   stay, so the hand entries remain verifiable). (b) changes every commit identifier and
   replaces `main` on GitHub; it is safe now because nobody else has a copy. Recommendation:
   (b), with your explicit go-ahead at that step, and new commits from then on with the noreply
   address.
3. **The analyst views in the three samples.** (a) You write three views of five to eight lines;
   or (b) I draft them from the tearsheets for you to rewrite in your own words, as for the M4
   example notes. Recommendation: (a) if you have the time, it is the one part of the PDF that
   shows your judgment; otherwise (b).
4. **Which three samples.** One per peer group: Air France-KLM FY2025 (network, hand-entered
   FY2025 figures, euro), easyJet FY2025 (low-cost, September year end, sterling), Aena FY2025
   (airport). Recommendation: these three; they show the range of what the tool handles.
5. **Commentary language** (open question in the spec, settled in M4 as English only). Tick it
   as decided, French later? Recommendation: yes.
6. **The second checklist item.** (a) A rehearsal in this chat: you explain each stage in your own
   words, I play the interviewer and note what to tighten; or (b) you read the explainer and
   tick it yourself. Recommendation: (a), about twenty minutes, once the explainer is written.

Working rule reminder: one milestone per session. Once you approve, I'd build M7 in a fresh
session (or this one, if you prefer), on the branch `m7-portfolio`.
