from wasabi import msg

from preprocessing import graph2json
from graph2vec import rungraph2vec
from clustering import clustering

log = graph2json('../datasets/twitter','input/')
msg.info(log)
log = rungraph2vec('input/',"output/")
msg.info(log)
log = clustering('output/')
msg.info(log)
