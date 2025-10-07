import requests
from unittest.mock import mock_open
import hashlib
from image_scraper.downloader import download_images


def test_download_images_success(mocker, tmp_path, mock_response_class):
    """
    Tests the successful download and logging of multiple images with a
    human-readable and hashed filename format.
    """
    dest_dir = tmp_path / "test_output"
    url1 = "https://example.com/image1.jpg"
    url2 = "https://example.com/logo.png"
    image_urls = [url1, url2]

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(
        content=b"fake-image-data",
        headers={"Content-Type": "image/jpeg"},  # Provide a valid image type
    )

    download_images(image_urls, str(dest_dir))

    hash1 = hashlib.sha256(url1.encode("utf-8")).hexdigest()[:8]
    hash2 = hashlib.sha256(url2.encode("utf-8")).hexdigest()[:8]

    file1_path = dest_dir / f"image1-{hash1}.jpg"
    file2_path = dest_dir / f"logo-{hash2}.png"
    log_file_path = dest_dir / "image_log.txt"

    assert dest_dir.exists()
    assert file1_path.exists()
    assert file2_path.exists()
    assert file1_path.read_bytes() == b"fake-image-data"

    assert log_file_path.exists()
    assert log_file_path.read_text() == f"{url1}\n{url2}\n"


def test_downloader_handles_filename_collisions(mocker, tmp_path, mock_response_class):
    """
    Tests that two different URLs with the same basename do not overwrite each other.
    """
    dest_dir = tmp_path / "test_output"
    url1 = "https://site1.com/assets/logo.png"
    url2 = "https://site2.com/images/logo.png"
    image_urls = [url1, url2]

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(
        content=b"fake-png-data", headers={"Content-Type": "image/png"}
    )

    download_images(image_urls, str(dest_dir))

    hash1 = hashlib.sha256(url1.encode("utf-8")).hexdigest()[:8]
    hash2 = hashlib.sha256(url2.encode("utf-8")).hexdigest()[:8]

    file1_path = dest_dir / f"logo-{hash1}.png"
    file2_path = dest_dir / f"logo-{hash2}.png"

    assert file1_path.exists()
    assert file2_path.exists()
    assert file1_path != file2_path


def test_downloader_skips_non_image_content_type(mocker, tmp_path, mock_response_class):
    """
    Tests that a URL with a non-image Content-Type (e.g., text/html) is skipped.
    """
    dest_dir = tmp_path / "test_output"
    image_urls = ["https://example.com/not_an_image"]

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(
        content=b"<html>this is not an image</html>",
        headers={"Content-Type": "text/html"},
    )

    download_images(image_urls, str(dest_dir))

    # Note: The log file is only created if there is at least one successful download.
    assert not list(dest_dir.iterdir())


def test_downloader_derives_extension_from_content_type(
    mocker, tmp_path, mock_response_class
):
    """
    Tests that an extension is correctly derived from the Content-Type header
    when the URL itself does not have one.
    """
    dest_dir = tmp_path / "test_output"
    url = "https://example.com/image-without-ext"
    image_urls = [url]

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(
        content=b"fake-gif-data", headers={"Content-Type": "image/gif"}
    )

    download_images(image_urls, str(dest_dir))

    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]
    # The extension should be .gif, derived from the header
    expected_filename = f"image-without-ext-{url_hash}.gif"

    assert (dest_dir / expected_filename).exists()


def test_download_images_network_failure(mocker, tmp_path, mock_response_class):
    """
    Tests that the downloader correctly handles a network error for one of the images
    and only downloads and logs the successful one.
    """
    dest_dir = tmp_path / "test_output"
    good_url = "https://example.com/good_image.jpg"
    bad_url = "https://example.com/bad_image.png"
    image_urls = [good_url, bad_url]

    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = [
        mock_response_class(
            content=b"good-data", headers={"Content-Type": "image/jpeg"}
        ),
        requests.exceptions.RequestException("Network Error"),
    ]

    download_images(image_urls, str(dest_dir))

    good_hash = hashlib.sha256(good_url.encode("utf-8")).hexdigest()[:8]
    good_filename = f"good_image-{good_hash}.jpg"

    assert (dest_dir / good_filename).exists()
    # Check that no other files (like from the bad URL) were created
    assert len(list(dest_dir.glob("*"))) == 2  # The image and the log file

    log_file = dest_dir / "image_log.txt"
    assert log_file.exists()
    assert log_file.read_text() == f"{good_url}\n"


def test_download_images_file_write_error(mocker, tmp_path, mock_response_class):
    """
    Tests that the downloader handles an IOError when trying to save a file
    and does not log the URL as successful.
    """
    dest_dir = tmp_path / "test_output"
    image_urls = ["https://example.com/image.jpg"]

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(
        content=b"some-data", headers={"Content-Type": "image/jpeg"}
    )

    # Mock the built-in `open` function to raise an IOError
    mocker.patch("builtins.open", mock_open()).side_effect = IOError(
        "Permission denied"
    )

    download_images(image_urls, str(dest_dir))

    assert dest_dir.exists()
    assert not list(dest_dir.iterdir())
