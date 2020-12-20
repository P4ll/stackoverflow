import qtester
import matplotlib.pyplot as plt  # doctest: +SKIP
import pandas as pd
from sklearn.metrics import plot_confusion_matrix

from qtester.model import NNModel, XGBModel
import numpy as np

import time

df = pd.read_csv('text3.csv')
df[:100]
y_test = df.post_type
df = df.drop(['post_type', 'id_post', 'id_user'], axis=1)

model = XGBModel()
model_nn = NNModel()

model.load('xgb_tmp.ser')
# model_nn.load('model_tmp2.ser')

time_nn = list()
time_xgb = list()

max_len = len(df.index)
for row in range(max_len):
    # bt = time.time_ns() / (10 ** 3)
    # res = model_nn.predict(np.array(df.loc[row]).reshape(1, 306))
    # et = bt - (time.time_ns() / (10 ** 3))
    # time_nn.append(et)
    z = np.array(df.loc[row]).reshape(1, 306)
    bt = time.time_ns() / (10 ** 3)
    res = model.predict(z)
    et = (time.time_ns() / (10 ** 3)) - bt
    time_xgb.append(et)

print(f"xgb avg: {np.average(time_xgb)}, min: {np.min(time_xgb)}")
# print(f"nn avg: {np.average(time_nn)}, min: {np.min(time_nn)}")

# plot_confusion_matrix(model, df, y_test)  # doctest: +SKIP
# plt.show()  # doctest: +SKIP
