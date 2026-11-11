# A copy of the Streamlit Community Cloud setup (M7, decision 0021), to test the app before
# deploying: Debian, Python 3.12, the system packages of packages.txt, the dependencies from
# uv.lock, the repository as cloned (no data/, no database), started from the repository root.
# BASE: python:3.12-slim-bookworm (Debian 12) or python:3.12-slim-bullseye (Debian 11, which
# Streamlit's documentation names; end of life since August 2026, so read from Debian's archive).
ARG BASE=python:3.12-slim-bookworm
FROM ${BASE}
WORKDIR /mount/src/airlines-analyzer
COPY packages.txt /tmp/packages.txt
RUN if grep -q bullseye /etc/os-release; then \
      sed -i -e 's|deb.debian.org/debian-security|archive.debian.org/debian-security|' \
             -e 's|deb.debian.org/debian|archive.debian.org/debian|' /etc/apt/sources.list; fi \
    && apt-get update && xargs -a /tmp/packages.txt apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv
COPY . .
RUN uv sync --frozen
EXPOSE 8501
CMD ["uv", "run", "--no-sync", "streamlit", "run", "src/tearsheet/app/main.py", \
     "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
