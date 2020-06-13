import pandas as pd
import re
import numpy as np
import scipy.stats as stats
from feature import IFeature


class UnnecessaryInformation(IFeature):
    def __init__(self):
        self.name = "debug_inf"

    def train(self, data: pd.DataFrame) -> None:
        len_of_each = []
        mid_count = 0

        for elem in data["post_body"]:
            mid_count += len(elem)
            text = re.search('<code>(.|\n)*?<\/code>', elem)
            if text != None:
                len_of_each.append(len(text.group(0)))
            else:
                text = len_of_each.append(0)
        h = len_of_each
        h.sort()

        self._right_border = np.mean(h) + np.std(h)

    def get_metric(self, data_row: pd.Series) -> float:
        code_data = re.search('<code>(.|\n)*?<\/code>', data_row['post_body'])

        if code_data != None:
            code_data = code_data.group(0)
        else:
            code_data = ''

        if(len(code_data) < self._right_border):
            return 0
        else:
            return 1

    def name(self):
        return self.name
