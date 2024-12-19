import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
import pandas as pd
import re
import scpper

def scrapping_scp(urls: list, file_path: str):
    #instance api
    #scp_api=scpper.Scpper()
    # Define the CSS selectors
    selectors = {
        'id': 'html head script',
        'title': 'div#page-title',
        'text': 'div#page-content',
        'tags': 'div.page-tags span a',
        'upvotes': 'span.rate-points span.number.prw54353',
        'comments': 'a#discuss-button'
    }

    # Open the CSV file in write mode
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['URL', 'ID', 'Title', 'Text', 'Tags', 'Upvotes', 'Comments', 'Has Image'])

        # Loop through each URL and scrape data
        for ind, url in enumerate(tqdm(urls)):
            try:
                # Send a GET request to the URL
                response = requests.get(url)
                response.encoding = 'utf-8'  # Handle character encoding

                # Parse the content of the page with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract data using the defined CSS selectors
                data = {}
                for key, selector in selectors.items():
                    element = soup.select(selector)
                    data[key] = ' '.join(e.text.strip() for e in element) if element else 'N/A'

                # Special handling for tags to include spaces
                tags_element = soup.select(selectors['tags'])
                data['tags'] = ', '.join(tag.text.strip() for tag in tags_element) if tags_element else 'N/A'

                # Check if there is an image on the page
                page_content_div = soup.find('div', id='page-content')
                if page_content_div.find('img') : 
                    has_image=True
                else:
                    has_image=False

                # Clean and process data
                data['text'] = data['text'].replace('\n', ' ').replace('\r', ' ')

                # Extract page ID from the JavaScript block
                match = re.search(r"WIKIREQUEST\.info\.pageId = (\d+);", response.text)
                data['id'] = match.group(1) if match else 'N/A'

                # Get the date through the api 
                #page=scp_api.get_page(data['id'])

                # Write the data to CSV file
                writer.writerow([url, data['id'], data['title'], data['text'], data['tags'], data['upvotes'], data['comments'], has_image])

            except Exception as e:
                print(f'Error at line {ind} for URL: {url} - {e}')
                continue  # Skip to the next URL in case of an error

    print(f"Data from all URLs has been successfully saved to {file_path}")
    return

# Running the function with test data
if __name__ == '__main__':
    path = 'scp_data_test.csv'
    scrapping_scp(urls=['https://scp-wiki.wikidot.com/scp-1000'], file_path=path)
    df = pd.read_csv(path)
    print(df.head())