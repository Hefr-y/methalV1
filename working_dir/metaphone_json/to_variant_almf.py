#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   to_variant_almf.py
@Create on :   2022/06/24 12:15:51
@Revise on :   2022/06/24 12:15:51
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   Convertit les données ngrams dans un format qui peut être traité par l'opération d'alignement.

@Inputs    :   "5grams.csv" - Tous les 5grammes (trois mesures： Craig, Eder, Khi2)
               "4grams.csv" - Tous les 4grammes (trois mesures： Craig, Eder, Khi2)
               "freq_bas_4gram.csv" - fréquences de 4gram dans bas-rhin
               "freq_bas_5gram.csv" - fréquences de 5gram dans bas-rhin
               "freq_haut_4gram.csv" - fréquences de 4gram dans haut-rhin
               "freq_haut_5gram.csv" - fréquences de 5gram dans haut-rhin
@Output    :   "2 CSV fichiers de ngrams dans bas-rhin et haut-rhin pour l'opération d'alignement

@Usage     :   python to_variant_almf.py --help
@Exemple   :   python to_variant_almf.py [-h] zeta seuil
'''

# Requirements:

import argparse
import pandas as pd

def set_up_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('zeta', help= "type de zeta, option : Craig, Eder, Khi2")
    parser.add_argument('seuil', help="seuil de fréquence de ngrams")

    return parser

# Obtenir l'entrée de la ligne de commande
parser = set_up_argparser()
args = parser.parse_args()

mesure = args.zeta
frequence = int(args.seuil)
# nom de output file
outfile_bas = mesure + "_bas_" + args.seuil + ".csv"
outfile_haut = mesure + "_haut_" + args.seuil + ".csv"

# reading csv
df_5grams = pd.read_csv("Inputs/5grams.csv",index_col = False)
df_4grams = pd.read_csv("Inputs/4grams.csv",index_col = False)

# convert to dict ==> list[dict1,dict2...]
dict_5grams = df_5grams.to_dict(orient='records')
dict_4grams = df_4grams.to_dict(orient='records')


## freq list of ngrams
freq_bas_4gram = pd.read_csv("Inputs/freq_bas_4gram.csv")
freq_bas_5gram = pd.read_csv("Inputs/freq_bas_5gram.csv")
freq_haut_4gram = pd.read_csv("Inputs/freq_haut_4gram.csv")
freq_haut_5gram = pd.read_csv("Inputs/freq_haut_5gram.csv")
freq_bas_4gram = freq_bas_4gram.to_dict(orient='records')
freq_bas_5gram = freq_bas_5gram.to_dict(orient='records')
freq_haut_4gram = freq_haut_4gram.to_dict(orient='records')
freq_haut_5gram = freq_haut_5gram.to_dict(orient='records')

freq_bas_45gram = freq_bas_4gram + freq_bas_5gram
freq_haut_45gram = freq_haut_4gram + freq_haut_5gram


def dict_data_freq(freq_list):
    freq_dict = {}
    for i in freq_list:
        freq_dict[i['data']] = i['Freq']
    return freq_dict

dict_freq_bas_45gram = dict_data_freq(freq_bas_45gram)
dict_freq_haut_45gram = dict_data_freq(freq_haut_45gram)


# # traiter chaque type de zeta séparément
# mesure = "Craig"

dict_4grams = list(filter(lambda x: x['mesure'] == mesure, dict_4grams))
dict_5grams = list(filter(lambda x: x['mesure'] == mesure, dict_5grams))

#sum 4grams et 5grams
dict_45grams = dict_4grams + dict_5grams


# extract metaphone key
key_mp_4grams = []
for elem in dict_4grams:
    key_mp_4grams.append(elem['BasRhinClés'])
key_mp_5grams = []
for elem in dict_5grams:
    key_mp_5grams.append(elem['BasRhinClés'])

# metaphone key in common
key_mp_common = list(set(key_mp_4grams) & (set(key_mp_5grams)))

# Filtrer les éléments ayant la même clé MP
dict_45grams_filter = list(filter(lambda x: x['BasRhinClés'] in key_mp_common, dict_45grams))

# for i in dict_45grams_filter:
#     print(i)



# 合并4grams 和 5grams 的variants 到同一个key中
# Combiner les variantes de 4grammes et 5grammes dans la même clé dict
def get_list_ngram(dict_ngrams_filter):
    data = []
    for key in key_mp_common:
        var_list_bas = []
        var_list_haut = []
        row = {"MetaphoneKey":key, "VariantsBas":var_list_bas, "VariantsHaut":var_list_haut}
        for i in dict_ngrams_filter:
            if i['BasRhinClés'] == key:
                var_pre = i['BasRhinPreferredNgram'].split('; ')
                var_avo = i['BasRhinAvoidedNgram'].split('; ')
                # i['VarsAll'] = var_avo + var_pre
                i['VarsBas'] = var_pre
                i['VarsHaut'] = var_avo
                # print(len(i['Vars']))
                row['VariantsBas'].extend(i['VarsBas'])
                row['VariantsHaut'].extend(i['VarsHaut'])
        row['VariantsBas'] = list(set(row['VariantsBas']))
        row['VariantsHaut'] = list(set(row['VariantsHaut']))
        data.append(row)
    return data

data = get_list_ngram(dict_45grams_filter)


def trier_par_freq(data, frequence):
    for idx in range(len(data)):

        # print(data[idx]["VariantsBas"])
        # print("before",len(data[idx]["VariantsBas"]))
        # trier par freq
        data[idx]["VariantsBas"] = list(filter(lambda x: dict_freq_bas_45gram[x] >= frequence, data[idx]["VariantsBas"]))
        data[idx]["VariantsHaut"] = list(filter(lambda x: dict_freq_haut_45gram[x] >= frequence, data[idx]["VariantsHaut"]))

        # sans underscores
        data[idx]["VariantsBasMiddle"] = list(filter(lambda x: "_" not in x, data[idx]["VariantsBas"]))
        data[idx]["VariantsHautMiddle"] = list(filter(lambda x: "_" not in x, data[idx]["VariantsHaut"]))
        if len(data[idx]["VariantsBasMiddle"]) == 0 or len(data[idx]["VariantsHautMiddle"]) == 0:
            del data[idx]["VariantsBasMiddle"]
            del data[idx]["VariantsHautMiddle"]

        # underscores debut
        data[idx]["VariantsBasBegin"] = list(filter(lambda x: x[0] == "_" and x[-1] != "_", data[idx]["VariantsBas"]))
        data[idx]["VariantsHautBegin"] = list(filter(lambda x: x[0] == "_" and x[-1] != "_", data[idx]["VariantsHaut"]))
        # delete empty list
        if len(data[idx]["VariantsBasBegin"]) == 0 or len(data[idx]["VariantsHautBegin"]) == 0:
            del data[idx]["VariantsBasBegin"]
            del data[idx]["VariantsHautBegin"]

        # underscores fin
        data[idx]["VariantsBasFin"] = list(filter(lambda x: x[-1] == "_" and x[0] != "_", data[idx]["VariantsBas"]))
        data[idx]["VariantsHautFin"] = list(filter(lambda x: x[-1] == "_" and x[0] != "_", data[idx]["VariantsHaut"]))
        # delete empty list
        if len(data[idx]["VariantsBasFin"]) == 0 or len(data[idx]["VariantsHautFin"]) == 0:
            del data[idx]["VariantsBasFin"]
            del data[idx]["VariantsHautFin"]

        # print("after",len(data[idx]["VariantsBas"]))
        # print(data[idx],"\n")

    return data

data = trier_par_freq(data, frequence)
# for i in data:
#     print(i,"\n")


# create list with variants of bas-rhin and haut-rhin
lst_haut = []
lst_bas = []

for i in data:
    if 'VariantsBasMiddle' in i.keys() and 'VariantsHautMiddle' in i.keys() :
        lst_bas.append(i['VariantsBasMiddle'])
        lst_haut.append(i['VariantsHautMiddle'])

    if 'VariantsBasBegin' in i.keys() and 'VariantsHautBegin' in i.keys():
        lst_bas.append(i['VariantsBasBegin'])
        lst_haut.append(i['VariantsHautBegin'])

    if 'VariantsBasFin' in i.keys() and 'VariantsHautFin' in i.keys():
        lst_bas.append(i['VariantsBasFin'])
        lst_haut.append(i['VariantsHautFin'])



#  n-grams generated by stylo have spaces between characters,
#  the spaces between characters are removed here
for i in lst_bas:
    for j in range(len(i)):
        i[j] = i[j].replace(' ','')
        i[j] = i[j].replace("’","'")
        i[j] = i[j].replace("‘","'")


for i in lst_haut:
    for j in range(len(i)):
        i[j] = i[j].replace(' ','')
        i[j] = i[j].replace("’","'")
        i[j] = i[j].replace("‘","'")




df_bas = pd.DataFrame(lst_bas)
df_haut = pd.DataFrame(lst_haut)
df_bas.drop(index=0,inplace=True)
df_haut.drop(index=0,inplace=True)

# df_bas = df_bas[:10]
# df_haut = df_haut[:10]

print("variants de bas-rhin: \n", df_bas)
print("variants de haut-rhin: \n", df_haut)
# df_bas.to_csv('variants_trie/craig/craig_bas_variant_list.csv',index=False)
# df_haut.to_csv('variants_trie/craig/craig_haut_variant_list.csv',index=False)
df_bas.to_csv("Outputs/" + outfile_bas,index=False)
df_haut.to_csv("Outputs/" + outfile_haut,index=False)