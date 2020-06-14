import numpy as np
import pandas as pd


class ModelTrainer:
    def __init__(self):
        self._model = None

    def train(self, data: pd.DataFrame, dm: DataMiner = None):
        pass

    def select_model(self, std_mod: str = 'xgb', model=None):
        pass

    def validate(self, val_data: pd.DataFrame):
        pass
