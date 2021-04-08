import pandas as pd
import numpy as np

def read_photos(ids_filename: str, features_filename: str):
    print('Loading files...')
    ids = pd.read_csv(ids_filename)
    features = np.load(features_filename)
    print('Files loaded.')
    print(features.shape)