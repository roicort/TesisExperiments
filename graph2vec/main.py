from wasabi import msg

from preprocessing import graph2json
from graph2vec import rungraph2vec
from clustering import clustering

log = graph2json('../GraphWeek','data/')
msg.info(log)
log = rungraph2vec('data/',"results/")
msg.info(log)
log = clustering('results/')
msg.info(log)
