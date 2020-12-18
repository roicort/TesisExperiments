from wasabi import msg
import os
from tqdm import tqdm
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pickle
from fa2 import ForceAtlas2

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
    forceatlas2 = ForceAtlas2(
                        # Behavior alternatives
                        outboundAttractionDistribution=False,  # Dissuade hubs
                        edgeWeightInfluence=1.0,

                        # Performance
                        jitterTolerance=1.0,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=1.2,

                        # Tuning
                        scalingRatio=50.0,
                        strongGravityMode=False,
                        gravity=1.0,

                        # Log
                        verbose=True)
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        msg.info("Reading "+str(path))
        msg.info("Plotting "+str(name))
        G = nx.read_gpickle(path)
        G.remove_edges_from(list(nx.selfloop_edges(G)))
        G.remove_nodes_from(list(nx.isolates(G)))
        pos = forceatlas2.forceatlas2_networkx_layout(G, pos=None, iterations=200)
        #pos = nx.spring_layout(G)
        plt.figure(dpi=800)
        plt.axis('off')
        nx.draw_networkx_nodes(G,pos,node_size=0.5,node_color='#939393',)
        nx.draw_networkx_edges(G,pos,width=0.15,edge_color='#BDBDBD',alpha=0.5,arrows=False)
        plt.savefig(save_path+name+" - "+groups[name]+".png")
        plt.clf()
        os.system("clear")

    return True
