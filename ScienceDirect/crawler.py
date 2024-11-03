import requests
import json
from unidecode import unidecode

def fetch_article_data(doi, api_key):
    url = f"https://api.elsevier.com/content/article/doi/{doi}"

    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching DOI {doi}: {response.status_code}, {response.text}")
        return None

def extract_data(article_data):
    if article_data and "full-text-retrieval-response" in article_data:
        article_info = article_data['full-text-retrieval-response']
        
        # Extracting basic fields
        title = article_info.get('coredata', {}).get('dc:title', '')
        doi = article_info.get('coredata', {}).get('dc:identifier', '')
        abstract = article_info.get('coredata', {}).get('dc:description', '')
        keywords = article_info.get('coredata', {}).get('dc:subject', [])

        authors = []
        affiliations = []

        # Extracting authors and converting to ASCII
        for author in article_info.get('coredata', {}).get('dc:creator', []):
            author_name = author['$']
            authors.append(unidecode(author_name))

        # Extracting affiliations
        for affiliation in article_info.get('coredata', {}).get('affil', []):
            affiliations.append(affiliation.get('affilname', ''))

        # Preparing the extracted data
        extracted_info = {
            "title": title,
            "doi": doi,
            "abstract": abstract,
            "keywords": keywords,
            "authors": authors,
            "affiliations": affiliations,
            "full_response": article_info  # Save the entire response
        }
        return extracted_info
    else:
        print("Article data is not available.")
        return None

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")

def main():
    dois = [
        "10.1016/j.jbiomech.2020.109800",  # Replace with your DOI
        "10.1016/j.neunet.2020.11.002",  # Example DOI
        "10.1016/j.asoc.2024.112405"  # Example DOI
    ]
    api_key = "d36f353dfe7a31739e6b1aa7289eee30"  # Replace with your ScienceDirect API key

    all_articles_data = []

    for doi in dois:
        article_data = fetch_article_data(doi, api_key)
        extracted_data = extract_data(article_data)
        
        if extracted_data:
            all_articles_data.append(extracted_data)

    save_to_json(all_articles_data, "./data/article_full_data.json")

if __name__ == "__main__":
    main()
