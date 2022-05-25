#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File      :   nospace.py
@Create on :   2022/05/12 10:24:11
@Revise on :   2022/05/12 10:24:11
@Author    :   Heng Yang
@Version   :   1.0
@Contact   :   heng.yang@etu.univ-grenoble-alpes.fr
@Desc      :   None
'''

# Requirements:
from multiprocessing import Pool
from pathlib import Path


def delete_space(file_path,skip_line: int = 7):
    # get_data_from_file
    with file_path.open('r') as file:
        for i in range(skip_line):
            next(file)
        datalist = file.readlines()

    # delete_space_in_datalist
    for i in range(len(datalist)):
        datalist[i] = datalist[i].replace(' ','')
        datalist[i] = datalist[i].replace('_','')

    # write_result
    new_file = file_path.parent / (file_path.stem + "_nospace_noline.txt")
    new_file.touch()

    with new_file.open('w') as f:
        for i in datalist:
            f.write(i)


if __name__ == '__main__':
    all_files = sorted(Path.cwd().rglob('words_*'))
    # print(all_files)
    pool = Pool()
    data_no_space = pool.map(delete_space, all_files)
    print("done")
