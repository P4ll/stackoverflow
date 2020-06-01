import pandas as pd
import numpy as np
import gensim
import nltk
import logging

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models
from gensim.test.utils import datapath

from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

np.random.seed(2020)

nltk.download('wordnet')
stemmer = SnowballStemmer('english')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import sys
sys.path.append('src')

from libs.my_progress_bar import MyBar
from libs.my_paths import base_data

def clear_text(text):
    text = re.sub('<code>(.|\n)*?<\/code>', '', text)
    text = re.sub(r'(\<(/?[^>]+)>)', '', text)
    return text

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    text = clear_text(text)
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def calc_series(ser, name):
    bar = MyBar(message=name, max=len(ser.index))
    max_l = len(ser.index)
    for i in range(max_l):
        ser[i] = preprocess(ser[i])
        bar.next()
    bar.finish()
    return ser

def calc_docs(docs):
    i = 0
    for doc in docs:
        df = pd.read_csv(doc)
        print('begin maping of proc_docs')
        proc_docs = df['post_body'].map(preprocess)
        print('begin maping of proc_head')
        proc_head  = df['post_title'].map(preprocess)
        df = None
        proc_docs = proc_docs.append(proc_head, ignore_index=True)
        proc_docs.to_pickle(f"test{i}.ser")

calc_docs([base_data + 'large_data1.csv'])