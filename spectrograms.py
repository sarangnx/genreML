# Slice audio into 100ms windows and
# create spectrograms.

import subprocess
import os
import re
import matplotlib
import pylab
import librosa
import librosa.display
import glob
import time
import numpy as np
import config


# Function to crop 30 seconds out of songs
# inpath - path to raw files directory
# outpath - path to slices directory
def cropSongs(inpath,outpath):
    files = os.listdir(inpath)
    files = [file for file in files if file.endswith(".mp3")]

    for file in files:
        infile = os.path.join(inpath,file)
        outfile = os.path.join(outpath,file)

        if not os.path.isdir(outpath):
            # If genre folder doesn't exist create one.
            os.makedirs(outpath)
        
        cmd = "ffmpeg -ss 10 -t 30 -i \"{}\" -c copy \"{}\"".format(infile,outfile)
        subprocess.call(cmd,shell=True)

def sliceSongs(inpath,outpath):
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
        
        cmd = "ffmpeg -i \"{}\" -f segment -segment_time 0.1 -c copy \"{}%03d.mp3\"".format(infile,outfile)
        subprocess.call(cmd,shell=True)


# def covertToSpectrogram(inpath,outpath):
#     pylab.axis('off')
#     pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])

#     S = librosa.feature.melspectrogram(y=sig, sr=fs)
#     librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
#     pylab.savefig(outpath, bbox_inches=None, pad_inches=0)
#     pylab.close()



# for song in glob.glob(os.path.join(path,'*.mp3')) :

    
#     sig, fs = librosa.load(song, mono=True) 
#     plot()
#     count+=1

# for genre in os.listdir(config.rawDataPath):
#     infolder = os.path.join(config.rawDataPath,genre)
#     outfolder = os.path.join(config.cropPath,genre)
#     cropSongs(infolder,outfolder)


# for genre in os.listdir(config.cropPath):
#     infolder = os.path.join(config.cropPath,genre)
#     outfolder = os.path.join(config.slicesPath,genre)
#     sliceSongs(infolder,outfolder)