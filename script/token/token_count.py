from pathlib import Path
import pandas as pd

wd = Path('../../working_dir')
tokpath = wd / "tokens/"
teipath = wd / "metadata/metadata_tei.csv"
tei2path = wd / "metadata/metadata_tei2.csv"

df_tei = pd.read_csv(teipath, index_col=0)
df_tei2 = pd.read_csv(tei2path, index_col=0)
# print(df_tei, df_tei2)
frames = [df_tei, df_tei2]
df_methal = pd.concat(frames)
df_methal['Tokens'] = 1

def all_txts(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

def count_tok(p):
    with p.open('r') as f:
        data = f.readlines()
        df_methal.loc[p.stem[:-4], 'Tokens'] = len(data)



def append_tok():
    txts = all_txts(tokpath)
    for i in txts:
        count_tok(i)

    print("Total : ", len(txts))
    print(df_methal)



def main():
    append_tok()

if __name__ == '__main__':
    main()

