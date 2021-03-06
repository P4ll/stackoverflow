import pandas as pd
import numpy as np
import sys
import math
sys.path.append('qtester')
from feature import IFeature
from features.miss_teg import MissTegFeature
from features.ans_count import AnsCount
from features.questions_count import QuestionsCount
from features.reached_people import ReachedPeople
from features.user_rating import UserRating
from features.debug_information import UnnecessaryInformation
from features.title_body_overlap import TitleBodyOverlap
from features.lda_distr import LdaDistr
from features.post_type import PostType
from libs.my_paths import base_optimal_data
from libs.my_progress_bar import MyBar

class DataMiner:
    def __init__(self, fea_list: IFeature = None, has_goal: bool = True):
        self.features = list()

        if (fea_list != None):
            for fea in fea_list:
                self.features.append(fea)
        else:
            self.features.append(AnsCount())
            self.features.append(QuestionsCount())
            self.features.append(ReachedPeople())
            self.features.append(UserRating())
            self.features.append(UnnecessaryInformation())
            self.features.append(TitleBodyOverlap())
            self.features.append(LdaDistr())

            if has_goal:
                self.features.append(PostType())

    def get_data(self, inp_data: pd.DataFrame, test_mod: bool=False) -> pd.DataFrame:
        rows_count = len(inp_data.index)
        names = [i.name for i in self.features]
        names.insert(0, 'id_post')
        names.insert(1, 'id_user')
        out_data = pd.DataFrame(columns=names)

        dbg_inf_model = list(filter(lambda x: x.name == "debug_inf", self.features))[0]
        dbg_inf_model.train(inp_data)

        if test_mod:
            rows_count = min(500, rows_count)

        bar = MyBar('Data handling.. ', max=rows_count)

        for row in range(rows_count):
            for fea in self.features:
                if fea.mode == "scalar":
                    out_data.loc[row, fea.name] = fea.get_metric(inp_data.loc[row])
                else:
                    out_vector = fea.get_metric(inp_data.loc[row])
                    for v in out_vector:
                        out_data.loc[row, v[0]] = v[1]
                out_data.loc[row, 'id_post'] = inp_data.loc[row, 'id_post']

            id_u = inp_data.loc[row, 'id_user']
            if not math.isnan(id_u):
                out_data.loc[row, 'id_user'] = int(round(id_u))
            else:
                out_data.loc[row, 'id_user'] = -1
            bar.next()

        bar.finish()
        return out_data


if __name__ == "__main__":
    dm = DataMiner()
    # data = dm.get_data(pd.read_csv(base_optimal_data))
    # data.to_csv('text.csv', index=False)
    data = dm.get_data(pd.read_csv('dataset/optimal_data2.csv'), True)
    data.to_csv('ttt.csv', index=False)