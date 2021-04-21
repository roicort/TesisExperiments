from wasabi import msg
from tqdm import tqdm
import os
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import plotly.figure_factory as ff

from sklearn.preprocessing import MinMaxScaler 

import scipy.stats as stats
from scipy.cluster import hierarchy

def dusers(read_path,save_path):

    msg.info("Reading Data...")
    df = pd.read_csv(save_path+"Complete-TSNE-WON.csv")
    df = df[['Network', 'Cluster']]
    print(df)

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.signatures.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.signatures.txt","")])
    files.sort()

    msg.good("Done")

    msg.info("Computing Embeddings...")
    embeddings = {}
    for file in tqdm(range(len(files))):
        #path = files[file][0]
        name = files[file][1]
        network = df[df["Network"] == name]
        #print(network)

        r1 = len(network[network["Cluster"] == 0])
        r2 = len(network[network["Cluster"] == 1])
        r3 = len(network[network["Cluster"] == 2])
        r4 = len(network[network["Cluster"] == 3])

        embeddings[name] = [r1,r2,r3,r4]

    embeddings = pd.DataFrame.from_dict(embeddings, orient='index')

    print(embeddings)

    for column in embeddings.columns:
        embeddings[column] = MinMaxScaler().fit_transform(embeddings[column].values.reshape(-1, 1))

    print(embeddings)

    labels = embeddings.index

    msg.good("Embeddings Done")
    embeddings = np.array(embeddings)
    #print(embeddings)
    for method in ['single','complete','average','weighted','centroid','median','ward']:
        fig = ff.create_dendrogram(embeddings, orientation='left', labels=labels, linkagefun=lambda alpha: hierarchy.linkage(alpha,method=method,optimal_ordering=True))
        fig.update_layout(autosize=True) 
        fig.update_layout(height=700) 
        fig.write_html(save_path+"UsersWON"+"-"+method.upper()+".dendrogram.html")


dusers("input/","users/")