import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import json
from wasabi import msg
import pickle
import networkx as nx

def graph2edges(read_path,save_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.graphml' in file:
                files.append([os.path.join(r, file),file.replace(".graphml","")])
    print("")
    files.sort()

    #-----------------------------------------------

    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        
        print("\n")
        msg.info("Parsing: "+ str(name))
        print("\n")

        G = nx.read_graphml(path)
        G = nx.convert_node_labels_to_integers(G)
        Edges = nx.to_pandas_edgelist(G,source="Source", target="Target")

        Edges['Source'] = Edges['Source'].astype(str)
        Edges['Target']= Edges['Target'].astype(str)
        
        Edges = Edges.sort_values(by=['Source', 'Target'],ascending=True)
        Edges.to_csv(save_path+name.replace(" ","_")+'.edges', columns=['Source','Target'],index=False,sep=" ",header=None)

        os.system('clear')
        print('\n\n')
        
    return "Done"