import pandas as pd
import numpy as np
import sys

sys.path.append('src')
sys.path.append('src/features')

from feature import Feature
from features.miss_teg import MissTegFeature

class DataMiner:
    def __init__(self):
        self.features = list()
        z = MissTegFeature()
        self.features.append(MissTegFeature())

    def get_data(self, inp_data: pd.DataFrame) -> pd.DataFrame:
        rows_count = len(inp_data.index)
        names = [i.name for i in self.features]
        names.insert(0, 'id_post')
        out_data = pd.DataFrame(columns=names)

        for row in range(rows_count):
            for fea in self.features:
                out_data.loc[row, fea.name] = fea.get_metric(inp_data.loc[row])
                out_data.loc[row, 'id_post'] = inp_data.loc[row, 'id_post']
        return out_data
