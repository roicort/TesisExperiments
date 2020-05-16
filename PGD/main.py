from wasabi import msg

from preprocessing import graph2edges
from pgd import runpgd
from clustering import clustering

log = graph2edges('../datasets/twitter','input/')
msg.info(log)
log = runpgd('input/',"output/")
msg.info(log)
log = clustering('output')
msg.info(log)