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
import argparse
from pathlib import Path
import pandas as pd
import json
import pygal

# Pygal style
mp_style = pygal.style.Style(
    background = 'rgba(211, 211, 211, 1)',
    plot_background = 'rgba(211, 211, 211, 1)',
    font_family="FreeSans",
    title_font_size = 18,
    legend_font_size = 14,
    label_font_size = 12,
    major_label_font_size = 12,
    value_font_size = 12,
    major_value_font_size = 12,
    tooltip_font_size = 12,
    opacity_hover=0.2)


# Obtenir l'entrée de la ligne de commande
def set_up_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('key_metaphone', help="une clé métaphone")

    return parser
parser = set_up_argparser()
args = parser.parse_args()

# Metaphone key set
KEY_MP = args.key_metaphone

# Path set
zetawd = Path('../../working_dir/mesures_discriminativite/pydistinto/working_dir/output_methal/results')
wd = Path("../../working_dir")
zeta_file = zetawd / "results_text-words-all_PubDept_Haut-Rhin-Bas-Rhin.csv"
json_file = wd / "metaphone_json" / "6lettres.json"
plot_file = wd / "plot" / "metaphone_forme_zeta" /str(KEY_MP+".svg")



# Functions: plot barchart
def get_data(zetafile, measure, jsonfile):

    # measure : "zeta_sd2", "eta_sg0"

    # zeta
    data = pd.read_csv(zetafile, sep= '\t', usecols = [0,7,9])
    data.columns = ['forme','zeta_sd2','eta_sg0']
    zetadata = dict(zip(data['forme'],data[measure]))
    # print("\nzetadata\n", zetadata)

    # formes with one same metaphone
    with jsonfile.open('r', encoding='utf-8') as load_f:
        mpdata = json.load(load_f)

    # forme match zeta score
    forme_zeta = {}
    for forme in mpdata[KEY_MP]:
        forme_zeta[forme] = zetadata[forme]

    return forme_zeta


def make_barchart(zeta_file, json_file, plotfile, measure):

    f_zeta = get_data(zeta_file, measure, json_file)
    sorted_f_zeta = sorted(f_zeta.items(), key = lambda item : item[1], reverse = True)

    # print(KEY_MP, ":", f_zeta)
    # print(sorted(f_zeta.items(), key = lambda item : item[1], reverse = True))

    range_min = min(list(f_zeta.values())) * 1.1
    range_max = max(list(f_zeta.values())) * 1.1
    plot = pygal.HorizontalBar(style = mp_style,
                               print_values = False,
                               print_labels = True,
                               show_legend = False,
                               range = (range_min, range_max),
                               title = ("Contrastive Analysis with " + str(measure) + "\n(Metaphone Key: "+KEY_MP+")"),
                               y_title = "Forms with the same metaphone key",
                               x_title = measure +"-"+ "text-words-all")
    for i in sorted_f_zeta:
        if i[1] < 0:
            color = "#29a329"
        else:
            color = "#60799f"
        # forme,
        plot.add(i[0], [{"value": float(i[1]), "label": i[0], "color": color}])
    plot.render_to_file(plotfile)

# print(get_data(zeta_file, "zeta_sd2", json_file))
make_barchart(zeta_file,json_file,plot_file,"zeta_sd2")