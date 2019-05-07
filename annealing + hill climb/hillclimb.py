"""
This file "hillclimb.py" was made by Jackie Wedgwood for the University of Portsmouth.

This constitutes the hill climbing algorithm of this project.

Associated files/folders:
    graph.txt:          adjacency matrix of initial graph
    new.txt:            adjacency matrix of best currently found graph
    0.txt:              if found, adjacency matrix of (5,5,43)-graph

Notes:
    This algorithm is rather simple, and is mentioned briefly in Chapter 4.2.

Imported module uses:
    The "networkx" module is used for graph functionality and computation.
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
change_edge(G,node1,node2):
    
    three arguments:
        G, the graph being modified
        node1, the first node
        node2, the second node

    return:
        the modified graph

    Two nodes of a graph are taken and it is checked if they contain an edge
    together. If they do, that edge is removed, otherwise it is created. The
    new graph is returned.
"""
def change_edge(G,node1,node2):
    if G.has_edge(node1,node2) == True:
        G.remove_edge(node1,node2)
    else:
        G.add_edge(node1,node2)
    return(G)

"""
hillclimb(G,cliques):
    
    two arguments:
        G, the initial graph being modified
        cliques, number of cliques of initial graph

    return:
        the modified graph if any improvements are found, otherwise G

    First, the nodes list of G is found. Then, the function cycles through every pairing
    of nodes, by generating a graph where that pair of nodes has an edge changed (see change_edge()
    for details). If the new clique count is lower, the newly generated graph is returned.
    Otherwise, the loop continues. The initial compared node is popped so no neighbouring graphs
    are repeated.
"""
def hillclimb(G,cliques):
    nodes_list = list(G.nodes())
    while len(nodes_list) != 0:
        node1 = nodes_list.pop()
        for node2 in nodes_list:
            H = G.copy()
            H = change_edge(H,node1,node2)
            cliquesH = give_K5_cliques(H)
            if cliquesH < cliques:
                nx.write_adjlist(G,"new.txt")
                return(H)
    return(G)

"""
main():
    
    no arguments

    no return

    The initial graph to be modified is opened and its cliques count is found. Then, the loop of hill
    climbing is started. A copy of the graph is run through hill climbing. If it returns and has an 
    equal 5-clique count (i.e., no progress is made), then a peak has been reached and the loop saves
    this graph and exits. Otherwise, this graph is run through hill climbing again, until above condition
    is met, or until the 5-clique count reaches zero, upon which the graph will be saved as "0.txt" instead.
"""
def main():
    G = nx.read_adjlist("graph.txt")
    cliques = give_K5_cliques(G)
    while cliques != 0:
        newG = hillclimb(G,cliques)
        G = newG.copy()
        cliquesN = give_K5_cliques(G)
        if cliques == cliquesN:
            nx.write_adjlist(G,"new.txt")
            exit()
        else:
            cliques = cliquesN
    nx.write_adjlist(G,"0.txt")

# main call
main()