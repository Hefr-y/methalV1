#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   mp.py
@Create on :   2022/04/11 09:43:43
@Revise on :   2022/04/23 11:00:12
@Author    :   Heng Yang
@Version   :   1.1
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements: multiprocessing, pathlib, pandas, metaphone_als

from collections import defaultdict
import json
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


def mk_file_json(resultats):

    json_file = DIR_OUT / Path("6lettres.json")
    json_file.touch()
    file_out_path = json_file
    try:
        if Path(file_out_path).exists:
            with file_out_path.open('w',encoding = 'utf-8') as rj:
                rj.write(resultats)

            contenu_json = file_out_path.read_text()
            print("==================================================")
            print(f"Contenu du fichier {json_file} (au format json):\n{contenu_json}")
    except IOError:
        print(f"The json file =>{file_out_path}<= does not exist, exiting...")



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


    d = defaultdict(list)
    for key in keys_mp:
        for tok in toks:
            if key in dm(tok):
                d[key].append(tok)

    match_key = {key: values for key, values in d.items() if len(values) > 1}

    # print(match_key)
    resultats_json = json.dumps(match_key, sort_keys=True, indent=4,ensure_ascii=False)
    mk_file_json(resultats_json)

if __name__ == '__main__':
    main()

