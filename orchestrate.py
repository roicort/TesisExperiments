
import os
import sys 
from wasabi import msg

if input("Run Stats? (Y/N) ")=="Y":
    msg.info("Running Stats")
    os.chdir("datasets/")
    os.system("python stats.py")
    os.chdir("..")
    msg.good("Finished Running Stats")

if input("Run Embedding Experiment? (Y/N) ")=="Y":
    msg.info("Running Embedding Experiment")
    os.chdir("embeddings/")
    os.system("python main.py")
    os.chdir("..")
    msg.good("Finished Embedding Experiment")

if input("Run GCDN Experiment? (Y/N) ")=="Y":
    msg.info("Running GCDN Experiment")
    os.chdir("GCDN/")
    os.system("python main.py")
    os.chdir("..")
    msg.good("Finished GCDN Experiment")
    
if input("Run Plots? (Y/N) ")=="Y":
    msg.info("Running Plots")
    os.chdir("plots/")
    os.system("python main.py")
    os.chdir("..")
    msg.good("Finished Plotting")

msg.good("All Done")
msg.info("Goodbye :)")
