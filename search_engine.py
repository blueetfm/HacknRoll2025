from collections import deque
from tqdm import tqdm
import time
from urllib.parse import urljoin, urlparse

from check_robots import REQUEST_DELAY, crawl_page

def crawl_site(start_url, max_pages=5):
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
        result = crawl_page(current_url)
        # Polite delay
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
                    # check that the queried name is in the links
                    if any(query in absolute_url.lower() for query in ['john lim', 'nanyang polytechnic']):  
                      queue.append(absolute_url)

    pbar.close()
    return crawled_data

