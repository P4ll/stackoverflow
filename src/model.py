import sys
import pandas as pd
import numpy as np
import keras as K

sys.path.append('src')
from data_miner import DataMiner


class Model:
    def __init__(self):
        self._data_miner = DataMiner()

    def train(self, dataset: pd.DataFrame):
        dataset = self._data_miner.get_data(dataset)

    def test(self):
        pass

    def load_weight(self):
        pass

    def get_res(self):
        pass

if __name__ == "__main__":
    pass