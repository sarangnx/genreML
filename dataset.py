# Create amd Load Datasets
# 
# Convert spectrograms into numpy arrays and
# pack them into single pickle dump files for
# each genre.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from PIL import Image
import numpy as np
import pickle
from random import shuffle
import h5py
import cv2

from config import validation_ratio

# Load the image and return numpy data
# @profile
def loadImage(filePath):
    # img = Image.open(filePath)
    # img = img.resize((500,200), resample=Image.ANTIALIAS)
   
    # imgData = np.asarray(img, dtype=np.uint8) / 255.
    # Remove Alpha Channel
    # imgData = imgData[:,:,:3]
    # img.close()
    # return imgData
    
    #using OpenCV
    img = cv2.imread(filePath, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (500, 200), cv2.INTER_LINEAR)
    return img

# Function to create numpy array dataset
# @profile
def createDataset(inpath,outpath):

    genres = os.listdir(inpath)
    # h5file = h5py.File(outpath+"/music_data.h5","a")
    images = []
    labels = []

    for genre in genres:
        filenames = os.listdir(os.path.join(inpath, genre))
        filenames = [filename for filename in filenames if filename.endswith('.png') ]
        shuffle(filenames)

        for filename in filenames:
            filePath = os.path.join(inpath,genre,filename)
            imgData = loadImage(filePath)
            label = [1. if genre == g else 0. for g in genres]
            # data.append((imgData,label))
            images.append(imgData)
            labels.append(label)
    

    # images = np.array(images, dtype=np.uint8) / 255
    # npimages = []
    # for image in images:
    #     image = np.array(image, dtype=np.uint8) / 255
    #     npimages.append(image)
    images = np.array(images)
    labels = np.array(labels)
    
    # data split percentage
    validation = int(validation_ratio * len(images))
    training   = len(images) - validation

    # split data 
    train_x = np.array(images[:training])
    train_y = np.array(labels[:training])

    validation_x = np.array(images[-validation:])
    validation_y = np.array(labels[-validation:])
    
    saveDataset(train_x,train_y,validation_x,validation_y,outpath)

# Function to save the dataset as pickle file
def saveDataset(train_x,train_y,validation_x,validation_y,path):
    # create directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    pickle.dump( train_x, open( os.path.join(path,"train_x.p") ,"wb" ))
    pickle.dump( train_y, open( os.path.join(path,"train_y.p") ,"wb" ))
    pickle.dump( validation_x, open( os.path.join(path,"validation_x.p") ,"wb" ))
    pickle.dump( validation_y, open( os.path.join(path,"validation_y.p") ,"wb" ))
    print("Dataset Saved")


# Function to load the saved dataset to train
def loadDataset(path,mode="train"):
    if mode == "train":
        print("⌛ Loading Training and Validation set")
        
        train_x = pickle.load(open( os.path.join(path,"train_x.p"), "rb" ))
        train_y = pickle.load(open( os.path.join(path,"train_y.p"), "rb" ))
        validation_x = pickle.load(open( os.path.join(path,"validation_x.p"), "rb" ))
        validation_y = pickle.load(open( os.path.join(path,"validation_y.p"), "rb" ))
        
        print("✅ Dataset Loaded.")
        return train_x, train_y, validation_x, validation_y
    
# import config
# createDataset(config.spectrograms,config.datasetPath)