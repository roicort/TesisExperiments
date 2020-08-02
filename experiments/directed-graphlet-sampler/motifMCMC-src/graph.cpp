/*
 * graph.cpp
 *
 * Created on: Oct 15, 2012
 * Author: Tanay Kumar Saha
 */


#include "graph.h"

using namespace std;

//no vertex with numbering -1 is allowed, no self loop, 
graph::graph()
{
	myverts.clear();
	myedges.clear();
	vertexmap.clear();	
}
graph::~graph()
{
	myverts.clear();
	myedges.clear();
	vertexmap.clear();
}
	
void graph::addVertex(Vertex* v)
{
        myverts.insert(v);
        vertexmap[v->label]=v->globallabel;
}

void graph::addEdge(Edge* E)
{
	myedges.insert(E);
}
/* undir true means undirected , false means directed */
void graph:: updateAdj(Vertex* s, Vertex* t, bool undir)
{
	
	if (s->list.find(t) == s->list.end())  s->list.insert(t);
	if(undir) {
		if(t->list.find(s)==t->list.end())
		{
			t->list.insert(s);
		}
	}
}
void graph:: printAdjacencyList()
{
	std::cout<<"printing Edge Pairs:"<<endl;
	
	for(ConstEdgeSetIterator itx=myedges.begin();itx!=myedges.end();++itx)
	{
	   std::cout<<(*itx)->st->label<<":"<<(*itx)->end->label<<endl;
	}
	std::cout<<endl<<endl;
        
	for(ConstVertexIterator it=myverts.begin();it!=myverts.end();++it)
	{
   	    std::cout<<"label"<<(*it)->label<<"("<<(*it)->globallabel<<")"<<(*it)->parent<<":";
	    for(ConstVertexIterator  it1=(*it)->list.begin();it1!=(*it)->list.end();++it1)
	    {
	      std::cout<<"->"<<(*it1)->label;
	    }
	    std::cout<<endl;
	}	


}
void graph:: printAdjacencyListBig()
{
	size_t length= biggraphvertex.capacity();
	size_t i;

	for(std::vector<Edge*>::iterator itx=ev.begin();itx!=ev.end();++itx)
	{
	   std::cout<<(*itx)->st->label<<":"<<(*itx)->end->label<<endl;
	}
	std::cout<<endl<<endl;
	
	for(i=0;i<length;i++)
	{
   	    std::cout<<"label"<<biggraphvertex[i]->label<<"("<<biggraphvertex[i]->globallabel<<")"<<biggraphvertex[i]->parent<<":";
	    for(ConstVertexIterator  it1=biggraphvertex[i]->list.begin();it1!=biggraphvertex[i]->list.end();++it1)
	    {
	      std::cout<<"->"<<(*it1)->label;
	    }
	    std::cout<<endl;
	}
}
	
