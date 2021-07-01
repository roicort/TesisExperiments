from wasabi import msg
from preprocessing import graph2edges
from runner import parallelrunnerGC, runnerdistances
#from clustering_distances import DistanceHierarchy, DistanceKMedoids
#from clustering_graphlets import GraphletKMeans, GraphletHierarchy
from clustering_users import UsersMiniBatchKMeansEmbedding, GetStabilityEmbedding, OptKEmbedding, OptKClustering, AuditCentroids
from clustering_users import GetStabilityClustering, UsersMiniBatchKMeansClustering, UsersDendrogramClustering, ViewNetworks, ColorNetworks
import shutil

from correlations import GraphletCorrelations

########################################################################

#Preprocessing

#if graph2edges('../datasets/Tweemes','input/'):
#    msg.good("Preprocessing Done")

########################################################################

#PreCompute

#if parallelrunnerGC('input/','logs/',threads=24):
#    msg.good("Parallel precompute done")

########################################################################

#Compute Distances

"""
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

#if OptKEmbedding("input/","stability/"):
#    msg.good("GAP Done")

if GetStabilityEmbedding("input/","stability/",runs=50,K=5):
    msg.good("Embedding Stability Done")

#if UsersMiniBatchKMeansEmbedding("input/","users/",K=5):
#    msg.good("KMeans Embedding Done!")

#OptKClustering("users/5-MiniBatchUsersEmbedding.csv","stability/")

#if GetStabilityClustering("users/4-MiniBatchUsersEmbedding.csv","stability/",runs=50,K=3):
#    msg.good("NetworkClustering Stability Done")

#UsersDendrogramClustering("users/5-MiniBatchUsersEmbedding.csv","users/")

#UsersDendrogramClustering("users/5-NormMiniBatchUsersEmbedding.csv","users/", name = "Norm")

#UsersMiniBatchKMeansClustering("users/5-MiniBatchUsersEmbedding.csv","users/", K=5)

########################################################################

#Others

#GraphletCorrelations("input/","correlations/")

#ViewNetworks("users/4-MiniBatchUsersClustering.csv","users/")

#AuditCentroids("users/3-CentroidsMiniBatchEmbedding.out")

#ColorNetworks("input/","users/5-CompleteMiniBatchUsers.csv","colored/")


