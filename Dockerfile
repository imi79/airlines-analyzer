# Airline Credit Tearsheet: the web app in demo mode, on any host (M7, decision 0021).
#
#   docker build -t airline-credit-tearsheet .
#   docker run -p 8501:8501 airline-credit-tearsheet      then open http://localhost:8501
#
# Demo mode only: the pre-built tearsheets in samples/, no API key, no database, no network.
FROM python:3.12-slim-bookworm

# System libraries for the PDF (WeasyPrint), the same list as Streamlit Community Cloud's
COPY packages.txt /tmp/packages.txt
RUN apt-get update \
    && xargs -a /tmp/packages.txt apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* /tmp/packages.txt \
    && pip install --no-cache-dir uv \
    && useradd --create-home --uid 1000 app && mkdir /app && chown app:app /app

WORKDIR /app
COPY --chown=app:app . .
USER app
RUN uv sync --frozen --no-dev

ENV TEARSHEET_DEMO_ONLY=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"
CMD ["uv", "run", "--no-sync", "streamlit", "run", "src/tearsheet/app/main.py", \
     "--server.address=0.0.0.0", "--server.port=8501"]
