import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        # Send an HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise error if the request fails

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all the text from the webpage's body
        page_text = ' '.join(soup.stripped_strings)
        return page_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
