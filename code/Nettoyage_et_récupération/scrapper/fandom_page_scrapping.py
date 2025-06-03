import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re

def recup_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text_tag = soup.find("textarea", class_="mw-editfont-default")
        text = text_tag.text if text_tag else 'No Text Found'

        tags = re.findall(r"\[\[Category.*\]\]", text)
        author = re.findall(r"\{\{User.*\}\}", text)
        return {
            'Auteur': author,
            'Texte': text,
            'Category': tags
        }
    else:
        print('Failed to retrieve the webpage')
        return {
            'Auteur': 'Failed to retrieve',
            'Texte': 'Failed to retrieve',
            'Category': 'Failed to retrieve'
        }

# Read URLs from CSV file
urls = pd.read_csv("17.02_CSV.CSV/fandom_links.csv")
urls_list = [i + "?action=edit" for i in urls['Links']]

header_added = False  # Indicates if header has been added to the CSV file
# Add a progress bar using tqdm
for url in tqdm(urls_list, total=len(urls_list)):
    info = recup_info(url)
    info['Lien'] = url  # Add the URL to the dictionary
    # Convert single info dict to DataFrame
    df = pd.DataFrame([info])
    # Append to CSV file, add header only for the first entry
    if not header_added:
        df.to_csv('17.02_CSV.CSV/cp_fandom_scrapped.csv', mode='w', index=False)  # 'w' to write initially
        header_added = True
    else:
        df.to_csv('17.02_CSV.CSV/cp_fandom_scrapped.csv', mode='a', header=False, index=False)  # 'a' to append after
