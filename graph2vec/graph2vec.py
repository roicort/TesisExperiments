
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sc
import json
from wasabi import msg
from karateclub import Graph2Vec, GL2Vec

#-----------------------------------------------

files = []

for r, d, f in os.walk("GraphWeek"):
    for file in f:
        if '.xlsx' in file:
            files.append([os.path.join(r, file),file.replace(".xlsx","")])
print("")
files.sort()

def connected_component_subgraphs(G, copy=True):
    for c in nx.connected_components(G):
        if copy:
            yield G.subgraph(c).copy()
        else:
            yield G.subgraph(c)

#-----------------------------------------------

graphs = []
names = []

for file in tqdm(range(len(files))):

    path = files[file][0]
    name = files[file][1]
    
    print("\n")
    msg.info("Parsing: "+ str(name))
    print("\n")

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
    'Relationship Date (UTC)',
    'Tweet',
    'URLs in Tweet',
    'Domains in Tweet',
    'Hashtags in Tweet',
    'Media in Tweet',
    'Tweet Image File',
    'Tweet Date (UTC)',
    'Date',
    'Time',
    'Twitter Page for Tweet',
    'Latitude',
    'Longitude',
    'Imported ID',
    'In-Reply-To Tweet ID',
    'Favorited',
    'Favorite Count',
    'In-Reply-To User ID',
    'Is Quote Status',
    'Language',
    'Possibly Sensitive',
    'Quoted Status ID',
    'Retweeted',
    'Retweet Count',
    'Retweet ID',
    'Source',
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

    #Edges['Relationship Date (UTC)'] = Edges['Relationship Date (UTC)'].map(lambda element: str(element.to_pydatetime()))
    #Edges['Tweet Date (UTC)'] = Edges['Tweet Date (UTC)'].map(lambda element: str(element.to_pydatetime()))
    #Edges['Date'] = Edges['Date'].map(lambda element: str(element.to_pydatetime()))
    #Edges['URLs in Tweet'] = Edges['URLs in Tweet'].map(lambda element: str(element))
    #print(Edges.dtypes)

    Edges = Edges.loc[Edges['Relationship'] != "Tweet"]    
    Edges = Edges.loc[Edges['Vertex 1'] != Edges['Vertex 2']]

    G=nx.from_pandas_edgelist(Edges,source="Vertex 1",target="Vertex 2")
    bigG = max(connected_component_subgraphs(G), key=len)
    GL = nx.to_edgelist(bigG)
    auxdf = pd.DataFrame(GL)
    auxdf.columns = ['Source', 'Target','Atributes']
    nodessss = list(auxdf['Source'])+list(auxdf['Target'])
    activenodes = set(nodessss)
    values = list(range(len(activenodes)))
    keys = list(activenodes)
    nodesdict = dict(zip(keys, values))
    auxdf['SourceIDS'] = auxdf['Source'].replace(nodesdict, inplace=False)
    auxdf['TargetIDS'] = auxdf['Target'].replace(nodesdict, inplace=False)
    newG=nx.from_pandas_edgelist(auxdf,source="SourceIDS",target="TargetIDS")
    graphs.append(newG)
    names.append(name)
    os.system('clear')
    print('\n\n')

#----------------------------------------------------------------------------

import pickle

with open('graphs.pickle', 'wb') as handle:
    pickle.dump(graphs, handle, protocol=pickle.HIGHEST_PROTOCOL)

#----------------------------------------------------------------------------
    
modelG2V = Graph2Vec(workers=32,min_count=16,dimensions=256)
modelG2V.fit(graphs)
g2vec_output = modelG2V.get_embedding()
msg.info("G2V Done")

g2vec_output_dictionary = dict(zip(names, g2vec_output))

with open('g2vec_output_dictionary256.pickle', 'wb') as handle:
    pickle.dump(g2vec_output_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
#----------------------------------------------------------------------------

modelGL2V = GL2Vec(workers=32,min_count=16,dimensions=256)
modelGL2V.fit(graphs)
gl2vec_output = modelGL2V.get_embedding()
msg.info("GL2V Done")

gl2vec_output_dictionary = dict(zip(names, gl2vec_output))

with open('gl2vec_output_dictionary256.pickle', 'wb') as handle:
    pickle.dump(gl2vec_output_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
#----------------------------------------------------------------------------   

print('\n')