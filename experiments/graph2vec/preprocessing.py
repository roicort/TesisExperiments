import os
import pandas as pd
from tqdm import tqdm
from wasabi import msg
import networkx as nx
import json 
import pickle

def graph2json(read_path,save_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.graphml' in file:
                files.append([os.path.join(r, file),file.replace(".graphml","")])
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

        G = nx.read_graphml(path)
        G = nx.convert_node_labels_to_integers(G)
        Edges = nx.to_pandas_edgelist(G,source="Source", target="Target")

        Edges['Source'] = Edges['Source'].astype(str)
        Edges['Target']= Edges['Target'].astype(str)
        
        Followers = nx.get_node_attributes(G, 'Followers')
        #Followed =  nx.get_node_attributes(G, 'Followed')
        #Tweets =  nx.get_node_attributes(G, 'Tweets')

        Followers = list(Followers.items()) 

        Nodes = pd.DataFrame(Followers, columns =['ID', 'Followers']) 
        Nodes['ID'] = Nodes['ID'].astype(str)

        JSON = {}

        edges_list = []
        for _, edge in Edges.iterrows():
            edges_list.append([int(edge['Source']),int(edge['Target']) ])
        JSON["edges"] = list(edges_list)        
       
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