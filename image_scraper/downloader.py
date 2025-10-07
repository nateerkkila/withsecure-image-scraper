import os
import requests
from typing import List
from urllib.parse import urlparse


def download_images(image_urls: List[str], dest_dir: str) -> None:
    """
    Downloads images from a list of URLs and saves them to a destination directory,
    along with a log file.


    Args:
       image_urls: A list of absolute URLs of the images to download.
       dest_dir: The local directory path where images and the log file will be saved.
    """

    os.makedirs(dest_dir, exist_ok=True)
    successful_urls = []

    print(f"\nDownloading {len(image_urls)} images to '{dest_dir}/'...")

    for url in image_urls:
        try:
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()

            # Generate a safe filename from the url.
            filename = os.path.basename(urlparse(url).path)
            if not filename:  # Handle cases where URL ends in a slash
                filename = "downloaded_image_" + url.split("/")[-2]

            file_path = os.path.join(dest_dir, filename)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f" Successfully downloaded {filename}")
            successful_urls.append(url)

        except requests.exceptions.RequestException as e:
            print(f"  Failed to download {url}. Reason: {e}")
        except IOError as e:
            print(f"  Failed to save image from {url}. Reason: {e}")

    _log_successful_downloads(successful_urls, dest_dir)


def _log_successful_downloads(urls: List[str], dest_dir: str) -> None:
    """
    Writes a list of URLs to a log file.
    This is a helper function intended for internal use within this module.
    """
    log_path = os.path.join(dest_dir, "image_log.txt")

    try:
        with open(log_path, "w") as f:
            for url in urls:
                f.write(f"{url}\n")
        print(f"\nSuccessfully created log file: {log_path}")
    except IOError as e:
        print(f"Error: Could not write to log file {log_path}. Reason: {e}")
