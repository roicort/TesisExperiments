import pickle
import numpy as np

with open('g2vec_output_dictionary.pickle', 'rb') as f:
    output_dictionary = pickle.load(f)

names = list(output_dictionary.keys())
X = list(output_dictionary.values())

print(names)

#-----------------------------------------------

from matplotlib import pyplot as plt
from scipy.cluster import hierarchy

Z = hierarchy.linkage(X, 'ward')
hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
hierarchy.dendrogram(Z,labels = names, orientation="left", color_threshold=11, above_threshold_color='grey', p=12,leaf_font_size=2)
plt.title('Model: G2V')
plt.savefig("G2V128.png",dpi=800)