
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sc

from networkx.algorithms.community.quality import modularity

from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx

def centralization(G):
    N=G.order()
    degree = nx.degree_centrality(G).values()
    max_ = max(degree)
    min_ = min(degree)
    num = sum([(max_ - cx) for cx in degree])
    den = (N-1)*(max_ - min_)
    return num/den

#-----------------------------------------------

files = []

for r, d, f in os.walk("/Users/roicort/Desktop/GraphWeek"):
    for file in f:
        if '.xlsx' in file:
            files.append([os.path.join(r, file),file.replace(".xlsx","")])
print("")
files.sort()

#-----------------------------------------------

cl = []

for file in tqdm(range(len(files))):

    path = files[file][0]
    name = files[file][1]

    print("")
    print("")
    print("Reading: "+ str(path))
    print("")

    Edges = pd.read_excel(path,sheet_name="Edges",header=1)
    Edges = Edges.drop(columns=[#'Vertex 1',
    #'Vertex 2',
    'Color',
    'Width',
    'Style',
    'Opacity',
    'Visibility',
    'Label',
    'Label Text Color',
    'Label Font Size',
    'Reciprocated?',
    'ID',
    'Dynamic Filter',
    'Add Your Own Columns Here',
    #'Relationship',
    #'Relationship Date (UTC)',
    #'Tweet',
    #'URLs in Tweet',
    'Domains in Tweet',
    #'Hashtags in Tweet',
    #'Media in Tweet',
    #'Tweet Image File',
    #'Tweet Date (UTC)',
    #'Date',
    #'Time',
    #'Twitter Page for Tweet',
    #'Latitude',
    #'Longitude',
    #'Imported ID',
    #'In-Reply-To Tweet ID',
    'Favorited',
    #'Favorite Count',
    'In-Reply-To User ID',
    #'Is Quote Status',
    #'Language',
    'Possibly Sensitive',
    'Quoted Status ID',
    'Retweeted',
    #'Retweet Count',
    #'Retweet ID',
    #'Source',
    'Truncated',
    'Unified Twitter ID',
    'Imported Tweet Type',
    'Added By Extended Analysis',
    'Corrected By Extended Analysis',
    'Place Bounding Box',
    'Place Country',
    'Place Country Code',
    'Place Full Name',
    'Place ID',
    'Place Name',
    'Place Type',
    'Place URL'])

    Edges['Relationship Date (UTC)'] = Edges['Relationship Date (UTC)'].map(lambda element: str(element.to_pydatetime()))
    Edges['Tweet Date (UTC)'] = Edges['Tweet Date (UTC)'].map(lambda element: str(element.to_pydatetime()))
    Edges['Date'] = Edges['Date'].map(lambda element: str(element.to_pydatetime()))
    Edges['URLs in Tweet'] = Edges['URLs in Tweet'].map(lambda element: str(element))

    #print(Edges.dtypes)

    Nodes = pd.read_excel(path,sheet_name="Vertices",header=1)
    Nodes = Nodes.drop(columns=[#'Vertex',
    'Color',
    'Shape',
    'Size',
    'Opacity',
    #'Image File',
    'Visibility',
    'Label',
    'Label Fill Color',
    'Label Position',
    #'Tooltip',
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
    #'Name',
    #'Followed',
    #'Followers',
    #'Tweets',
    #'Favorites',
    'Time Zone UTC Offset (Seconds)',
    #'Description',
    #'Location',
    #'Web',
    'Time Zone',
    #'Joined Twitter Date (UTC)',
    'Profile Banner Url',
    'Default Profile',
    'Default Profile Image',
    #'Geo Enabled',
    #'Language',
    #'Listed Count',
    'Profile Background Image Url',
    #'Verified',
    'Custom Menu Item Text',
    'Custom Menu Item Action',
    'Tweeted Search Term?'])

    Nodes['Joined Twitter Date (UTC)'] = Nodes['Joined Twitter Date (UTC)'].map(lambda element: str(element.to_pydatetime()))

#-----------------------------------------------

    G=nx.from_pandas_edgelist(Edges,source="Vertex 1",target="Vertex 2",edge_attr=True,create_using=nx.DiGraph())
    G.remove_edges_from(nx.selfloop_edges(G))

    central = centralization(G)
    density = nx.density(G)
    per_isolates = nx.number_of_isolates(G)/G.order()

    push = [name,[central,density,per_isolates]]
    cl.append(push)

    os.system("clear")

    print("")
    print("")
    print("")

np.save("points",cl)