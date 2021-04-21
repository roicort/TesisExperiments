from wasabi import msg

from preprocessing import graph2pickle

from models import runG2Vec
from models import runSF
from models import runNetLSD
from models import runGL2Vec
from models import runGeoScattering
from models import size_only

from distance import compute_distance
from clustering import clustering

data = graph2pickle('../datasets/Tweemes','input/')

time = size_only('input/',"outputs/")

logs = open("logs.txt", "a")
time = runG2Vec('input/',"outputs/")
print("G2V running time: " + str(time), file=logs)
logs.close()

logs = open("logs.txt", "a")
time = runSF('input/',"outputs/")
print("SF running time: " + str(time), file=logs)
logs.close()

logs = open("logs.txt", "a")
time = runNetLSD('input/',"outputs/")
print("NetLSD running time: " + str(time), file=logs)
logs.close()

"""logs = open("logs.txt", "a")
time = runGL2Vec('input/',"outputs/")
print("GL2V running time: " + str(time), file=logs)
logs.close()"""

logs = open("logs.txt", "a")
time = runGeoScattering('input/',"outputs/")
print("GeoScattering running time: " + str(time), file=logs)
logs.close()

distance = compute_distance("outputs/","distance/")
cluster = clustering("outputs/","results/")
