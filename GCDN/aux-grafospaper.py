import pandas as pd
import numpy as np
import networkx as nx

def ColorNetworks():

    edges = pd.read_csv("input/Coco.edges",header= None,sep = " ")
    edges.columns =['Source','Target']

    G=nx.from_pandas_edgelist(edges, "Source", "Target",create_using=nx.DiGraph())

    clusterdict = pd.read_csv("../../../../Downloads/Coco_labels.csv",header= None)
    clusterdict.columns =['Cluster']
    clusterdict = pd.Series(clusterdict["Cluster"].values).to_dict()
    
    nx.set_node_attributes(G, clusterdict, name="Cluster")

    nx.write_gexf(G, "CocoPrueba"+".gexf") 

ColorNetworks()