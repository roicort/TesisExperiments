import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import scipy as sc
import scipy.spatial.distance as ssd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import pickle
from wasabi import msg
import plotly.figure_factory as ff

from pyclustering.cluster.kmedoids import kmedoids
import sklearn.metrics.cluster as met

def DistanceHierarchy(read_path,save_path,groupsfile='../datasets/Tweemes/groups.pickle'):
    try:
        with open(groupsfile, 'rb') as handle:
            groups = pickle.load(handle)
    except:
        print("No groups found. Run Stats First")

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.txt' in file:
                files.append([os.path.join(r, file),file.replace(".txt","")])
    print("")
    files.sort()

    #-----------------------------------------------

    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path, sep="\t")
        names = df[df.columns.values.tolist()[0]][0:].apply(lambda x: x.replace("input//", "").replace(".edges",""))
        df.drop([df.columns.values.tolist()[0]], axis=1, inplace = True)
        df.index = names
        df.columns = names

        mdf = df.to_numpy()

        fig, ax = plt.subplots()
        im = ax.imshow(mdf)

        # We want to show all ticks...
        ax.set_xticks(np.arange(len(names)))
        ax.set_yticks(np.arange(len(names)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(names,{'fontsize': 2})
        ax.set_yticklabels(names,{'fontsize': 2})

        #Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")

        fig.colorbar(im)
        fig.savefig(save_path+name.upper()+"-Distance"+".png",dpi=1500)
        fig.clf()

        # convert the redundant n*n square matrix form into a condensed nC2 array
        X = ssd.squareform(mdf)
        labels = list([ str(name.replace("_"," "))+" - "+str(groups[name.replace("_"," ")]) for name in names.to_numpy()])
        for method in ['single','complete','average','weighted','centroid','median','ward']:
            #Matplotlib
            """Z = hierarchy.linkage(X, method=method,optimal_ordering=True)
            #hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
            hierarchy.dendrogram(Z,labels = labels, orientation="left", color_threshold=9, above_threshold_color='grey', p=12,leaf_font_size=1)
            plt.title('Model: '+name.upper()+' - Method: '+method.upper())
            plt.savefig(save_path+name.upper()+"-"+method.upper()+".dendrogram.svg")
            plt.clf()"""
            #Plotly
            X = mdf
            fig = ff.create_dendrogram(X, orientation='left', labels=labels, linkagefun=lambda alpha: hierarchy.linkage(alpha,method=method,optimal_ordering=True))
            """fig.update_layout(
            width=1024,
            height=1024,
            title_text='Model: '+name.upper()+' - Method: '+method.upper(),
            )"""
            #fig.layout.font.size = 2
            fig.layout.height = 720
            fig.write_html(save_path+name.upper()+"-"+method.upper()+".dendrogram.html")
            
            msg.good(name.upper()+"-"+method+".dendrogram"+ " Saved")
            os.system('clear')
        print('\n\n')
     
    return True

def DistanceKMedoids(read_path,save_path,groupsfile='../datasets/Tweemes/groups.pickle'):

    try:
        with open(groupsfile, 'rb') as handle:
            groups = pickle.load(handle)
    except:
        print("No groups found. Run Stats First")

    #-----------------------------------------------

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.txt' in file:
                files.append([os.path.join(r, file),file.replace(".txt","")])
    print("")
    files.sort()

    #-----------------------------------------------

    globalclusters = {}
    for file in tqdm(range(len(files))):

        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path, sep="\t")
        names = df[df.columns.values.tolist()[0]][0:].apply(lambda x: x.replace("input//", "").replace(".edges",""))
        df.drop([df.columns.values.tolist()[0]], axis=1, inplace = True)
        df.index = names
        df.columns = names

        #print(df)

        mdf = df.to_numpy()
        #print(mdf)

        # Set random initial medoids.
        initial_medoids = [10,20,30,40]
        # create K-Medoids algorithm for processing distance matrix instead of points
        kmedoids_instance = kmedoids(mdf, initial_medoids, data_type='distance_matrix')
        # run cluster analysis and obtain results
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()
        #medoids = kmedoids_instance.get_medoids()

        # Show allocated clusters.
        
        msg.info(name)

        newrep=[]
        for c in range(len(clusters)):
            cluster = clusters[c]
            newrep+=[(names[i],c) for i in cluster]

        skindex = sorted(newrep, key = lambda x: x[0])
        #print("\n\n\t"+"ClustersOrder: "+str(skindex)+"\n")
        globalclusters[name] = skindex
        os.system("clear")

    originalgroupskeys = dict(zip(set(groups.values()),range(len(set(groups.values())))))
    #print(originalgroupskeys)

    #print(groups)

    for key in groups.keys():
        groups[key] = originalgroupskeys[groups[key]]

    orggroup = [(k, v) for k, v in groups.items()] 
    orggroup = sorted(orggroup, key = lambda x: x[0])

    globalclusters["GroundTruth"] = orggroup
    globkeys = list(globalclusters.keys())

    dfClusters = pd.DataFrame(columns=["Names"]+globkeys)
    dfClusters["Names"] = list([a[0] for a in orggroup])
    for k,v in globalclusters.items():
        dfClusters[k]=[a[1] for a in v]
    print("")
    #print(dfClusters)

    dfClusters.to_csv(save_path+"KMedoids-Clusters.csv")

    admultscore = np.zeros((len(globkeys),len(globkeys)))
    multscore = np.zeros((len(globkeys),len(globkeys)))
    randscore = np.zeros((len(globkeys),len(globkeys)))

    print("")
    msg.info("Computing Scores")

    for clusterA in range(len(globkeys)):
        for clusterB in range(len(globkeys)):
            keyA = globkeys[clusterA]
            keyB = globkeys[clusterB]
            A = list(dfClusters[keyA])
            B = list(dfClusters[keyB])
            admultscore[clusterA][clusterB] = met.adjusted_mutual_info_score(A, B)
            multscore[clusterA][clusterB] = met.mutual_info_score(A, B)
            randscore[clusterA][clusterB] = met.adjusted_rand_score(A,B)

    scores = dict(zip(["AdjustedMutualInfoScore","AdjustedRandomScore","MutualInfoScore"],[admultscore,randscore,multscore]))
    msg.good("Scores Done!")

    #print(randscore)
    msg.info("Plotting...")

    for metricname,metricmatrix in scores.items():

        fig, ax = plt.subplots()
        im = ax.imshow(metricmatrix)
        #print(metricmatrix)

        for i in range(len(globkeys)):
            for j in range(len(globkeys)):
                c = metricmatrix[j][i]
                ax.text(i, j, str(c), va='center', ha='center',fontsize = 4)

        # We want to show all ticks...
        ax.set_xticks(np.arange(len(globkeys)))
        ax.set_yticks(np.arange(len(globkeys)))
        # ... and label them with the respective list entries
        ax.set_xticklabels(globkeys,{'fontsize': 4})
        ax.set_yticklabels(globkeys,{'fontsize': 4})

        #Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=90, ha="right",rotation_mode="anchor")

        fig.colorbar(im)
        plt.title(metricname)
        fig.savefig(save_path+metricname+"-KMedoidsVSBaseline.png",dpi=800)
        fig.clf()
        msg.info(metricname+" Done")
    msg.good("Plotting Done!")
    msg.good("All Done!")
    print("")




