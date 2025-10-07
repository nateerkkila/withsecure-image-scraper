import pytest
import requests


@pytest.fixture
def mock_response_class():
    """Provides a reusable MockResponse class for testing."""

    class MockResponse:
        def __init__(self, text="", content=b"", status_code=200, headers=None):
            self.text = text
            self.content = content
            self.status_code = status_code
            self.headers = headers if headers is not None else {}  # Add headers support

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError(f"HTTP Error {self.status_code}")

        def iter_content(self, chunk_size=8192):
            yield self.content

    return MockResponse
