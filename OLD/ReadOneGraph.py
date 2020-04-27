import os
import time
import pandas as pd
import networkx as nx
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

selected = int(input("Which file? "))

filepath = files[selected][0]
filename = files[selected][1]

print("")
print("Reading: "+ str(filepath))
print("")

start_time = time.time()

Edges = pd.read_excel(filepath,sheet_name="Edges",header=1)
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

Nodes = pd.read_excel(filepath,sheet_name="Vertices",header=1)
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

print(Nodes['ID'])
#print(Nodes.dtypes)

print("Done in %s seconds" % (time.time() - start_time))
print("")

#-----------------------------------------------

if input("Generate graph? (y/n) ") == "y":

    print("")
    print("Generating Graph") 
    print("")

    start_time = time.time()

    G=nx.from_pandas_edgelist(Edges,source="Vertex 1",target="Vertex 2",edge_attr=True)

    print("Done in %s seconds" % (time.time() - start_time)) 
    print("")

    if input("Plot graph? (y/n) ") == "y":

        plot = figure(title=filename, x_range=(-1.1,1.1), y_range=(-1.1,1.1),
                    tools="", toolbar_location=None)

        graph = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))
        plot.renderers.append(graph)

        show(plot)
    
    if input("Save graph? (y/n) ") == "y":

        nx.write_gexf(G, "/Users/roicort/Desktop/"+str(filename)+".gexf")

#-----------------------------------------------