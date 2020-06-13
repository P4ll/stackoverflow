import pandas as pd
import numpy as np
from feature import IFeature


class UserRating(IFeature):
    def __init__(self):
        self.name = "user_rating"

    def get_metric(self, data_row: pd.Series) -> float:
        return data_row.user_rating

    def name(self):
        return self.name
