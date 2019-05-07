"""
This file "check.py" was made by Jackie Wedgwood for the University of Portsmouth.

This script simply checks the 5-clique count of a graph.

Associated files/folders:
    graph.txt:          adjacency matrix of graph to be checked

Notes:
    This is mainly used to verify graph 5-clique counts, but otherwise has
    no reported use.

Imported module uses:
    The "networkx" module is used for graph functionality.
"""
import networkx as nx

"""
give_K5_cliques(G):
    
    one argument:
        G, the graph to have its 5-clique count found

    return:
        the 5-clique count of G

    This enumerates all the cliques of a graph and its complement and filters the list
    by 5-cliques. The length of both lists are summed and returned.
"""
def give_K5_cliques(G):
    C = [x for x in list(nx.clique.enumerate_all_cliques(G)) if len(x)==5]
    Gc = nx.complement(G)
    Cc = [x for x in list(nx.clique.enumerate_all_cliques(Gc)) if len(x)==5]
    return(len(C)+len(Cc))

"""
main():
    
    no arguments

    no return

    This main loop opens a graph's adjacency matrix file and prints the result of
    give_K5_cliques().
"""
def main():
    G = nx.read_adjlist("graph.txt")
    print(str(give_K5_cliques(G)))

# main call
main()