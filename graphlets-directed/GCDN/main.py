from wasabi import msg
from preprocessing import graph2edges
from runner import runnerGC, runnerdistances
from clustering import clustering

""" 	

Methods

DGCD-13: Directed graphlet correlation distance using 2- to 3- node directed graphlet orbits #
DGCD-129: Directed graphlet correlation distance using 2- to 4- node directed graphlet orbits 
RDGF: Directed relative graphlet frequency distribution distance 
DGDDA: Directed graphlet degree distribution agreement 
DSD: Directed spectral distance #
IODD: In and Out degree distribution distances #                  

"""

#log = graph2edges('../../datasets/twitter','input/')
#log = runnerGC('input/','logs/')

#log = runnerdistances('input/','logs/',method = "DGCD-129",threads = 32)
#log = runnerdistances('input/','logs/',method = "RDGF",threads = 32)
#log = runnerdistances('input/','logs/',method = "DGDDA",threads = 32)

log = clustering("output/","results/")