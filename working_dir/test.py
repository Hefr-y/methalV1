#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   test.py
@Create on :   2022/04/26 10:01:56
@Revise on :   2022/04/26 10:01:56
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements:

from pathlib import Path
import pandas as pd


filename = "./working_dir/results_text-words-all_PubDept_Haut-Rhin-Bas-Rhin.csv"
df = pd.read_csv(filename, sep= '\t', usecols = [0,7,9])
df.columns = ['forme','zeta_sd2','eta_sg0']
print(df)


