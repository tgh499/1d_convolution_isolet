import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random

features = [i for i in range(1,618)]

test = pd.read_csv('validation.csv', header=None)
label_train = test.columns[0]

y_train = test[label_train]
y_train = y_train.as_matrix()

print(features)
print(features)

X_train = test[features]
X_train = X_train.as_matrix()


y_fm = []

for i in y_train:
    y_fm.append([int(i)])

y_fm = pd.DataFrame(y_fm)
X_train = pd.DataFrame(X_train)

frames = [y_fm, X_train]
result = pd.concat([y_fm, X_train], axis=1)

result.to_csv('validation_original.csv', encoding='utf-8', index=False, header=None)

test = pd.read_csv('training.csv', header=None)
label_train = test.columns[0]

y_train = test[label_train]
y_train = y_train.as_matrix()


X_train = test[features]
X_train = X_train.as_matrix()


y_fm = []

for i in y_train:
    y_fm.append([int(i)])

y_fm = pd.DataFrame(y_fm)
X_train = pd.DataFrame(X_train)

frames = [y_fm, X_train]
result = pd.concat([y_fm, X_train], axis=1)

result.to_csv('training_original.csv', encoding='utf-8', index=False, header=None)


test = pd.read_csv('test.csv', header=None)

label_train = test.columns[0]

y_train = test[label_train]
y_train = y_train.as_matrix()


X_train = test[features]
X_train = X_train.as_matrix()


y_fm = []

for i in y_train:
    y_fm.append([int(i)])

y_fm = pd.DataFrame(y_fm)
X_train = pd.DataFrame(X_train)

frames = [y_fm, X_train]
result = pd.concat([y_fm, X_train], axis=1)

result.to_csv('test_original.csv', encoding='utf-8', index=False, header=None)
'''

sample_index = 119
C = []
X = []
Y = []
for i in mapping:
    X.append(i[0])
    Y.append(i[1])
for i in X_train[sample_index]:
    C.append(i)

plt.scatter(X, Y, c = C, cmap='gray')
plt.show()
'''
