import random
import re

import httpx
import pyalex
from abstructs.logging_config import setup_logging
from playwright.async_api import async_playwright
from pyalex import Authors, Funders, Institutions, Publishers, Sources, Topics, Works
from selectolax.parser import HTMLParser

logger = setup_logging()

pyalex.config.email = "beau@beauhilton.com"
pyalex.config.max_retries = 0
pyalex.config.retry_backoff_factor = 0.1
pyalex.config.retry_http_codes = [429, 500, 503]

JOURNAL_SELECTORS = {
    "nejm.org": "#summary-abstract",
    "doi.org": "",  # for doi urls, OpenAlex will give us the abstract without a selector
}

# List of User-Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more user agents if needed
]


def extract_doi(url: str) -> str:
    if url.startswith("https://doi.org/"):
        return url
    elif "nejm.org" in url:
        parts = url.split("/")
        if "full" in parts:
            doi_index = parts.index("full") + 1
            if doi_index < len(parts):
                return f"https://doi.org/{'/'.join(parts[doi_index:])}"
    else:
        # Check if the input is a DOI itself using a regular expression
        doi_pattern = re.compile(r"10.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
        match = doi_pattern.search(url)
        if match:
            return f"https://doi.org/{match.group(0)}"
    return ""


def ensure_https_protocol(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


async def fetch_abstract(url: str) -> str:
    url = ensure_https_protocol(url)
    doi_url = extract_doi(url)
    if doi_url:
        abstract = await get_pyalex_abstract(doi_url)
        if abstract:
            return abstract
    matching_domain = get_matching_domain(url)
    if not matching_domain:
        raise HTTPException(status_code=400, detail="Unsupported journal")
    selector = JOURNAL_SELECTORS[matching_domain]
    try:
        abstract = await fetch_abstract_with_httpx(url, selector)
        return abstract
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPX Request failed: {e}")
        if e.response.status_code == 403:
            return await fetch_abstract_with_playwright(url, selector)
        else:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))


async def get_pyalex_abstract(doi_url: str) -> str | None:
    try:
        w = Works()[doi_url]
        abstract = w["abstract"]
        return abstract
    except Exception as e:
        logger.error(f"Failed to get abstract from pyalex: {e}")
        return None


def get_matching_domain(url: str) -> str | None:
    for domain in JOURNAL_SELECTORS:
        if domain in url:
            return domain
    return None


async def fetch_abstract_with_httpx(url: str, selector: str) -> str:
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com",
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, headers=headers)
        logger.info(f"HTTPX Response Status: {response.status_code}")
        logger.info(f"HTTPX Response Headers: {response.headers}")
        logger.info(f"HTTPX Response Content: {response.text}")
        response.raise_for_status()
        html = response.text

    parser = HTMLParser(html)
    abstract_node = parser.css_first(selector)
    if not abstract_node:
        raise HTTPException(status_code=404, detail="Abstract not found on the page")

    return abstract_node.text(strip=True)
