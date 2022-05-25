#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   test.py
@Create on :   2022/05/25 14:19:03
@Revise on :   2022/05/25 14:19:03
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements:

import pandas as pd
import json
from pandas import json_normalize


# # data path
# # n-gram
# ## khi2
# json_path_preferred_chi2 = "./bas_chi2_3grams_preferred.json"
# json_path_avoided_chi2 = "./bas_chi2_3grams_avoided.json"
# ## eder
# json_path_preferred_eder = "./bas_eder_3grams_preferred.json"
# json_path_avoided_eder = "./bas_eder_3grams_avoided.json"
# ## craig
# json_path_preferred_craig = "./bas_craig_3grams_preferred.json"
# json_path_avoided_craig = "./bas_craig_3grams_avoided.json"
# # read file data
# ## khi2
# with open(json_path_preferred_chi2,'r',encoding='utf8') as f:
#     json_data_preferred_chi2 = json.load(f)
# with open(json_path_avoided_chi2,'r',encoding='utf8') as f:
#     json_data_avoided_chi2 = json.load(f)
# ## eder
# with open(json_path_preferred_eder,'r',encoding='utf8') as f:
#     json_data_preferred_eder = json.load(f)
# with open(json_path_avoided_eder,'r',encoding='utf8') as f:
#     json_data_avoided_eder = json.load(f)
# ## craig
# with open(json_path_preferred_craig,'r',encoding='utf8') as f:
#     json_data_preferred_craig = json.load(f)
# with open(json_path_avoided_craig,'r',encoding='utf8') as f:
#     json_data_avoided_craig = json.load(f)




# token
## khi2
token_json_path_preferred_chi2 = "./mp_stylo_token/bas_chi2_words_preferred.json"
token_json_path_avoided_chi2 = "./mp_stylo_token/bas_chi2_words_avoided.json"
## eder
token_json_path_preferred_eder = "./mp_stylo_token/bas_eder_words_preferred.json"
token_json_path_avoided_eder = "./mp_stylo_token/bas_eder_words_avoided.json"
## craig
token_json_path_preferred_craig = "./mp_stylo_token/bas_craig_words_preferred.json"
token_json_path_avoided_craig = "./mp_stylo_token/bas_craig_words_avoided.json"

# read file data
## khi2
with open(token_json_path_preferred_chi2,'r',encoding='utf8') as f:
    json_data_preferred_chi2 = json.load(f)
with open(token_json_path_avoided_chi2,'r',encoding='utf8') as f:
    json_data_avoided_chi2 = json.load(f)
## eder
with open(token_json_path_preferred_eder,'r',encoding='utf8') as f:
    json_data_preferred_eder = json.load(f)
with open(token_json_path_avoided_eder,'r',encoding='utf8') as f:
    json_data_avoided_eder = json.load(f)
## craig
with open(token_json_path_preferred_craig,'r',encoding='utf8') as f:
    json_data_preferred_craig = json.load(f)
with open(token_json_path_avoided_craig,'r',encoding='utf8') as f:
    json_data_avoided_craig = json.load(f)




# Find keys in common
## khi2
keys_common_chi2 = json_data_preferred_chi2.keys() & json_data_avoided_chi2.keys()
## Eder
keys_common_eder = json_data_preferred_eder.keys() & json_data_avoided_eder.keys()
## Craig
keys_common_craig = json_data_preferred_craig.keys() & json_data_avoided_craig.keys()

# print(keys_common_chi2)


def mp_ngram(mesure, keys_common, data_preferred, data_avoided):
    data = []
    for key_mp in keys_common:
        l_pre = [key for item in data_preferred[key_mp] for key in item]
        l_avo = [key for item in data_avoided[key_mp] for key in item]
        l_pre = '; '.join(str(i) for i in l_pre)
        l_avo = '; '.join(str(i) for i in l_avo)
        row = { "mesure": mesure, "BasRhinClés": key_mp ,"BasRhinPreferredNgram":l_pre,"BasRhinAvoidedNgram":l_avo}
        data.append(row)
    return data

# craig_data = mp_ngram("Craig", keys_common_craig, json_data_preferred_craig, json_data_avoided_craig)
# eder_data = mp_ngram("Eder", keys_common_eder, json_data_preferred_eder, json_data_avoided_eder)
# chi2_data = mp_ngram("Khi2", keys_common_chi2, json_data_preferred_chi2, json_data_avoided_chi2)


def mp_words(mesure, keys_common, data_preferred, data_avoided):
    data = []
    for key_mp in keys_common:
        l_pre = '; '.join(str(i) for i in data_preferred[key_mp])
        l_avo = '; '.join(str(i) for i in data_avoided[key_mp])
        row = { "mesure": mesure, "BasRhinClés": key_mp ,"BasRhinPreferredNgram":l_pre,"BasRhinAvoidedNgram":l_avo}
        data.append(row)
    return data

craig_data = mp_words("Craig", keys_common_craig, json_data_preferred_craig, json_data_avoided_craig)
eder_data = mp_words("Eder", keys_common_eder, json_data_preferred_eder, json_data_avoided_eder)
chi2_data = mp_words("Khi2", keys_common_chi2, json_data_preferred_chi2, json_data_avoided_chi2)




data = craig_data + eder_data + chi2_data
info = json.loads(json.dumps(data))
df = json_normalize(info)
# print(df)

df.to_csv("words.csv",index = False)

read_csv = pd.read_csv("words.csv")
print(read_csv)