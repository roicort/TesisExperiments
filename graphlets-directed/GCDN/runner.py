import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
import sys

def runnerGC(read_path,save_path):

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
        rungdgv = "{ time " +"src/./gdgv_exe " + path + " ; }" + " 2> " + save_path+name+".log"
        os.system(rungdgv)
        os.system("clear")
        msg.info(rungdgv)
    return "Done"

def runnerdistances(read_path,save_path,method,threads):
    distances = { "DGCD-13": 1, "DGCD-129": 2, "RDGF": 3, "DGDDA": 4, "DSD": 5, "IODD": 6}
    rungdgv = "{ time " +"python src/./Directed_Distances_v2.py " + read_path+" "+str(distances[method])+ " "+str(threads) + " ; }" + " 2> " + save_path+method+".log"
    os.system(rungdgv)
    os.system("clear")
    msg.info(rungdgv)
    return "Done"