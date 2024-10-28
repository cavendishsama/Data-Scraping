# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # Define the base URL and the paper's unique identifier (DOI or URL)
# BASE_URL = "https://ieeexplore.ieee.org/document/10681095/keywords#keywords"
# PAPER_ID = "10681095"  # Replace with the actual paper ID

# # Construct the full URL
# url = f"{BASE_URL}{PAPER_ID}"

# # Send a GET request to the URL
# response = requests.get(url)

# # Check if the response is successful
# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Extract title
#     title = soup.find('h1', class_='document-title').get_text(strip=True)

#     # Extract authors
#     authors = soup.find_all('a', class_='author-name')
#     authors_list = [author.get_text(strip=True) for author in authors]

#     # Extract abstract
#     abstract_section = soup.find('div', class_='abstract-text')
#     abstract = abstract_section.get_text(strip=True) if abstract_section else "N/A"

#     # Extract keywords
#     keywords_section = soup.find('div', class_='keywords-section')
#     keywords = [keyword.get_text(strip=True) for keyword in keywords_section.find_all('a')] if keywords_section else []

#     # Create a dictionary to store the information
#     paper_info = {
#         "Title": title,
#         "Authors": ", ".join(authors_list),
#         "Abstract": abstract,
#         "Keywords": ", ".join(keywords)
#     }
    
#     # Save to a DataFrame and then to CSV
#     df = pd.DataFrame([paper_info])
#     df.to_csv("ieee_xplore_paper_info.csv", index=False)
    
#     print("Data extracted and saved to ieee_xplore_paper_info.csv.")
# else:
#     print(f"Failed to retrieve data: {response.status_code}")



import requests
import pandas as pd
import time

# Define the DOAJ API endpoint
DOAJ_API_URL = "https://doaj.org/api/v4/search/articles/bibjson.journal.subjects:{S}"
# https://doaj.org/api/search/articles/bibjson.title:%22mina%22

# Define a list of broad subjects or topics to gather data on
# subjects = ["biology", "computer science", "chemistry", "physics", "economics", 
#             "medicine", "engineering", "artificial intelligence", "social sciences"]
subjects = ['computer science']

# Initialize a list to collect all articles
all_articles = []

# Iterate over each subject
for subject in subjects:
    print(f"Gathering data for subject: {subject}")
    page = 1  # Start from the first page
    
    # Loop through pages for each subject
    while True:
        # Define parameters for the API call
        params = {
            "q": subject,
            "page": page,
            "pageSize": 100  # Maximum records per page for larger datasets
        }
        
        # Send request to DOAJ API
        response = requests.get(DOAJ_API_URL, params=params)
        
        # Check if response is successful
        if response.status_code == 200:
            data = response.json()
            
            # Break loop if there are no more results
            if not data.get("results"):
                break
            
            # Extract data for each article
            for item in data["results"]:
                title = item.get("bibjson", {}).get("title", "N/A")
                abstract = item.get("bibjson", {}).get("abstract", "N/A")
                authors = [author.get("name") for author in item.get("bibjson", {}).get("author", [])]
                keywords = item.get("bibjson", {}).get("keywords", [])
                
                # Append data to the main list
                all_articles.append({
                    "Subject": subject,
                    "Title": title,
                    "Abstract": abstract,
                    "Authors": ", ".join(authors),
                    "Keywords": ", ".join(keywords)
                })
            
            # Increment page number for the next request
            page += 1
            
            # Optional: Print progress
            print(f"Page {page - 1} completed for {subject}")
            
            # Optional: Save incrementally every few pages
            if page % 5 == 0:
                pd.DataFrame(all_articles).to_csv("doaj_articles_backup.csv", index=False)
        
        else:
            print(f"Failed to retrieve data for {subject} on page {page}: {response.status_code}")
            break
        
        # Rate limiting: delay between requests
        time.sleep(1)

# Save the final dataset to a CSV file
df = pd.DataFrame(all_articles)
df.to_csv("doaj_articles_all_subjects.csv", index=False)

print("Data collection completed and saved.")
