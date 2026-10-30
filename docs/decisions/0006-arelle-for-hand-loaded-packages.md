# 0006 · Arelle to read hand-loaded ESEF packages (M1)

Date: 2026-10-30 · Status: accepted (approved by Imane)

**Why.** Choice 4b (decision 0004) loads Air France-KLM's and ADP's FY2025 filings from the
packages the companies publish, because filings.xbrl.org doesn't have them. A package is a zip
holding the tagged report (iXBRL). The rest of the tool reads xBRL-JSON, which is what the
database provides.

**Choice.** Convert each package with **Arelle** (`arelle-release`), the open-source XBRL
processor that filings.xbrl.org itself uses. That way the output has exactly the same shape, and
nothing downstream changes. The alternative was to write our own iXBRL reader, which carries more
risk (number formats, scales, signs) and offers no benefit.

**How.** `uv run tearsheet add-package <zip> --issuer afkl --origin "..." --url "..."`:
1. records the package's SHA-256 fingerprint
2. converts it with Arelle
3. checks that the LEI and the year-end date match the issuer
4. stores the gzipped xBRL-JSON in `filings/<issuer>/`
5. registers it in `filings/manual.yaml` with origin, link, download date and Arelle version

The zip itself is not committed (it's around 70 MB).

**Network.** Taxonomy files are referenced with http:// addresses, and this environment only
allows HTTPS. A small Arelle plug-in (`src/tearsheet/ingest/arelle_https.py`) fetches the same
files over HTTPS.

**Check.** ADP's FY2024 package, downloaded from filings.xbrl.org, has the same fingerprint as
that site's record of the filing. Converted with Arelle, it gives the same 343 numeric facts as
the database's own xBRL-JSON (none missing, none extra), and the same 30 mapped lines.
