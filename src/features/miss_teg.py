import pandas as pd
import numpy as np
from feature import Feature

class MissTegFeature(Feature):
    def __init__(self):
        self.name = "miss_teg"

    def get_metric(self, data_row: pd.Series) -> float:
        return 1

    def name(self):
        return self.name