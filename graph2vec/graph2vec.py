import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg

def rungraph2vec(read_path,save_path):

    rung2v = "python src/graph2vec.py " + "--input-path " +read_path+" --output-path " + save_path+ "/embeddings.csv"
    msg.info(rung2v)
    os.system(rung2v)
    return "Done"
