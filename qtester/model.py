import pandas as pd
import numpy as np
from abc import ABC, abstractmethod, abstractproperty, ABCMeta
from typing import Dict, List

import keras
from keras.models import Sequential
from keras.optimizers import SGD, RMSprop, Adam
from keras.layers import Dense, Activation, Dropout, Flatten

from sklearn.metrics import average_precision_score, mean_squared_error, roc_curve, auc, accuracy_score, classification_report
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split, KFold

from sklearn.linear_model import LogisticRegression

import xgboost as xgb

from qtester.libs.data_preprocessing import *


class IClassModel():
    __metaclass__ = ABCMeta

    @abstractproperty
    def code_name(self):
        """Get name of feature"""

    @abstractmethod
    def train(self, *args, **kwargs):
        """Train model"""

    @abstractmethod
    def predict(self, *args, **kwargs):
        """Predict"""

    @abstractmethod
    def save(self, *args, **kwargs):
        """Save model data"""

    @abstractmethod
    def load(self, *args, **kwargs):
        """Load model data"""


class NNModel(IClassModel):
    def __init__(self):
        self.model = Sequential()

    def train(self, data: pd.DataFrame):
        data['title_overlap'] = get_norms(data['title_overlap'])
        data['ans_count'] = get_norms(data['ans_count'])
        data['questions_count'] = get_norms(data['questions_count'])
        data['reached_people'] = get_norms(data['reached_people'])
        data['user_rating'] = get_norms(data['user_rating'])

        data = data.drop(['id_post', 'id_user'], axis=1)

        train_data, test_data = data_divider(data)
        x_train = train_data.drop('post_type', axis=1)
        y_train = train_data['post_type']
        x_test = test_data.drop('post_type', axis=1)
        y_test = test_data['post_type']

        self.model.add(Dense(output_dim=200, init='uniform',
                             activation='relu', input_dim=x_train.shape[1]))
        self.model.add(Dropout(0.2, noise_shape=None, seed=None))

        self.model.add(
            Dense(output_dim=180, init='uniform', activation='relu'))
        self.model.add(Dropout(0.2, noise_shape=None, seed=None))

        self.model.add(
            Dense(output_dim=100, init='uniform', activation='relu'))
        self.model.add(Dropout(0.3, noise_shape=None, seed=None))

        self.model.add(Dense(output_dim=30, init='uniform', activation='relu'))
        self.model.add(Dropout(0.4, noise_shape=None, seed=None))

        self.model.add(Dense(output_dim=15, init='uniform', activation='relu'))
        self.model.add(Dropout(0.2, noise_shape=None, seed=None))

        self.model.add(Dense(output_dim=10, init='uniform', activation='relu'))
        self.model.add(Dropout(0.2, noise_shape=None, seed=None))

        self.model.add(Dense(output_dim=5, init='uniform', activation='relu'))
        self.model.add(Dropout(0.2, noise_shape=None, seed=None))

        self.model.add(
            Dense(output_dim=3, init='uniform', activation='sigmoid'))
        self.model.compile(
            optimizer='rmsprop', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        history = self.model.fit(
            x_train, y_train, validation_split=0.2, batch_size=128, nb_epoch=50)

    def predict(self, data) -> List:
        prediction = self.model.predict(data).tolist()
        res = np.argmax(prediction, axis=1)
        return res

    def save(self, path: str):
        self.model.save(path)

    def load(self, path):
        self.model = keras.models.load_model(path)


class XGBModel(IClassModel):
    def __init__(self):
        self.model = xgb.XGBClassifier()

    def train(self, data: pd.DataFrame):
        data['title_overlap'] = get_norms(data['title_overlap'])
        data['ans_count'] = get_norms(data['ans_count'])
        data['questions_count'] = get_norms(data['questions_count'])
        data['reached_people'] = get_norms(data['reached_people'])
        data['user_rating'] = get_norms(data['user_rating'])

        data = data.drop(['id_post', 'id_user'], axis=1)

        train_data, test_data = data_divider(data)
        x_train = train_data.drop('post_type', axis=1)
        y_train = train_data['post_type']
        x_test = test_data.drop('post_type', axis=1)
        y_test = test_data['post_type']
        self.model.fit(x_train, y_train)

    def predict(self, data) -> List:
        res = self.model.predict(data).tolist()
        return res

    def save(self, path: str):
        self.model.save_model(path)

    def load(self, path):
        xgb.XGBRFClassifier.load_model(self.model, path)