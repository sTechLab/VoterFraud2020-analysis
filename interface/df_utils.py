import pandas as pd
import pickle

def load_pickled_df(filename):
    with open(filename, "rb") as fh:
        return pd.DataFrame(pickle.load(fh))