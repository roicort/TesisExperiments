
import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------

files = []

for r, d, f in os.walk("/Users/roicort/Desktop/filtered"):
    for file in f:
        if '.npz' in file:
            files.append([os.path.join(r, file),int(file.replace(".npz",""))])
print("")
files.sort(key = lambda x: x[1])
for f in range(len(files)):
    print(str(files[f][0]))
print("")

#-----------------------------------------------

for f in tqdm(range(len(files))):
    path = files[f][0]
    ax = np.load(path)
    ax = ax['arr_0']

    plt.spy(ax)
    plt.savefig("filteredIM/"+str(files[f][1])+".png")
    plt.clf()