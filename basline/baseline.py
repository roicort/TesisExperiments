import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import json
from wasabi import msg
import pickle
import networkx as nx

def Centralization(G):
    
    inc = nx.algorithms.centrality.out_degree_centrality(G)
    outc = nx.algorithms.centrality.in_degree_centrality(G)

    centralities = [inc,outc]
    centralization = []

    for centrality in centralities:

        n_val = len(centrality)
        c_denominator = (n_val-1)*(n_val-2)
        c_node_max = max(centrality.values())
        c_sorted = sorted(centrality.values(),reverse=True)

        #print("\t Max Node: " + str(c_node_max) + "\n")

        c_numerator = 0

        for value in c_sorted:
            c_numerator += (c_node_max*(n_val-1) - value*(n_val-1))

        res = c_numerator/c_denominator

        #print ('\t Numerator:' + str(c_numerator)  + "\n")	
        #print ('\t Denominator:' + str(c_denominator)  + "\n")	
        #print('\t Centralization:' + str(res)  + "\n")

        centralization.append(res)
        
    return centralization

def main(read_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.graphml' in file:
                files.append([os.path.join(r, file),file.replace(".graphml","")])
    print("")
    files.sort()

    #-----------------------------------------------

    nclas  = pd.DataFrame(columns=['Network',"CentralizationIN","CentralizationOUT","Density","Modularity","Isolates","Label"]) 

    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        
        print("\n")
        msg.info("Parsing: "+ str(name))
        print("\n")

        G = nx.read_graphml(path)
        G.remove_edges_from(list(nx.selfloop_edges(G)))

        vector = Computemeasures(G)

        print("Centralization Indegree "+str(vector[0][0]))
        print("Centralization Outdegre "+str(vector[0][1]))  
        print("Density "+str(vector[1]))  
        print("Modularity "+str(vector[2]))
        print("Isolates "+str(vector[3]))

        label = getLabel(vector)

        nclas = nclas.append({'Network': name, 'CentralizationIN': vector[0][0], 'CentralizationOUT': vector[0][1], "Density": vector[1], "Modularity":vector[2],"Isolates": vector[3],"Label":label}, ignore_index=True)
        print(nclas)

        os.system('clear')
        print('\n\n')
    nclas.to_csv("baseline.csv")
    return True

def Computemeasures(G):

    centralization = Centralization(G)
    uniDirG = nx.Graph(G)
    density = nx.classes.function.density(uniDirG)
    partition = list(nx.algorithms.community.modularity_max.greedy_modularity_communities(uniDirG))
    modularity = nx.algorithms.community.quality.modularity(uniDirG, partition)
    isolfrac = nx.algorithms.isolate.number_of_isolates(G) / nx.classes.function.number_of_nodes(G)

    return [centralization,density,modularity,isolfrac]

def getLabel(vector):

    centralizationtreshold = 0.59
    densitytreshold = 0.5
    modularitytreshold = 0.5
    isolatestreshold = 0.5

    if vector[0][0] > centralizationtreshold or vector[0][1] > centralizationtreshold: #Centralization
        if vector[0][0] > vector[0][1]: #Direction Of Centralization (IN)
            return "InWard Hub and Spoke"
        if vector[0][0] < vector[0][1]: #Direction Of Centralization (OUT)
            return "OutWard Hub and Spoke"
    elif vector[1] > densitytreshold: #Density
        if vector[2] > modularitytreshold: #Modularity
            return "Divided"
        else:
            return "Unified"
    elif vector[3] > isolatestreshold: #IsolateFraction (HIGH) - More Isolates (Isolates/Total)
        return "Fragmented"
    elif vector[3] < isolatestreshold: #IsolateFraction (LOW) - Less Isolates (Isolates/Total)
        return "Clustered"


main('../datasets/Tweemes')