# Slice audio into 100ms windows and
# create spectrograms.

import subprocess
import os
import re
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import config


# Function to crop 90 seconds out of songs
# inpath - path to raw files directory
# outpath - path to cropped directory
def _cropSongs(inpath,outpath):
    files = os.listdir(inpath)
    files = [file for file in files if file.endswith(".mp3")]

    for file in files:
        infile = os.path.join(inpath,file)
        outfile = os.path.join(outpath,file)

        if not os.path.isdir(outpath):
            # If genre folder doesn't exist create one.
            os.makedirs(outpath)
        # crop the song to 90 seconds
        cmd = "ffmpeg -y -t 90 -i \"{}\" -map 0:a -c copy  -map_metadata -1 \"{}\"".format(infile,outfile)
        subprocess.call(cmd,shell=True)


# Slice the songs to 30s windows
# inpath - path to cropped files directory
# outpath - path to slices directory
def _sliceSongs(inpath,outpath):
    files = os.listdir(inpath)
    files = [file for file in files if file.endswith(".mp3")]

    for file in files:
        infile = os.path.join(inpath,file)

        name = re.sub(".mp3","",file)
        name = re.sub(" ","_",name)

        outfile = os.path.join(outpath,name)

        if not os.path.isdir(outpath):
            # If genre folder doesn't exist create one.
            os.makedirs(outpath)
        
        # Command to create segments of duration 10s
        cmd = "ffmpeg -y -i \"{}\" -f segment -segment_time 30 -c copy \"{}%03d.mp3\"".format(infile,outfile)
        subprocess.call(cmd,shell=True)


# This is the method that should be called to 
# crop the songs directly taking the input from
# "rawDataPath"
def crop():
    for genre in os.listdir(config.rawDataPath):
        infolder = os.path.join(config.rawDataPath,genre)
        outfolder = os.path.join(config.cropPath,genre)
        _cropSongs(infolder,outfolder)

# This is the method that should be called to 
# segment/slice the songs directly taking the input from
# "croppedPath"
def segment():
    for genre in os.listdir(config.cropPath):
        infolder = os.path.join(config.cropPath,genre)
        outfolder = os.path.join(config.slicesPath,genre)
        _sliceSongs(infolder,outfolder)
        _cleanup(outfolder)


# Convert segments into spectrograms
def _convertToSpectrogram(inpath,outpath):

    files = os.listdir(inpath)
    files = [file for file in files if file.endswith(".mp3")]

    for song in files:
        plt.figure(figsize=[10,4],frameon=False)
        plt.axis("off")
        plt.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
        
        songfile = os.path.join(inpath,song)
        sig, fs = librosa.load(songfile, mono=True)
        S = librosa.feature.melspectrogram(y=sig, sr=fs)
        librosa.display.specshow(librosa.power_to_db(S, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')

        name = re.sub(".mp3",".png",song)
        outfile = os.path.join(outpath,name)

        if not os.path.isdir(outpath):
            # If genre folder doesn't exist create one.
            os.makedirs(outpath)
        plt.savefig(outfile, bbox_inches=None, pad_inches=0,frameon=None)
        plt.close()
        


# This is the method that should be called to 
# create spectrograms from the segments
def createSpectrogram():
    for genre in os.listdir(config.slicesPath):
        infolder = os.path.join(config.slicesPath,genre)
        outfolder = os.path.join(config.spectrograms,genre)
        _convertToSpectrogram(infolder,outfolder)


# Unwanted 4th file is created for some songs
# Files having only <1kb of size, and ends with 3.mp3
def _cleanup(path):
    files = [ file for file in os.listdir(path) if file.endswith("3.mp3")]
    for file in files:
        os.remove(os.path.join(path,file))