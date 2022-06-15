setwd("~/methal/methalV1/Rstylo/data4r/regions")
library(stylo)
library(rlist)

# Preprocessing

# = = = = = = = = = = = = = =
#       load corpus         =
# = = = = = = = = = = = = = =
primary.raw.corpus.bas <- load.corpus(files = "all", corpus.dir = "bas_underscore", encoding = "UTF-8")
secondary.raw.corpus.haut <- load.corpus(files = "all", corpus.dir = "haut_underscore", encoding = "UTF-8")


# = = = = = = = = = = = = = =
#         tokenizer         =
# = = = = = = = = = = = = = =
primary.tokenized.corpus.bas <- txt.to.words(primary.raw.corpus.bas, splitting.rule="[[:space:]]+", preserve.case = FALSE)
secondary.tokenized.corpus.haut <- txt.to.words(secondary.raw.corpus.haut, splitting.rule="[[:space:]]+", preserve.case = FALSE)

# = = = = = = = = = = = = = =
#     token analysis        =
# = = = = = = = = = = = = = =
bas.zeta = oppose(primary.corpus = primary.tokenized.corpus.bas, secondary.corpus = secondary.tokenized.corpus.haut, 
                  text.slice.length = 545, path = "./chi2_zeta")

rm(primary.raw.corpus.bas, secondary.raw.corpus.haut)


# = = = = = = = = = = = = = =
#          n-grams          =
# = = = = = = = = = = = = = =

## 2-grams(characters)
primary.2gram.corpus = txt.to.features(primary.tokenized.corpus.bas, features = "c", ngram.size = 2)
secondary.2gram.corpus = txt.to.features(secondary.tokenized.corpus.haut, features = "c", ngram.size = 2)

## 3-grams(characters)
primary.3gram.corpus = txt.to.features(primary.tokenized.corpus.bas, features = "c", ngram.size = 3)
secondary.3gram.corpus = txt.to.features(secondary.tokenized.corpus.haut, features = "c", ngram.size = 3)

## 4-grams(characters)
primary.4gram.corpus = txt.to.features(primary.tokenized.corpus.bas, features = "c", ngram.size = 4)
secondary.4gram.corpus = txt.to.features(secondary.tokenized.corpus.haut, features = "c", ngram.size = 4)

## 5-grams(characters)
primary.5gram.corpus = txt.to.features(primary.tokenized.corpus.bas, features = "c", ngram.size = 5)
secondary.5gram.corpus = txt.to.features(secondary.tokenized.corpus.haut, features = "c", ngram.size = 5)

rm(primary.tokenized.corpus.bas, secondary.tokenized.corpus.haut)

# = = = = = = = = = = = = = =
#       filtering ngrams    =
# = = = = = = = = = = = = = =
regexpattern = "^(?!.*[ ](?=[ ]))\\S.*?\\S$"

## 2-grams(characters)
primary.2gram.corpus = list.search(primary.2gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])
secondary.2gram.corpus = list.search(secondary.2gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])

## 3-grams(characters)
primary.3gram.corpus = list.search(primary.3gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])
secondary.3gram.corpus = list.search(secondary.3gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])

## 4-grams(characters)
primary.4gram.corpus = list.search(primary.4gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])
secondary.4gram.corpus = list.search(secondary.4gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])

## 5-grams(characters)
primary.5gram.corpus = list.search(primary.5gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])
secondary.5gram.corpus = list.search(secondary.5gram.corpus, .[grepl(regexpattern, ., perl = TRUE)])


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#    generating a frequency list of (linguistic) features =
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

freq.bas.5gram = make.frequency.list(primary.5gram.corpus,value=TRUE,relative = FALSE)
freq.haut.5gram = make.frequency.list(secondary.5gram.corpus,value=TRUE,relative = FALSE)
# write to file
write.csv(freq.bas.5gram,"freq_bas_5gram.csv",row.names = FALSE)
write.csv(freq.haut.5gram,"freq_haut_5gram.csv",row.names = FALSE)



freq.bas.4gram = make.frequency.list(primary.4gram.corpus,value=TRUE,relative = FALSE)
freq.haut.4gram = make.frequency.list(secondary.4gram.corpus,value=TRUE,relative = FALSE)
# write to file
write.csv(freq.bas.4gram,"freq_bas_4gram.csv",row.names = FALSE)
write.csv(freq.haut.4gram,"freq_haut_4gram.csv",row.names = FALSE)



freq.bas.3gram = make.frequency.list(primary.3gram.corpus,value=TRUE,relative = FALSE)
freq.haut.3gram = make.frequency.list(secondary.3gram.corpus,value=TRUE,relative = FALSE)
# write to file
write.csv(freq.bas.3gram,"freq_bas_3gram.csv",row.names = FALSE)
write.csv(freq.haut.3gram,"freq_haut_3gram.csv",row.names = FALSE)



freq.bas.2gram = make.frequency.list(primary.2gram.corpus,value=TRUE,relative = FALSE)
freq.haut.2gram = make.frequency.list(secondary.2gram.corpus,value=TRUE,relative = FALSE)
# write to file
write.csv(freq.bas.2gram,"freq_bas_2gram.csv",row.names = FALSE)
write.csv(freq.haut.2gram,"freq_haut_2gram.csv",row.names = FALSE)




# = = = = = = = = = = = = = =
#    contrastive analysis   =
# = = = = = = = = = = = = = =
# Nécessite une modification manuelle de la méthode et path

## 2-grams
region.2gram.zeta = oppose(primary.corpus = primary.2gram.corpus, secondary.corpus = secondary.2gram.corpus, 
                           text.slice.length = 2333, path = "./Bas-Rhin_2grams/chi2_zeta", gui = FALSE, write.png.file = TRUE,
                           rare.occurrences.threshold = 0, zeta.filter.threshold = 0, oppose.method = "chisquare.zeta")
setwd("~/methal/methalV1/Rstylo/data4r/regions")
rm(region.2gram.zeta)

## 3-grams
region.3gram.zeta = oppose(primary.corpus = primary.3gram.corpus, secondary.corpus = secondary.3gram.corpus,
                           text.slice.length = 1788, path = "./Bas-Rhin_3grams/craig_zeta", gui = FALSE, write.png.file = TRUE,
                           rare.occurrences.threshold = 0, zeta.filter.threshold = 0, oppose.method = "craig.zeta")
setwd("~/methal/methalV1/Rstylo/data4r/regions")
rm(region.3gram.zeta)

## 4-grams
region.4gram.zeta = oppose(primary.corpus = primary.4gram.corpus, secondary.corpus = secondary.4gram.corpus,
                           text.slice.length = 1243, path = "./Bas-Rhin_4grams/craig_zeta", gui = FALSE, write.png.file = TRUE,
                           rare.occurrences.threshold = 0, zeta.filter.threshold = 0, oppose.method = "craig.zeta")
setwd("~/methal/methalV1/Rstylo/data4r/regions")
rm(region.4gram.zeta)

## 5-grams
region.5gram.zeta = oppose(primary.corpus = primary.5gram.corpus, secondary.corpus = secondary.5gram.corpus, 
                           text.slice.length = 819, path = "./Bas-Rhin_5grams/craig_zeta", gui = FALSE, write.png.file = TRUE,
                           rare.occurrences.threshold = 0, zeta.filter.threshold = 0, oppose.method = "craig.zeta")
setwd("~/methal/methalV1/Rstylo/data4r/regions")
rm(region.5gram.zeta)


