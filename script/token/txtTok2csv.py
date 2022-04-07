from multiprocessing.pool import Pool
from pathlib import Path
import pandas as pd

DIR_IN = Path('../../working_dir/tokens')

DIR_OUT = DIR_IN / Path('outcsv')
DIR_OUT.mkdir(exist_ok=True,parents=True)

# filename = 'clemens-gift.txt.tok'
# p = Path(filename)


def all_txts(input_dir):
    return sorted(Path(input_dir).rglob('*tok'))

def txt2csv(p):
    with p.open('r') as f:
        data = f.readlines()
        for i in range(len(data)):
            data[i] = data[i].strip('\n')
    # print(data)


    df = pd.DataFrame(data, columns=[''])

    df['empty1'] = 'NaN'
    df['empty2'] = 'NaN'

    filename = p.stem.strip('.txt')
    print(f"{filename} Processed")
    print(df)

    out_file_path = DIR_OUT / Path(p.stem.strip('.txt') + '.csv')
    df.to_csv(out_file_path ,sep='\t', header = None, index=None)

def main():
    txts = all_txts(DIR_IN)
    pool = Pool()
    pool.map(txt2csv, txts)


if __name__ == '__main__':
    main()

