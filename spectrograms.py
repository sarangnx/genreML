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


def cropSongs(inpath,outpath):
    files = os.listdir(inpath)
    files = [file for file in files if file.endswith(".mp3")]

    for file in files:
        cmd = "ffmpeg -ss 10 -t 30 -i {} -c copy {}".format(file,outpath + file)
        subprocess.call(cmd,shell=True)


def sliceSongs(inpath,outpath):
    files = os.listdir(inpath)
    files = [file for file in files if file.endswith(".mp3")]

    for file in files:
        name = re.sub(".mp3","",file)
        name = re.sub(" ","_",name)
        
        cmd = "ffmpeg -i \"{}\" -f segment -segment_time 0.1 -c copy {}%03d.mp3".format(file,outpath + name)
        subprocess.call(cmd,shell=True)


def covertToSpectrogram(inpath,outpath):
    pylab.axis('off')
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])

    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    pylab.savefig(outpath, bbox_inches=None, pad_inches=0)
    pylab.close()



path = '/home/midhun/Documents/Project/pgms/v2/sample/' #<--where the splitted songs are stored
count = 0
def plot() :
    save_path = str(count)+'.png'
    pylab.axis('off')

    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])

    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    pylab.savefig(save_path, bbox_inches=None, pad_inches=0)
    pylab.close()



for song in glob.glob(os.path.join(path,'*.mp3')) :

    
    sig, fs = librosa.load(song, mono=True) 
    plot()
    count+=1
