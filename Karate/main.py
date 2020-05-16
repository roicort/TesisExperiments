from wasabi import msg

from preprocessing import graph2pickle
from GL2Vec import runGL2Vec

#log = graph2pickle('../datasets/twitter','input/')
log = runGL2Vec('input/',"outputs/")
