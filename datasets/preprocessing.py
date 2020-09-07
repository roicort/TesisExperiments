import os
import pandas as pd
from tqdm import tqdm
from wasabi import msg
import networkx as nx 
import matplotlib.pyplot as plt

def excel2networkx(read_path,save_path):

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

        Edges = Edges.loc[Edges['Relationship'] != "Tweet"]    
        Edges = Edges.loc[Edges['Vertex 1'] != Edges['Vertex 2']]
        Edges = Edges.drop_duplicates()

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

        Nodes = Nodes.drop_duplicates()

        nodessss = list(Edges['Vertex 1'])+list(Edges['Vertex 2'])
        activenodes = set(nodessss)
        activenodes = sorted(activenodes)

        Nodes = Nodes[Nodes["Vertex"].isin(activenodes)]
        Nodes = Nodes.sort_values(by='Vertex',ascending=True)

        G = nx.from_pandas_edgelist(Edges, source='Vertex 1', target='Vertex 2', edge_attr="Relationship", create_using=nx.DiGraph())
      
        for _ , node in Nodes.iterrows():       
            G.add_node(node["Vertex"],Followed = node['Followed'], Followers = node['Followers'], Tweets = node['Tweets'])

        file2save = save_path+name+".graphml"

        nx.write_graphml(G,file2save)
        #newG = nx.read_graphml(file2save)

        #tests = [nx.get_edge_attributes(G,"Relationship")==nx.get_edge_attributes(G,"Relationship"),nx.get_node_attributes(G,"Followed")==nx.get_node_attributes(newG,"Followed"),nx.get_node_attributes(G,"Followers")==nx.get_node_attributes(newG,"Followers"),nx.get_node_attributes(G,"Tweets")==nx.get_node_attributes(G,"Tweets"),G.edges==newG.edges,sorted(G.nodes)==sorted(newG.nodes)]
        
        os.system('clear')
        print('\n\n')
        
    return "Done"
    
excel2networkx("raw_data","data/")
