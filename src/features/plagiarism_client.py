import requests
import re
import pandas as pd
import math
import sys
import json
sys.path.append('src')

from libs.my_progress_bar import MyBar


ADD_URL = "http://localhost:5000/api/v1/plagiarism/documents"
DETECT_URL = "http://localhost:5000/api/v1/plagiarism/detect"


class PlagiatClient:
    def __init__(self):
        pass

    def fill_from_df(self, df: pd.DataFrame) -> None:
        len_df = len(df.index)
        bar = MyBar(max=len_df)
        for i in range(len_df):
            self.fill_from_row(df.iloc[i])
            bar.next()
        bar.finish()

    def fill_from_row(self, row: pd.Series) -> None:
        self.add_doc(str(row['id_post']), row['post_title'],
                     row['post_tags'], row['post_body'])

    def add_doc(self, user: str, title: str, decr: str, content: str) -> None:
        content = self.preproc_text(content)

        data = {
            "content": content,
            "title": title,
            "author": user,
            "description": decr
        }
        r = requests.post(ADD_URL, json=data)

    def text_test(self, text: str, post_id: int) -> float:
        data = {
            "text": text
        }

        r = requests.post(DETECT_URL, json=data)
        json_data = json.loads(r.text)
        ans = 0.0
        if json_data['success']:
            if int(json_data['data']['doc']['author']) != post_id:
                ans = json_data['data']['similarity_score']
        return ans

    def del_code(self, text: str) -> str:
        text = re.sub('<code>(.|\n)*?<\/code>', '', text)
        text = re.sub(r'(\<(/?[^>]+)>)', '', text)
        return text

    def del_delims(self, text: str) -> str:
        text = re.sub('\r\n', ' ', text)
        text = re.sub('\n', ' ', text)
        text = re.sub('\r', ' ', text)
        return text

    def preproc_text(self, text: str) -> str:
        text = self.del_code(text)
        text = self.del_delims(text)
        return text


if __name__ == "__main__":
    df = pd.read_csv('dataset/optimal_data.csv')
    client = PlagiatClient()
    client.fill_from_df(df)