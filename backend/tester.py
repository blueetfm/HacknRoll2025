from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import flask_cors
from flask import Flask, request, jsonify

from ocr import read_resume
from scrape_test import REQUEST_DELAY, crawl_page, crawl_site, crawl_google_search, scrape_google_search_queries

API_KEY = "AIzaSyB9-OpOGk5bwLNcosU4HpA35HAcvhMrBT8"
CX = "f1d45d72b7570443b"

# app = Flask(__name__)
# CORS(app)                             

# def scrape_site(links):
#     res = []
#     for link in links:
#         response = requests.get(link)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         results = soup.find_all('div', class_='g')
#         text = ' '.join([result.get_text() for result in results[:]])
#         print(f"text: {text} \n")
#         res.append(text)
        
#     return res


def crawl(url):

    """
    API endpoint to crawl a site.
    Expects JSON input with keys:
      - start_url: The starting URL for the crawl
      - queries: List of query strings to match links
      - max_pages: (optional) Maximum number of pages to crawl (default: 15)
    """
    # data = request.get_json()
    # url = data.get("link")
    info = read_resume(url)
    queries = []
    # Extract name
    name = info['name']

    # Get the 2 most recent job titles
    recent_jobs = info['job_titles'][:1]  # Slice the first 2 job titles

    # Get the 2 most recent education titles
    recent_education = info['education'][:1]  # Slice the first 2 education titles

    # Construct the query
    query = (
        f"{'+'.join(name.split())}+"
        f"{'+'.join('+'.join(job.split()) for job in recent_jobs)}+"
        f"{'+'.join('+'.join(school.split()) for school in recent_education)}"
    )
    # query = "Jiang Zong Zhe"
    print(query)
    seed_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"
    search_results = crawl_google_search(seed_url)
    print(search_results)

    if search_results:
        crawled_results = scrape_google_search_queries(search_results, queries)
    else:
        print("No search results found.")

    if crawled_results:
        print(crawled_results)
        return crawled_results

print(crawl("https://tdbzbuocqslnmyfvxokj.supabase.co/storage/v1/object/public/images/Resume.jpg"))
