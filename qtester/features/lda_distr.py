import pandas as pd
import numpy as np
from feature import IFeature
from libs.text_processing import TextProcessor


class LdaDistr(IFeature):
    def __init__(self):
        self.name = "lda"
        self.mode = "dict"
        self._text_proc = TextProcessor()

    def get_metric(self, data_row: pd.Series):
        lda = self._text_proc.get_lda(data_row['post_body'])
        out_data = list()
        for i, val in enumerate(lda):
            out_data.append(['{}{}'.format(self.name, i), val])
        return out_data

    def name(self):
        return self.name

    def mode(self):
        return self.mode