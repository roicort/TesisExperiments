
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

os.system('clear')

inter = np.load('InterUSERS.npz', allow_pickle=True)

aInter = inter['arr_0']

q = len(aInter)

names = []

for i in tqdm(range(q)):
    ax = []
    for j in range(q):
        ax+=list(aInter[i][j])
    ax = set(ax)
    names.append(ax)


all = np.load('PARSED.npz', allow_pickle=True)

all = all['arr_0']

def nom(x):
    if x > 0:
        return 1
    elif x<0:
        return 0

for d in tqdm(range(len(all))):
    df = all[d][0]
    dfm = pd.crosstab(df["Vertex 1"], df["Vertex 2"])
    dfm.apply(nom)
    idx = dfm.columns.union(dfm.index)
    dfm = dfm.reindex(index = idx, columns=idx, fill_value=0)
    dfm.where(dfm > 1, 1)
    input()
    #f = dfm.filter(items=names[d],axis=0).filter(items=names[d],axis=1)
    #np.savez_compressed("filtered/"+str(d), f)
