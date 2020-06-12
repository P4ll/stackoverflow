import bq_helper
from bq_helper import BigQueryHelper
stackOverflow = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="stackoverflow")
import pandas as pd
import numpy as np

import urllib.request
from lxml import html, etree

import os
import sys
import math
sys.path.append('src')
from libs.my_progress_bar import MyBar
import libs.my_paths as mp

def get_init_data() -> pd.DataFrame:
    post_q = """SELECT
        id AS id_post,
        owner_user_id AS id_user,
        score AS post_score,
        answer_count AS post_ans_count,
        tags AS post_tags,
        title AS post_title,
        body AS post_body,
        view_count AS post_view_count,
        creation_date AS post_date,
        (SELECT reputation FROM `bigquery-public-data.stackoverflow.users` WHERE id = owner_user_id) AS user_rating,
        (SELECT creation_date FROM `bigquery-public-data.stackoverflow.users` WHERE id = owner_user_id) AS user_reg_date
    FROM   `bigquery-public-data.stackoverflow.posts_questions`
    WHERE EXTRACT(YEAR FROM creation_date) = 2019 AND EXTRACT(MONTH FROM creation_date) = 10
    """
    resp = stackOverflow.query_to_pandas(post_q)
    return resp

def get_post_is_closed(df: pd.DataFrame) -> pd.DataFrame:
    arr = np.zeros(len(df.index), dtype=np.int8)
    i = 0
    bar = MyBar('post is closed', max=len(df.index))
    for title in df['post_title']:
        bar.next()
        strs = title.split(' ')
        if strs[-1] == '[closed]' or strs[-1] == '[duplicate]':
            arr[i] = 1
        i += 1
    df['post_is_closed'] = arr
    bar.finish()
    return df

def get_post_type(df: pd.DataFrame) -> pd.DataFrame:
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
    df['type'] = arr
    bar.finish()
    print('good: {}, bad: {}, neutral: {}'.format(good_count, bad_count, neu_count))
    return df

def get_all_data(init_data: pd.DataFrame=None) -> pd.DataFrame:
    tmp_file = mp.base_file_name
    df = pd.DataFrame()

    if init_data is None:
        df = get_init_data()
    else:
        df = init_data

    df.to_csv(tmp_file, index=False)
    print('init data loaded')

    df = get_post_is_closed(df)
    df.to_csv(tmp_file, index=False)
    print('post closed loaded')
    
    df = get_post_type(df)
    df.to_csv(tmp_file, index=False)
    print('all data loaded')

    return df

def get_user_ids(df: pd.DataFrame) -> pd.DataFrame:
    user_ids = set()
    for id in df.id_user:
        if not math.isnan(id):
            user_ids.add(int(round(id)))

    out_data = pd.DataFrame()
    out_data['id_user'] = list(user_ids)
    out_data.to_csv(mp.base_users_id_file, index=False)

    return out_data

if __name__ == "__main__":
    df = get_all_data()
    users_id = get_user_ids(df)