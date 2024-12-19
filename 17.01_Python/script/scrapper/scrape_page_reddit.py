import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def recup_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        titre_tag = soup.find('p', class_="title")
        titre = titre_tag.text if titre_tag else 'No Title Found'
        author_tag = soup.find(lambda tag: tag.get('data-author'))
        author_name = author_tag.get('data-author') if author_tag else 'Unknown'
        text_tag = soup.find('div', class_='expando')
        text = text_tag.text if text_tag else 'No Text Found'
        upvote_tag = soup.find('div', class_='score unvoted')
        upvote = upvote_tag.text if upvote_tag else 'No Upvotes'
        date_tag = soup.find('div', class_='date')
        date = date_tag.text if date_tag else 'No Date'
        return {
            'Titre': titre,
            'Auteurs': author_name,
            'Upvotes': upvote,
            'Date': date,
            'Texte': text,
            'taille': len(text)
        }
    else:
        print('Failed to retrieve the webpage')
        return {
            'Titre': 'Failed to retrieve',
            'Auteurs': 'Failed to retrieve',
            'Upvotes': 'Failed to retrieve',
            'Date': 'Failed to retrieve',
            'Texte': 'Failed to retrieve',
            'taille' : 'Failed to retrieve'
        }

# Read URLs from CSV file
urls = pd.read_csv("../17.02_CSV.CSV/reddit_links_01_mars.csv")
urls_list = [i for i in urls['Links'] if 'alb.' not in i]

results = []
# Add a progress bar using tqdm
for url in tqdm(urls_list, total=len(urls_list)):
    info = recup_info(url)
    info['Lien'] = url  # Add the URL to the dictionary
    results.append(info)

# Create DataFrame from results
df = pd.DataFrame(results)

# Save to CSV
df.to_csv('../17.02_CSV.CSV/scrapping_reddit_01_mars.csv', index=False)
