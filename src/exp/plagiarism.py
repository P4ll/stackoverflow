from text_matcher import matcher
import pandas as pd
import re
import sys
sys.path.append('src')

from libs.my_progress_bar import MyBar

def del_code(text: str) -> str:
    text = re.sub('<code>(.|\n)*?<\/code>', '', text)
    text = re.sub(r'(\<(/?[^>]+)>)', '', text)
    return text

def del_delims(text: str) -> str:
    text = re.sub('\r\n', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('\r', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def preproc_text(text: str) -> str:
    text = del_code(text)
    text = del_delims(text)
    return text


text1 = "Within the proc, I have a MERGE statement that updates tables based on whether it is an INSERT (if ActId is 0) or an UPDATE. I would like to update the JSON @ChangeSet variable"
text2 = "I am trying to invoke an HTTP triggered Azure function built on with a GET request. I setup the linked service as per the recommended steps and the function itself works with a query string"


df = pd.read_csv('dataset/optimal_data.csv')

max_len = len(df.index)
bar = MyBar(max=max_len)
for i in range(max_len):
    text2 = preproc_text(df.loc[i, 'post_body'])
    if text2 == '' or text2 == ' ':
        bar.next()
        continue
    ta = matcher.Text(text1, 'a')
    tb = matcher.Text(text2, 'b')

    z = matcher.Matcher(ta, tb).match()
    bar.next()
    if z[0] != 0:
        print(z)
bar.finish()