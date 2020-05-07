from wasabi import msg

from preprocessing import graph2edges
from pgd import runpgd
from clustering import clustering

#log = graph2edges('../GraphWeek','data/')
#msg.info(log)
log = runpgd('data/',"results/")
msg.info(log)
log = clustering('results')
msg.info(log)
