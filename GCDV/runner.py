import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
import sys
import subprocess
import multiprocessing as mp

def precomputeGDGV(file,save_path):
    path = file[0]
    name = file[1]
    rungdgv = "{ time " +"src/./gdgv_exe " + path + " ; }" + " 2> " + save_path+name+".log"
    os.system(rungdgv)
    return rungdgv

def parallelprecomputeGDGV(file):
    path = file[0]
    name = file[1]
    save_path = file[2]+name+".log"
    rungdgv = "{ time " +"src/./gdgv_exe " + path + " ; }" + " 2> " + save_path
    os.system(rungdgv)
    return rungdgv

def runnerGC(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges' in file:
                files.append([os.path.join(r, file),file.replace(".edges","")])
    files.sort()

    for file in tqdm(files):
        rungdgv = precomputeGDGV(file,save_path)
        os.system("clear")
        msg.info(rungdgv)

    return True

def parallelrunnerGC(read_path,save_path,threads=8):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges' in file:
                files.append([os.path.join(r, file),file.replace(".edges","")])
    files.sort()

    with mp.Pool(threads) as p:
        p.map(parallelprecomputeGDGV,[[file[0],file[1],save_path] for file in files])

    return True

def runnerdistances(read_path,save_path,method,threads):
    distances = { "DGCD-13": 1, "DGCD-129": 2, "RDGF": 3, "DGDDA": 4, "DSD": 5, "IODD": 6}
    rungdgv = "{ time " +"python src/./Directed_Distances_v2.py " + read_path+" "+str(distances[method])+ " "+str(threads) + " ; }" + " 2> " + save_path+method+".log"
    os.system(rungdgv)
    os.system("clear")
    msg.info(rungdgv)
    return True