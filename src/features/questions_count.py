import pandas as pd
import numpy as np
from feature import IFeature


class QuestionsCount(IFeature):
    def __init__(self):
        self.name = "questions_count"

    def get_metric(self, data_row: pd.Series) -> float:
        return data_row.user_questions_count

    def name(self):
        return self.name
