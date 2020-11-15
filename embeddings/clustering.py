import os
from tqdm import tqdm
import scipy as sc
from wasabi import msg
import pickle
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
from sklearn.manifold import TSNE
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.palettes import viridis
from bokeh.plotting import figure
from bokeh.transform import transform

def clustering(read_path,save_path,groupsfile='../datasets/Tweemes/groups.pickle'):

    with open(groupsfile, 'rb') as handle:
        groups = pickle.load(handle)

    files = []

    for r, _, f in os.walk(read_path):
        for file in f:
            if '.pickle' in file:
                files.append([os.path.join(r, file),file.replace(".pickle","")])
    print("")
    files.sort()

    for file in tqdm(range(len(files))):
        path = files[file][0]
        name = files[file][1]

        with open(path, 'rb') as handle:
            embeddings = pickle.load(handle)
            names, X = list(embeddings.keys()), list(embeddings.values())

        Z = hierarchy.linkage(X, 'ward')
        labels = list([ str(name.replace("_"," "))+" - "+str(groups[name.replace("_"," ")]) for name in names])
        hierarchy.set_link_color_palette(['#03396C','#17BEBB','#C82B38','#FFC914','#562999','#76B041'])
        hierarchy.dendrogram(Z,labels = labels, orientation="left", color_threshold=0.5e15, above_threshold_color='grey', p=12,leaf_font_size=1)
        plt.title('Model: '+name)
        plt.savefig(save_path+name+"_dendrogram.svg")
        plt.clf()

        msg.good(name+ " Figure Saved")

        X_embedded = TSNE(n_components=2).fit_transform(X)

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

        p = figure(tools=[hover,"crosshair,pan,wheel_zoom,box_zoom,reset,tap,save"], title="TSNE-"+name)

        p.circle('x', 'y', size=10, source=source,
                fill_color=transform('y', mapper))

        output_file(save_path+'TSNE-'+name+'.html')
        save(p)
        msg.good("TSNE-"+name+" Done")

    return "Done"
