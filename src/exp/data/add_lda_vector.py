import sys
sys.path.append('src')

import pandas as pd
import numpy as np

from libs.text_processing import TextProcessor
from libs.my_paths import *
from libs.my_progress_bar import MyBar


def add_lda_vec(df_with_text, df_out):
    tp = TextProcessor()

    max_len = len(df_out.index)

    bar = MyBar(max=max_len)

    arr = np.zeros((max_len, 300))

    for i in range(max_len):
        text = df_with_text.loc[i, 'post_body']
        arr[i] = tp.get_lda(text)

        bar.next()
    bar.finish()
    arr = arr.T
    for i in range(arr.shape[0]):
        df_out[f"lda{i}"] = arr[i]
    return df_out


if __name__ == "__main__":
    # print(pd.read_csv(base_optimal_data).columns)
    out_df = add_lda_vec(pd.read_csv(base_optimal_data), pd.read_csv('text2.csv'))
    out_df.to_csv('text3.csv', index=False)

    # data = pd.read_csv('text3.csv')
    # max_len = len(data.index)
    # bar = MyBar(max=max_len)
    # for i in range(max_len):
    #     bar.next()
    #     cur = [float(b) for b in data.loc[i, 'lda'].strip('[]').split(', ')]
    #     for j in range(len(cur)):
    #         data.loc[i, f"lda{j}"] = cur[j]
    # bar.finish()

    # data.to_csv('text4.csv', index=False)