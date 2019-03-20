# Create amd Load Datasets
# 
# Convert spectrograms into numpy arrays and
# pack them into single pickle dump files for
# each genre.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import pickle
from random import shuffle
import h5py
import cv2

from config import validation_ratio

# Load the image and return numpy data
def loadImage(filePath):
    #using OpenCV
    img = cv2.imread(filePath, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (500, 200), cv2.INTER_LINEAR)
    return img

# Function to create numpy array dataset
def createDataset(inpath,outpath):
    print("⌛ Creating Dataset")
    genres = os.listdir(inpath)
    images = []
    labels = []

    for genre in genres:
        filenames = os.listdir(os.path.join(inpath, genre))
        filenames = [filename for filename in filenames if filename.endswith('.png') ]
        shuffle(filenames)

        for filename in filenames:
            filePath = os.path.join(inpath,genre,filename)
            imgData = loadImage(filePath)
            imgData = imgData /255
            images.append(imgData)

            # Hot encoding of labels
            label = [1. if genre == g else 0. for g in genres]
            labels.append(label)
                
    # data split percentage
    validation = int(validation_ratio * len(images))
    training   = len(images) - validation

    # split data into training and vaildation sets
    train_x = np.array(images[:training])
    train_y = np.array(labels[:training])

    validation_x = np.array(images[-validation:])
    validation_y = np.array(labels[-validation:])
    
    # save the dataset to disk
    saveDataset(train_x,train_y,validation_x,validation_y,outpath)

# Function to save the dataset as h5 file
def saveDataset(train_x,train_y,validation_x,validation_y,path):
    print("⌛ Saving Dataset")

    # create directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    with h5py.File(os.path.join(path,"music_data.h5"),"w") as h5file :
        train = h5file.create_group("training_set")
        train.create_dataset("train_x",data=train_x)
        train.create_dataset("train_y",data=train_y)

        validation = h5file.create_group("validation_set")
        validation.create_dataset("validation_x",data=validation_x)
        validation.create_dataset("validation_y",data=validation_y)

    print("💾 Dataset Saved")


# Function to load the saved dataset to train
def loadDataset(path,mode="train"):
    if mode == "train":
        print("⌛ Loading Training and Validation set")
        
        with h5py.File(os.path.join(path,"music_data.h5"),"r") as h5file:
            training_set = h5file["training_set"]
            train_x = training_set["train_x"]
            train_y = training_set["train_y"]

            validation_set = h5file["validation_set"]
            validation_x = validation_set["validation_x"]
            validation_y = validation_set["validation_y"]
        
        print("✅ Dataset Loaded.")
        return train_x, train_y, validation_x, validation_y
    