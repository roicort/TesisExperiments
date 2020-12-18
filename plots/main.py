from preprocessing import graph2pickle
from plot import runPlot
from wasabi import msg

if graph2pickle("../datasets/Tweemes","input/"):
    msg.good("Reading Done!")
else:
    msg.fail("Something went wrong while reading!")
if runPlot("input/","plots/"):
    msg.good("Plots Done!")
else:
    msg.fail("Something went wrong while plotting!")
