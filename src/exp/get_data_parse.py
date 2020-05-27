import pandas as pd
import numpy as np

import urllib.request
from lxml import html, etree

import os
from progress.bar import Bar

import sys
import time

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
    for user_id in df['id_user']:
        try:
            resp = urllib.request.urlopen(f'https://stackoverflow.com/users/{int(user_id)}')
            # resp = urllib.request.urlopen(f'https://stackoverflow.com/users/142124')
            readed = resp.read()

            if str(readed).find("Too many requests") != -1:
                print("BANNED, W8 for STACK")
                time.sleep(5 * 61)
                resp = urllib.request.urlopen(f'https://stackoverflow.com/users/{int(user_id)}')
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

    new_df = pd.DataFrame()
    new_df['user_reached_people'] = reached_arr
    new_df['user_ans_count'] = ans_arr
    new_df['user_questions_count'] = quest_arr

    new_df.to_csv('dataset/add_data.csv', index=False)

    bar.finish()
    return df


def get_all_data(init_data: pd.DataFrame) -> pd.DataFrame:
    df = init_data

    print('init data loaded')

    df = get_user_reached(df)
    sys.exit()
    df.to_csv('temp.csv', index=False)
    print('Reached people calculated')

    return df

if __name__ == "__main__":
    df = get_all_data(pd.read_csv('temp.csv'))
    df.to_csv('dataset/data.csv')