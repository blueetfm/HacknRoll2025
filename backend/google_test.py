import requests

API_KEY = "AIzaSyB9-OpOGk5bwLNcosU4HpA35HAcvhMrBT8"
CX = "f1d45d72b7570443b"
query = "john nanyang"

url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"
response = requests.get(url)
data = response.json()

for item in data.get("items", []):
    print("Title:", item["title"])
    print("Link:", item["link"])
    print("Snippet:", item["snippet"])