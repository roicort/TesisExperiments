
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx

#-----------------------------------------------

files = []

for r, d, f in os.walk("/Users/roicort/Desktop/GraphWeek"):
    for file in f:
        if '.xlsx' in file:
            files.append([os.path.join(r, file),file.replace(".xlsx","")])
print("")
files.sort()
for f in range(len(files)):
    print(str(files[f][1])+" ---- "+str(f))
print("")

#-----------------------------------------------

All = []
print("")

for file in tqdm(range(len(files))):

    path = files[file][0]

    print("")
    print("")
    print("Reading: "+ str(path))
    print("")

    Nodes = pd.read_excel(path,sheet_name="Vertices",header=1)
    Nodes = Nodes.drop(columns=[#'Vertex',
    'Color',
    'Shape',
    'Size',
    'Opacity',
    'Image File',
    'Visibility',
    'Label',
    'Label Fill Color',
    'Label Position',
    'Tooltip',
    'Layout Order',
    'X',
    'Y',
    'Locked?',
    'Polar R',
    'Polar Angle',
    'Degree',
    'In-Degree',
    'Out-Degree',
    'Betweenness Centrality',
    'Closeness Centrality',
    'Eigenvector Centrality',
    'PageRank',
    'Clustering Coefficient',
    'Reciprocated Vertex Pair Ratio',
    'ID',
    'Dynamic Filter',
    'Add Your Own Columns Here',
    'Name',
    'Followed',
    'Followers',
    'Tweets',
    'Favorites',
    'Time Zone UTC Offset (Seconds)',
    'Description',
    'Location',
    'Web',
    'Time Zone',
    'Joined Twitter Date (UTC)',
    'Profile Banner Url',
    'Default Profile',
    'Default Profile Image',
    'Geo Enabled',
    'Language',
    'Listed Count',
    'Profile Background Image Url',
    'Verified',
    'Custom Menu Item Text',
    'Custom Menu Item Action',
    'Tweeted Search Term?'])

    Nodes = Nodes.to_numpy()
    All.append(Nodes)

    os.system('clear')
    print("")
    print("")
    print("")

#-----------------------------------------------

import networkx as nx

q = len(All)
Inter = [[[] for _ in range(q)] for _ in range(q)]

for i in tqdm(range(q)):
    for j in range(i,q):
        Inter[i][j] = np.intersect1d(All[i], All[j])

np.savez("InterUSERS", Inter)


