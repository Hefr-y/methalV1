#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   Combine_CSVs.py
@Create on :   2022/04/09 16:11:48
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements: os, glob, pandas


import os
import glob
import pandas as pd
#set working directory
os.chdir("../working_dir/metaphone/test_combine")

#find all csv files in the folder
#use glob pattern matching -> extension = 'csv'
#save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
print(all_filenames)

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.columns = ['forme', 'key1', 'key2']
#export to csv
combined_csv.to_csv( "../combined_csv.csv", index=False, encoding='utf-8-sig')