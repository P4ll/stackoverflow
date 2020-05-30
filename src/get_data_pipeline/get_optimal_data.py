import sys
import os
import pandas as pd
import numpy as np
import math

sys.path.append('src')

from libs.my_paths import base_final_file, base_optimal_data
from libs.my_progress_bar import MyBar

df = pd.read_csv(base_final_file)

new_df = pd.DataFrame(columns=df.columns)

max_len = len(df.index)
cur_len = 0

bar = MyBar('Data extracting...', max=max_len)

for row in range(max_len):
    if not math.isnan(df.loc[row, 'id_user']) and not math.isnan(df.loc[row, 'user_rating']) and df.loc[row, 'user_ans_count'] != -1:
        new_df.loc[cur_len] = df.loc[row]
        new_df.loc[cur_len, 'id_user'] = int(round(new_df.loc[cur_len, 'id_user']))
        new_df.loc[cur_len, 'user_rating'] = int(round(new_df.loc[cur_len, 'user_rating']))
        cur_len += 1
    bar.next()

bar.finish()

new_df.id_user = new_df.id_user.astype('int64')
new_df.user_rating = new_df.user_rating.astype('int64')

new_df.to_csv(base_optimal_data, index=False)
print(f"Saved {cur_len} rows")