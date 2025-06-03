
from tqdm import tqdm
import numpy as np
import string
#from nrclex import NRCLex
import pandas as pd
import textstat
import unicodedata
import re


def pretraitement(texte,mon_modele):

    """
    Args:
      texte: texte à lemmatiser
      mon_modele : modèle spacy à utiliser (rec: spacy.load('en_core_web_sm', disable=["ner", "textcat"])) 
    Returns:
    lemmatized texte + without Proper nouns
    """
    if len(texte) > 1000000:
        return np.nan
    doc = mon_modele(texte)
    lemmas = []

    for token in doc:
        if token.pos_ == 'PROPN' or token.pos_ == 'PUNCT':
            pass
        else:
            lemmas.append(token.lemma_)

    return ' '.join(lemmas)


def nettoyage_texte(text):
    # Supprimer la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Mettre en minuscules
    text = text.lower()
    return text


def emotion_processing(texte):
    """
    Prend le texte et lui applique un modèle NRCLex.
    
    Args:
        texte (str): Le texte à analyser.

    Returns:
        dict: Scores émotionnels bruts.
    """
    emotion = NRCLex(texte)
    return emotion.raw_emotion_scores  # On passe au score brut sans pondération pour éviter problème de corrélation

def emotion_processing_dataframe(df, texte_col='texte_lemma'):
    """
    Applique la fonction d'analyse des émotions à une colonne d'un DataFrame.

    Args:
        df (pd.DataFrame): Le DataFrame contenant la colonne de texte.
        texte_col (str): Le nom de la colonne contenant le texte.

    Returns:
        pd.DataFrame: Le DataFrame mis à jour avec les scores émotionnels.
    """
    # Appliquer le traitement des émotions à la colonne spécifiée
    df['emotions'] = df[texte_col].apply(emotion_processing)
    
    # Convertir les scores émotionnels en colonnes
    df = pd.concat([df.drop(['emotions'], axis=1), df['emotions'].apply(pd.Series)], axis=1)
    
    return df


def longueur_phrase(txt): 
    liste_phrase=txt.split('.')
    return np.mean([len(i.split(' ')) for i in liste_phrase])

def nombre_de_mots(txt) : 
    return len(txt.split(' '))

# readability_metrics.py


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


def readability_comput(text): 
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


def process_dataframe(df, text_col='Texte'):
    """
    Applique les calculs de lisibilité à une colonne d'un DataFrame.

    Args:
        df (pd.DataFrame): Le DataFrame contenant la colonne de texte.
        text_col (str): Le nom de la colonne contenant le texte.

    Returns:
        pd.DataFrame: Le DataFrame mis à jour avec les métriques de lisibilité.
    """
    tqdm.pandas()  # Initialise tqdm pour l'affichage des progrès
    df['Readability Metrics'] = df[text_col].progress_apply(readability_comput)
    
    # Convertir les résultats des métriques de lisibilité en colonnes
    df = pd.concat([df.drop(['Readability Metrics'], axis=1), df['Readability Metrics'].apply(pd.Series)], axis=1)
    
    return df




def remove_non_latin(text):
    # Définir un motif pour détecter les caractères latins
    latin_pattern = r'[\u0000-\u007F\u0100-\u024F]'

    # Garder uniquement les caractères correspondant au motif
    cleaned_text = ''.join(char for char in text if re.match(latin_pattern, char))

    return cleaned_text

def remove_punctuation(text):
    # Utiliser une classe Unicode pour identifier la ponctuation
    cleaned_text = ''.join(char for char in text if not unicodedata.category(char).startswith('P'))

    return cleaned_text
