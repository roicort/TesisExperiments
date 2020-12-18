import os
import pandas as pd
from tqdm import tqdm
from wasabi import msg
import networkx as nx 
import matplotlib.pyplot as plt
import pickle

def stats(read_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.graphml' in file:
                files.append([os.path.join(r, file),file.replace(".graphml","")])
    print("")
    files.sort()

    #-----------------------------------------------
    stats = []
    errors=[]
    for file in tqdm(range(len(files))):
        path = files[file][0]
        #name = files[file][1]
        #print("\n")
        #msg.info("Parsing: "+ str(name))
        #print("\n")
        try:
            G = nx.read_graphml(path)
            filegr = list(path.replace(".graphml","").split("/"))[1:]
            stats.append((filegr[0],filegr[1],G.number_of_nodes(),G.size()))
        except:
            msg.fail("Problem parsing "+path)
            errors.append(path)
        os.system('clear')
        print('\n\n')
    stats = pd.DataFrame(stats)
    stats.columns=["Label","Graph","Nodes","Edges"]
    stats.groupby(["Label"]).count().to_csv(read_path+"count.csv")
    stats.to_csv(read_path+"stats.csv")
    try:    
        errors = pd.DataFrame(errors)
        errors.columns=["Errors"]
        errors.to_csv(read_path+"errors.csv")
        msg.warn("Some errors encountered while parsing graphs")
    except:
        msg.good("All good!")
        return True

stats("Tweemes/")

def getgroups(read_path):

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.graphml' in file:
                files.append([os.path.join(r, file),file.replace(".graphml","")])
    print("")
    files.sort()

    #-----------------------------------------------
    groups = {}
    for file in tqdm(range(len(files))):
        path = files[file][0]
        aux = path.split("/")[1:]
        #print(aux)
        groups[aux[1].replace(".graphml","")]=aux[0]
    
    with open(read_path+'groups.pickle', 'wb') as handle:
        pickle.dump(groups, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(read_path+'groups.pickle', 'rb') as handle:
        reconstructedgroups = pickle.load(handle)

    if reconstructedgroups == groups:
        msg.info(str(groups))
        msg.good("Groups saved!")
    else:
        msg.wrong("Something went wrong :(")
        os.system("rm "+read_path+"groups.pickle")

getgroups("Tweemes/")


