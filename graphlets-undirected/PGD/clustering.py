import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
from io import StringIO

def clustering(read_path):

    files = []

    for r, d, f in os.walk(read_path):
        for file in f:
            if '.gfd' in file:
                files.append([os.path.join(r, file),file.replace(".gfd","")])
    print("")
    files.sort()

    X = []
    names = []

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        f = open(path, "r")
        txt = f.read()
        dif = txt.split(sep="************************************************************")
        stats = dif[0].replace("[reading generic edge list: read_edge_list func]"," ").replace("=",":")
        count = dif[1].replace("-","").replace("="," ")
        gfd = dif[2].split(sep="--------------------------------------------------------------------------------")
        stats+=gfd[0]
        gfd.pop(0)
        GFD = gfd[0]+gfd[1]
        GFD_connected = gfd[2]+gfd[3]
        GFD_disconnected = gfd[4] + gfd[5] 

        stats = pd.read_csv(StringIO(stats),sep=":",header=None)
        count = pd.read_csv(StringIO(count),sep="\s+",header=None)
        GFD = pd.read_csv(StringIO(GFD),sep="\t",header=0)
        GFD_connected = pd.read_csv(StringIO(GFD_connected),sep="\t",header=0)
        GFD_disconnected = pd.read_csv(StringIO(GFD_disconnected),sep="\t",header=0)

        #print(stats)
        #print(count)
        #print(GFD)
        #print(GFD_connected)
        #print(GFD_disconnected)
        
        X.append(GFD["Graphlet Frequency Distribution (GFD)"].to_numpy())
        names.append(name)

    #-----------------------------------------------

    from matplotlib import pyplot as plt
    from scipy.cluster import hierarchy

    Z = hierarchy.linkage(X, 'ward')
    hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
    hierarchy.dendrogram(Z,labels = names, orientation="left", color_threshold=0.5e15, above_threshold_color='grey', p=12,leaf_font_size=2)
    plt.title('Model: GFD')
    plt.savefig("GFD.png",dpi=1000)

    from sklearn.manifold import TSNE
    X_embedded = TSNE(n_components=2).fit_transform(X)

    from bokeh.io import output_file, save
    from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
    from bokeh.palettes import viridis
    from bokeh.plotting import figure
    from bokeh.transform import transform

    list_x = [point[0] for point in X_embedded]
    list_y = [point[1] for point in X_embedded]
    title = [str(i) for i in names]

    source = ColumnDataSource(data=dict(x=list_x, y=list_y, title=title))
    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ('title', '@title'),
        ("(x,y)", "(@x, @y)"),
    ])
    mapper = LinearColorMapper(palette=viridis(256), low=min(list_y), high=max(list_y))

    p = figure(tools=[hover,"crosshair,pan,wheel_zoom,box_zoom,reset,tap,save"], title="TSNE-PGD")

    p.circle('x', 'y', size=10, source=source,
            fill_color=transform('y', mapper))

    output_file('TSNE-GFD.html')
    save(p)

    return "Done"