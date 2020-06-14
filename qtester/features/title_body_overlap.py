import pandas as pd
import numpy as np

from qtester.feature import IFeature
from qtester.libs.my_paths import base_model
from qtester.libs.text_processing import TextProcessor


class TitleBodyOverlap(IFeature):
    def __init__(self):
        self.name = "title_overlap"
        self._text_proc = TextProcessor()

    def get_metric(self, data_row: pd.Series) -> float:
        return self._text_proc.title_body_sim(data_row['post_title'], data_row['post_body'])

    def name(self):
        return self.name
