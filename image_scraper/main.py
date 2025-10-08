import argparse
import logging
from .scraper import get_image_urls
from .downloader import download_images

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    """
    The main entry point for the image scraper application.

    This function parses command-line arguments and orchestrates the scraping
    and downloading process.
    """
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="A command-line tool to fetch and download all "
        "static images from a webpage."
    )

    parser.add_argument(
        "url", metavar="URL", type=str, help="The full URL of the webpage to scrape."
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        type=str,
        default="downloaded_images",
        help="The directory where images will be saved. (default: downloaded_images)",
    )

    args = parser.parse_args()

    # MAIN LOGIC
    logger.info(f"Starting image scraper for: {args.url}")

    # Scrape the webpage to get image URLs
    image_urls = get_image_urls(args.url)

    if not image_urls:
        logger.warning(
            "No images found on the page or an error occurred during scraping."
        )
        return

    # Download the found images
    download_images(image_urls, args.output_dir)

    logger.info("Scraping and downloading process completed.")


if __name__ == "__main__":
    main()
