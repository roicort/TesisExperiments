import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
import sys

def runner(read_path,save_path,size):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges' in file:
                files.append([os.path.join(r, file),file.replace(".edges","")])
    print("")
    files.sort()

    gtriefile = "gtries/dir"+str(size)+".gt"

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        runpgd = "src/./gtrieScanner " +"--size " +str(size)+" --graph "+ path+" --directed "+ " --format simple " + " --method gtrie " + gtriefile + " --output " + save_path+name+".txt" + " --type txt" + " > " + save_path+name+".log"
        os.system(runpgd)
        os.system("clear")
        msg.info(runpgd)
    return "Done"
