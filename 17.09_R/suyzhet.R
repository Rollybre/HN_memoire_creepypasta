library(syuzhet)

# Fonction pour diviser un texte en parties
split_text_into_n_parts <- function(text, n) {
  total_length <- nchar(text)
  part_length <- total_length %/% n
  extra_chars <- total_length %% n
  parts <- vector("character", n)
  start_index <- 1
  
  for (i in 1:n) {
    current_part_length <- part_length + ifelse(i <= extra_chars, 1, 0)
    parts[i] <- substr(text, start_index, start_index + current_part_length - 1)
    start_index <- start_index + current_part_length
  }
  
  return(parts)
}

# Fonction pour analyser le sentiment d'un texte

analyze_sentiment <- function(text) {
  chunked <- split_text_into_n_parts(text, 100)
  sentiments <- get_sentiment(chunked, method="bing")
  sentiments_tr <-get_dct_transform(sentiments)
  return(sentiments_tr)
}


# Chemin vers le dossier contenant les fichiers texte
dossier <- "/Users/rolly/Documents/10-19_Université_et_scolarité/17_Memoire/17.04_txt/corpus"

# Liste des fichiers texte dans le dossier
fichiers <- list.files(dossier, pattern = "\\.txt$", full.names = TRUE)

# Initialisation d'une liste pour stocker les résultats de sentiment pour chaque fichier
resultats_sentiment <- list()

# Analyse du sentiment pour chaque fichier
library(progress)

pb <- progress_bar$new(format = "[:bar] :percent :eta", total = length(fichiers))

# Boucle sur chaque fichier
for (fichier in fichiers) {
  texte <- readLines(fichier)
  texte <- paste(texte, collapse=' ')
  
  # Analyse du sentiment
  resultats_sentiment[[fichier]] <- analyze_sentiment(texte)
  
  # Mettre à jour la barre de progression
  pb$tick()
}

# Finaliser la barre de progression
pb$close()

# Normalisation des valeurs de sentiment
max_sentiment <- max(unlist(lapply(resultats_sentiment, max)))
min_sentiment <- min(unlist(lapply(resultats_sentiment, min)))



resultats_sentiment_tr<-list()

for (i in 1:length(resultats_sentiment)) {
  tr_sentiment <- get_dct_transform(resultats_sentiment[[i]])
  tr_sentiment <- scale(tr_sentiment, center = min_sentiment, scale = max_sentiment - min_sentiment)
  resultats_sentiment_tr[[i]] <- tr_sentiment
  x <- 1:length(tr_sentiment)

}


# Calcul des distances euclidiennes entre chaque paire de vecteurs
distances <- dist(do.call(rbind, resultats_sentiment))

# Convertir les distances en une matrice carrée
dist_matrix <- as.matrix(distances)

# Tracez un histogramme des distances ou un graphique de densité
plot(density(distances))

vecteur_moyen <- numeric(length(resultats_sentiment_tr[[1]]))

# Calculer la somme des vecteurs
for (v in resultats_sentiment_tr) {
  vecteur_moyen <- vecteur_moyen + v
}

# Diviser par le nombre total de vecteurs
vecteur_moyen <- vecteur_moyen / length(resultats_sentiment_tr)

print("Vecteur moyen :", vecteur_moyen)
