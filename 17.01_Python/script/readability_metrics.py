# readability_metrics.py

import pandas as pd
import textstat
from tqdm import tqdm

def calculate_lix(text):
    """
    Calcule l'indice Lix d'un texte.

    Args:
        text (str): Le texte à analyser.

    Returns:
        float: Indice Lix calculé.
    """
    words = text.split()
    num_words = len(words)
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    long_words = [word for word in words if len(word) > 6]
    num_long_words = len(long_words)

    # Éviter la division par zéro
    if num_sentences == 0:
        return 0

    return num_words / num_sentences + (num_long_words * 100) / num_words


def readability_compute(text): 
    """
    Calcule plusieurs métriques de lisibilité pour un texte.

    Args:
        text (str): Le texte à analyser.

    Returns:
        dict: Dictionnaire des métriques de lisibilité.
    """
    readability_results = {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "Gunning Fog Index": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
        "Coleman-Liau Index": textstat.coleman_liau_index(text),
        "Dale-Chall Readability Score": textstat.dale_chall_readability_score(text),
        "Indice Lix": calculate_lix(text)
    }
    return readability_results


def process_dataframe(df:pd.DataFrame, text_col:str='Texte'):
    """
    Applique les calculs de lisibilité à une colonne d'un DataFrame.

    Args:
        df (pd.DataFrame): Le DataFrame contenant la colonne de texte.
        text_col (str): Le nom de la colonne contenant le texte.

    Returns:
        pd.DataFrame: Le DataFrame mis à jour avec les métriques de lisibilité.
    """
    tqdm.pandas()  # Initialise tqdm pour l'affichage des progrès
    df['Readability Metrics'] = df[text_col].progress_apply(readability_compute)
    
    # Convertir les résultats des métriques de lisibilité en colonnes
    df = pd.concat([df.drop(['Readability Metrics'], axis=1), df['Readability Metrics'].apply(pd.Series)], axis=1)
    
    return df

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de DataFrame
    data = {'Texte': ["Ceci est un exemple de texte.", "Le texte est court."]}
    df = pd.DataFrame(data)
    
    # Traitement du DataFrame
    df = process_dataframe(df)
    print(df)