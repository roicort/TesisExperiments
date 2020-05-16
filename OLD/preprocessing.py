import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import json
from wasabi import msg
import pickle
import networkx as nx

def graph2classic(read_path,save_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.xlsx' in file:
                files.append([os.path.join(r, file),file.replace(".xlsx","")])
    print("")
    files.sort()

    #-----------------------------------------------
    
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        with open('data/'+name+'.graph', 'w', encoding='utf-8') as f:
            print("\n")
            msg.info("Parsing: "+ str(name))
            print("\n")

            st = "t "+'# ' + str(0)+"\n"
            f.write(st)

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
            Edges = Edges.drop_duplicates()

            G = nx.from_pandas_edgelist(Edges,source="Vertex 1", target="Vertex 2")
            S = [G.subgraph(c).copy() for c in nx.algorithms.components.connected_components(G)]
            BCC = nx.to_pandas_edgelist(max(S, key=len),source="Vertex 1", target="Vertex 2")

            nodessss = list(BCC['Vertex 1'])+list(BCC['Vertex 2'])
            activenodes = set(nodessss)
            keys = sorted(activenodes)
            values = list(range(len(keys)))
            nodesdict = dict(zip(keys, values))

            savedf = pd.DataFrame()
            savedf['Source'] = BCC['Vertex 1'].replace(nodesdict, inplace=False)
            savedf['Target'] = BCC['Vertex 2'].replace(nodesdict, inplace=False)

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
            #'Followed',
            #'Followers',
            #'Tweets',
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
            Nodes.drop_duplicates()

            Nodes = Nodes[Nodes["Vertex"].isin(keys)]
            Nodes["ID"] = Nodes['Vertex'].replace(nodesdict, inplace=False)

            Nodes = Nodes.sort_values(by='ID',ascending=True)
            savedf = savedf.sort_values(by=['Source', 'Target'],ascending=True)

            for _ , node in Nodes.iterrows():
                rawnode = 'v '+str(node['ID'])+" "+"0"+'\n'
                f.write(rawnode)
            for _ , edge in savedf.iterrows():
                rawedge = 'e ' + str(edge['Source'])+' '+str(edge["Target"])+" "+"0"+'\n'
                f.write(rawedge)
            f.close()
            os.system('clear')
            print('\n\n')
    return "Done"       