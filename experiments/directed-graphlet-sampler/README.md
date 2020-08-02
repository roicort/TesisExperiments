# Directed Graphlet Sampler

## Installation
To make executable, please run the following command under individual folder.

```
make
```

You can run the code in following way (In this version -undir should always be 1): 

```
./executablename -d [fileName] -i 100000 [iteration no] -s 4 [size] -q 1000 [queue size] -dir 1 
```

## Example Run and corresponding output (0 for out edges, 1 for in edge, 2 for bidirection edge)

```
./motifMCMC-directed -d ../inputfile_maker_mcmcsampler/mal1_dir_graph.txt-mcmc-format  -i 1000 -s 3 -q 1000 -dir 1
#(0,1,1,1,1)(1,2,1,1,1)(2,0,1,1,1)-(0,0,1,)#4|0.004|
#(0,1,1,1,1)(1,2,1,1,1)-(0,0,)#118|0.118|
#(0,1,1,1,1)(1,2,1,1,1)-(1,0,)#256|0.256|
#(0,1,1,1,1)(1,2,1,1,1)-(0,1,)#622|0.622|

```
You may find the code inside graphvisualizer useful for generating directed networks. 




# Reference
If you are using the code for research purposes, please consider citing one of the following paper: 

```
@inproceedings{saha.hasan:15*2,
  title={Finding Network Motifs Using MCMC Sampling.},
  author={Saha, Tanay Kumar and Al Hasan, Mohammad},
  booktitle={CompleNet},
  pages={13--24},
  year={2015}
}


@INPROCEEDINGS{acts, 
  author={Wei Peng and Tianchong Gao and D. Sisodia and T. K. Saha and Feng Li and M. Al Hasan}, 
  booktitle={2016 IEEE Conference on Communications and Network Security (CNS)}, 
  title={ACTS: Extracting Android App topologiCal signature through graphleT Sampling}, 
  year={2016}, 
  pages={37-45}
}
  
```



