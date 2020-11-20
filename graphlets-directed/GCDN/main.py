from wasabi import msg
from preprocessing import graph2edges
from runner import runnerGC, runnerdistances
from clustering import clustering
import shutil

"""
Methods

DGCD-13: Directed graphlet correlation distance using 2- to 3- node directed graphlet orbits #
DGCD-129: Directed graphlet correlation distance using 2- to 4- node directed graphlet orbits
DRGF: Directed relative graphlet frequency distribution distance
DGDDA: Directed graphlet degree distribution agreement
DSD: Directed spectral distance #
IODD: In and Out degree distribution distances #
"""

if graph2edges('../../datasets/Tweemes','input/'):
    msg.good("Preprocessing Done")
if runnerGC('input/','logs/'):
    msg.good("Precompute Done")
if runnerdistances('input/','logs/',method = "DGCD-129",threads = 32):
    shutil.move('input/DGCD-129.txt', 'output/DGCD-129.txt')
    msg.good("DGCD-129 Done!")
if runnerdistances('input/','logs/',method = "RDGF",threads = 32):
    shutil.move('input/RDGF.txt', 'output/RDGF.txt')
    msg.good("RDGF Done!")
if runnerdistances('input/','logs/',method = "DGDDA",threads = 32):
    shutil.move('input/gdda.txt', 'output/gdda.txt')
    shutil.move('input/gddg.txt', 'output/gddg.txt')
    msg.good("DGDDA Done!")
if clustering("output/","results/"):
    msg.good("Clustering Done!")

