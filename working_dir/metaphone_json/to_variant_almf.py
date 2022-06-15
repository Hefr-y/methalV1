import pandas as pd
from requests import head

# reading csv
df_5grams = pd.read_csv("5grams.csv",index_col = False)
df_4grams = pd.read_csv("4grams.csv",index_col = False)

# convert to dict ==> list[dict1,dict2...]
dict_5grams = df_5grams.to_dict(orient='records')
dict_4grams = df_4grams.to_dict(orient='records')


## freq list of ngrams
freq_bas_4gram = pd.read_csv("freq_bas_4gram.csv")
freq_bas_5gram = pd.read_csv("freq_bas_5gram.csv")
freq_haut_4gram = pd.read_csv("freq_haut_4gram.csv")
freq_haut_5gram = pd.read_csv("freq_haut_5gram.csv")
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


# traiter chaque type de zeta séparément
mesure = "Eder"

dict_4grams = list(filter(lambda x: x['mesure'] == mesure, dict_4grams))
dict_5grams = list(filter(lambda x: x['mesure'] == mesure, dict_5grams))

#单纯的相加 4grams和5grams
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

# 筛选出具有相同mp key的元素
dict_45grams_filter = list(filter(lambda x: x['BasRhinClés'] in key_mp_common, dict_45grams))

# for i in dict_45grams_filter:
#     print(i)



# 合并4grams 和 5grams 的variants 到同一个key中
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

        data[idx]["VariantsBas"] = list(filter(lambda x: "_" not in x and dict_freq_bas_45gram[x] >= frequence, data[idx]["VariantsBas"]))
        data[idx]["VariantsHaut"] = list(filter(lambda x: "_" not in x and dict_freq_haut_45gram[x] >= frequence, data[idx]["VariantsHaut"]))


        # print("after",len(data[idx]["VariantsBas"]))
        # print(data[idx],"\n")

    # delete empty list
    data_trie = list(filter(lambda x: len(x["VariantsHaut"]) != 0 and len(x["VariantsBas"]) != 0, data))

    # for i in data_trie:
        # print(i,"\n")

    return data_trie

data = trier_par_freq(data, 30)


# create list with variants of bas-rhin and haut-rhin
lst_haut = []
lst_bas = []
for i in data:
    lst_bas.append(i['VariantsBas'])
    lst_haut.append(i['VariantsHaut'])



# trier apres extract variants
# #  n-grams generated by stylo have spaces between characters,
# #  the spaces between characters are removed here
# for i in range(len(lst_bas)):
#     # trier par fréquence

#     ## print(lst_bas[i])
#     ## print("before trier: ", len(lst_bas[i]))
#     lst_bas[i] = list(filter(lambda x: dict_freq_bas_45gram[x] >= 30, lst_bas[i]))

#     ## print(lst_bas[i])
#     ## print("after trier: ", len(lst_bas[i]),"\n")

#     for j in range(len(lst_bas[i])):
#         lst_bas[i][j] = lst_bas[i][j].replace(' ','')


# for i in range(len(lst_haut)):
#     # trier par fréquence
#     lst_haut[i] = list(filter(lambda x: dict_freq_haut_45gram[x] >= 30, lst_haut[i]))

#     for j in range(len(lst_haut[i])):
#         lst_haut[i][j] = lst_haut[i][j].replace(' ','')




#  n-grams generated by stylo have spaces between characters,
#  the spaces between characters are removed here
for i in lst_bas:
    for j in range(len(i)):
        i[j] = i[j].replace(' ','')


for i in lst_haut:
    for j in range(len(i)):
        i[j] = i[j].replace(' ','')




df_bas = pd.DataFrame(lst_bas)
df_haut = pd.DataFrame(lst_haut)
df_bas.drop(index=0,inplace=True)
df_haut.drop(index=0,inplace=True)

df_bas = df_bas[:10]
df_haut = df_haut[:10]

print("variants de bas-rhin: \n", df_bas)
print("variants de haut-rhin: \n", df_haut)
df_bas.to_csv('eder_bas_variant_list.csv',index=False)
df_haut.to_csv('eder_haut_variant_list.csv',index=False)
