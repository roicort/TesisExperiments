import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg

"""
--dimensions     INT          Number of dimensions.                             Default is 128.
  --workers        INT          Number of workers.                                Default is 4.
  --epochs         INT          Number of training epochs.                        Default is 1.
  --min-count      INT          Minimal feature count to keep.                    Default is 5.
  --wl-iterations  INT          Number of feature extraction recursions.          Default is 2.
  --learning-rate  FLOAT        Initial learning rate.                            Default is 0.025.
  --down-sampling  FLOAT        Down sampling rate for frequent features.         Default is 0.0001.
  """

epochs = 1
workers = 32
mincount = 5
wliterations = 2
dim = 128

def rungraph2vec(read_path,save_path):
    rung2v = "python src/graph2vec.py " + "--input-path " +read_path+" --output-path " + save_path+ "embeddings.csv "+" --dimensions "+str(dim)+" --epochs " + str(epochs) +" --wl-iterations "+str(wliterations)+" --min-count "+str(mincount)+" --workers " + str(workers)
    msg.info(rung2v)
    os.system(rung2v)
    return "Done"
