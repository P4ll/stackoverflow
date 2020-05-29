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
from progress.bar import Bar

sys.path.append('scr/exp')
from TorCrowler import TorCrawler
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class MyBar(Bar):
    message = 'Loading'
    add_info = ""
    suffix = '%(index)d/%(max)d | %(percent).1f%% - %(rem_min)d min %(get_add)s'

    @property
    def rem_min(self):
        return self.eta // 60
    
    @property
    def get_add(self):
        return self.add_info

def get_user_reached(df: pd.DataFrame) -> pd.DataFrame:
    reached_arr = np.zeros(len(df.index), dtype=np.int64)
    ans_arr = np.zeros(len(df.index), dtype=np.int64)
    quest_arr = np.zeros(len(df.index), dtype=np.int64)

    i = 0
    bar = MyBar('Progress', max=len(df.index))
    prev_i = 0
    if path.isfile('save.csv'):
        ss = pd.read_csv('save.csv')
        prev_i = len(ss.index)
        for j in range(prev_i):
            reached_arr[j] = ss.iloc[j]['user_reached_people']
            ans_arr[j] = ss.iloc[j]['user_ans_count']
            quest_arr[j] = ss.iloc[j]['user_questions_count']
    for user_id in df['id_user']:
        if i < prev_i:
            i += 1
            continue

        if i % 200 == 0 and i != 0:
            new_df = pd.DataFrame()
            new_df['id_user'] = df['id_user'][:i - 1]
            new_df['user_reached_people'] = reached_arr[:i - 1]
            new_df['user_ans_count'] = ans_arr[:i - 1]
            new_df['user_questions_count'] = quest_arr[:i - 1]
            new_df.to_csv('save.csv', index=False)
            print('DATA SAVED')

        try:
            try:
                resp = urllib.request.urlopen(f'https://stackoverflow.com/users/{int(user_id)}')
            except HTTPError:
                if str(sys.exc_info()[1]) != "HTTP Error 404: Not Found":
                    new_df = pd.DataFrame()
                    new_df['id_user'] = df['id_user'][:i - 1]
                    new_df['user_reached_people'] = reached_arr[:i - 1]
                    new_df['user_ans_count'] = ans_arr[:i - 1]
                    new_df['user_questions_count'] = quest_arr[:i - 1]
                    new_df.to_csv('save.csv', index=False)

                    print("\nBANNED, W8 for STACK")
                    time.sleep(5 * 61)
                    resp = urllib.request.urlopen(f'https://stackoverflow.com/users/{int(user_id)}')
                else:
                    raise Exception("Page not found")

            readed = resp.read()

            tree = html.fromstring(readed)

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

            reached_arr[i] = int(reached_n)
            ans_arr[i] = int(ans_n)
            quest_arr[i] = int(quest_n)
        except Exception:
            reached_arr[i] = -1
            ans_arr[i] = -1
            quest_arr[i] = -1
        # print(f" user_id: {user_id}, ans: {ans_arr[i]}, quest: {quest_arr[i]}, reached: {reached_arr[i]}")
        state_str = f" user_id: {user_id}, ans: {ans_arr[i]}, quest: {quest_arr[i]}, reached: {reached_arr[i]}"
        bar.add_info = state_str
        bar.next()
        i += 1
        time.sleep(0.3)

    new_df = pd.DataFrame()
    new_df['id_user'] = df['id_user']
    new_df['user_reached_people'] = reached_arr
    new_df['user_ans_count'] = ans_arr
    new_df['user_questions_count'] = quest_arr

    new_df.to_csv('dataset/add_data.csv', index=False)

    bar.finish()
    return df

users_data_types = {
    'id_user': 'int64',
    'user_questions_count': 'int64',
    'user_ans_count': 'int64',
    'user_reached_people': 'int64'
}

def save_add_user_info(df: pd.DataFrame) -> None:
    out_df = pd.DataFrame(columns=['id_user', 'user_questions_count', 'user_ans_count', 'user_reached_people'])

    i = 0
    if path.isfile('save.csv'):
        out_df = pd.read_csv('save.csv')
        i = len(out_df.index)
    
    crawler = TorCrawler(ctrl_pass='mypassword')
    bar = MyBar('Progress', max=len(df.index))
    bar.index = i
    user_count = len(df.index)
    fail_count = 0
    while i < user_count:
        u_id = int(df.loc[i]['id_user'])

        if i != 0 and i % 200 == 0:
            out_df.to_csv('save.csv', index=False)

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

    out_df.to_csv('dataset/users_data.csv', index=False)
    bar.finish()

def get_users_table():
    df = pd.read_csv('temp.csv')
    a = set()
    for u_id in df['id_user']:
        if (not math.isnan(u_id)):
            a.add(int(u_id))
    user_df = pd.DataFrame()
    user_df['id_user'] = list(a)
    user_df.to_csv('id_user.csv', index=False)

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

    main_data.to_csv('temp.csv', index=False)

if __name__ == "__main__":
    df = save_add_user_info(pd.read_csv('id_user.csv'))
    # insert_user_data(pd.read_csv('temp.csv'), pd.read_csv('save.csv'))