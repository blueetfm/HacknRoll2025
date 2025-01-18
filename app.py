from search_engine import crawl_site

def main():
    name = input("What's your name? ")
    school = input("What's your school? ")
    query=f"{'+'.join(name.split())}+{'+'.join(school.split())}"
    seed_url = f"https://www.google.com/search?q={query}"

    crawled_results = crawl_site(seed_url, max_pages=5)

    print("Total pages crawled:", len(crawled_results))

    # Let's list the crawled URLs
    for i, url in enumerate(crawled_results.keys(), 1):
        print(f"{i}. {url}")

    if crawled_results:
        print(crawled_results)
        # page = next(iter(crawled_results))  # get one URL from dictionary
        # info = crawled_results[page]
        # print("\nTitle of first page:", info['title'])
        # print("Text sample:", info['text'], "...")
        # print("Outbound links found:", len(info['links']))



main()