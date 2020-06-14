import sys
import time
import math

import pandas as pd
import numpy as np

import urllib.request
from urllib.error import HTTPError
from lxml import html, etree

import os
from os import path
sys.path.append('qtester/libs')

from my_progress_bar import MyBar
from TorCrowler import TorCrawler
from my_paths import base_file_name, base_final_file, base_user_info_file, base_users_id_file
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def insert_user_data(main_data: pd.DataFrame, user_data: pd.DataFrame):
    max_len = len(main_data.index)
    bar = MyBar('Inserting...', max=max_len)
    # 'user_questions_count', 'user_ans_count', 'user_reached_people'
    main_data['user_questions_count'] = [-1 for i in range(max_len)]
    main_data['user_ans_count'] = [-1 for i in range(max_len)]
    main_data['user_reached_people'] = [-1 for i in range(max_len)]

    user_dict = dict()
    for i in range(len(user_data.index)):
        user_dict[user_data.iloc[i, 0]] = (user_data.iloc[i, 1], user_data.iloc[i, 2], user_data.iloc[i, 3])

    for i in range(max_len):
        if not math.isnan(main_data.loc[i, 'id_user']):
            u_id = int(round(main_data.loc[i, 'id_user']))

            if u_id in user_dict:
                q, a, r = user_dict[u_id]
                main_data.loc[i, 'user_questions_count'] = q
                main_data.loc[i, 'user_ans_count'] = a
                main_data.loc[i, 'user_reached_people'] = r

        bar.next()
    bar.finish()

    main_data.to_csv(base_final_file, index=False)

if __name__ == "__main__":
    df = insert_user_data(pd.read_csv(base_file_name), pd.read_csv(base_user_info_file))
