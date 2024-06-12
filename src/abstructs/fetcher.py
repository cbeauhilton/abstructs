import httpx
import random
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser
import pyalex
from pyalex import Works, Authors, Sources, Institutions, Topics, Publishers, Funders

from abstructs.logging_config import setup_logging

logger = setup_logging()

pyalex.config.email = "beau@beauhilton.com"
pyalex.config.max_retries = 0
pyalex.config.retry_backoff_factor = 0.1
pyalex.config.retry_http_codes = [429, 500, 503]

# Journal to CSS selector mapping
JOURNAL_SELECTORS = {
    "nejm.org": "#summary-abstract",
    "example.com": ".abstract-section",  # Add more journals and their respective selectors here
}

# List of User-Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more user agents if needed
]


def extract_doi(url: str) -> str:
    if "nejm.org" in url:
        parts = url.split("/")
        if "full" in parts:
            doi_index = parts.index("full") + 1
            if doi_index < len(parts):
                return "/".join(parts[doi_index:])
    return ""


def ensure_https_protocol(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def get_pyalex_abstract(doi: str) -> str:
    full_doi = f"https://doi.org{doi}"
    w = Works()[full_doi]
    abstract = w["abstract"]
    return abstract


async def fetch_abstract(url: str) -> str:
    url = ensure_https_protocol(url)
    doi = extract_doi(url)

    # Try getting the abstract using pyalex
    if doi:
        try:
            abstract = get_pyalex_abstract(doi)
            if abstract:
                return abstract
        except Exception as e:
            logger.error(f"Failed to get abstract from pyalex: {e}")

    matching_domain = None
    for domain in JOURNAL_SELECTORS:
        if domain in url:
            matching_domain = domain
            break

    if not matching_domain:
        raise HTTPException(status_code=400, detail="Unsupported journal")

    selector = JOURNAL_SELECTORS[matching_domain]

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com",
    }

    try:
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
            raise HTTPException(
                status_code=404, detail="Abstract not found on the page"
            )

        return abstract_node.text(strip=True)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPX Request failed: {e}")
        if e.response.status_code == 403:
            return await fetch_abstract_with_playwright(url, selector)
        else:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))


async def fetch_abstract_with_playwright(url: str, selector: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False
        )  # Launch browser in headful mode
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(
            5000
        )  # Wait for 5 seconds to ensure the page loads completely
        content = await page.content()
        await browser.close()

        logger.info(f"Fetched content with Playwright: {content}")

        parser = HTMLParser(content)
        abstract_node = parser.css_first(selector)
        if not abstract_node:
            raise HTTPException(
                status_code=404, detail="Abstract not found on the page"
            )

        return abstract_node.text(strip=True)
