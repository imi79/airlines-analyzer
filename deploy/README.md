# Deployment files (M7, decision 0021)

- `../packages.txt`: system libraries the PDF needs, installed by Streamlit Community Cloud
  and by the Dockerfile (Pango, HarfBuzz, Fontconfig; names valid on Debian 11, 12 and 13).
- `../Dockerfile`: the app in demo mode on any host.
- `hosting-copy.Dockerfile`: a copy of the Streamlit Community Cloud setup, to test the app
  before deploying (Debian 12 by default; `--build-arg BASE=python:3.12-slim-bullseye` for
  Debian 11, which Streamlit's documentation names).

Test either one from a clean export of the repository (what a clone holds: no `data/`):

```bash
mkdir -p /tmp/tearsheet-clean && git archive HEAD | tar -x -C /tmp/tearsheet-clean
docker build -f /tmp/tearsheet-clean/deploy/hosting-copy.Dockerfile -t tearsheet-hosting /tmp/tearsheet-clean
docker run -p 8501:8501 tearsheet-hosting
```

Then open http://localhost:8501 in a fresh browser window: the tearsheet, a source card, the
verifier on the Method page, and a PDF download must all work with no key.
