import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg

files = []

for r, d, f in os.walk("data"):
    for file in f:
        if '.edges' in file:
            files.append([os.path.join(r, file),file.replace(".edges","")])
print("")
files.sort()


for file in tqdm(range(len(files))):
    path = files[file][0]
    name = files[file][1]
    runpgd = "pgd/./pgd " +"-f "+path+" --macro "+"results/"+name+".macro"
    os.system(runpgd)
    os.system("clear")
    msg.info(runpgd)
    df = pd.read_csv("results/"+name+".macro",delimiter="=",header=None)
    df[0] = df[0].str.replace('total_', '')
    df[0] = df[0].str.replace('"', '')
    df[0] = df[0].str.replace(' ', '')
    df.to_csv('results/'+name+'.txt', index=False, sep=" ",header=False)
    os.system("rm "+"results/"+name+".macro")
