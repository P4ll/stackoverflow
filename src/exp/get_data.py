import bq_helper
from bq_helper import BigQueryHelper
stackOverflow = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="stackoverflow")
import pandas as pd
import numpy as np

import urllib.request
from lxml import html, etree

import os
from progress.bar import Bar

class MyBar(Bar):
    message = 'Loading'
    suffix = '%(index)d/%(max)d | %(percent).1f%% - %(rem_min)d min'

    @property
    def rem_min(self):
        return self.eta // 60

dtypes = {
    'id_user': 'int64',
    'post_score': 'int64',
    'post_ans_count': 'int64',
    'post_tags': 'category',
    'post_title': 'category',
    'post_body': 'category',
    'post_view_count': 'int64',
    'post_date': 'category',
    'post_is_closed': 'int8',
    'user_rating': 'int64',
    'user_reg_date': 'category',
    'user_reached_people': 'int64',
    'user_questions_count': 'int64',
    'type': 'int8',
}

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

def get_user_quest_count(df: pd.DataFrame) -> pd.DataFrame:
    count_ser = np.zeros(len(df.index), dtype=np.int64)
    i = 0
    bar = MyBar('Questions count', max=len(df.index))
    for user_id in df['id_user']:
        bar.next()
        # q = f"""SELECT
        # COUNT(*) AS q_count
        # FROM `bigquery-public-data.stackoverflow.posts_questions`
        # WHERE owner_user_id = {int(user_id)}
        # """
        # resp = stackOverflow.query_to_pandas(q)
        # count_ser[i] = resp.iloc[0][0]

        try:
            resp = urllib.request.urlopen(f'https://stackoverflow.com/users/{int(user_id)}')
            tree = html.fromstring(resp.read())
            a = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text
            a = a.strip('~')
            n = float(a.strip('km'))
            if a[-1] == 'k':
                n *= 1000
            elif a[-1] == 'm':
                n *= 1000000
            count_ser[i] = int(n)
        except Exception:
            count_ser[i] = -1

        i += 1
    df['user_questions_count'] = count_ser
    new_df = pd.DataFrame()
    new_df['user_questions_count'] = count_ser
    new_df.to_csv('user_quest_count', index=False)
    bar.finish()
    return df

def get_user_reached(df: pd.DataFrame) -> pd.DataFrame:
    arr = np.zeros(len(df.index), dtype=np.int64)
    i = 0
    bar = MyBar('User reached', max=len(df.index))
    for user_id in df['id_user']:
        bar.next()
        try:
            resp = urllib.request.urlopen(f'https://stackoverflow.com/users/{int(user_id)}')
            tree = html.fromstring(resp.read())
            a = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text
            a = a.strip('~')
            n = float(a.strip('km'))
            if a[-1] == 'k':
                n *= 1000
            elif a[-1] == 'm':
                n *= 1000000
            arr[i] = int(n)
        except Exception:
            arr[i] = -1
        i += 1
    df['user_reached_people'] = arr
    new_df = pd.DataFrame()
    new_df['user_reached_people'] = arr
    new_df.to_csv('user_reached_people', index=False)
    bar.finish()
    return df

def get_post_is_closed(df: pd.DataFrame) -> pd.DataFrame:
    arr = np.array(len(df.index), dtype=np.int8)
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
    arr = np.array(len(df.index), dtype=np.int8)
    bar = MyBar('Post typing', max=len(df.index))
    for i in range(len(df.index)):
        bar.next()
        sc = int(df.iloc[i]['post_score'])
        ans_count = int(df.iloc[i]['post_ans_count'])
        is_closed = int(df.iloc[i]['post_is_closed'])
        if (sc > 0 or ans_count > 0 and sc == 0 and not is_closed):
            arr[i] = 1
    df['type'] = arr
    bar.finish()
    return df

def get_all_data(init_data: pd.DataFrame=None) -> pd.DataFrame:
    df = pd.DataFrame()

    if init_data is None:
        df = get_init_data()
    else:
        df = init_data
    df.to_csv('temp.csv', index=False)
    print('init data loaded')

    df = get_user_quest_count(df)
    df.to_csv('temp.csv', index=False)
    print('user question count loaded')

    df = get_user_reached(df)
    df.to_csv('temp.csv', index=False)
    print('Reached people calculated')

    df = get_post_is_closed(df)
    df.to_csv('temp.csv', index=False)
    print('post closed loaded')
    
    df = get_post_type(df)
    df.to_csv('temp.csv', index=False)
    print('all data loaded')

    return df

def test():
    post_q = """SELECT
    id,
    reputation
    FROM `bigquery-public-data.stackoverflow.users`
    WHERE id = 123
    """
    resp = stackOverflow.query_to_pandas_safe(post_q)
    print(resp.head(10))

if __name__ == "__main__":
    # df = get_all_data()
    # df.to_csv('test.csv', index=False, dtype=dtypes)
    # df = pd.read_csv('test.csv', dtype=dtypes)
    # df.dtypes = dtypes
    # df = pd.read_csv('test.csv')
    # print(df.head(5))
    df = get_all_data(pd.read_csv('temp.csv'))
    os.remove('temp.csv')
    df.to_csv('dataset/data.csv')

    # df.to_csv('dataset/dataset.csv', index=False)
