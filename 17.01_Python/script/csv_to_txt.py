import pandas as pd
from tqdm import tqdm
#Ouvrir le fichier csv
def csv_to_txt(chemin_csv): 
    data = pd.read_csv(chemin_csv)
    for i in tqdm(range(len(data))):
        titre=data.iloc[i]['Titre'].replace(' ','_').replace('/','_')
        chemin= f'./17.04_txt/{titre}.txt'
        with open(chemin, 'w',encoding='utf-8') as f :
            f.write(data.iloc[i]['Texte'])
    return
