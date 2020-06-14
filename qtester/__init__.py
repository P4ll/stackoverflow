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
    def __init__(self):
        self._model = None

    def load_model(self, path: str, model_type: str) -> None:
        if model_type == 'nn':
            self._model = models.load_model(path)
        elif model_type == 'xgb':
            self._model = xgb.XGBClassifier.load_model(path)
            pass
        else:
            raise Exception("Unexpected model type, use nn or xgb")

    def get_res(self, data: pd.DataFrame):
        pass


if __name__ == "__main__":
    pass
