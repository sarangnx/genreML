from model import createModel
import dataset as ds
import spectrograms as sp

from config import datasetPath
from config import spectrograms

import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("mode", nargs="+",
        choices=["crop","segment","spectrogram",
            "dataset","train"])
args = parser.parse_args()

if "crop" in args.mode:
    sp.crop()
    sys.exit()

if "segment" in args.mode:
    sp.segment()
    sys.exit()

if "spectrogram" in args.mode:
    sp.createSpectrogram()
    sys.exit()

if "dataset" in args.mode:
    ds.createDataset(spectrograms,datasetPath)
    sys.exit()


# List the genres and count
genres = [ genre for genre in  os.listdir(spectrograms)
            if os.path.isdir(os.path.join(spectrograms,genre)) ]
genreNum = len(genres)

# Create Model
# model = createModel(genres,genreNum)

# if "train" in args.mode:
    # train()