# import requests
# import time
# import json

# def fetch_crossref_metadata(keyword, rows=1000):
#     url = "https://api.crossref.org/works"
#     params = {
#         "query": keyword,
#         "rows": rows,
#         "filter": "type:journal-article"
#     }
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # Retrieve the complete metadata for each article
#         articles = data.get('message', {}).get('items', [])
#         return articles

#     except requests.RequestException as e:
#         print(f"An error occurred with keyword '{keyword}':", e)
#         return []

# def save_to_json(data, filename):
#     with open(filename, 'w') as json_file:
#         json.dump(data, json_file, indent=4)

# # Fetch data for both keywords with rate limit consideration
# all_articles = []
# keywords = ["sharif", "tehran"]

# for keyword in keywords:
#     print(f"Fetching data for keyword: {keyword}")
#     articles = fetch_crossref_metadata(keyword)
#     all_articles.extend(articles)
#     time.sleep(1)  # Respect rate limits between requests

# # Save combined data to JSON
# save_to_json(all_articles, "crossref_articles_full_metadata.json")
# print("Data has been saved to crossref_articles_full_metadata.json.")

# ##################################################################################
# import requests
# import time
# import json

# def fetch_crossref_metadata(keyword, rows=1000):
#     url = "https://api.crossref.org/works"
#     params = {
#         "query": keyword,
#         "rows": rows,
#         "filter": "type:journal-article"
#     }
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # Collecting only relevant metadata
#         articles = []
#         if 'message' in data:
#             for item in data['message']['items']:
#                 article_data = {
#                     "title": item.get("title", ["No Title"])[0],
#                     "authors": [author.get("given", "") + " " + author.get("family", "") for author in item.get("author", [])],
#                     "journal": item.get("container-title", ["No Journal"])[0],
#                     "doi": item.get("DOI", "No DOI"),
#                     "published_date": item.get("published-print", {}).get("date-parts", [["No Date"]])[0]
#                 }
#                 articles.append(article_data)
#         return articles

#     except requests.RequestException as e:
#         print(f"An error occurred with keyword '{keyword}':", e)
#         return []

# def save_to_json(data, filename):
#     with open(filename, 'w') as json_file:
#         json.dump(data, json_file, indent=4)

# # Fetch data for both keywords with rate limit consideration
# all_articles = []
# keywords = ["sharif", "tehran"]

# for keyword in keywords:
#     print(f"Fetching data for keyword: {keyword}")
#     articles = fetch_crossref_metadata(keyword)
#     all_articles.extend(articles)
#     time.sleep(1)  # Respect rate limits between requests

# # Save combined data to JSON
# save_to_json(all_articles, "crossref_articles.json")
# print("Data has been saved to crossref_articles.json.")

############################################################

import requests
import time
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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

# Fetch data for both keywords with rate limit consideration
all_articles = []
keywords = ["sharif", "tehran"]

for keyword in keywords:
    print(f"Fetching data for keyword: {keyword}")
    articles = fetch_crossref_metadata(keyword)
    all_articles.extend(articles)
    time.sleep(1)  # Respect rate limits between requests

# Save combined data to JSON
save_to_json(all_articles, "crossref_articles_full_metadata.json")
print("Data has been saved to crossref_articles_full_metadata.json.")
