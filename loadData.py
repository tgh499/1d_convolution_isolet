import numpy as np
import math
import pandas as pd

train = pd.read_csv('testData.csv', header=None)
train = train.as_matrix()
np.random.shuffle(train)
train = pd.DataFrame(train)
features_train = train.columns[range(0,617)]
label_train = train.columns[617]

X_train = train[features_train]
z_train = train[label_train]
X_train = X_train.as_matrix()
z_train = z_train.as_matrix()

y_train = []

for i in z_train:
    y_train.append(int(i-1))


for i,j in enumerate(X_train):
    for k,l in enumerate(j):
        X_train[i][k] = (l + 1) * 127

X_train = pd.DataFrame(X_train)
y_train = pd.DataFrame(y_train)

result = pd.concat([y_train, X_train], axis=1)
result.to_csv('test_max254.csv', encoding='utf-8', index=False, header=None)
