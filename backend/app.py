from collections import deque
from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

from backend.check_robots import REQUEST_DELAY, crawl_page

def crawl_site(start_url, queries, max_pages=15):
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

def scrape_site(links):
    res = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = soup.find_all('div', class_='g')
        text = ' '.join([result.get_text() for result in results[:]])
        print(f"text: {text} \n")
        res.append(text)
        
    return res

def main():
    queries = []
    name = input("What's your name? ")
    school = input("What's your school? ")
    queries.append(name)
    queries.append(school)

    query = f"{'+'.join(name.split())}+{'+'.join(school.split())}"
    seed_url = f"https://www.google.com/search?q={query}"

    crawled_results = crawl_site(seed_url, queries,max_pages=5)

    print("Total pages crawled:", len(crawled_results))

    # Let's list the crawled URLs
    for i, url in enumerate(crawled_results.keys(), 1):
        print(f"{i}. {url}")

    if crawled_results:
        # page = next(iter(crawled_results))
        print(crawled_results)
        # for link in page['links']:
        #     if link.contains(any(query for query in queries)):         

        page = next(iter(crawled_results))  # get one URL from dictionary
        info = crawled_results[page]
        print("\nTitle of first page:", info['title'])
        print("Text sample:", info['text'], "...")
        print("Outbound links found:", len(info['links']))
    
        scrape_results = scrape_site(info['links'])
        print(scrape_results)



main()