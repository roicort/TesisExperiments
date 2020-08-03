
import os
from tqdm import tqdm
import scipy as sc
from wasabi import msg
import pickle
from matplotlib import pyplot as plt
import numpy as np

from scipy.spatial import distance

def compute_distance(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.pickle' in file:
                files.append([os.path.join(r, file),file.replace(".pickle","")])
    print("")
    files.sort()

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]

        with open(path, 'rb') as handle:
            embeddings = pickle.load(handle)
            names, X = list(embeddings.keys()), list(embeddings.values())
        
        dist_matrix = distance.cdist(X,X,'euclidean')
        print(dist_matrix)

        fig, ax = plt.subplots()
        im = ax.imshow(dist_matrix)

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

    return "Done"
#paudelgado
compute_distance("outputs/","distance/")