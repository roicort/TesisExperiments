import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import json
from wasabi import msg
import pickle
import networkx as nx

def main(read_path):

    df = pd.read_csv(read_path)
    df.drop(columns=["Label","Unnamed: 0"],inplace=True)
    print(df)

main('baseline.csv')