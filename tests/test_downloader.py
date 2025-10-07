import pytest
import requests
from unittest.mock import mock_open
from image_scraper.downloader import download_images


def test_download_images_success(mocker, tmp_path, mock_response_class):
    """
    Tests the successful download and logging of multiple images.
    """
    dest_dir = tmp_path / "test_output"
    image_urls = ["https://example.com/image1.jpg", "https://example.com/logo.png"]
    fake_image_bytes = b"fake-image-data"

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(content=fake_image_bytes)

    download_images(image_urls, str(dest_dir))

    image1_path = dest_dir / "image1.jpg"
    image2_path = dest_dir / "logo.png"
    log_file = dest_dir / "image_log.txt"

    assert dest_dir.exists()
    assert image1_path.exists()
    assert image2_path.exists()
    assert image1_path.read_bytes() == fake_image_bytes
    assert log_file.exists()
    assert (
        log_file.read_text()
        == "https://example.com/image1.jpg\nhttps://example.com/logo.png\n"
    )


def test_download_images_network_failure(mocker, tmp_path, mock_response_class):
    """
    Tests that the downloader correctly handles a network error for one of the images.
    """
    dest_dir = tmp_path / "test_output"
    image_urls = [
        "https://example.com/good_image.jpg",
        "https://example.com/bad_image.png",
    ]

    mock_get = mocker.patch("requests.get")
    mock_get.side_effect = [
        mock_response_class(content=b"good-data"),
        requests.exceptions.RequestException("Network Error"),
    ]

    download_images(image_urls, str(dest_dir))

    assert (dest_dir / "good_image.jpg").exists()
    assert not (dest_dir / "bad_image.png").exists()

    log_file = dest_dir / "image_log.txt"
    assert log_file.exists()
    assert log_file.read_text() == "https://example.com/good_image.jpg\n"


def test_download_images_file_write_error(mocker, tmp_path, mock_response_class):
    """
    Tests that the downloader handles an IOError when trying to save a file.
    """
    dest_dir = tmp_path / "test_output"
    image_urls = ["https://example.com/image.jpg"]

    mock_get = mocker.patch("requests.get")
    mock_get.return_value = mock_response_class(content=b"some-data")

    # Mock the built-in `open` function to raise an IOError
    mocker.patch("builtins.open", mock_open()).side_effect = IOError(
        "Permission denied"
    )

    download_images(image_urls, str(dest_dir))

    assert dest_dir.exists()
    assert not (dest_dir / "image.jpg").exists()
    assert not (dest_dir / "image_log.txt").exists()
