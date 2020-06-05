import pandas as pd
import numpy as np
import sys
import math

sys.path.append('src')
sys.path.append('src/features')

from feature import Feature
from features.miss_teg import MissTegFeature
from features.ans_count import AnsCount
from features.questions_count import QuestionsCount
from features.reached_people import ReachedPeople
from features.user_rating import UserRating

class DataMiner:
    def __init__(self):
        self.features = list()

        self.features.append(AnsCount())
        self.features.append(QuestionsCount())
        self.features.append(ReachedPeople())
        self.features.append(UserRating())

    def get_data(self, inp_data: pd.DataFrame) -> pd.DataFrame:
        rows_count = len(inp_data.index)
        names = [i.name for i in self.features]
        names.insert(0, 'id_post')
        names.insert(1, 'id_user')
        out_data = pd.DataFrame(columns=names)

        for row in range(rows_count):
            for fea in self.features:
                out_data.loc[row, fea.name] = fea.get_metric(inp_data.loc[row])
                out_data.loc[row, 'id_post'] = inp_data.loc[row, 'id_post']
                id_u = inp_data.loc[row, 'id_user']
                if not math.isnan(id_u):
                    out_data.loc[row, 'id_user'] = int(round(id_u))
                else:
                    out_data.loc[row, 'id_user'] = -1
        return out_data
