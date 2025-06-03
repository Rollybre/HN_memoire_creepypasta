import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
import re  # Import the regular expressions library

def crawl(url, max_depth=3):
    base_url = "https://creepypasta.fandom.com/wiki/"
    # Regex pattern to match links that follow the base_url without another slash
    link_pattern = re.compile(r'^https://creepypasta.fandom.com/wiki/[^/:]+$')    
    visited = set()
    to_visit = [(url, 0)]
    while to_visit:
        url, depth = to_visit.pop(0)
        if url.startswith(base_url) and url not in visited and depth <= max_depth:
            try:
                response = requests.get(url, headers={'User-Agent': 'Custom'})
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Process the page content
                    process_page(url, soup)
                    
                    # Add page to visited
                    visited.add(url)
                    
                    # Find and process all links in the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        abs_url = urllib.parse.urljoin(url, href)
                        if link_pattern.match(abs_url) and abs_url not in visited:  # Check if the link matches the regex
                            to_visit.append((abs_url, depth + 1))
                            
            except requests.RequestException as e:
                print(f"Request failed for {url}: {str(e)}")
    print("Crawling completed.")

def process_page(url, soup):
    print(f"Processing: {url}")
    
    # Extract title
    title = soup.find('title').text if soup.find('title') else 'No title'
    
    # Extract description
    description = soup.find('meta', attrs={"name": "description"})
    description = description['content'] if description else 'No description'

    with open('crawled_data.csv', 'a', newline='') as f :
        writer = csv.writer(f)
        writer


# Starting URL
start_url = "https://creepypasta.fandom.com/wiki/"

# Start crawling
crawl(start_url)
