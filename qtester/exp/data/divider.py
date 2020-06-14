import pandas as pd
import numpy as np

import urllib.request
from lxml import html, etree

import os
import sys
import math
sys.path.append('qtester')
from libs.my_progress_bar import MyBar
import libs.my_paths as mp

df = pd.read_csv(mp.base_data + 'large_data.csv')

pp = len(df.index) // 3
df = df[:pp]

df.to_csv(mp.base_data + 'large_data1.csv', index=False)
