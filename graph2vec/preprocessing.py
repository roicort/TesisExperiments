import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import json
from wasabi import msg
import pickle

def graph2json(read_path,save_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.xlsx' in file:
                files.append([os.path.join(r, file),file.replace(".xlsx","")])
    print("")
    files.sort()

    #-----------------------------------------------
    dictnames = {}
    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        dictnames[file] = name
        name = str(file)
        
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
        Edges = Edges.drop_duplicates()

        nodessss = list(Edges['Vertex 1'])+list(Edges['Vertex 2'])
        activenodes = set(nodessss)
        keys = sorted(activenodes)
        values = list(range(len(keys)))
        nodesdict = dict(zip(keys, values))

        savedf = pd.DataFrame()
        savedf['Source'] = Edges['Vertex 1'].replace(nodesdict, inplace=False)
        savedf['Target'] = Edges['Vertex 2'].replace(nodesdict, inplace=False)

        JSON = {}
        edges_list = []
        for _, edge in savedf.iterrows():
            edges_list.append([int(edge['Source']),int(edge['Target']) ])
        JSON["edges"] = list(edges_list)        

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
        features = {} 
        for _, node in Nodes.iterrows():
            features[node["ID"]]=int(node["ID"])
        JSON["features"] = features

        with open(save_path+name+'.json', 'w') as outfile:
           json.dump(JSON, outfile)
        os.system('clear')
        print('\n\n')

    with open("dictnames" + '.pickle', 'wb') as f:
        pickle.dump(dictnames, f, pickle.HIGHEST_PROTOCOL)
    return "Done"