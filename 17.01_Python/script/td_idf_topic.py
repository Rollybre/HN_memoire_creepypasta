# text_similarity_analysis.py

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import igraph as ig
import matplotlib.pyplot as plt
import pickle

def load_stop_words(file_path):
    """Charge les mots vides depuis un fichier pickle."""
    with open(file_path, mode='rb+') as f:
        stop_words = pickle.load(f)
    return stop_words

def remove_pron(txt):
    """Enlève '-PRON-' des textes."""
    return txt.replace('-PRON-', ' ')

def adjacency_matrix_to_weighted_edgelist(adjacency_matrix):
    """Convertit la matrice d'adjacence en liste d'arêtes pondérées."""
    num_nodes = len(adjacency_matrix)
    weighted_edgelist = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adjacency_matrix[i][j] != 0:
                weighted_edgelist.append([i, j, adjacency_matrix[i][j]])
    return weighted_edgelist

def analyze_similarity(df, stop_words, threshold):
    """Analyse la similarité des textes dans un DataFrame donné."""
    vectorizer = TfidfVectorizer(analyzer='word', stop_words=stop_words)
    
    for source in ['fandom', "reddit"]:
        df_temp = df[df['source'] == source]
        documents = df_temp['texte_lemma']
        documents = [remove_pron(i) for i in documents]

        print("PRON removed")
        
        doc_ids = list(range(len(documents)))
        tfidf_vectors = vectorizer.fit_transform(documents)
        tfidf_matrix = tfidf_vectors.toarray()
        tfidf_features = np.array(vectorizer.get_feature_names_out())

        cosar = cosine_similarity(tfidf_vectors, tfidf_vectors)
        for i in tqdm(range(len(cosar))):
            cosar[i, i] = 0

        print(f"\nAnalyzing with similarity threshold: {threshold}")
        e = ((cosar > threshold).sum()) / 2
        print(f"Keeping the threshold at {threshold}, there are {e} links in the resulting network.")

        adjmat = cosar.copy()
        adjmat[adjmat < threshold] = 0

        unconnected_nodes = sum(len(adjmat[i].nonzero()[0]) == 0 for i in range(len(adjmat)))
        connected_nodes = len(adjmat) - unconnected_nodes
        
        print(f"There are {connected_nodes} connected nodes and {unconnected_nodes} unconnected nodes.")

        adjmat = np.triu(adjmat, k=0)
        weighted_edgelist = adjacency_matrix_to_weighted_edgelist(adjmat)
        tfidf_graph = ig.Graph.TupleList(weighted_edgelist, directed=False, weights=True)

        gc = tfidf_graph.components().giant()
        G = gc.copy()
        communities = G.community_leiden(objective_function="modularity", weights=G.es['weight'])
        G.vs['community'] = communities.membership

        # Dictionnaire pour stocker les communautés et leur c-tfidf
        community_dict = {i: {'members': []} for i in range(max(G.vs['community']) + 1)}
        for v in G.vs:
            com = v['community']
            community_dict[com]['members'].append(v['name'])

        for i in range(len(community_dict)):
            community_dict[i]['c-tfidf-mat'] = np.mean(tfidf_matrix[community_dict[i]['members']], axis=0)

        # Liste des termes les plus importants pour chaque communauté
        comslist = []
        for com_idx in range(len(community_dict)):
            tfidf_subset_mean = community_dict[com_idx]['c-tfidf-mat']
            topterms_idxs = np.argsort(tfidf_subset_mean)[::-1][:10]
            topterms_words = [tfidf_features[i] for i in topterms_idxs]
            topterms_vals = [tfidf_subset_mean[i] for i in topterms_idxs]
            comslist.append(dict(zip(topterms_words, topterms_vals)))

        # Affichage des communautés
        cats = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        cats = cats * 100
        fig = plt.figure(figsize=(12, 18))

        for com_idx in range(min(14, len(comslist))):
            ncomlet = len(community_dict[com_idx]['members'])
            ax = fig.add_subplot(7, 2, com_idx + 1)
            ax.set_title(f"COM {com_idx + 1} ({ncomlet} letters)", loc='left', fontdict={'size': 11.5, 'weight': 'bold'})
            ax.barh(y=list(comslist[com_idx].keys())[::-1], width=list(comslist[com_idx].values())[::-1], color=cats[com_idx])
            plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        
        plt.show()

        # Association des textes aux communautés
        text_to_communities = {idx: [] for idx in range(len(df_temp))}
        for idx, doc_id in enumerate(doc_ids):
            similarities = cosar[idx]
            communities = [i for i, sim in enumerate(similarities) if sim > threshold]
            text_to_communities[idx] = communities

        for com_idx in range(len(community_dict)):
            df_temp[f'topic_{com_idx}'] = df_temp.index.map(lambda x: 1 if com_idx in text_to_communities.get(x, []) else 0)

        # Afficher le nombre de textes par communauté
        for com_idx in range(len(community_dict)):
            count = df_temp[f'topic_{com_idx}'].sum()
            print(f"Topic {com_idx}: {count} textes")

def main():
    """Fonction principale pour exécuter l'analyse de similarité."""
    df = pd.read_csv("to_process.csv")
    stop_words = load_stop_words('../sauvegarde_pkl/stop_words.pkl')
    
    while True:
        # Demander à l'utilisateur de saisir le seuil
        try:
            threshold = float(input("Veuillez entrer un seuil de similarité (par exemple, 0.13) : "))
            if 0 <= threshold <= 1:
                analyze_similarity(df, stop_words, threshold)
                
                # Demander confirmation pour continuer avec ce seuil
                confirm = input("Êtes-vous satisfait des résultats? (o/n) : ")
                if confirm.lower() == 'o':
                    print("Analyse terminée.")
                    break
            else:
                print("Veuillez entrer une valeur entre 0 et 1.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    main()