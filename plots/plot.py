from wasabi import msg
import os
from tqdm import tqdm
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle

def runPlot(read_path,save_path,groupsfile='../datasets/Tweemes/groups.pickle'):

    with open(groupsfile, 'rb') as handle:
        groups = pickle.load(handle)

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    msg.info("Executing...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        msg.info("Reading "+str(path))
        msg.info("Plotting "+str(name))
        G = nx.read_gpickle(path)
        plt.figure(dpi=800)
        plt.axis('off')
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G,pos,node_size=1,node_color='#939393',)
        nx.draw_networkx_edges(G,pos,width=0.25,edge_color='#BDBDBD',alpha=0.8,arrows=False)
        plt.savefig(save_path+name+" - "+groups[name]+".png")
        plt.clf()
        os.system("clear")

    return True
