import numpy as np

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression


def createModel(imageShape, numClasses):
    print("Creating Network")

    convnet = input_data(shape=imageShape,name="input")

    convnet = conv_2d(convnet,32,3,activation='relu', weights_init="Xavier")
    convnet = max_pool_2d(convnet,3)

    convnet = conv_2d(convnet,64,3,activation='relu', weights_init="Xavier")
    convnet = max_pool_2d(convnet,3)

    convnet = conv_2d(convnet,128,3,activation='relu', weights_init="Xavier")
    convnet = max_pool_2d(convnet,3)

    convnet = conv_2d(convnet,256,3,activation='relu', weights_init="Xavier")
    convnet = max_pool_2d(convnet,3)

    convnet = fully_connected(convnet, 512, activation='relu')
    convnet = dropout(convnet, 0.2)

    convnet = fully_connected(convnet, numClasses, activation='softmax')
    convnet = regression(convnet, optimizer='rmsprop', loss='categorical_crossentropy')

    model = tflearn.DNN(convnet)
    print("Model Created 🎉")
    return model