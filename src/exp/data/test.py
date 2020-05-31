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
        tags AS post_tags,
        title AS post_title,
        body AS post_body,
    FROM   `bigquery-public-data.stackoverflow.posts_questions`
    WHERE EXTRACT(YEAR FROM creation_date) BETWEEN 2018 AND 2019
    """
    resp = stackOverflow.query_to_pandas(post_q)
    return resp

if __name__ == "__main__":
    df = get_init_data()
    df.to_csv('dataset/large_data.csv', index=False)