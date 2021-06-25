from scipy import cluster
from wasabi import msg
from tqdm import tqdm
import os
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.manifold import TSNE
from sklearn import preprocessing as skp

from yellowbrick.cluster import KElbowVisualizer

import matplotlib.pyplot as plt
import seaborn as sns

import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px

import scipy.spatial.distance as ssd
import scipy.stats as stats
from scipy.cluster import hierarchy as h

from sklearn.metrics.cluster import normalized_mutual_info_score

from gap_statistic import OptimalK


def OptKEmbedding(read_path, save_path, nrefs=5, maxClusters=15):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.signatures.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.signatures.txt","")])
    files.sort()

    msg.info("Preprocessing orbits")
    aux = pd.DataFrame()
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.DataFrame(np.loadtxt(path),index=None)
        df["Network"] = name
        aux = pd.concat([aux, df])
    
    X = aux.drop(columns=["Network"])
    aux = aux["Network"]

    X = X.div(X.sum(axis=1), axis=0) #Normalize

    #for index, row in X.iterrows():
    #    print(sum(row.to_numpy()))

    msg.good("Preprocessing Done")

    #Finding-K---------------------------------------------------------


    msg.info("Computing Distortion")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,12),metric='distortion',timings = True)
    visualizer.fit(X)        
    visualizer.show()        
    plt.savefig(save_path+"Embedding-Distortion-Kusers"+".svg")
    msg.good("Elbow Done")
    plt.clf()

    #msg.info("Computing Silhouette")
    #model = KMeans()
    #visualizer = KElbowVisualizer(model, k=(2,12),metric='silhouette', timings = True)
    #visualizer.fit(X)
    #visualizer.show()  
    #plt.savefig(save_path+"Silhouette-Kusers"+".svg")
    #msg.good("Silhouette Done")
    #plt.clf()

    msg.info("Computing CalinskiHarabasz")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,12),metric='calinski_harabasz', timings = True)
    visualizer.fit(X)
    visualizer.show()  
    plt.savefig(save_path+"Embedding-CalinskiHarabasz-Kusers"+".svg")
    msg.good("CalinskiHarabasz Done")
    plt.clf()

    #X = X.to_numpy()

    """
    
    gaps = np.zeros((len(range(1, maxClusters)),))
    resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
    msg.info("Computing GAP Stats")
    for gap_index, k in enumerate(tqdm(range(1, maxClusters))):

        # Holder for reference dispersion results
        refDisps = np.zeros(nrefs)

        # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
        for i in range(nrefs):
            
            # Create new random reference set
            randomReference = np.random.random_sample(size=X.shape)
            
            # Fit to it
            km = MiniBatchKMeans(k)
            km.fit(randomReference)
            
            refDisp = km.inertia_
            refDisps[i] = refDisp

        # Fit cluster to original data and create dispersion
        km = MiniBatchKMeans(k)
        km.fit(X)

        origDisp = km.inertia_

        # Calculate gap statistic
        gap = np.log(np.mean(refDisps)) - np.log(origDisp)

        # Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap

        resultsdf = resultsdf.append({'clusterCount':k, 'gap':gap}, ignore_index=True)

    KO = gaps.argmax() + 1 

    plt.grid(True)
    plt.plot(resultsdf['clusterCount'], resultsdf['gap'], linestyle='--', marker='o', color='b');
    plt.xlabel('K');
    plt.ylabel('GAP Statistic');
    plt.title('Optimal K Found in K = ' + str(KO));
    plt.savefig(save_path+"GAP-Kusers.svg")
    plt.clf()
    """

    optimalK = OptimalK(parallel_backend='multiprocessing',n_jobs=16)

    optimalK(X, cluster_array=np.arange(1, maxClusters))

    plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df.gap_value, linewidth=3)
    plt.scatter(
        optimalK.gap_df[optimalK.gap_df.n_clusters == optimalK.n_clusters].n_clusters,
        optimalK.gap_df[optimalK.gap_df.n_clusters == optimalK.n_clusters].gap_value,
        s=250,
        c="r",
    )
    plt.grid(True)
    plt.xlabel("Cluster Count")
    plt.ylabel("Gap Stats")
    plt.title("Gap Stats by Cluster Count")
    plt.savefig(save_path+"Embedding-GAPStats-Kusers.svg")
    plt.clf()

    # diff plot
    plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df["diff"], linewidth=3)
    plt.grid(True)
    plt.xlabel("Cluster Count")
    plt.ylabel("Diff Value")
    plt.title("Diff Values by Cluster Count")
    plt.savefig(save_path+"Embedding-GAPDiff-Kusers.svg")
    plt.clf()


    # Gap* plot
    #max_ix = optimalK.gap_df[optimalK.gap_df["gap*"] == optimalK.gap_df["gap*"].max()].index[0]
    #plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df["gap*"], linewidth=3)
    #plt.scatter(
    #    optimalK.gap_df.loc[max_ix]["n_clusters"],
    #    optimalK.gap_df.loc[max_ix]["gap*"],
    #    s=250,
    #    c="r",
    #)
    
    #plt.grid(True)
    #plt.xlabel("Cluster Count")
    #plt.ylabel("Gap* Stats")
    #plt.title("Gap* Stats by Cluster Count")
    #plt.savefig(save_path+"GAP*Stats-Kusers.svg")
    #plt.clf()


    # diff* plot
    #plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df["diff*"], linewidth=3)
    #plt.grid(True)
    #plt.xlabel("Cluster Count")
    #plt.ylabel("Diff* Value")
    #plt.title("Diff* Values by Cluster Count")
    #plt.savefig(save_path+"GAP*Diff-Kusers.svg")
    #plt.clf()

    return True # Plus 1 because index of 0 means 1 cluster is optimal, index 2 = 3 clusters are optimal


def GetMiniBatchKMeans(X,K):

    kmeans = MiniBatchKMeans(n_clusters=K, n_init=1, init='k-means++',random_state=None,verbose=0)
    kmeans.fit(X)

    clusters = kmeans.predict(X)
    #X["Cluster"] = clusters

    #print("Centroids: " + str(kmeans.cluster_centers_))

    #print("Inertia: "+str(kmeans.inertia_))

    #print("Iterations: "+str(kmeans.n_iter_))

    return [clusters,kmeans.inertia_,kmeans.n_iter_]

    #---------------------------------------------------------

def GetStabilityEmbedding(read_path,save_path,runs,K):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.signatures.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.signatures.txt","")])
    files.sort()

    msg.info("Preprocessing orbits")
    aux = pd.DataFrame()
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.DataFrame(np.loadtxt(path),index=None)
        df["Network"] = name
        aux = pd.concat([aux, df])
    
    X = aux.drop(columns=["Network"])
    aux = aux["Network"]

    X = X.div(X.sum(axis=1), axis=0) #Normalize

    msg.good("Preprocessing Done")

   # z = np.abs(stats.zscore(X))

    #XClean = X[(z<4).all(axis=1)]

    #print("LenX "+str(len(X)))
    #print("LenXClean ="+str(len(XClean)))
    #print("Outliers = "+str(len(X)-len(XClean)))

    clusters = []
    inertias = []
    iters = []

    msg.info("Computing MiniBatch")

    for i in tqdm(range(runs)):
        res =  GetMiniBatchKMeans(X,K)
        clusters.append(res[0])
        iters.append(res[2])
        inertias.append(res[1])

    msg.good("MiniBatch Done")

    NMIs = np.zeros((len(clusters),len(clusters)))

    msg.info("Computing NMIs")

    for i in tqdm(range(len(clusters))):
        for j in range(i+1):
            NMIs[i][j] = normalized_mutual_info_score(clusters[i],clusters[j])
    
    msg.good("NMI Done")

    name=str(np.random.randint(0,1000))

    msg.info("Plotting...")

    sns.set(font_scale=0.1)
    sns.heatmap(NMIs, annot=True)
    plt.savefig(save_path+str(K)+"Embedding-NMIs.svg")
    plt.clf()

    fig = go.Figure([go.Bar(x=list(range(len(inertias))), y=inertias)])

    fig.write_html(save_path+str(K)+"Embedding-inertias.html")
    np.savetxt(save_path+str(K)+'Embedding-intertias.out', np.array(inertias), delimiter=',')

    msg.good("Plotting Done")

    nmim = [np.mean(NMIs)]
    print(nmim)

    np.savetxt(save_path+str(K)+'Embedding-NMIsMean.out', np.array(nmim), delimiter=',')

    #print(NMIs)

    return True

def UsersMiniBatchKMeansEmbedding(read_path,save_path, K,seed=None):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.signatures.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.signatures.txt","")])
    files.sort()

    msg.info("Preprocessing orbits")
    aux = pd.DataFrame()
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.DataFrame(np.loadtxt(path),index=None)
        df["Network"] = name
        aux = pd.concat([aux, df])
    
    X = aux.drop(columns=["Network"])
    aux = aux["Network"]

    X = X.div(X.sum(axis=1), axis=0) #Normalize

    msg.good("Preprocessing Done")

    #z = np.abs(stats.zscore(X))

    #XClean = X[(z<4).all(axis=1)]

    #print("LenX "+str(len(X)))
    #print("LenXClean ="+str(len(XClean)))
    #print("Outliers = "+str(len(X)-len(XClean)))

    kmeans = MiniBatchKMeans(n_clusters=K, n_init=500, init='k-means++',random_state=seed,verbose=0)
    kmeans.fit(X)

    clusters = kmeans.predict(X)
    X["Cluster"] = clusters
    X["Network"] = aux
    XS = X[["Network","Cluster"]]

    G = XS.pivot_table(index='Network', columns='Cluster', aggfunc=len,fill_value=0)

    G.to_csv(save_path+str(K)+'-MiniBatchUsersEmbedding.csv')

    msg.good("Clustering Done")

    GNorm = G.div(G.sum(axis=1), axis=0) #Normalize
    GNorm.to_csv(save_path+str(K)+'-NormMiniBatchUsersEmbedding.csv')

    msg.good("Clustering Saved")


    #print("Centroids: " + str(kmeans.cluster_centers_))

    #print("Inertia: "+str(kmeans.inertia_))

    #print("Iterations: "+str(kmeans.n_iter_))

    np.savetxt(save_path+str(K)+'-CentroidsMiniBatchEmbedding.out', kmeans.cluster_centers_, delimiter=',')

    return True



##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################



def OptKClustering(embedding_path, save_path, nrefs=5, maxClusters=12):
    
    X = pd.read_csv(embedding_path)
    nets = X["Network"]
    X = X.drop(columns=["Network"])

    X = X.to_numpy(dtype=np.float64)

    msg.good("Loading.. Done")

    #Finding-K---------------------------------------------------------

    msg.info("Computing Distortion")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,maxClusters),metric='distortion',timings = True)
    visualizer.fit(X)        
    visualizer.show()        
    plt.savefig(save_path+"Cluster-Distortion-Kusers"+".svg")
    msg.good("Elbow Done")
    plt.clf()

    msg.info("Computing Silhouette")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,maxClusters),metric='silhouette', timings = True)
    visualizer.fit(X)
    visualizer.show()  
    plt.savefig(save_path+"Cluster-Silhouette-Kusers"+".svg")
    msg.good("Silhouette Done")
    plt.clf()

    msg.info("Computing CalinskiHarabasz")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,maxClusters),metric='calinski_harabasz', timings = True)
    visualizer.fit(X)
    visualizer.show()  
    plt.savefig(save_path+"Cluster-CalinskiHarabasz-Kusers"+".svg")
    msg.good("CalinskiHarabasz Done")
    plt.clf()


    """

    gaps = np.zeros((len(range(1, maxClusters)),))
    resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
    msg.info("Computing GAP Stats")
    for gap_index, k in enumerate(tqdm(range(1, maxClusters))):

        # Holder for reference dispersion results
        refDisps = np.zeros(nrefs)

        # For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
        for i in range(nrefs):
            
            # Create new random reference set
            randomReference = np.random.random_sample(size=X.shape)
            
            # Fit to it
            km = MiniBatchKMeans(k)
            km.fit(randomReference)
            
            refDisp = km.inertia_
            refDisps[i] = refDisp

        # Fit cluster to original data and create dispersion
        km = MiniBatchKMeans(k)
        km.fit(X)

        origDisp = km.inertia_

        # Calculate gap statistic
        gap = np.log(np.mean(refDisps)) - np.log(origDisp)

        # Assign this loop's gap statistic to gaps
        gaps[gap_index] = gap

        resultsdf = resultsdf.append({'clusterCount':k, 'gap':gap}, ignore_index=True)

    KO = gaps.argmax() + 1 

    plt.grid(True)
    plt.plot(resultsdf['clusterCount'], resultsdf['gap'], linestyle='--', marker='o', color='b');
    plt.xlabel('K');
    plt.ylabel('GAP Statistic');
    plt.title('Optimal K Found in K = ' + str(KO));
    plt.savefig(save_path+"GAP-Kusers.svg")
    plt.clf()
    """

    optimalK = OptimalK(parallel_backend='joblib',n_jobs=32)

    optimalK(X, cluster_array=np.arange(2, maxClusters))

    plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df.gap_value, linewidth=3)
    plt.scatter(
        optimalK.gap_df[optimalK.gap_df.n_clusters == optimalK.n_clusters].n_clusters,
        optimalK.gap_df[optimalK.gap_df.n_clusters == optimalK.n_clusters].gap_value,
        s=250,
        c="r",
    )
    plt.grid(True)
    plt.xlabel("Cluster Count")
    plt.ylabel("Gap Stats")
    plt.title("Gap Stats by Cluster Count")
    plt.savefig(save_path+"Cluster-GAPStats-Kusers.svg")
    plt.clf()

    # diff plot
    plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df["diff"], linewidth=3)
    plt.grid(True)
    plt.xlabel("Cluster Count")
    plt.ylabel("Diff Value")
    plt.title("Diff Values by Cluster Count")
    plt.savefig(save_path+"Cluster-GAPDiff-Kusers.svg")
    plt.clf()


    # Gap* plot
    #max_ix = optimalK.gap_df[optimalK.gap_df["gap*"] == optimalK.gap_df["gap*"].max()].index[0]
    #plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df["gap*"], linewidth=3)
    #plt.scatter(
    #    optimalK.gap_df.loc[max_ix]["n_clusters"],
    #    optimalK.gap_df.loc[max_ix]["gap*"],
    #    s=250,
    #    c="r",
    #)
    
    #plt.grid(True)
    #plt.xlabel("Cluster Count")
    #plt.ylabel("Gap* Stats")
    #plt.title("Gap* Stats by Cluster Count")
    #plt.savefig(save_path+"GAP*Stats-Kusers.svg")
    #plt.clf()


    # diff* plot
    #plt.plot(optimalK.gap_df.n_clusters, optimalK.gap_df["diff*"], linewidth=3)
    #plt.grid(True)
    #plt.xlabel("Cluster Count")
    #plt.ylabel("Diff* Value")
    #plt.title("Diff* Values by Cluster Count")
    #plt.savefig(save_path+"GAP*Diff-Kusers.svg")
    #plt.clf()

    return True # Plus 1 because index of 0 means 1 cluster is optimal, index 2 = 3 clusters are optimal

def GetStabilityClustering(embedding_path,save_path,runs,K):

    X = pd.read_csv(embedding_path)
    nets = X["Network"]
    X = X.drop(columns=["Network"])

    X = X.to_numpy(dtype=np.float64)

    msg.good("Loading.. Done")

   # z = np.abs(stats.zscore(X))

    #XClean = X[(z<4).all(axis=1)]

    #print("LenX "+str(len(X)))
    #print("LenXClean ="+str(len(XClean)))
    #print("Outliers = "+str(len(X)-len(XClean)))

    clusters = []
    inertias = []
    iters = []

    msg.info("Computing MiniBatch")

    for i in tqdm(range(runs)):
        res =  GetMiniBatchKMeans(X,K)
        clusters.append(res[0])
        iters.append(res[2])
        inertias.append(res[1])

    msg.good("MiniBatch Done")

    NMIs = np.zeros((len(clusters),len(clusters)))

    msg.info("Computing NMIs")

    for i in tqdm(range(len(clusters))):
        for j in range(i+1):
            NMIs[i][j] = normalized_mutual_info_score(clusters[i],clusters[j])
    
    msg.good("NMI Done")

    name=str(np.random.randint(0,1000))

    msg.info("Plotting...")

    sns.set(font_scale=0.1)
    sns.heatmap(NMIs, annot=True)
    plt.savefig(save_path+str(K)+"Clustering-NMIs.svg")

    #print(inertias)

    plt.clf()

    fig = go.Figure([go.Bar(x=list(range(len(inertias))), y=inertias)])

    fig.write_html(save_path+str(K)+"Clustering-inertias.html")
    np.savetxt(save_path+str(K)+'Clustering-intertias.out', np.array(inertias), delimiter=',')

    msg.good("Plotting Done")

    #print(NMIs)

    return True

def UsersMiniBatchKMeansClustering(embedding_path,save_path, K,seed=None):

    X = pd.read_csv(embedding_path)
    nets = X["Network"]
    X = X.drop(columns=["Network"])

    #X = X.to_numpy(dtype=np.float64)

    msg.good("Loading.. Done")

    kmeans = MiniBatchKMeans(n_clusters=K, n_init=2000, init='k-means++',random_state=seed,verbose=0)
    kmeans.fit(X)

    clusters = kmeans.predict(X)

    X["Network"] = nets
    X["Cluster"] = clusters

    X.to_csv(save_path+str(K)+'-MiniBatchUsersClustering.csv')

    #print("Centroids: " + str(kmeans.cluster_centers_))

    #print("Inertia: "+str(kmeans.inertia_))

    #print("Iterations: "+str(kmeans.n_iter_))

    np.savetxt(save_path+str(K)+'-CentroidsMiniBatchClustering.out', kmeans.cluster_centers_, delimiter=',')

    return True


def UsersDendrogramClustering(embedding_path,save_path,name=""):

    X = pd.read_csv(embedding_path)
    labels = X["Network"].to_numpy()
    X = X.drop(columns=["Network"])
    X = X.to_numpy(dtype=np.float64)

    msg.good("Loading Done")

    msg.info("Computing Distances")

    SD = ssd.squareform(ssd.pdist(X,metric='cosine'))

    sns.set(font_scale=0.1)
    sns.heatmap(SD, annot=True)
    plt.savefig(save_path+name+"DendrogramDistances-UsersClustering.svg")
    plt.clf()

    msg.good("Distances Done")

    msg.info("Computing Dendrograms")

    for method in ['single','complete','average','weighted','centroid','median','ward']:
        fig = ff.create_dendrogram(X, orientation='left', labels=labels, distfun=lambda alpha: ssd.pdist(alpha,metric='cosine'),linkagefun=lambda alpha: h.linkage(alpha,method=method,optimal_ordering=True))
        fig.layout.width = 1256
        fig.layout.height = 1256
        fig.write_image(save_path+name+"UsersClustering-Dendrogram-"+method+".svg")

    msg.good("Dengrograms Done")

    return True

##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def ViewNetworks(embedding_path,save_path):

    colorscale = py.colors.sequential.Rainbow

    X = pd.read_csv(embedding_path)

    fig1 = px.scatter_3d(X, x='0', y='1', z='2',color='Cluster',hover_name='Network',color_continuous_scale=colorscale)
    fig1.write_html(save_path+"3D-Networks-Viz.html")

    labels = X["Network"]
    clusters = X["Cluster"]

    X = X.drop(columns=["Network","Cluster"])

    X_embedded = TSNE(n_components=2).fit_transform(X)

    X_embedded = pd.DataFrame(X_embedded)

    X_embedded["Network"] = labels
    X_embedded["Cluster"] = clusters

    #print(X_embedded)

    fig2 = px.scatter(X_embedded, x=0, y=1 ,color='Cluster',hover_name='Network',color_continuous_scale=colorscale)
    fig2.update_traces(marker=dict(size=20))
    fig2.write_html(save_path+"2D-Networks-Viz.html")

def AuditCentroids(centroids_path):

    X = np.loadtxt(centroids_path,delimiter=",")
    for c in X:
        aux = sorted(enumerate(c),reverse=True, key=lambda x:x[1])
        print(aux)

    #sort(enumerate(fila),reverse=True, key=lambda x:x[1])

