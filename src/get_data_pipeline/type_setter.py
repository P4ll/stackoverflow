import pandas as pd
import numpy as np
import sys

sys.path.append('src')

from libs.my_progress_bar import MyBar
from libs.my_paths import *


def get_post_type(df: pd.DataFrame, neutral=True) -> pd.DataFrame:
    arr = np.zeros(len(df.index), dtype=np.int8)
    bar = MyBar('Post typing', max=len(df.index))
    for i in range(len(df.index)):
        bar.next()
        sc = int(df.loc[i, 'post_score'])
        ans_count = int(df.loc[i, 'post_ans_count'])
        is_closed = int(df.loc[i, 'post_is_closed'])
        if neutral:
            if (sc > 0 or ans_count > 0 and sc == 0 and not is_closed):
                arr[i] = 1
        else:
            if sc > 0:
                arr[i] = 1
    df['type'] = arr
    bar.finish()
    return df


if __name__ == "__main__":
    out_df = get_post_type(pd.read_csv(base_optimal_data), False)
    out_df.to_csv(base_optimal_data, index=False)