import time
import os
import pandas as pd
from tqdm import tqdm
import numpy as np

#-----------------------------------------------

files = []

for r, d, f in os.walk("/Users/roicort/Desktop"):
    for file in f:
        if '.npy' in file:
            files.append(os.path.join(r, file))

for f in range(len(files)):
    print(str(files[f]))
#-----------------------------------------------

for f in tqdm(range(len(files))):
    path = files[f]
    ax = np.load(path,allow_pickle=True)
os.system("clear")

#-----------------------------------------------
# #############################################################################
#-----------------------------------------------

from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_swiss_roll
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

from sklearn.datasets import make_swiss_roll

X = [np.array(a[1]) for a in ax]
names = [np.array(a[0]) for a in ax]

#-----------------------------------------------
# Compute clustering

print("Computing hierarchical clustering")
#os.system("say "+"Computando clustering jerárquico")
st = time.time()
ward = AgglomerativeClustering(n_clusters=6, linkage='ward').fit(X)
elapsed_time = time.time() - st
labels = ward.labels_

#os.system("say "+"Tiempo transcurrido: %.2fs" % elapsed_time)
print("Elapsed time: %.2fs" % elapsed_time)
print("Number of points: %i" % labels.size)

#-----------------------------------------------
# Plot result

fig = plt.figure()
ax = fig.gca(projection='3d')

for p in range(len(X)):
    point = X[p]
    label = labels[p]
    ax.scatter(point[0],point[1],point[2],color=plt.cm.gist_rainbow(np.float(label) / np.max(label + 1)))
    
plt.show()

#-----------------------------------------------

from matplotlib import pyplot as plt
from scipy.cluster import hierarchy

Z = hierarchy.linkage(X, 'ward')
hierarchy.set_link_color_palette(['#00F2D5','#F20000','#5CF200','#0700F2','#DC00F2'])
hierarchy.dendrogram(Z,labels = names, leaf_rotation=0, orientation="left", color_threshold=0.07, above_threshold_color='grey')
plt.show()