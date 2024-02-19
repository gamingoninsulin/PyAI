import csv
import requests
from bs4 import BeautifulSoup


def scrape_code_snippet(url, selector):
    """
    Scrapes a code snippet from the given URL using the specified selector.

    Args:
        url: The URL of the documentation page.
        selector: A CSS selector string to identify the code block element.

    Returns:
        The extracted code text or None if not found.
    """
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    code_block = soup.select_one(selector)

    return code_block.get_text(strip=True) if code_block else None

# No if __name__ == "__main__": block or main() function needed here.
