## script

### text_extract

TEI -> dataframe initial

- **tei_reader.py** : Créer la classe (object) intégrant les données extraites des fichiers TEI
- **tei_to_dataframe.py**, **tei2_to_dataframe.py** :  traitement initial
  - Parsing TEI XML fichiers avec pandas.DataFrame, où les métadonnées sont extraites de ses tags de fichier XML, certaines données seront donc manquantes
  - **tei2** est différent des autres corpus, il est donc traité séparément ici
  - **tei_to_dataframe.py** pour corpus tei + tei-lustig, **tei2_to_dataframe.py** pour corpus tei2
  - Colonnes contenues dans le dataframe provisoire :  'IdMtl', 'FileName', 'Title', 'Author', 'Publisher', 'PubPlace', 'dateWritten', 'datePrint', 'Front', 'Body', 'textBrut'

Compléter les métadonnées et extraire le texte brut

- **extract_complete_tei.py**, **extract_complete_tei2.py** :  C'est à partir de ce [classeur](https://docs.google.com/spreadsheets/d/1_xUK1uP209UCjJ9agqr_Zik65u08A8rOAVo53PTtj8Y/edit#gid=731925022) google docs ou [autres/md ](https://gitlab.huma-num.fr/methal/corpus-methal-all/-/tree/main/autres/md)que les métadonnées sont complétées. De plus, un fichier (.txt) **texte brut** de chaque pièce est extrait et stocké dans [working_dir/text_brut](https://gitlab.huma-num.fr/methal/corpus-methal-all/-/tree/main/code/working_dir/text_brut)
  - **extract_complete_tei.py** pour corpus tei + tei-lustig, **extract_complete_tei2.py** pour corpus tei2
  - Colonnes contenues dans le dataframe provisoire :  'FileName', 'Author', 'authorPlaceOfBirth',  'PubPlace', 'PubDept', 'datePrint'

### token

Tokenize et calcul du nombre de tokens

- **alsatian_tokeniser_multi.py** :  alsatian tokeniser de @dbernhard
- **token_count.py** :  calcul du nombre de tokens

### metaphone

Générer la clé métaphone pour chaque mot des fichiers .tok

- **metaphone_als.py** :  Based on metaphone.py

- **match_mp.py** :  Faites correspondre des mots avec au moins une clé métaphone identique
  - Complexité en temps ：O(n^2)
  - Entrée ：*working_dir/tokens/all*
  - Sortie ：*working_dir/metaphone_json/nlettres.json*

- **match_mp_revdict.py** : Même fonction que ci-dessus mais inverser les valeurs des clés du dictionnaire. C'est plus rapide, mais étant donné qu'il y a trois cas de correspondance métaphone, il ne peux faire que la correspondance forte ( key1 == key1) et la correspondance minimale ( key2 == key2)
  - Complexité en temps ：O(n)
  - Entrée ：*working_dir/tokens/all*
  - Sortie ：Pas sûr qu'il soit utile par la suite, car les résultats sont incomplets

- **forme_zeta.py** :  Faire diagramme à barres basé sur les différents scores(zeta) de forme
  - Entrée ：*working_dir/metaphone_json/6lettres.json* et *mesures discriminativite par pydistinto*
  - Sortie ：*working_dir/plot/metaphone_forme_zeta/.svg*

**Combine_CSVs.py** :  combiner les fichiers csv

## working_dir

### mesures_discriminativite

Documents originalement sur Seafile, transférés ici

- **output_quanteda_sans_TEI2** : keyness (khi2) et autres mesures (pas nécessairement de "discriminativité", il y a aussi des distributions de fréquences et un dendrogramme par pièce
- **pydistinto** : Dépôt pydistinto cloné avec modifs @hyang1, y compris des diagrammes discriminativité et dataframe dont les résultats sont visualisés

### metadata

- **temp** :  Fichiers de métadonnées provisoires générés par le script
- **metadata.csv** :  Métadonnées complètes actuelles, colonnes =>  'FileName', 'Author', 'authorPlaceOfBirth',  'PubPlace', 'PubDept', 'datePrint', 'period', 'Tokens', 'TokensNoPunctuation'

### text_brut

- **bas-rhin** :  Texte brut de chaque pièce (bas-rhin)
- **haut-rhin** :  Texte brut de chaque pièce (haut-rhin)

### tokens

- **all** :  Tokens de chaque pièce à partir du texte brut (bas-rhin et haut-rhin)
- **bas-rhin** :  Tokens de chaque pièce à partir du texte brut (bas-rhin)
- **haut-rhin** :  Tokens de chaque pièce à partir du texte brut (haut-rhin)

### metaphone_json

 La structure initiale, sans contexte

- **6lettres.json** : Toutes les correspondances des clés métaphone pour les mots d'une longueur supérieure ou égale à 6 lettres
- **16lettres.json** : Toutes les correspondances des clés métaphone pour les mots d'une longueur supérieure ou égale à 16 lettres.

### plot

**metadata_ratio_plots** : Diagrammes de distribution des pièces et tokens par période, auteur·e et région
**metadata_ratio_plots** : Diagrammes basé sur les différents scores(zeta) de forme avec une même clé métaphone
