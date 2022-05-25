#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   match_mp.py
@Create on :   2022/04/11 09:43:43
@Revise on :   2022/04/23 11:00:12
@Author    :   Heng Yang
@Version   :   1.1
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements: multiprocessing, pathlib, pandas, metaphone_als

import argparse
from collections import defaultdict
import json
from multiprocessing.pool import Pool
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")
from metaphone_als import dm

# Get command-line input
def set_up_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help="input directory containing TEI XML files")
    parser.add_argument('outfile', help="output file as CSV with information about the TEI corpus")
    return parser

def mk_file_json(outfile,resultats):

    json_file = outfile
    json_file.touch()
    file_out_path = json_file
    try:
        if Path(file_out_path).exists:
            with file_out_path.open('w',encoding = 'utf-8') as rj:
                rj.write(resultats)

            contenu_json = file_out_path.read_text()
            print("==================================================")
            # print(f"Contenu du fichier {json_file} (au format json):\n{contenu_json}")
            print("done")
    except IOError:
        print(f"The json file =>{file_out_path}<= does not exist, exiting...")




def get_toks(inputfile, skip_line: int = 7):

    ngrams_ori = []

    # get_data_from_file
    with open(inputfile,'r') as f:
        for i in range(skip_line):
            next(f)
        data = f.readlines()
        for line in data:
            line = line.strip('\n')
            ngrams_ori.append(line)

    # delete_space_in_toks, {ngrams sans espace et tiret : ngrams original}
    dict_ngrams = {}
    for i in range(len(ngrams_ori)):
        dict_ngrams[ngrams_ori[i]] = ngrams_ori[i].replace(' ','').replace('_','')

    print(f"{inputfile} Processed")

    print(f"Total of {len(dict_ngrams)} tokens.")
    return dict_ngrams




def main():
    parser = set_up_argparser()
    args = parser.parse_args()

    dict_ngrams = get_toks(args.inputfile)

    keys1 = [dm(dict_ngrams[i])[0] for i in dict_ngrams]
    keys2 = [dm(dict_ngrams[i])[1] for i in dict_ngrams if dm(dict_ngrams[i])[1] != None]
    keys_mp = set(keys1 + keys2)


    d = defaultdict(list)
    for key in keys_mp:
        for ng_origin in dict_ngrams:
            if key in dm(dict_ngrams[ng_origin]):
                d[key].append({ng_origin:dict_ngrams[ng_origin]})

    match_key = {key: values for key, values in d.items() if len(values) >= 1}

    # print(match_key)
    resultats_json = json.dumps(match_key, sort_keys=True, indent=4,ensure_ascii=False)
    mk_file_json(Path(args.outfile),resultats_json)

if __name__ == '__main__':
    main()

