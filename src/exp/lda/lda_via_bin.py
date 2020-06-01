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

print('begin load docs')
processed_docs = pd.Series()
for i in range(1, 4):
  processed_docs = processed_docs.append(pd.read_pickle(f"proc_docs{i}.ser"), ignore_index=True)

print(len(processed_docs.index))
print(processed_docs[:5])

print('begin create the dict')
dictionary = gensim.corpora.Dictionary(processed_docs)
dictionary.filter_extremes(no_below=25, no_above=0.6, keep_n=300000)

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
processed_docs = None

tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]
print(dictionary)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print('begin train lda')
lda_model_tfidf = gensim.models.LdaModel(corpus_tfidf, num_topics=200, id2word=dictionary, passes=2) # LdaMulticore with workers=2


for idx, topic in lda_model_tfidf.print_topics(5):
    print('Topic: {} Word: {}'.format(idx, topic))


temp_file = datapath("models_data/lda_model/model")
lda_model_tfidf.save(temp_file)