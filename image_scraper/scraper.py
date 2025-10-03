import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from typing import List, Optional

def get_image_urls(page_url: str) -> List[str]:
    """
    Fetches the HTML content of a webpage and extracts all image URLs.

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
        print(f"Error: Could not fetch URL {page_url}. Reason: {e}")
        return []
    
 
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = set() # Set to handle duplicates.

    for img_tag in soup.find_all('img'):
        if 'src' in img_tag.attrs:
            src = img_tag['src']
            if not src: 
                continue
            
            absolute_url = urljoin(page_url, src)
            image_urls.add(absolute_url)

    return list(image_urls)


# Just to test, to be removed...
# if __name__ == '__main__':


#     test_url = "https://devguide.python.org/versions/" 
    
#     print(f"Attempting to scrape images from: {test_url}")
    
#     found_urls = get_image_urls(test_url)
    
#     if found_urls:
#         print(f"\nSuccessfully found {len(found_urls)} image URLs:")
#         for url in found_urls:
#             print(url)
#     else:
#         print("\nNo image URLs were found or an error occurred.")