import requests
import time
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import import_ipynb
from persian_institution import extracted_names

def fetch_crossref_metadata(keyword, rows=1000):
    url = "https://api.crossref.org/works"
    params = {
        "query": keyword,
        "rows": rows,
        "filter": "type:journal-article"
    }

    # Configure a session with retries and no proxy
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    try:
        # Add `proxies` parameter with `None` values to bypass any system proxies
        response = session.get(url, params=params, proxies={"http": None, "https": None}, verify=True)
        response.raise_for_status()
        data = response.json()
        
        # Retrieve the complete metadata for each article
        articles = data.get('message', {}).get('items', [])
        return articles

    except requests.RequestException as e:
        print(f"An error occurred with keyword '{keyword}':", e)
        return []

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


print(extracted_names[0])

# Fetch data for both keywords with rate limit consideration
all_articles = []
# keywords = extracted_names

for keyword in extracted_names[0:5]:
    print(f"Fetching data for keyword: {keyword}")
    articles = fetch_crossref_metadata(keyword)
    all_articles.extend(articles)
    time.sleep(1)  # Respect rate limits between requests

# Save combined data to JSON
save_to_json(all_articles, "crossref_articles_full_metadata_sample1.json")
# print("Data has been saved to crossref_articles_full_metadata.json.")
