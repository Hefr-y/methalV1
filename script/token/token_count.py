from pathlib import Path
import pandas as pd

wd = Path('../../working_dir')
tokpath = wd / "tokens/"
metapath = wd / "metadata/metadata_avec_period.csv"
outpath = wd / "metadata/metadata_V1.csv"

df_meta = pd.read_csv(metapath, index_col=0)
df_meta['Tokens'] = 1

def all_txts(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

def count_tok(p):
    with p.open('r') as f:
        data = f.readlines()
        df_meta.loc[p.stem[:-4], 'Tokens'] = len(data)



def main():
    txts = all_txts(tokpath)
    for i in txts:
        count_tok(i)

    print("Total : ", len(txts))
    print(df_meta)
    df_meta.to_csv(outpath)


if __name__ == '__main__':
    main()

