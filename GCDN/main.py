from wasabi import msg
from preprocessing import graph2edges
from runner import runnerGC, runnerdistances, parallelrunnerGC
from clustering_distances import DistanceHierarchy, DistanceKMedoids
from clustering_graphlets import GraphletKMeans, GraphletHierarchy
from clustering_users import UsersKMeans, UsersHierarchy
import shutil

from correlations import GraphletCorrelations

"""

########################################################################

#Preprocessing

if graph2edges('../datasets/Tweemes','input/'):
    msg.good("Preprocessing Done")

########################################################################

#PreCompute

if parallelrunnerGC('input/','logs/',threads=32):
    msg.good("Parallel precompute done")

########################################################################

#Compute Distances

#Methods

# DGCD-13: Directed graphlet correlation distance using 2- to 3- node directed graphlet orbits #
# DGCD-129: Directed graphlet correlation distance using 2- to 4- node directed graphlet orbits
# DRGF: Directed relative graphlet frequency distribution distance
# DGDDA: Directed graphlet degree distribution agreement
# DSD: Directed spectral distance #
# IODD: In and Out degree distribution distances #


if runnerdistances('input/','logs/',method = "DGCD-129",threads = 32):
    shutil.move('input/DGCD-129.txt', 'distancematrix/DGCD-129.txt')
    msg.good("DGCD-129 Done!")

if runnerdistances('input/','logs/',method = "RDGF",threads = 32):
    shutil.move('input/RDGF.txt', 'distancematrix/RDGF.txt')
    msg.good("RDGF Done!")

if runnerdistances('input/','logs/',method = "DGDDA",threads = 32):
    shutil.move('input/gdda.txt', 'distancematrix/gdda.txt')
    shutil.move('input/gddg.txt', 'distancematrix/gddg.txt')
    msg.good("DGDDA Done!")

######################################################################## """

#ByDistance

#if DistanceHierarchy("distancematrix/","distances/"):
#    msg.good("DistanceHierarchy Done!")

#if DistanceKMedoids("distancematrix/","distances/"):
#    msg.good("DistanceKMedoids Done!")

########################################################################

#ByGraphletCounts

#if GraphletKMeans("input/","graphlets/"):
#    msg.good("GraphletKMeans Done!")

#if GraphletHierarchy("input/","graphlets/"):
#    msg.good("GraphletHierarchy Done!")

########################################################################

#ByUsers

#if UsersKMeans("input/","users/"):
#    msg.good("UsersKMeans Done!")
#if UsersHierarchy("input/","users/"):
#    msg.good("UsersHierarchy Done!")

########################################################################

GraphletCorrelations("input/","correlations/")