import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List

logger = logging.getLogger(__name__)


def get_image_urls(page_url: str) -> List[str]:
    """
    Fetches the HTML content of a webpage and extracts all image URLs from
    src and srcset attributes.

    Args:
        page_url: The URL of the webpage to scrape.

    Returns:
        A list of absolute URLs for all images found on the page.
        Returns an empty list if the page cannot be fetched or an error occurs.

    """

    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Could not fetch URL {page_url}. Reason: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    image_urls = set()  # Set to handle duplicates.

    for tag in soup.find_all(["img", "source"]):

        src = tag.get("src")
        if src and not src.startswith("data:"):  # skip data URIs
            absolute_url = urljoin(page_url, src)
            image_urls.add(absolute_url)

        srcset = tag.get("srcset")
        if srcset:
            # Split the srcset string by commas to get individual candidates
            # e.g., "image-small.jpg 400w, image-large.jpg 800w"
            for candidate in srcset.split(","):
                url_part = candidate.strip().split(" ")[0]

                if url_part and not url_part.startswith("data:"):
                    absolute_url = urljoin(page_url, url_part)
                    image_urls.add(absolute_url)

    return list(image_urls)
