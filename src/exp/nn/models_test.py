#!/usr/bin/env python
# coding: utf-8

# In[1]:

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import sklearn as skl

from keras.models import Sequential
from keras.optimizers import SGD, RMSprop, Adam
from keras.layers import Dense, Activation, Dropout, Flatten

from sklearn.metrics import average_precision_score, mean_squared_error, roc_curve, auc, accuracy_score, classification_report
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split, KFold

from sklearn.linear_model import LogisticRegression

import xgboost as xgb

from keras.utils import plot_model
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

base_path = "d:/work/stackoverflow/"
base_path_nn = base_path + "exp/nn/"


# In[2]:




# In[3]:


def data_divider(data, per=0.8, shuffle=True):
    if shuffle:
        data = data.sample(frac=1).reset_index(drop=True)
    rr = round(len(data.index) * per)
    return data[:rr], data[rr:]

def get_norms(ser):
    return normalize(ser[:,np.newaxis], axis=0).ravel()
    #return [[i] for i in normalize(ser[:,np.newaxis], axis=0).ravel()]


# In[4]:


data = pd.read_csv(base_path + 'text3.csv')
data = data

#data['lda'] = [[float(b) for b in a.strip('[]').split(', ')] for a in data['lda']]
#data['lda'] = data['lda'].tolist()

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

data[:5]


# In[5]:


classifier = Sequential()

#classifier.add(Flatten(output_dim = 7, init = 'uniform', activation = 'relu', input_shape=(7, )))
classifier.add(Dense(output_dim = 300, init = 'uniform', activation = 'relu', input_dim = x_train.shape[1]))
classifier.add(Dropout(0.2, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 300, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.3, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 180, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.2, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 100, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.3, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 30, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.4, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 15, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.2, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 10, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.2, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 5, init = 'uniform', activation = 'relu'))
classifier.add(Dropout(0.2, noise_shape=None, seed=None))

classifier.add(Dense(output_dim = 3, init = 'uniform', activation = 'sigmoid'))
classifier.compile(optimizer = 'rmsprop', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])


# In[6]:


classifier.summary()

history = classifier.fit(x_train, y_train, validation_split=0.2, batch_size = 128, nb_epoch = 80)

classifier.save("model_tmp2.ser")


# In[ ]:


def res_eval(goal, res):
    #eval_res(res, y_test, history)
    print('classification report')
    print(classification_report(goal, res))
    print('confusion matrix')
    print(skl.metrics.confusion_matrix(goal, res))
    f1_score = skl.metrics.f1_score(y_test, np.argmax(prediction, axis=1), average="micro")
    print('F1 score: {}'.format(f1_score))
    
    fpr, tpr, thresholds = roc_curve(y_test, res, pos_label=2)
    au_curve = auc(fpr, tpr)

    plt.figure(3)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr, tpr, label='area = {:.3f}'.format(au_curve))
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.show()


# In[ ]:


prediction = classifier.predict(x_test).tolist()
plot_model(classifier, to_file="model2.png")

res = np.argmax(prediction, axis=1)

res_eval(y_test, res)
        
_, train_acc = classifier.evaluate(x_train, y_train, verbose=0)
_, test_acc = classifier.evaluate(x_test, y_test, verbose=0)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

plt.figure(1)
#plt.subplot(211)
plt.title('Loss')
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()

plt.figure(2)
#plt.subplot(212)
plt.title('Accuracy')
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='test')
plt.legend()
plt.show()


# In[ ]:


# model = xgb.XGBClassifier()
# model.fit(x_train, y_train)
# res = model.predict(x_test)
# res_eval(y_test, res)


# In[ ]:




