# check if a specific DOI exists in the DOAJ API -> it worked

# import requests

# def check_specific_doi_in_doaj(doi):
#     url = f"https://doaj.org/api/v2/search/articles/doi:{doi}"
#     try:
#         # Add `proxies` parameter with `None` values to bypass any system proxies
#         response = requests.get(url, proxies={"http": None, "https": None})
#         response.raise_for_status()
#         data = response.json()
        
#         # Check if there's any result in DOAJ for the DOI
#         if "results" in data and data["results"]:
#             doaj_id = data["results"][0]["id"]
#             print(f"DOI found in DOAJ with ID: {doaj_id}")
#             return doaj_id
#         else:
#             print("DOI not found in DOAJ.")
#             return None

#     except requests.RequestException as e:
#         print(f"An error occurred while checking DOI '{doi}':", e)
#         return None

# # Check if the DOI exists in DOAJ
# specific_doi = "10.1027/2698-1866/a000056"
# check_specific_doi_in_doaj(specific_doi)


####################################################################################

# checking through the whole list of Iranian Institution papers' DOI

import requests
import json

def load_dois_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Extract DOIs and titles, handling cases where keys might be absent
    articles = []
    for article in data:
        doi = article.get("DOI")
        title = article.get("title", ["No Title"])[0] if article.get("title") else "No Title"
        
        if doi:  # Only include articles that have a DOI
            articles.append({"doi": doi, "title": title})
    
    return articles

def check_doi_in_doaj(doi):
    url = f"https://doaj.org/api/v2/search/articles/doi:{doi}"
    try:
        # Add `proxies` parameter with `None` values to bypass any system proxies
        response = requests.get(url, proxies={"http": None, "https": None})
        response.raise_for_status()
        data = response.json()
        
        # Check if there's any result in DOAJ for the DOI
        if "results" in data and data["results"]:
            # Extract the first matching result's DOAJ ID and title for verification
            doaj_article = data["results"][0]
            doaj_id = doaj_article.get("id")
            doaj_title = doaj_article.get("bibjson", {}).get("title", "No Title")
            return doaj_id, doaj_title
        else:
            return None, None

    except requests.RequestException as e:
        print(f"An error occurred while checking DOI '{doi}':", e)
        return None, None

def check_dois_in_doaj(filename):
    articles = load_dois_from_file(filename)
    found_articles = []
    
    for article in articles:
        doi = article["doi"]
        original_title = article["title"]
        print(f"Checking DOI: {doi}")
        
        doaj_id, doaj_title = check_doi_in_doaj(doi)
        if doaj_id:
            print(f"DOI found in DOAJ - Title: {doaj_title}, DOAJ ID: {doaj_id}")
            found_articles.append({"original_title": original_title, "doaj_title": doaj_title, "doi": doi, "doaj_id": doaj_id})
        else:
            print("DOI not found in DOAJ.")
    
    return found_articles

# Load DOIs from Crossref JSON data and check them in DOAJ
crossref_filename = "crossref_articles_full_metadata.json"
doaj_results = check_dois_in_doaj(crossref_filename)

# Output results
print("\nArticles found in DOAJ:")
for article in doaj_results:
    print(f"Original Title: {article['original_title']}, DOAJ Title: {article['doaj_title']}, DOI: {article['doi']}, DOAJ ID: {article['doaj_id']}")

# doi = load_dois_from_file(crossref_filename)
# print(doi[0:10])