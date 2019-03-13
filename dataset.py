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

from config import datasetPath
from config import spectrograms

def loadImage(filePath):
    img = Image.open(filePath)
    imgData = np.asarray(img) / 255.
    return imgData

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

    print(type(data))