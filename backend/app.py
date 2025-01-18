from tqdm import tqdm
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import flask_cors

from scrape import REQUEST_DELAY, crawl_page, crawl_site

API_KEY = "AIzaSyB9-OpOGk5bwLNcosU4HpA35HAcvhMrBT8"
CX = "f1d45d72b7570443b"

# app = Flask(__name__)
# CORS(app)


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
    seed_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"

    crawled_results = crawl_site(seed_url, queries,max_pages=3)

    print("Total pages crawled:", len(crawled_results))

    for i, url in enumerate(crawled_results.keys(), 1):
        print(f"{i}. {url}")

    if crawled_results:
        # print(crawled_results)    

        for pages in crawled_results.keys():
            info = crawled_results[pages]
            print("\nTitle of first page:", info['title'])
            print("Text sample:", info['text'], "...")
            print("Outbound links found:", len(info['links']))

        # page = next(iter(crawled_results))  # get one URL from dictionary
        # info = crawled_results[page]
        
    
        scrape_results = scrape_site(info['links'])
        print(scrape_results)

main()

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.json
#     name = data.get('name')
#     school = data.get('school')
    
#     if not name or not school:
#         return jsonify({"error": "Name and school are required"}), 400
    
#     try:
#         scraped_text = scrape_web(name, school)
#         analysis_result = analyze_sentiment(scraped_text)
#         return jsonify(analysis_result)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)