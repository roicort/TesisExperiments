import os
import pandas as pd
from tqdm import tqdm
from wasabi import msg
import networkx as nx
import json 
import pickle

def graph2pickle(read_path,save_path):

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
        #G = G.to_undirected()
        #S = [G.subgraph(c).copy() for c in nx.algorithms.components.connected_components(G)]
        #G = max(S, key=len)
        #G = nx.convert_node_labels_to_integers(G)
        nx.write_gpickle(G, save_path+name+".gpickle")

        os.system('clear')
        print('\n\n')
    return True
