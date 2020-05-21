from wasabi import msg

from preprocessing import graph2pickle

from models import runG2Vec
from models import runSF
from models import runNetLSD
from models import runGL2Vec
from models import runGeoScattering

from plot import runPlot
from clustering import clustering

#data = graph2pickle('../datasets/twitter','input/')

logs = open("logs.txt", "a")
time = runG2Vec('input/',"outputs/")
print("G2V running time: %s" % time, file=logs)
logs.close()

"""logs = open("logs.txt", "a")
time = runSF('input/',"outputs/")
print("SF running time: %s" % time, file=logs)
logs.close()

logs = open("logs.txt", "a")
time = runNetLSD('input/',"outputs/")
print("NetLSD running time: %s" % time, file=logs)
logs.close()

logs = open("logs.txt", "a")
time = runGL2Vec('input/',"outputs/")
print("GL2V running time: %s" % time, file=logs)
logs.close()

logs = open("logs.txt", "a")
time = runGeoScattering('input/',"outputs/")
print("GeoScattering running time: %s" % time, file=logs)
logs.close()"""

cluster = clustering("outputs/","results/")
#plots = runPlot('input/',"plots/")