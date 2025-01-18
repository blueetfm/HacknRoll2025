import requests

API_KEY = "AIzaSyB9-OpOGk5bwLNcosU4HpA35HAcvhMrBT8"
CX = "f1d45d72b7570443b"
query = "john nanyang"

url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"

def test():
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

results = test()
print(results)