#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   token_count.py
@Create on :   2022/04/12 10:53:30
@Revise on :   2022/04/12 10:53:30
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   calcul du nombre de tokens
'''

# Requirements: pathlib, pandas

from collections import Counter
from pathlib import Path
import pandas as pd

wd = Path('../../working_dir')
rwd = Path('../../Rstylo')
# tokpath = wd / "tokens/all"
tokpath = wd / "tokens/bas-rhin"
metapath = wd / "metadata/temp/metadata_avec_period.csv"
outpath = wd / "metadata/metadata.csv"
punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»'

df_meta = pd.read_csv(metapath, index_col=0)
df_meta['Tokens'] = 1
df_meta['TokensNoPunctuation'] = 1

def all_txts(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

def is_punc(word):
    if word in punc:
        return False
    else:
        return True

def count_tok(p):
    with p.open('r') as f:
        data = f.readlines()
        df_meta.loc[p.stem[:-4], 'Tokens'] = len(data)
        data_sans_punc = []
        for line in data:
            if is_punc(line.strip('\n')):
                data_sans_punc.append(line)
        df_meta.loc[p.stem[:-4], 'TokensNoPunctuation'] = len(data_sans_punc)





def main():
    # num of token of each piece
    # txts = all_txts(tokpath)
    # for i in txts:
    #     count_tok(i)

    # print("Total : ", len(txts))
    # print(df_meta)
    # df_meta.to_csv(outpath)

    # frequency
    txts = all_txts(tokpath)
    alltokens = []

    for i in txts:
        # print(i)
        with i.open('r') as f:
            data = f.readlines()
            alltokens.extend(data)

    # delete "\n"
    alltokens = [x.lower() for x in alltokens if isinstance(x,str)]
    alltokens = list(map(str.strip,alltokens))

    tokfrequency = Counter(alltokens)
    # print(tokfrequency)

    r_bas_zeta_words = rwd / "output_oppose()/par_token/region/bas_chi2_zeta/words_preferred.txt"
    test_out = rwd / "output_oppose()/par_token/region/bas_chi2_zeta/words_preferred_frequency.txt"

    wordspre_frequency = {}
    with r_bas_zeta_words.open('r') as f:
        for i in range(7):
            next(f)
        words = f.readlines()
        words = list(map(str.strip,words))
    for word in words:
        wordspre_frequency[word] = tokfrequency[word]



    file_write_obj = open(test_out, 'w')
    for var in wordspre_frequency.items():
        file_write_obj.write(str(var)+"\n")

    # file_write_obj.close()
    # print(tokfrequency)

if __name__ == '__main__':
    main()