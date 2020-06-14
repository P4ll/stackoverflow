import sys
import pandas as pd
import numpy as np
import keras
from keras import layers, models
import xgboost as xgb
import matplotlib
import matplotlib.pyplot as plt

from data_miner import DataMiner


class QTester:
    def __init__(self, dm: DataMiner = None):
        self._model = None
        if dm == None:
            self._data_miner = DataMiner(has_goal=False)

    def load_model(self, path: str, model_type: str) -> None:
        if model_type == 'nn':
            self._model = models.load_model(path)
        elif model_type == 'xgb':
            self._model = xgb.XGBClassifier.load_model(path)
        else:
            raise Exception("Unexpected model type, use nn or xgb")

    def get_res(self, data: pd.DataFrame):
        data = self._data_miner.get_data(data)
        predict = self._model.predict(data).tolist()
        ans = list()
        for p in predict:
            if len(p) == 1:
                ans.append(p)
            else:
                ans.append(np.argmax(p))
        return ans

if __name__ == "__main__":
    pass
