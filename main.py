from model import createModel
import dataset as ds
import spectrograms as sp

from config import datasetPath
from config import spectrograms
from config import epoch

import argparse
import sys
import os
import time

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
model = createModel([None,500,200,3],genreNum)

if "train" in args.mode:
    
    # Load Dataset
    train_x, train_y, validation_x, validation_y = ds.loadDataset(datasetPath)

    run_id = "Genre-" + time.time()
    
    # Training the model
    print("🏋 Training Model!")
    model.fit(train_x, train_y, n_epoch=epoch, batch_size=None, shuffle=True, 
        validation_set=(validation_x, validation_y), 
        snapshot_step=100, show_metric=True, run_id=run_id)

    print("💃 Training Completed")

    # Saving Trained Model
    model.save("genreDNN.tfl")
    print("💾 Model Saved!")