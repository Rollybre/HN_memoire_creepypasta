# Installer les packages si vous ne les avez pas déjà installés
install.packages("proxy")
install.packages("reshape2")
install.packages("ggplot2")

# Charger les packages nécessaires
library(proxy)
library(reshape2)
library(ggplot2)

# Supposons que votre DataFrame s'appelle df et qu'il contienne une colonne nommée "text_lemmatized" avec les listes de mots lemmatisés

# Créer une fonction pour calculer la distance de Jaccard entre deux listes de mots
jaccard_distance <- function(list1, list2) {
  intersection <- length(intersect(list1, list2))
  union <- length(union(list1, list2))
  return(1 - intersection / union)  # Retourner 0 si les deux ensembles sont vides
}

# Créer une matrice de distances de Jaccard
num_texts <- nrow(df)
distances <- matrix(0, nrow=num_texts, ncol=num_texts)

for (i in 1:num_texts) {
  for (j in (i+1):num_texts) {
    distance <- jaccard_distance(df$text_lemmatized[[i]], df$text_lemmatized[[j]])
    distances[i, j] <- distance
    distances[j, i] <- distance
  }
}

# Convertir la matrice de distances en format long pour le traçage
distances_long <- melt(distances)

# Traçage de la distribution des distances de Jaccard
ggplot(data=distances_long, aes(x=value)) +
  geom_histogram(bins=20, fill="blue", color="black", alpha=0.7) +
  labs(title="Distribution des distances de Jaccard entre les textes",
       x="Distance de Jaccard",
       y="Nombre de paires de textes") +
  theme_minimal()
