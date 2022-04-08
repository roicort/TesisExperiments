from wasabi import msg
from tqdm import tqdm
import os
import pandas as pd

import numpy as np

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler 

from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster import SilhouetteVisualizer

import seaborn as sns
import matplotlib.pyplot as plt

import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import plotly.figure_factory as ff

def GraphletCorrelations(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.graphletcounts.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.graphletcounts.txt","")])
    files.sort()

    complete = pd.DataFrame()
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path,sep=" ",names=["Graphlet",name])
        df = pd.pivot_table(df,columns="Graphlet")
        #print(df)
        complete = pd.concat([complete, df])
        #os.system("clear")
        #msg.info(rungdgv)

    for column in complete.columns:
        complete[column] = MinMaxScaler().fit_transform(complete[column].values.reshape(-1, 1))

    corr_matrix = complete.corr()
    
    sns.set(font_scale=0.1)
    sns.heatmap(corr_matrix, annot=True)
    plt.savefig(save_path+"Graphlet-Corr.svg")