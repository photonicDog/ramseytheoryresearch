"""
This file "annealing.py" was made by Jackie Wedgwood for the University of Portsmouth.

This constitutes the simulated annealing algorithm of this project.

Associated files/folders:
    graph.txt:          adjacency list of initial graph
    best.txt:           adjacency list of best currently found graph

Notes:
    This algorithm is more detailed in the report, and uses terminology from
    said report. Details can be found in Chapter 4.2.

    Run folders are designated as: run[index]-[genetic run index]-[final 5-clique count].

Imported module uses:
    The "networkx" module is used for graph functionality and computation.

    The "random" module is used to generate a random number when deciding
    whether to transition to a neighbour state.

    The "math" module is used for the natural exponent function.

    The "decimal" module is used for the Decimal type for accurate calculations
    during the annealing process.
"""
import networkx as nx
import random
import math
from decimal import Decimal

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
annealing(G1, temp):
    
    two arguments:
        G1, the initial state
        temp, the current temperature of the system

    return:
        the new active state (graph)

    This gets a new graph with a random swapped edge which becomes the neighbour state,
    and checks to see if it has less cliques. If it does, it becomes the new active state,
    and is checked against the best recorded graph. If not, a value using the formula
    exp(cliques difference/temp) is calculated, and measured against a random number between
    0 and 1. If it is higher, it becomes the new active state anyway, otherwise nothing changes.
"""
def annealing(G1, temp):
    nodes = list(G1.nodes())
    random.shuffle(nodes)
    node1 = nodes.pop()
    node2 = nodes.pop()
    G2 = change_edge(G1.copy(),node1,node2)
    cliques1 = give_K5_cliques(G1)
    cliques2 = give_K5_cliques(G2)
    if cliques2 < cliques1:
        write_best(G2)
        return(G2)
    else:
        write_best(G1)
        annealing = math.exp((cliques1 - cliques2) / temp)
        if annealing > random.random():
            return(G2)
        else:
            return(G1)

"""
find_new_graph(G):
    
    one argument:
        G, the initial graph in graph.txts

    return:
        the final result of this simulated annealing run

    This checks to see if the system has cooled yet, and comprises the main loop
    of the algorithm. It sets the temperature to 5, and starts the loop. If the
    temperature has reached 0, it breaks loop and returns, otherwise it goes
    through the annealing() function and the temperature decreases by the cooling
    rate of 0.00001, and loops again.
"""
def find_new_graph(G):
    temp = Decimal(5)
    while temp <= 0:
        G = annealing(G, temp)
        temp -= Decimal(0.00001)
    return(G)
            
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
write_best(G):
    
    one argument:
        G, the graph to be compared to the current best

    no return

    The best graph is read from a file, and the 5-clique count of it and G are
    found. If G has a higher 5-clique count, it overwrites best.txt and becomes
    the new best saved graph
"""
def write_best(G):
    best = nx.read_adjlist("graphs/best.txt")
    if give_K5_cliques(G) < give_K5_cliques(best):
        nx.write_adjlist(G,"graphs/best.txt")

"""
main():
    
    no arguments

    no return

    Reads the initial graph and starts the main algorithm loop
"""
def main():
    G = nx.read_adjlist("graphs/graph.txt")
    while True:
        G = find_new_graph(G)

# main call
main()