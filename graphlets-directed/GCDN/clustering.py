import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import scipy.spatial.distance as ssd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import pickle
from wasabi import msg

def clustering(read_path,save_path,groupsfile='../../datasets/Tweemes/groups.pickle'):

    with open(groupsfile, 'rb') as handle:
        groups = pickle.load(handle)

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.txt' in file:
                files.append([os.path.join(r, file),file.replace(".txt","")])
    print("")
    files.sort()

    #-----------------------------------------------

    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path, sep="\t")
        names = df[df.columns.values.tolist()[0]][0:].apply(lambda x: x.replace("input//", "").replace(".edges",""))
        df.drop([df.columns.values.tolist()[0]], axis=1, inplace = True)
        df.index = names
        df.columns = names

        mdf = df.to_numpy()

        fig, ax = plt.subplots()
        im = ax.imshow(mdf)

        # We want to show all ticks...
        ax.set_xticks(np.arange(len(names)))
        ax.set_yticks(np.arange(len(names)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(names,{'fontsize': 2})
        ax.set_yticklabels(names,{'fontsize': 2})

        #Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")

        fig.colorbar(im)
        fig.savefig(save_path+name+".png",dpi=1500)
        fig.clf()

        # convert the redundant n*n square matrix form into a condensed nC2 array
        X = ssd.squareform(mdf)
        Z = hierarchy.linkage(X, 'ward')
        labels = list([ str(name.replace("_"," "))+" - "+str(groups[name.replace("_"," ")]) for name in names.to_numpy()])
        hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
        hierarchy.dendrogram(Z,labels = labels, orientation="left", color_threshold=9, above_threshold_color='grey', p=12,leaf_font_size=1)
        plt.title('Model: '+name)
        plt.savefig(save_path+name+"_dendrogram.svg")
        plt.clf()
        msg.good(name+ " Figure Saved")
        os.system('clear')
        print('\n\n')

        
    return "Done"
