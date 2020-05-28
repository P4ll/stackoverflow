import pandas as pd
import numpy as np

df = pd.DataFrame()
df['test'] = [1, 2, 3, 4, 5]
df['ttt'] = [31, 1, 1, 1, 1]
df.loc[5] = [12, 12]
df.loc[6] = [12, 12]
print(df.head(10))