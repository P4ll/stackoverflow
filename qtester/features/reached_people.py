import pandas as pd
import numpy as np
from qtester.feature import IFeature


class ReachedPeople(IFeature):
    def __init__(self):
        self.name = "reached_people"

    def get_metric(self, data_row: pd.Series) -> float:
        return data_row.user_reached_people

    def name(self):
        return self.name
