import pandas as pd
import numpy as np
from feature import IFeature


class AnsCount(IFeature):
    def __init__(self):
        self.name = "ans_count"
        self.mode = super().work_mode

    def get_metric(self, data_row: pd.Series) -> float:
        return data_row.user_ans_count

    def name(self):
        return self.name

    def mode(self):
        return self.mode