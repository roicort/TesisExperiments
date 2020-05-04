import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
import pickle

def clustering(read_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.csv' in file:
                files.append([os.path.join(r, file),file.replace(".csv","")])
    print("")
    files.sort()

    X = []
    names = []

    with open("dictnames" + '.pickle', 'rb') as f:
        dictnames = pickle.load(f)
    for file in tqdm(range(len(files))):
        path = files[file][0]
        df = pd.read_csv(path,delimiter=",")
        df['type'].replace(dictnames, inplace=True)
        for _, row in df.iterrows():
            nmpy = row.to_numpy()
            X.append(nmpy[1:])
            names.append(nmpy[0])

    print(names)
    #-----------------------------------------------

    from matplotlib import pyplot as plt
    from scipy.cluster import hierarchy

    Z = hierarchy.linkage(X, 'ward')
    hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
    hierarchy.dendrogram(Z,labels = names, orientation="left", color_threshold=11, above_threshold_color='grey', p=12,leaf_font_size=2)
    plt.title('Model: PGD')
    plt.savefig("PGD.png",dpi=1000)
    return "Done"
