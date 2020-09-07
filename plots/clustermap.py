import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(color_codes=True)
from sklearn import preprocessing


def clustermap_PGD(read_path):

    files = []

    for r, d, f in os.walk(read_path):
        for file in f:
            if '.gfd' in file:
                files.append([os.path.join(r, file),file.replace(".gfd","")])
    print("")
    files.sort()
    frames=[]
    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        f = open(path, "r")
        txt = f.read()
        dif = txt.split(sep="************************************************************")
        stats = dif[0].replace("[reading generic edge list: read_edge_list func]"," ").replace("=",":")
        count = dif[1].replace("-","").replace("="," ")
        gfd = dif[2].split(sep="--------------------------------------------------------------------------------")
        stats+=gfd[0]
        gfd.pop(0)
        GFD = gfd[0]+gfd[1]
        GFD_connected = gfd[2]+gfd[3]
        GFD_disconnected = gfd[4] + gfd[5] 

        stats = pd.read_csv(StringIO(stats),sep=":",header=None)
        count = pd.read_csv(StringIO(count),sep="\s+",header=None)
        GFD = pd.read_csv(StringIO(GFD),sep="\t",header=None,skiprows=2,names=["theta","r"])
        GFD_connected = pd.read_csv(StringIO(GFD_connected),sep="\t",header=None,skiprows=2,names=["theta","r"])
        GFD_disconnected = pd.read_csv(StringIO(GFD_disconnected),sep="\t",header=None,skiprows=2,names=["theta","r"])

        #print(stats)
        #print(count)
        #print(GFD)
        #print(GFD_connected)
        #print(GFD_disconnected)


        df = GFD.pivot_table(columns='theta')
        df.index=[None]
        df = df.drop(df.columns[[8]], axis=1)
        frames.append(df)

    result = pd.concat(frames)
    print(result)
    g = sns.clustermap(result)
    plt.savefig("GFD_clustermap2.png",dpi=1000)
    #paudelgado&roicortez

clustermap_PGD("../PGD/output")