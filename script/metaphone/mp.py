#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   mp.py
@Create on :   2022/04/20 14:56:09
@Revise on :   2022/04/20 14:56:09
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements:
import pandas as pd

df = pd.read_csv('mp_bas.csv')
print(df.head())

a = df.key1.tolist()

duplicated = set()
for i in range(0, len(a)):
    if a[i] in a[i+1:]:
        duplicated.add(a[i])
print(duplicated)

# for indexs in df.index:
#     for i in range(len(df.loc[indexs].values)):
#         if df.loc[indexs].values[i] =='NN':
#             print(indexs,i)
#             print(df.loc[indexs].values[i])