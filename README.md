## script

### text_extract

- #### TEI -> dataframe initial

  - **tei_reader.py** : Créer la classe (object) intégrant les données extraites des fichiers TEI
  - **tei_to_dataframe.py**, **tei2_to_dataframe.py** :  traitement initial
    - Parsing TEI XML fichiers avec pandas.DataFrame, où les métadonnées sont extraites de ses tags de fichier XML, certaines données seront donc manquantes
    - **tei2** est différent des autres corpus, il est donc traité séparément ici
    - **tei_to_dataframe.py** pour corpus tei + tei-lustig, **tei2_to_dataframe.py** pour corpus tei2
    - Colonnes contenues dans le dataframe provisoire :  'IdMtl', 'FileName', 'Title', 'Author', 'Publisher', 'PubPlace', 'dateWritten', 'datePrint', 'Front', 'Body', 'textBrut'

- #### Compléter les métadonnées et extraire le texte brut

  - **extract_complete_tei.py**, **extract_complete_tei2.py** :  C'est à partir de ce [classeur](https://docs.google.com/spreadsheets/d/1_xUK1uP209UCjJ9agqr_Zik65u08A8rOAVo53PTtj8Y/edit#gid=731925022) google docs ou [autres/md ](https://gitlab.huma-num.fr/methal/corpus-methal-all/-/tree/main/autres/md)que les métadonnées sont complétées. De plus, un fichier (.txt) **texte brut** de chaque pièce est extrait et stocké dans [working_dir/text_brut](https://gitlab.huma-num.fr/methal/corpus-methal-all/-/tree/main/code/working_dir/text_brut)
    - **extract_complete_tei.py** pour corpus tei + tei-lustig, **extract_complete_tei2.py** pour corpus tei2
    - Colonnes contenues dans le dataframe provisoire :  'FileName', 'Author', 'authorPlaceOfBirth',  'PubPlace', 'PubDept', 'datePrint'

### token

- #### Tokenize et calcul du nombre de tokens

  - **alsatian_tokeniser_multi.py** :  alsatian tokeniser de @dbernhard
  - **token_count.py** :  calcul du nombre de tokens

**Combine_CSVs.py** :  combiner les fichiers csv

### metaphone

- #### Générer la clé métaphone pour chaque mot des fichiers .tok

  - **metaphone_als.py** :  Based on metaphone.py
  - **txtTok2csv.py** :  Générer un fichier csv, à partir de forme, clé métaphone 1, clé métaphone 2

## working_dir

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

### metaphone

- **bas-rhin** :  résultats de metaphone à partir des tokens de chaque pièce (bas-rhin)
- **haut-rhin** :  résultats de metaphone à partir des tokens de chaque pièce (haut-rhin)
- **combined_csv_bas.csv** :  résultats métaphone combinés de bas-rhin
- **combined_csv_haut.csv** :  résultats métaphone combinés de haut-rhin