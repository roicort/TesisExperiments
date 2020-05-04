import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg

def clustering(read_path):

    files = []

    for r, d, f in os.walk(read_path):
        for file in f:
            if '.txt' in file:
                files.append([os.path.join(r, file),file.replace(".txt","")])
    print("")
    files.sort()

    X = []
    names = []

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path,header=None,delimiter=" ")
        X.append(df[1].to_numpy())
        names.append(name)

    #-----------------------------------------------

    from matplotlib import pyplot as plt
    from scipy.cluster import hierarchy

    Z = hierarchy.linkage(X, 'ward')
    hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
    hierarchy.dendrogram(Z,labels = names, orientation="left", color_threshold=0.5e15, above_threshold_color='grey', p=12,leaf_font_size=2)
    plt.title('Model: PGD')
    plt.savefig("PGD.png",dpi=1000)
    return "Done"