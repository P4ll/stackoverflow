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
sys.path.append('qtester')

from libs.my_progress_bar import MyBar
from libs.TorCrowler import TorCrawler
from libs.my_paths import base_file_name, base_final_file, base_user_info_file, base_users_id_file
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

def save_add_user_info(df: pd.DataFrame) -> pd.DataFrame:
    out_df = pd.DataFrame(columns=['id_user', 'user_questions_count', 'user_ans_count', 'user_reached_people'])

    i = 0
    if path.isfile(base_user_info_file):
        out_df = pd.read_csv(base_user_info_file)
        i = len(out_df.index)
    
    crawler = TorCrawler(ctrl_pass='mypassword')
    bar = MyBar('Progress', max=len(df.index))
    bar.index = i
    user_count = len(df.index)
    fail_count = 0
    while i < user_count:
        u_id = int(df.loc[i]['id_user'])

        if i != 0 and i % 200 == 0:
            out_df.to_csv(base_user_info_file, index=False)

        try:
            response = crawler.get(f"https://stackoverflow.com/users/{u_id}", headers={'User-Agent': UserAgent().chrome})
            tree = html.fromstring(str(response))

            reached = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[3]/div/div[1]')[0].text
            reached = reached.strip('~')
            reached_n = float(reached.strip('km'))
            if reached[-1] == 'k':
                reached_n *= 1000
            elif reached[-1] == 'm':
                reached_n *= 1000000
            
            ans = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]')[0].text
            ans = ans.replace(',', '')
            ans_n = int(ans)

            quest = tree.xpath('//*[@id="user-card"]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]')[0].text
            quest = quest.replace(',', '')
            quest_n = int(quest)

            out_df.loc[i] = [u_id, quest_n, ans_n, reached_n]
        except Exception:
            if str(sys.exc_info()[1]) != "HTTP Error 404: Not Found" and fail_count < 2 and str(sys.exc_info()[1]) != "list index out of range":
                print(f"SLEEP ON 60 id: {u_id}, message: {str(sys.exc_info()[1])}")
                time.sleep(60)
                crawler.rotate()
                fail_count += 1
                continue
            out_df.loc[i] = [u_id, -1, -1, -1]

        bar.next()
        i += 1
        fail_count = 0

    out_df.to_csv(base_user_info_file, index=False)
    bar.finish()
    return out_df

if __name__ == "__main__":
    df = save_add_user_info(pd.read_csv(base_users_id_file))