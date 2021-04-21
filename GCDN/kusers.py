from wasabi import msg
from tqdm import tqdm
import os
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler 

from yellowbrick.cluster import KElbowVisualizer
from yellowbrick.cluster import SilhouetteVisualizer

import matplotlib.pyplot as plt

import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot

import scipy.stats as stats

def users(read_path,save_path):

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
    
    print(aux)
    X = aux.drop(columns=["Network"])
    aux = aux["Network"]

    for column in X:
        X[column] = MinMaxScaler().fit_transform(X[column].values.reshape(-1, 1))

    msg.good("Preprocessing Done")

    z = np.abs(stats.zscore(X))

    XClean = X[(z<4).all(axis=1)]

    print("LenX "+str(len(X)))
    print("LenXClean ="+str(len(XClean)))
    print("Outliers = "+str(len(X)-len(XClean)))

    #Finding-K---------------------------------------------------------

    msg.info("Computing Elbow")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,12))
    visualizer.fit(X)        # Fit the data to the visualizer
    visualizer.show()        # Finalize and render the figure
    plt.savefig(save_path+"ElbowPlotKUsersWON"+".png",dpi=1500)
    msg.good("Elbow Done")
    plt.clf()

    #KMEANS---------------------------------------------------------
    """
    msg.info("Computing KMeans")
    for k in tqdm(range(2,9)):
        kmeans = KMeans(n_clusters=k, n_init=100, init='k-means++',random_state=10,verbose=0,n_jobs=-1)
        kmeans.fit(X)
        centroids = kmeans.cluster_centers_
        inertia = np.array([kmeans.inertia_])
        np.savetxt(save_path+'K'+str(k)+'inertia.out', inertia, delimiter=',') 
        np.savetxt(save_path+'K'+str(k)+'centroids.out', centroids, delimiter=',') 
    msg.good("KMeans Done")
    """
    #TSNE---------------------------------------------------------

    kmeans = KMeans(n_clusters=4, n_init=100, init='k-means++',random_state=10,verbose=0,n_jobs=-1)
    kmeans.fit(X)
    clusters = kmeans.predict(X)
    X["Cluster"] = clusters
    X["Network"] = aux

    msg.info("Computing TSNE")
    
    X_embedded = TSNE(n_components=2).fit_transform(X.drop(columns=["Cluster","Network"]))

    TCs_2d = pd.DataFrame(X_embedded)
    TCs_2d.columns = ["TC1_2d","TC2_2d"]
    TCs_2d.to_csv(save_path+'TSNE-WON.csv')
    
    X["TC1_2d"] = TCs_2d["TC1_2d"]
    X["TC2_2d"] = TCs_2d["TC2_2d"]
    X.to_csv(save_path+'Complete-TSNE-WON.csv')

    cluster1 = X[X["Cluster"] == 0]
    cluster2 = X[X["Cluster"] == 1]
    cluster3 = X[X["Cluster"] == 2]
    cluster4 = X[X["Cluster"] == 3]

    print("C1 Size = "+str(len(cluster1)))
    print("C2 Size = "+str(len(cluster2)))
    print("C3 Size = "+str(len(cluster3)))
    print("C4 Size = "+str(len(cluster4)))

    colors = ["#0396FF","#EA5455","#7367F0","#32CCBC"]

    size = 2.5

    trace1 = go.Scattergl(
                    x = cluster1["TC1_2d"],
                    y = cluster1["TC2_2d"],
                    mode = "markers",
                    name = "Cluster 1",
                    marker = dict(color = colors[0], size = size),
                    text = None)

    trace2 = go.Scattergl(
                        x = cluster2["TC1_2d"],
                        y = cluster2["TC2_2d"],
                        mode = "markers",
                        name = "Cluster 2",
                        marker = dict(color = colors[1],size = size),
                        text = None)

    trace3 = go.Scattergl(
                        x = cluster3["TC1_2d"],
                        y = cluster3["TC2_2d"],
                        mode = "markers",
                        name = "Cluster 3",
                        marker = dict(color = colors[2],size = size),
                        text = None)

    trace4 = go.Scattergl(
                        x = cluster4["TC1_2d"],
                        y = cluster4["TC2_2d"],
                        mode = "markers",
                        name = "Cluster 4",
                        marker = dict(color = colors[3],size = size),
                        text = None)

    data = [trace1, trace2, trace3,trace4]

    title = "Visualizing Clusters in Two Dimensions Using T-SNE"

    layout = dict(title = title,
                xaxis= dict(title= 'TC1',ticklen= 5,zeroline= False),
                yaxis= dict(title= 'TC2',ticklen= 5,zeroline= False)
                )

    fig = go.Figure(dict(data = data, layout = layout))

    fig.write_html(save_path+'TSNE-WON.html')

    msg.good("TSNE Done")

    #---------------------------------------------------------

users("input/","users/")