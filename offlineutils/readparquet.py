import pandas as pd
import os

df = pd.read_parquet(os.path.join('testdata','offline','csku.parquet'), engine='pyarrow')

print(df)