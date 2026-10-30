"""Arelle plug-in: fetch taxonomy files over HTTPS.

ESEF filings point to the IFRS, ESMA and XBRL International taxonomies with http:// addresses.
This environment only allows HTTPS, and those hosts serve the same files over HTTPS, so the
address is switched before Arelle downloads (and caches) the file.
"""


def transform_url(cntlr, url, base=None):
    if isinstance(url, str) and url.startswith("http://"):
        return "https://" + url[len("http://") :], False
    return url, False


__pluginInfo__ = {
    "name": "HTTPS taxonomy fetch",
    "version": "1.0",
    "description": "Fetch http:// taxonomy files over https://",
    "license": "MIT",
    "WebCache.TransformURL": transform_url,
}
