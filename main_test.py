import qtester
import matplotlib.pyplot as plt  # doctest: +SKIP
import pandas as pd
from sklearn.metrics import plot_confusion_matrix

from qtester.model import NNModel, XGBModel

df = pd.read_csv('text3.csv')
df[:100]
y_test = df.post_type
df = df.drop(['post_type', 'id_post', 'id_user'], axis=1)

model = XGBModel()

model.load('xgb_tmp.ser')

plot_confusion_matrix(model, df, y_test)  # doctest: +SKIP
plt.show()  # doctest: +SKIP
