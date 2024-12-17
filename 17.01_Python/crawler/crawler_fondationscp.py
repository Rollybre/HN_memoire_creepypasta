import requests
from bs4 import BeautifulSoup 
from scpper import Scpper

def crawler_page_scp(lien:str,mock:bool= False) -> list :
    """
    Crawler qui va récupérer tous les liens href d'une page
    Retourne une liste de tous les éléments
    """
    #Request pour vérifier que la page existe : 
    response = requests.get(lien, headers={'User-Agent': 'Custom'})

    if response.status_code == 200 : 
        print('Accès au lien...')
        soup = BeautifulSoup(response.text, 'html.parser')
        links=soup.find_all('a',href=True)
    return ["https://scp-wiki.wikidot.com"+i['href'] for i in links if str(i['href']).startswith("/scp")]

#def scrapping


def crawler_tale_scp(lien:str) ->list :
    """
    Crawler qui va récupérer tous les liens href de la page du tag "tale"
    Retourne une liste de tous les éléments href trouvés.
    """
    # Initialisation de la liste des liens
    href_list = []

    # Request pour vérifier que la page existe : 
    response = requests.get(lien, headers={'User-Agent': 'Custom'})

    if response.status_code == 200:
        print('Accès au lien...')
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sélecteur pour obtenir la liste des pages taguées
        selector = "html body#html-body div#skrollr-body div#container-wrap-wrap div#container-wrap div#container div#content-wrap div#main-content div#page-content div#tagged-pages-list.pages-list"

        # Sélectionner tous les éléments correspondant au sélecteur
        elements = soup.select(selector)

        # Parcourir chaque élément sélectionné
        for elem in elements:
            # Trouver tous les <a> tags dans chaque élément
            links = elem.find_all('a')
            # Extraire l'attribut href de chaque lien et l'ajouter à la liste
            for link in links:
                href = link.get('href')
                if href:  # S'assurer que le href n'est pas None
                    href_list.append(href)

    return ["https://scp-wiki.wikidot.com"+i for i in href_list ]


def scrapping_scp(url,mock=False):
    scpper=Scpper(site='en')
    if mock : 
        page=scpper.get_page(_id=11411322)
        return page._data
    else: 
        response = requests.get(url, headers={'User-Agent': 'Custom'})
        if response.status_code == 200 :
            b=BeautifulSoup(response.text, 'html.parser')
            #titre
            titre=b.find('div',id_='page-title')
            #texte
            texte=b.find_all('p', id_='page-content')
            print(titre,texte)
            #Auteur
            #tags
            #Upvote
            #nb_comm
            #is_media
            #is_canon
            #nb_href

            

    





if __name__=="__main__" :
    #print('scrapping')
    #liste=crawler_page_scp('https://scp-wiki.wikidot.com/system:page-tags/tag/scp')
    #print(liste[:4])

    res=crawler_tale_scp("https://scp-wiki.wikidot.com/system:page-tags/tag/tale#pages")

    
    print(res)