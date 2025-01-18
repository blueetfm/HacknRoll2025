import requests
from bs4 import BeautifulSoup
import time
import networkx as nx
from pyvis.network import Network
from tqdm import tqdm
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse

REQUEST_DELAY = 1 # in seconds
def get_robots_parser(domain):
    """
    Create and initialize a RobotFileParser for the given domain.
    """
    rp = RobotFileParser()
    try:
        # Construct robots.txt URL
        robots_url = urljoin(domain, '/robots.txt')
        rp.set_url(robots_url)
        rp.read()
        return rp
    except Exception as e:
        print(f"Error reading robots.txt from {domain}: {e}")
        return None

def can_fetch(url, user_agent="*"):
    """
    Check if a URL can be fetched according to the site's robots.txt rules.
    """
    domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    rp = get_robots_parser(domain)

    if rp is None:
        # If we can't read robots.txt, we should err on the side of caution
        print(f"Could not read robots.txt for {domain}, assuming URL is not allowed")
        return False

    return rp.can_fetch(user_agent, url)

# Example usage of robots.txt checking
def check_robots_example():
    """
    Demonstrate how to use robots.txt checking functions.
    """
    test_urls = [
        "https://nushackers.org",
        "https://google.com",
        "https://wikipedia.org"
    ]

    print("\nRobots.txt Check Examples:")
    print("-" * 50)
    for url in test_urls:
        allowed = can_fetch(url)
        print(f"URL: {url}")
        print(f"Allowed to crawl: {allowed}")

        # Get the robots.txt content for demonstration
        domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        robots_url = urljoin(domain, '/robots.txt')
        try:
            response = requests.get(robots_url, timeout=5)
            print(f"Robots.txt preview (first 3 lines):")
            print("\n".join(response.text.split("\n")[:20]))
        except Exception as e:
            print(f"Could not fetch robots.txt: {e}")
        print("-" * 50)

# Crawls a single page

def crawl_page(url):
    """Fetch a single URL and return its title, text, and links."""
    try:
        # First check robots.txt
        # Ignore for now 
        # # if not can_fetch(url):
        # #     print(f"[Warning] URL not allowed by robots.txt: {url}")
        # #     return None

        response = requests.get(url, timeout=5)
        # Check if the request was successful
        if response.status_code != 200:
            print(f"[Warning] Status code {response.status_code} for URL: {url}")
            return None
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Extract text (this is a simplistic approach)
        # Removing scripts and style tags can help reduce noise
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()
        page_text = soup.get_text(separator=' ', strip=True)

        # Extract all outbound links
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Skip internal page links (starting with #) and empty links
            if href.startswith('#') or not href:
                continue
            # Skip mailto links or javascript void
            if href.startswith('mailto:') or href.startswith('javascript:'):
                continue
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            # Skip if the absolute URL is the same as current page
            if absolute_url == url:
                continue
            links.append(absolute_url)

        return {
            'url': url,
            'title': title,
            'text': page_text,
            'links': links
        }
    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to retrieve {url}: {e}")
        return None