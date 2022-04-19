from pathlib import Path
import pandas as pd
wd = Path("../../working_dir/metaphone")
df = pd.read_csv(wd / Path('combined_csv_haut.csv'))
print(df.head(10))