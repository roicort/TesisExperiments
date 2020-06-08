from wasabi import msg
from karateclub import Graph2Vec, SF, NetLSD, GL2Vec, GeoScattering
import os
from tqdm import tqdm
import networkx as nx
import numpy as np
import pickle 

import time

def size_only(read_path,save_path):
    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    names = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        G = nx.read_gpickle(path)
        graphs.append(G)
        names.append(name)
    
    embeddings = []

    start_time = time.time()
    for graph in graphs:
        embeddings.append([graph.number_of_nodes(),graph.number_of_edges()])
    end_time = time.time() - start_time

    msg.info("Saving...")
    data = dict(zip(names, embeddings))
    with open(save_path+'size'+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return end_time

def runG2Vec(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    names = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        G = nx.read_gpickle(path)
        graphs.append(G)
        names.append(name)
    
    epochs = 1
    workers = 32
    mincount = 5
    wliterations = 2
    dim = 128

    model = Graph2Vec(wl_iterations=wliterations, dimensions=dim, workers=workers, epochs=epochs, min_count=mincount)
    msg.info("Running Graph2Vec...")
    model.fit(graphs)
    start_time = time.time()
    embeddings = model.get_embedding()
    end_time = time.time() - start_time
    msg.info("Saving...")
    data = dict(zip(names, embeddings))
    with open(save_path+'Graph2Vec'+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return end_time


def runSF(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    names = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        G = nx.read_gpickle(path)
        graphs.append(G)
        names.append(name)
    
    model = SF(dimensions=128)
    msg.info("Running SF...")
    model.fit(graphs)
    start_time = time.time()
    embeddings = model.get_embedding()
    end_time = time.time() - start_time
    msg.info("Saving...")
    data = dict(zip(names, embeddings))
    with open(save_path+'SF'+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return end_time


def runNetLSD(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    names = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        G = nx.read_gpickle(path)
        graphs.append(G)
        names.append(name)
    
    model = NetLSD(scale_min=-2.0, scale_max=2.0, scale_steps=250, approximations=200)
    msg.info("Running NetLSD...")
    model.fit(graphs)
    start_time = time.time()
    embeddings = model.get_embedding()
    end_time = time.time() - start_time
    msg.info("Saving...")
    data = dict(zip(names, embeddings))
    with open(save_path+'NetLSD'+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return end_time

def runGL2Vec(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    names = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        G = nx.read_gpickle(path)
        graphs.append(G)
        names.append(name)

    epochs = 1
    workers = 32
    mincount = 5
    wliterations = 2
    dim = 128
    
    model = GL2Vec(wl_iterations=wliterations, dimensions=dim, workers=workers, down_sampling=0.0001, epochs=epochs, learning_rate=0.025, min_count=mincount)
    msg.info("Running GL2Vec...")
    model.fit(graphs)
    start_time = time.time()
    embeddings = model.get_embedding()
    end_time = time.time() - start_time
    msg.info("Saving...")
    data = dict(zip(names, embeddings))
    with open(save_path+'GL2Vec'+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return end_time

def runGeoScattering(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.gpickle' in file:
                files.append([os.path.join(r, file),file.replace(".gpickle","")])
    print("")
    files.sort()
    
    graphs = []
    names = []
    msg.info("Reading...")
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        G = nx.read_gpickle(path)
        graphs.append(G)
        names.append(name)
    
    model = GeoScattering(order=4, moments=4)
    msg.info("Running GeoScattering...")
    model.fit(graphs)
    start_time = time.time()
    embeddings = model.get_embedding()
    end_time = time.time() - start_time
    msg.info("Saving...")
    data = dict(zip(names, embeddings))
    with open(save_path+'GeoScattering'+'.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return end_time