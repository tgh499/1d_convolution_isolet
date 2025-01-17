#!/usr/bin/env python

import numpy as np
import pandas as pd
import random
import tensorflow as tf

# the behavior of the architecture can be controlled by the following
suffix = ""
var = 10
layer_1 = 50
layer_2 = 50
fc_layer = 300
lrn_rate = 9e-05
sample_size = 4678
f1_row = 1
f1_column = 10
f2_row = 1
f2_column = 10
train_fileName = "training_original.csv"
test_fileName = "validation_original.csv"

print(test_fileName)
# reading and splitting dataset by training samples and labels
print("CNN with 2 convolution layers, Isolet dataset. Sample size: " +
        str(sample_size) + " " +  str(layer_1) + " " +  str(layer_2)
        + " "+  str(fc_layer)+ " " + str(lrn_rate) + " " + str(f1_row) + " "
            + str(f1_column) + " " + str(f2_row) + " " + str(f2_column))
pd_train = pd.read_csv(train_fileName, header=None)
pd_test = pd.read_csv(test_fileName, header=None)

#extract the labels of the samples
cols = [0]
label_train_temp = pd_train.as_matrix(pd_train.columns[cols])
label_test = pd_test.as_matrix(pd_test.columns[cols])

# drop the labels; only the training data remain
pd_train = pd_train.drop(pd_train.columns[cols], axis=1)
pd_test = pd_test.drop(pd_test.columns[cols], axis = 1)
data_train_temp = pd_train.as_matrix(columns = pd_train.columns)
data_test = pd_test.as_matrix(columns = pd_test.columns)

# shuffling the samples so that a different set of the given size is picked
# in each run. The number of samples will be chosen by the sample_size
randIDs = np.arange(0 , sample_size)
np.random.shuffle(randIDs)
randIDs = randIDs[:sample_size]
data_train = [data_train_temp[ i] for i in randIDs]
label_train = [label_train_temp[ i] for i in randIDs]

# creates a one_hot vector for the given digit
def one_hot(i):
    a = np.zeros(26, 'uint16')
    a[i] = 1
    return (a)

# sends a set of random samples (stochastic batch)
def next_batch(num, data, labels):
    randIDs = np.arange(0 , len(data))
    np.random.shuffle(randIDs)
    randIDs = randIDs[:num]
    data_shuffle = [data[ i] for i in randIDs]
    labels_shuffle = [labels[ i] for i in randIDs]
    for i,j in enumerate(labels_shuffle):
        labels_shuffle[i] = one_hot(j)
    batch = []
    batch.append(np.asfarray(data_shuffle))
    batch.append(np.asfarray(labels_shuffle))
    return(batch)

# same as next_batch, except IDs are not suffled
def next_batch_test(num, data, labels):
    randIDs = np.arange(0 , len(data))
    randIDs = randIDs[:num]
    data_shuffle = [data[ i] for i in randIDs]
    labels_shuffle = [labels[ i] for i in randIDs]
    for i,j in enumerate(labels_shuffle):
        labels_shuffle[i] = one_hot(j)
    batch = []
    batch.append(np.asfarray(data_shuffle))
    batch.append(np.asfarray(labels_shuffle))
    return(batch)

# the convolution operation. uses 2d convolution for 4d input
def convolution(X, W):
    return(tf.nn.conv2d(X, W, strides=[1,1,1,1], padding='SAME'))

# max_pool downsamples by 2. 28x28 image will become 14x14 and so on.
def pooling(X):
    return(tf.nn.max_pool(X, ksize=[1,1,2,1], strides=[1,1,2,1],
                                    padding='SAME'))

# initialize random weights and biases
# Note to self- do some experiments for the following
def initWeights(shape):
    return(tf.Variable(tf.truncated_normal(shape, stddev=0.1)))
def initBiases(shape):
    return(tf.Variable(tf.constant(0.1, shape=shape)))

# the neural network graph
# Note to self- try adding another convolution layer
def nnGraph(X):
    X_2d = tf.reshape(X, [-1, 1, 617, 1])
    #pool01 = pooling(X_2d)

    # first convolution layer
    W_1 = initWeights([f1_row,f1_column,1,layer_1])
    b_1 = initBiases([layer_1])
    cnv_1 = tf.nn.relu(convolution(X_2d, W_1) + b_1)
    #pool_1 = pooling(cnv_1)

    # second convolution layer
    W_2 = initWeights([f2_row,f2_column,layer_1, layer_2])
    b_2 = initBiases([layer_2])
    cnv_2 = tf.nn.relu(convolution(cnv_1, W_2) + b_2)
    #pool_2 = pooling(cnv_2)

    # fully connected layer
    W_fcl_1 = initWeights([617*layer_2, fc_layer])
    b_fcl_1 = initBiases([fc_layer])
    image_to_flat = tf.reshape(cnv_2, [-1, 617*layer_2])
    fcl_output = tf.nn.relu(tf.matmul(image_to_flat, W_fcl_1) + b_fcl_1)

    # apply dropout
    drop_prb = tf.placeholder(tf.float32)
    fcl_af_drop = tf.nn.dropout(fcl_output, drop_prb)

    # map to 10 classes
    W_fcl_2 = initWeights([fc_layer, 26])
    b_fcl_2 = initBiases([26])
    y_af_conv = tf.matmul(fcl_af_drop, W_fcl_2) + b_fcl_2
    return(y_af_conv, drop_prb)

def main(_):
    X = tf.placeholder(tf.float32, [None, 617])
    y_actual = tf.placeholder(tf.float32, [None, 26])
    y_af_conv, drop_prb = nnGraph(X)

    # apply softmax
    sftmax = tf.nn.softmax_cross_entropy_with_logits(labels=y_actual,
                                                        logits=y_af_conv)
    cross_entropy = tf.reduce_mean(sftmax)
    training = tf.train.AdamOptimizer(lrn_rate).minimize(cross_entropy)

    predict = tf.equal(tf.argmax(y_af_conv, 1), tf.argmax(y_actual, 1))
    cast_predict = tf.cast(predict, tf.float32)
    accuracy = tf.reduce_mean(cast_predict)

    # training iterations
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        batch_test = next_batch_test(1560, data_test, label_test)
        for i in range(30000):
            batch = next_batch(50, data_train, label_train)
            if i % 100 == 0:
                train_accuracy = accuracy.eval(feed_dict={X: batch[0],
                y_actual: batch[1], drop_prb: 1.0})
            training.run(feed_dict={X: batch[0], y_actual: batch[1],
                        drop_prb: 0.5})

        print('test accuracy %g' % accuracy.eval(feed_dict={X: batch_test[0],
                y_actual: batch_test[1], drop_prb: 1.0}))


if __name__ == '__main__':
	tf.app.run(main=main)
