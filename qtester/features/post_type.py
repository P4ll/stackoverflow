import pandas as pd
import numpy as np
from feature import IFeature


class PostType(IFeature):
    def __init__(self):
        self.name = "post_type"
        self.mode = super().work_mode

    def get_metric(self, data_row: pd.Series) -> float:
        return data_row['type']

    def name(self):
        return self.name

    def mode(self):
        return self.mode