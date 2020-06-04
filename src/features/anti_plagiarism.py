import pandas as pd
import numpy as np
from feature import Feature
from features.plagiarism_client import PlagiatClient


class AntiPlagiarism(Feature):
    def __init__(self):
        self.name = "plagiarism"
        self._client = PlagiatClient()

    def get_metric(self, data_row: pd.Series) -> float:
        return self._client.text_test(data_row['post_body'])

    def name(self):
        return self.name

