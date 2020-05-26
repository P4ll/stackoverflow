import bq_helper
from bq_helper import BigQueryHelper
stackOverflow = bq_helper.BigQueryHelper(active_project="bigquery-public-data",
                                   dataset_name="stackoverflow")
import pandas as pd

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
    return df

def get_user_reached(df: pd.DataFrame) -> pd.DataFrame:
    return df

def get_post_is_closed(df: pd.DataFrame) -> pd.DataFrame:
    return df

def get_post_type(df: pd.DataFrame) -> pd.DataFrame:
    return df

def get_all_data(init_data: pd.DataFrame=None) -> pd.DataFrame:
    df = pd.DataFrame()

    if init_data == None:
        df = get_init_data()
    else:
        df = init_data

    df = get_user_quest_count(df)
    df = get_post_is_closed(df)
    df = get_post_type(df)
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
    df = get_all_data()
    df.to_csv('test.csv', index=False)