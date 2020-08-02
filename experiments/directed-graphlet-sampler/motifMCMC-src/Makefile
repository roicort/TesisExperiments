LDFLAGS+=-O2 -g
CXXFLAGS+=-O2 -g

.PHONY: clean

motifMCMC-directed: graph.o StringTokenizer.o random.o randomMiner.o randomMining.o dfs.o canonicalcode.o
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	-rm -rf *.o
