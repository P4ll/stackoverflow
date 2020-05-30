import pandas as pd
import numpy as np
import math
import sys
sys.path.append('src/libs')

from my_paths import base_file_name, base_final_file, base_user_info_file, base_users_id_file
from my_progress_bar import MyBar

df = pd.read_csv(base_user_info_file)

bar = MyBar(max=len(df.index))

max_l = len(df.index)

for i in range(max_l):
    for j in range(4):
        df.iloc[i, j] = int(round(df.iloc[i, j]))
    bar.next()

df = df.astype('int64')
bar.finish()
df.to_csv(base_user_info_file, index=False)