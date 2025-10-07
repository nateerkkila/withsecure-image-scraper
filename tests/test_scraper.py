import pytest
import requests
from image_scraper.scraper import get_image_urls

def test_get_image_urls_success(mocker, mock_response_class):
    """
    Tests that the function extracts expected image URLs, ignoring duplicates and empty src tags.
    """
    test_html = """
    <html>
        <body>
            <h1>Hello World</h1>
            <img src="/images/logo.png">
            <img src="https://example.com/images/banner.jpg">
            <!-- This one is a duplicate and should be ignored -->
            <img src="/images/logo.png">
            <!-- This one has an empty src -->
            <img src="">
        </body>
    </html>
    """
    base_url = "https://example.com"
    
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response_class(text=test_html)

    actual_urls = get_image_urls(base_url)

    expected_urls = {
        "https://example.com/images/logo.png",
        "https://example.com/images/banner.jpg",
    }

    assert set(actual_urls) == expected_urls

def test_get_image_urls_network_error(mocker):
    """
    Tests that the function returns an empty list when a network error occurs.
    """
    base_url = "https://example.com"

    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = requests.exceptions.RequestException("Connection timed out")

    actual_urls = get_image_urls(base_url)

    assert actual_urls == []

def test_get_image_urls_no_images_found(mocker, mock_response_class):
    """
    Tests that an empty list is returned for a page with no <img> tags.
    """
    test_html = "<html><body><p>This is a page with no images.</p></body></html>"
    base_url = "https://noimages.com"
    
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response_class(text=test_html)

    actual_urls = get_image_urls(base_url)

    assert actual_urls == []

def test_get_image_urls_handles_various_formats(mocker, mock_response_class):
    """
    Tests that the scraper correctly handles various URL formats and ignores invalid ones.
    """
    test_html = """
    <html>
        <body>
            <!-- Standard relative URL -->
            <img src="/images/relative.jpg">
            <!-- Full URL to an external domain -->
            <img src="http://cdn.com/absolute.png">
            <!-- Protocol-relative URL, should adopt the base URL's protocol -->
            <img src="//cdn.com/protocol_relative.gif">
            <!-- A data URI, which should be ignored as it's not a downloadable link -->
            <img src="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==">
            <!-- A tag with no src attribute -->
            <img>
        </body>
    </html>
    """
    base_url = "https://example.com"
    
    mock_get = mocker.patch('requests.get')
    mock_get.return_value = mock_response_class(text=test_html)

    actual_urls = get_image_urls(base_url)

    expected_urls = {
        "https://example.com/images/relative.jpg",
        "http://cdn.com/absolute.png",
        "https://cdn.com/protocol_relative.gif"
    }

    assert set(actual_urls) == expected_urls