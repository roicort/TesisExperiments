import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import networkx as nx
import scipy as sc
from wasabi import msg
import pickle

def clustering(read_path):

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.csv' in file:
                files.append([os.path.join(r, file),file.replace(".csv","")])
    print("")
    files.sort()

    X = []
    names = []

    with open("dictnames" + '.pickle', 'rb') as f:
        dictnames = pickle.load(f)
    for file in tqdm(range(len(files))):
        path = files[file][0]
        df = pd.read_csv(path,delimiter=",")
        df['type'].replace(dictnames, inplace=True)
        for _, row in df.iterrows():
            nmpy = row.to_numpy()
            X.append(nmpy[1:])
            names.append(nmpy[0])

    print(names)
    #-----------------------------------------------

    from matplotlib import pyplot as plt
    from scipy.cluster import hierarchy

    Z = hierarchy.linkage(X, 'ward')
    hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
    hierarchy.dendrogram(Z,labels = names, orientation="left", color_threshold=2, above_threshold_color='grey', p=12,leaf_font_size=2)
    plt.title('Model: G2V')
    plt.savefig("G2V.png",dpi=1000)

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

    p = figure(tools=[hover,"crosshair,pan,wheel_zoom,box_zoom,reset,tap,save"], title="TSNE-G2V")

    p.circle('x', 'y', size=10, source=source,
            fill_color=transform('y', mapper))

    output_file('TSNE-G2V.html')
    save(p)

    return "Done"
