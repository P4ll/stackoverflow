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

def set_by_doc(df, df2, neutral=True):
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
    df2['post_type'] = arr
    bar.finish()
    return df2


def doc_setter_classification(df, df2):
    arr = np.zeros(len(df.index), dtype=np.int8)
    bar = MyBar('Post typing', max=len(df.index))
    good_count = 0
    bad_count = 0
    neu_count = 0
    for i in range(len(df.index)):
        bar.next()
        sc = int(df.loc[i, 'post_score'])
        ans_count = int(df.loc[i, 'post_ans_count'])
        is_closed = int(df.loc[i, 'post_is_closed'])
        if sc > 0:
            arr[i] = 1
            good_count += 1
        elif sc < 0 or is_closed:
            arr[i] = 0
            bad_count += 1
        else:
            arr[i] = 2
            neu_count += 1
    df2['post_type'] = arr
    bar.finish()
    print('good: {}, bad: {}, neutral: {}'.format(good_count, bad_count, neu_count))
    return df2

if __name__ == "__main__":
    # out_df = get_post_type(pd.read_csv(base_optimal_data))
    # out_df.to_csv(base_optimal_data, index=False)
    out_df = doc_setter_classification(pd.read_csv(base_optimal_data), pd.read_csv('text2.csv'))
    out_df.to_csv('text2.csv', index=False)