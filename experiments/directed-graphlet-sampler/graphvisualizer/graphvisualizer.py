import os;
import sys;
import subprocess;

from igraph import *;



fileToRead=open(sys.argv[1]);
size= int (sys.argv[2]);
count=1;
all_edge_tuples = [];
directions = [];


for	line 	in	 fileToRead:
	if	line.startswith("#"):
		codeline=line[line.find("#")+1: line.rfind("#")];
		g=Graph(directed=True);
		g.add_vertices (size-1);


		# get all the edges 
		codestring = codeline [: codeline.find("-")];
		codesplitted = codestring.strip().split (")");
		for	pos	in	range (0,len(codesplitted)-1):
			code_ = codesplitted[pos][1:];
			edge_tuple = code_.split (",");
			all_edge_tuples.append ((int(edge_tuple[0]), int(edge_tuple[1])));

		# get all the directions
		dirline = codeline [ codeline.find("-")+1: ];
		dirline = dirline [1:-1];
		dirlinetuples = dirline.split (",");

		for	pos	in	range (0,len(all_edge_tuples)):
			directions.append (int(dirlinetuples[pos]));

	

		print all_edge_tuples;
		#print directions;

		#print directions;
		print g;	


		for	pos	in	range (0,len (directions)):
			# this is an in edge 
			if	directions[pos] ==1 :
				g.add_edges ((all_edge_tuples[pos][1], all_edge_tuples[pos][0]));	

			# this is an out edge
			elif	directions [pos] == 0:
				g.add_edges ((all_edge_tuples[pos][0], all_edge_tuples[pos][1]));	
			else:
				g.add_edges ((all_edge_tuples[pos][0], all_edge_tuples[pos][1]));	
				g.add_edges ((all_edge_tuples[pos][1], all_edge_tuples[pos][0]));	

			print g;	

		filetosave=str(size)+"-"+str(count)+".pdf";
		plot(g,filetosave,layout= "fr");
		
		count=count+1;
