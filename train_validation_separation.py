import numpy as np
import math
import pandas as pd

df = pd.read_csv('mappingTest_max254.csv', header=None)
data = df.as_matrix()

labels = [i for i in range(0,26)]

training = []
validation = []
for i,j in enumerate(labels):
    count = 0
    for k,l in enumerate(data):
        if l[0] == j:
            if count < 60:
                validation.append(l)
            else:
                training.append(l)
            count += 1

np.random.shuffle(training)
np.random.shuffle(validation)

training =  pd.DataFrame(training)
validation = pd.DataFrame(validation)

training.to_csv('training_max254.csv', encoding='utf-8', index=False, header=None)
validation.to_csv('validation_max254.csv', encoding='utf-8', index=False, header=None)

'''
X_train = pd.DataFrame(X_train)
y_train = pd.DataFrame(y_train)

result = pd.concat([y_train, X_train], axis=1)
result.to_csv('mappingtest.csv', encoding='utf-8', index=False, header=None)
'''
