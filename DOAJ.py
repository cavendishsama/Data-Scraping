import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Define the DOAJ API URL for searching articles
BASE_URL = "https://doaj.org/api/v4/search/articles"

# Specify the DOI you want to search for
doi = "10.1027/2698-1866/a000056"  # Replace with the actual DOI

# Set up the parameters for the API request
params = {
    "query": f'doi:"{doi}"'
}

# Send a GET request to the DOAJ API
# response = requests.get(BASE_URL, params=params)
response = requests.get(BASE_URL, params=params, verify=False)


# Check if the response is successful
if response.status_code == 200:
    data = response.json()
    articles = data.get('results', [])
    
    # Check if any articles are found
    if articles:
        article = articles[0]
        title = article.get("title", "N/A")
        authors = ", ".join(author.get("name", "N/A") for author in article.get("author", []))
        abstract = article.get("abstract", "N/A")
        
        print(f"Title: {title}\nAuthors: {authors}\nAbstract: {abstract}\n")
    else:
        print("No article found with that DOI.")
else:
    print(f"Error fetching data: {response.status_code}")
