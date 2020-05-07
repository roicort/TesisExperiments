import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg

def clustering(read_path):

    files = []

    for r, d, f in os.walk(read_path):
        for file in f:
            if '.txt' in file:
                files.append([os.path.join(r, file),file.replace(".txt","")])
    print("")
    files.sort()

    X = []
    names = []

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]
        df = pd.read_csv(path,header=None,delimiter=" ")
        X.append(df[1].to_numpy())
        names.append(name)

    #-----------------------------------------------

    from matplotlib import pyplot as plt
    from scipy.cluster import hierarchy

    Z = hierarchy.linkage(X, 'ward')
    hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
    hierarchy.dendrogram(Z,labels = names, orientation="left", color_threshold=0.5e15, above_threshold_color='grey', p=12,leaf_font_size=2)
    plt.title('Model: PGD')
    plt.savefig("PGD.png",dpi=1000)

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

    output_file('TSNE-PGD.html')
    save(p)

    return "Done"