import argparse
from .scraper import get_image_urls
from .downloader import download_images


def main():
    """
    The main entry point for the image scraper application.

    This function parses command-line arguments and orchestrates the scraping
    and downloading process.
    """
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="A command-line tool to fetch and download all static images from a webpage."
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

    # --- Main Logic ---
    print(f"Starting image scraper for: {args.url}")

    # 1. Scrape the webpage to get image URLs
    image_urls = get_image_urls(args.url)

    if not image_urls:
        print("No images found on the page or an error occurred during scraping.")
        return

    # 2. Download the found images
    download_images(image_urls, args.output_dir)

    print("\nScraping and downloading process completed.")


if __name__ == "__main__":
    main()
