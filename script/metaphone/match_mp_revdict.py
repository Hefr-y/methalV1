#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   match_mp_revdict.py
@Create on :   2022/04/11 09:43:43
@Revise on :   2022/04/23 11:00:12
@Author    :   Heng Yang
@Version   :   1.1
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements: multiprocessing, pathlib, pandas, metaphone_als

from collections import defaultdict
from multiprocessing.pool import Pool
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")
from metaphone_als import dm


DIR_IN_BAS = Path('../../working_dir/tokens/bas-rhin')
DIR_IN_HAUT = Path('../../working_dir/tokens/haut-rhin')
DIR_IN_ALL = Path('../../working_dir/tokens/all')

DIR_OUT = Path('../../working_dir/metaphone_json/')
DIR_OUT.mkdir(exist_ok=True,parents=True)

# punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»'

def all_toks_file(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

# def isword(word):
#     if word in punc:
#         return False
#     else:
#         return True



def get_toks(filepath, tok_length):
    toks_file = all_toks_file(filepath)
    print(len(toks_file), "documents to be processed \n")
    toks = []

    for p in toks_file:

        with p.open('r') as f:
            data = f.readlines()
            for line in data:
                line = line.strip('\n')
                toks.append(line)

        filename = p.stem.strip('.txt')
        print(f"{filename} Processed")

    # Length limit
    toks_after_filter = [x.lower() for x in toks if len(x) >= tok_length]
    # de-duplication
    toks_after_filter = list(set(toks_after_filter))



    print(f"\nAfter de-duplication and retaining tokens longer than or equal to {tok_length} letters,\
\n{len(toks_after_filter)} tokens remain, the original had a total of {len(toks)} tokens.")
    return toks_after_filter




def main():
    toks = get_toks(DIR_IN_ALL, 6)
    keys1 = [dm(i)[0] for i in toks]
    keys2 = [dm(i)[1] for i in toks if dm(i)[1] != None]
    keys_mp = set(keys1 + keys2)

    print("all", len(keys_mp))

    dict_mp = defaultdict(set)

    # key1 匹配 Strong match
    mp_tok_key1 = {}
    for i in toks:
        mp_tok_key1[i] = dm(i)[0]

    rev_multidict_key1 = {}
    for key, value in mp_tok_key1.items():
        rev_multidict_key1.setdefault(value, set()).add(key)

    match_key1 = {key: values for key, values in rev_multidict_key1.items() if len(values) > 1}
    # print(match_key1)



    # key2 弱匹配 Minimal match
    mp_tok_key2 = {}
    for i in toks:
        if dm(i)[1] != None:
            mp_tok_key2[i] = dm(i)[1]

    rev_multidict_key2 = {}
    for key, value in mp_tok_key1.items():
        rev_multidict_key2.setdefault(value, set()).add(key)

    match_key2 = {key: values for key, values in rev_multidict_key2.items() if len(values) > 1}
    print(len(match_key2) + len(match_key1))



    # key3 Normal match




    # print(mp_tok_key2)



if __name__ == '__main__':
    main()

