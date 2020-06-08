import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
import sys

def runpgd(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges' in file:
                files.append([os.path.join(r, file),file.replace(".edges","")])
    print("")
    files.sort()

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        runpgd = "src/./pgd " +"-f "+path+" --gfd " + "> " +save_path+name+".gfd"
        os.system(runpgd)
        os.system("clear")
        msg.info(runpgd)
    return "Done"
