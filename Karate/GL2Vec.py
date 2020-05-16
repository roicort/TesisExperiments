from wasabi import msg
from karateclub import GL2Vec
import os
from tqdm import tqdm
import networkx as nx
import numpy as np
import pickle 

def runGL2Vec(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        G = nx.read_gpickle(path)
        graphs.append(G)
    
    model = GL2Vec(wl_iterations=2, dimensions=128, workers=32, down_sampling=0.0001, epochs=10, learning_rate=0.025, min_count=25, seed=42)
    msg.info("Running...")
    model.fit(graphs)
    X = model.get_embedding()
    msg.info("Saving...")
    with open(save_path+'GL2Vec'+'.pickle', 'wb') as handle:
        pickle.dump(X, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return "Done"