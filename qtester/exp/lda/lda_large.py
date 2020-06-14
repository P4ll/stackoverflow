import pandas as pd
import numpy as np
import gensim
import nltk
import logging
import sys
sys.path.append('src')

from libs.my_paths import base_model

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

data = pd.read_csv('dataset/large_data.csv', low_memory=True)
data.head(3)

doc_sample = data.loc[3, 'post_body']

print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))

print('begin preprocess')
processed_docs = data['post_body'].map(preprocess)
processed_headers = data['post_title'].map(preprocess)
print('end preprocess')
data = None

processed_docs.to_pickle('processed_docs')
processed_headers.to_pickle('processed_headers')


processed_docs = processed_docs.append(processed_headers, ignore_index=True)
len(processed_docs)

dictionary = gensim.corpora.Dictionary(processed_docs)
dictionary.filter_extremes(no_below=50, no_above=0.6, keep_n=300000)

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

print('begin train')
lda_model_tfidf = gensim.models.LdaModel(corpus_tfidf, num_topics=200, id2word=dictionary, passes=2, workers=2)
print('end train')

for idx, topic in lda_model_tfidf.print_topics(5):
    print('Topic: {} Word: {}'.format(idx, topic))

temp_file = datapath(base_model + 'lmodel/model')
lda_model_tfidf.save(temp_file)
