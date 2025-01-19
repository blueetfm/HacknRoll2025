from collections import deque
import requests
from bs4 import BeautifulSoup
import time
import networkx as nx
# from pyvis.network import Network
from tqdm import tqdm
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from keybert import KeyBERT
from transformers import pipeline

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

def crawl_page(url, queries):
    """Fetch a single URL and return its title, text, and links."""
    try:
        # First check robots.txt
        if not can_fetch(url):
            print(f"[Warning] URL not allowed by robots.txt: {url}")
            return None

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

            # Skip if the page text doesnt include anything about the person / school
            if not any(query in page_text for query in queries):
                print("Skipping as no content found")
                continue
            # Skip if the absolute URL is the same as current page
            if absolute_url == url:
                continue
            links.append(absolute_url)

        return {
            'url': url,
            'title': title,
            'text': page_text[:5000],
            'links': links
        }
    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to retrieve {url}: {e}")
        return None
   
    
def crawl_site(start_url, queries, max_pages=3):
    """
    Crawl from start_url up to max_pages pages.
    Returns a dictionary: { url: {'title':..., 'text':..., 'links':[...] } }
    """
    crawled_data = {}
    visited = set()
    queue = deque([start_url])

    # Create progress bar without URL initially
    pbar = tqdm(total=max_pages, desc="Starting crawl...")

    while queue and len(crawled_data) < max_pages:
        current_url = queue.popleft()
        if current_url in visited:
            continue

        # Update progress bar description with current URL
        pbar.set_description(f"Crawling: {current_url[:50]}...")

        visited.add(current_url)
        result = crawl_page(current_url, queries)
        time.sleep(REQUEST_DELAY)

        if result:
            crawled_data[current_url] = result
            pbar.update(1)

            # Convert links to absolute URLs and add them to queue
            for link in result['links']:
                # Skip mailto links or javascript void
                if link.startswith('mailto:') or link.startswith('javascript:'):
                    continue
                absolute_url = urljoin(current_url, link)

                # Basic domain check or skip if you only want to crawl same domain
                parsed = urlparse(absolute_url)
                if parsed.scheme in ('http', 'https'):
                    # check that the queried name and school are in the links
                    for query in queries:
                        if query in absolute_url.lower():
                            print(absolute_url)  
                            queue.append(absolute_url)

    pbar.close()
    return crawled_data

def crawl_google_search(url) -> [{}]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        print(f"Length of items: {len(items)}")
        results = [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            }
            for item in items
        ]
        return results

    except Exception as e:
        print(f"Error fetching page {url}: {e}")
        return None
    

def scrape_google_search_queries(search_results, queries):
    crawled_results = []
    for result in search_results:
        site_result = crawl_page(result['link'], queries)
        crawled_results.append(site_result)
    
    return crawled_results

def summarize_and_extract_keywords_multi_topic(text, topics, num_keywords=5, summary_length=100):
    kw_model = KeyBERT()
    
    keywords = kw_model.extract_keywords(
        text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10, use_maxsum=True, diversity=0.7
    )
    
    relevant_keywords = [
        kw[0] for kw in keywords 
        if any(topic.lower() in kw[0].lower() for topic in topics)
    ][:num_keywords]
    
    combined_topics = " ".join(topics)
    
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    context_enhanced_text = f"{combined_topics}: {text}"  # Adding topics as a prefix for context
    summary = summarizer(context_enhanced_text, max_length=10, min_length=5, do_sample=False)
    
    return {
        "summary": summary[0]['summary_text'],
        "keywords": relevant_keywords
    }

def summarize_scraped_text(crawled_results: [{}], queries):
    summary = []
    for url in crawled_results:
        if url is not None and url['text'] is not None:
            print(f"url text: {url['text']}")
            summarized_url = summarize_and_extract_keywords_multi_topic(url['text'], queries)
            summary.append(summarized_url)
    
    return summary
        