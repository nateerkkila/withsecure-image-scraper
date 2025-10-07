import pytest
from image_scraper.main import main

def test_main_success_flow(mocker):
    """
    Tests the main function's successful execution path.
    This is an integration test for the main() orchestration logic.
    """
    mock_get_urls = mocker.patch('image_scraper.main.get_image_urls', return_value=['http://example.com/image.jpg'])
    mock_download = mocker.patch('image_scraper.main.download_images')

    test_args = ['main.py', 'https://example.com', '-o', 'test_output']
    mocker.patch('sys.argv', test_args)

    main()

    mock_get_urls.assert_called_once_with('https://example.com')
    
    mock_download.assert_called_once_with(['http://example.com/image.jpg'], 'test_output')

def test_main_no_images_found_flow(mocker, caplog):
    """
    Tests that the main function handles the "no images found" case gracefully.
    """
    mock_get_urls = mocker.patch('image_scraper.main.get_image_urls', return_value=[])
    # The downloader should NOT be called in this case.
    mock_download = mocker.patch('image_scraper.main.download_images')
    
    test_args = ['main.py', 'https://empty.com']
    mocker.patch('sys.argv', test_args)

    main()

    mock_get_urls.assert_called_once_with('https://empty.com')
    mock_download.assert_not_called()

    # Use the `caplog` fixture to check the captured log text (contains all levels).
    assert "No images found" in caplog.text