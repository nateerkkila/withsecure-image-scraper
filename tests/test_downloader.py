import pytest
import requests
from unittest.mock import mock_open
from image_scraper.downloader import download_images

class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError()
    
    # Add an iter_content method to simulate file streaming
    def iter_content(self, chunk_size=8192):
        yield self.content

def test_download_images_success(mocker, tmp_path):
    """
    Tests the happy path: successful download and logging of images.
    
    Args:
        mocker: The pytest-mock fixture.
        tmp_path: A pytest fixture that provides a temporary directory path.
    """
    # 1. Arrange
    # Define the temporary directory for this test
    dest_dir = tmp_path / "test_output"
    
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/logo.png"
    ]
    
    # Mock the response from requests.get
    # The content can be any fake image data
    fake_image_bytes = b'fake-image-data'
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = MockResponse(fake_image_bytes, 200)

    # 2. Act
    download_images(image_urls, str(dest_dir))

    # 3. Assert
    # Check that the directory was created
    assert dest_dir.exists()
    
    # Check that the image files were created
    image1_path = dest_dir / "image1.jpg"
    image2_path = dest_dir / "logo.png"
    assert image1_path.exists()
    assert image2_path.exists()
    
    # Check that the image content is correct
    assert image1_path.read_bytes() == fake_image_bytes

    # Check that the log file was created and has the correct content
    log_file = dest_dir / "image_log.txt"
    assert log_file.exists()
    expected_log_content = "https://example.com/image1.jpg\nhttps://example.com/logo.png\n"
    assert log_file.read_text() == expected_log_content

def test_download_images_network_failure(mocker, tmp_path):
    """
    Tests that the downloader handles a network error for one of the images.
    """
    # 1. Arrange
    dest_dir = tmp_path / "test_output"
    image_urls = [
        "https://example.com/good_image.jpg",
        "https://example.com/bad_image.png"
    ]

    # Configure the mock to succeed for the first URL and fail for the second
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = [
        MockResponse(b'good-data', 200),
        requests.exceptions.RequestException("Network Error")
    ]

    # 2. Act
    download_images(image_urls, str(dest_dir))

    # 3. Assert
    # Check that only the good image was downloaded
    assert (dest_dir / "good_image.jpg").exists()
    assert not (dest_dir / "bad_image.png").exists()

    # Check that the log file only contains the URL of the successful download
    log_file = dest_dir / "image_log.txt"
    assert log_file.exists()
    assert log_file.read_text() == "https://example.com/good_image.jpg\n"

def test_download_images_file_write_error(mocker, tmp_path):
    """
    Tests that the downloader handles an IOError when trying to save a file.
    """
    # 1. Arrange
    dest_dir = tmp_path / "test_output"
    image_urls = ["https://example.com/image.jpg"]

    # Mock a successful network request
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = MockResponse(b'some-data', 200)

    # Mock the built-in `open` function to raise an error
    mocker.patch('builtins.open', mock_open()).side_effect = IOError("Permission denied")

    # 2. Act
    download_images(image_urls, str(dest_dir))

    # 3. Assert
    # The directory is created, but the file fails to write
    assert dest_dir.exists()
    assert not (dest_dir / "image.jpg").exists()

    # The log file should also fail to write or be empty
    log_file = dest_dir / "image_log.txt"
    assert not log_file.exists()