library(textreuse)
## text reuse
dir <- "/Users/rolly/Documents/10-19_Université_et_scolarité/17.Memoire/17.04_txt/reddit"
minhash <- minhash_generator(200, seed = 235)
ats <- TextReuseCorpus(dir = dir,
                       tokenizer = tokenize_ngrams, n = 5,
                       minhash_func = minhash)
buckets <- lsh(ats, bands = 50, progress = TRUE)
candidates <- lsh_candidates(buckets)
scores <- lsh_compare(candidates, ats, jaccard_similarity, progress = TRUE)
scores

### Test pour faire apparaître les alignements entre les textes sélectionnés

## On parcours le df et on isole les chemins
chemin_texte_1<- paste0(dir,"/",scores[7,1],'.txt')
chemin_texte_2<- paste0(dir,"/",scores[7,2],'.txt')

## On y accèse et on stock dans une variable
texte_1<-paste(readLines(chemin_texte_1), collapse=" ")
texte_2<-paste(readLines(chemin_texte_2), collapse=" ")

## On compare ! 
align_local(texte_1,texte_2)

