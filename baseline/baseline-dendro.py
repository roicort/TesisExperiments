import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import json
from wasabi import msg
import pickle
import networkx as nx

import plotly.figure_factory as ff

from sklearn.preprocessing import MinMaxScaler 

import scipy.stats as stats
from scipy.cluster import hierarchy

def main(read_path,save_path="results/"):

    X = pd.read_csv(read_path)
    X.drop(columns=["Label","Unnamed: 0"],inplace=True)

    labels = list(X["Network"])
    X = X.drop(columns=["Network"],inplace=False)

    print(labels)
    print(X)

    X = np.array(X)

    for method in tqdm(['single','complete','average','weighted','centroid','median','ward']):
        fig = ff.create_dendrogram(X, orientation='left', labels=labels, linkagefun=lambda alpha: hierarchy.linkage(alpha,method=method,optimal_ordering=True))
        fig.update_layout(autosize=True) 
        fig.update_layout(height=700) 
        fig.write_html(save_path+"Baseline"+"-"+method.upper()+".dendrogram.html")

main('baseline.csv')