import pandas as pd
import numpy as np
import math

users_data_types = {
    'id_user': 'int64',
    'user_questions_count': 'int64',
    'user_ans_count': 'int64',
    'user_reached_people': 'int64'
}
# df = pd.read_csv('save.csv')
# print(df.loc[2, 'id_user'])
# tt = dict()

# for i in range(len(df.index)):
#     tt[df.iloc[i, 0]] = (df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3])

# print(tt)

df = pd.read_csv('dataset/data.csv')
import sys
sys.path.append('src/')
from data_miner import DataMiner

dd = DataMiner()

oo = dd.get_data(df.head(10))

print(oo.head(10))