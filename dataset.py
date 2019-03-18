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

from config import validation_ratio

# Load the image and return numpy data
def loadImage(filePath):
    img = Image.open(filePath)
    img = img.resize((500,200), resample=Image.ANTIALIAS)
    imgData = np.asarray(img, dtype=np.uint8) / 255.
    # Remove Alpha Channel
    imgData = imgData[:,:,:3]
    img.close()
    return imgData

# Function to create numpy array dataset
def createDataset(inpath,outpath):
    data = []
    genres = os.listdir(inpath)

    for genre in genres:
        filenames = os.listdir(os.path.join(inpath, genre))
        filenames = [filename for filename in filenames if filename.endswith('.png') ]
        shuffle(filenames)

        for filename in filenames:
            filePath = os.path.join(inpath,genre,filename)
            imgData = loadImage(filePath)
            label = [1. if genre == g else 0. for g in genres]
            data.append((imgData,label))

    shuffle(data)

    # unzip data from iterator
    x,y = zip(*data)
    
    # data split percentage
    validation = int(validation_ratio * len(x))
    training   = len(x) - validation

    # split data 
    train_x = np.array(x[:training])
    train_y = np.array(y[:training])
    
    validation_x = np.array(x[-validation:])
    validation_y = np.array(y[-validation:])
    
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