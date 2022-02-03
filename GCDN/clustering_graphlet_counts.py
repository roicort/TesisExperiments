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

from scipy.cluster import hierarchy

import plotly as py
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import plotly.figure_factory as ff

def GraphletHierarchy(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.graphletcounts.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.graphletcounts.txt","")])
    files.sort()

    complete = pd.DataFrame()
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path,sep=" ",names=["Graphlet",name])
        df = pd.pivot_table(df,columns="Graphlet")
        #print(df)
        complete = pd.concat([complete, df])
        #os.system("clear")
        #msg.info(rungdgv)

    for column in complete.columns:
        complete[column] = MinMaxScaler().fit_transform(complete[column].values.reshape(-1, 1))

    embeddings = np.array(complete)

    labels = complete.index.values.tolist()

    for method in ['single','complete','average','weighted','centroid','median','ward']:
        fig = ff.create_dendrogram(embeddings, orientation='left', labels=labels, linkagefun=lambda alpha: hierarchy.linkage(alpha,method=method,optimal_ordering=True))
        fig.update_layout(autosize=True) 
        fig.update_layout(height=700) 
        fig.write_html(save_path+"Graphlet"+"-"+method.upper()+".dendrogram.html")

def GraphletKMeans(read_path,save_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.edges.graphletcounts.txt' in file:
                files.append([os.path.join(r, file),file.replace(".edges.graphletcounts.txt","")])
    files.sort()

    complete = pd.DataFrame()
    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path,sep=" ",names=["Graphlet",name])
        df = pd.pivot_table(df,columns="Graphlet")
        #print(df)
        complete = pd.concat([complete, df])
        #os.system("clear")
        #msg.info(rungdgv)

    for column in complete.columns:
        complete[column] = MinMaxScaler().fit_transform(complete[column].values.reshape(-1, 1))

    #print(complete)

    #Finding-K---------------------------------------------------------

    names = complete.index
    X = complete.to_numpy()

    #print(len(X))

    msg.info("Computing Elbow")
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(2,12))
    visualizer.fit(X)        # Fit the data to the visualizer
    visualizer.show()        # Finalize and render the figure
    plt.savefig(save_path+"Graphlet-ElbowPlot"+".png",dpi=1500)
    msg.good("Elbow Done")
    plt.clf()

    msg.info("Silhouette Elbow")
    model = KMeans()
    visualizer = SilhouetteVisualizer(model, k=(2,12))
    visualizer.fit(X)        # Fit the data to the visualizer
    visualizer.show()        # Finalize and render the figure
    plt.savefig(save_path+"Graphlet-SilhouettePlot"+".png",dpi=1500)
    msg.good("Silhouette Done")
    plt.clf()

    #KMEANS---------------------------------------------------------

    kmeans = KMeans(n_clusters=5, n_init=100, init='k-means++',random_state=10,verbose=1,n_jobs=-1)
    kmeans.fit(X)
    
    labels = kmeans.labels_

    print(kmeans.predict(X))

    lb = dict(zip(names,labels))

    df = pd.DataFrame.from_dict(lb, orient='index')
   
    df.to_csv(save_path+"Graphlet-KMeans.csv")

    #TSNE---------------------------------------------------------

    X_embedded = TSNE(n_components=2).fit_transform(X)

    list_x = [point[0] for point in X_embedded]
    list_y = [point[1] for point in X_embedded]

    source = ColumnDataSource(data=dict(x=list_x, y=list_y, title=names))

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ('title', '@title'),
        ("(x,y)", "(@x, @y)"),
    ])

    #mapper = LinearColorMapper(palette=viridis(256), low=min(list_y), high=max(list_y))

    p = figure(tools=[hover,"crosshair,pan,wheel_zoom,box_zoom,reset,tap,save"], title="TSNE-"+'SimpleKmeans')

    p.circle('x', 'y', size=10, source=source)

    output_file(save_path+'TSNE-'+'Graplets'+'.html')
    save(p)
    msg.good("TSNE Done")

    #---------------------------------------------------------
    return True