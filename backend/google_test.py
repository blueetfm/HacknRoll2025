from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
# import flask_cors
from flask import Flask, request, jsonify

# from ocr import read_resume
from scrape_test import REQUEST_DELAY, crawl_page, crawl_site, crawl_google_search, scrape_google_search_queries, summarize_scraped_text
from sentiment_analysis import analyze_sentiment

API_KEY = "AIzaSyB9-OpOGk5bwLNcosU4HpA35HAcvhMrBT8"
CX = "f1d45d72b7570443b"


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
    # info = read_resume(url)
    queries = []
    # Extract name
    name = "celebration"
    crawled_results = False

    # Get the 2 most recent job titles
    recent_jobs = "" # Slice the first 2 job titles

    # Get the 2 most recent education titles
    recent_education = [""]  # Slice the first 2 education titles

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
    # print(search_results)

    if search_results:
        crawled_results = scrape_google_search_queries(search_results, queries)
    else:
        print("No search results found.")

    if crawled_results:
        print("These are the crawled results")
        print(crawled_results)
        summary = summarize_scraped_text(crawled_results, queries)
        if summary:
            for url in summary:
                sentiment_analysis = analyze_sentiment(url['summary'])
                print(sentiment_analysis)
        return crawled_results

print(crawl(""))
