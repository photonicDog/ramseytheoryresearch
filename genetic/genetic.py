"""
This file "genetic.py" was made by Jackie Wedgwood for the University of Portsmouth.

This constitutes the genetic algorithm of this project.

Associated files/folders:
    graphs folder:      holds data set (current generation) of graphs
    graphs/[num.txt]:   individual graph of data set
    cliques.txt:        file holding fitness values of every graph in data set
    fitness_log.txt:    log of best fitness value of each generation
    best.txt:           adjacency list of the best graph from the data set
    found.txt:          if found, an adjacency list of a (5,5,43)-graph

Notes:
    This algorithm is more detailed in the report, and uses terminology from
    said report. Details can be found in Chapter 4.1.

Imported module uses:
    The "networkx" module is used for graph functionality and computation.

    The "random" module is used during a genetic step to make mutations and
    recombinations random.

    The "scipy.sparse" module is used in tandem with "networkx", as graphs
    are recorded as sparse matrices when recombined.

    The "pathlib" module is just used to check if a set of graphs already
    exists in the main loop.
"""
import networkx as nx
import random
import scipy.sparse as scs
from pathlib import Path

"""
initial_sampling(num):

    one argument:
        num, used to record graph placement when writing to file for
        "cliques.txt" (for finding minimal current fitness values (number
        of 5-cliques) to be recombined)

    return:
        an int consisting of the total amount of 5-cliques in both the
        graph and its compliment 

    Generates a random subgraph of K43 (a subgraph of K43 can have up to 903
    edges, but the bounds are reduced to 200-703, explained in the report). The
    5-cliques of it and its compliment are found and counted, and then saved as
    an adjecency matrix to a text file with the number designated in the "graphs"
    folder, where they are kept for generating offspring.
"""
def initial_sampling(num):
    G = nx.gnm_random_graph(43,(random.randint(200,703)))
    C = [x for x in list(nx.clique.enumerate_all_cliques(G)) if len(x)==5]

    Gc = nx.complement(G)
    Cc = [x for x in list(nx.clique.enumerate_all_cliques(Gc)) if len(x)==5]
    
    nx.write_adjlist(G,"graphs/"+str(num)+".txt")
    return(len(C)+len(Cc))


"""
generate_set(limit):

    one argument:
        limit, used to define how many graphs should be generated

    return:
        none

    This generates an initial set of graphs, and references initial_sampling to
    build each graph with each number given. "cliques.txt" records each graph's
    number and its fitness value.
"""
def generate_set(limit):
    f = open("cliques.txt","w+")
    cliques_list = []

    for i in range(0,limit):
        cliques_list.append((i,initial_sampling(i)))
    for c in cliques_list:
        f.write(str(c)+"\n")

    f.close()


"""
offspring_set(graphs):

    one argument:
        graphs, a set of graph indices that will be parents to offspring

    return:
        the new set of graphs after genetic operations

    This function creates offspring from a generation set of graphs. This is done
    via mutation, where up to 20 edges are inverted (either added or removed), or
    via crossover, where up to 8 points are selected on two matrices and are crossed
    over across both. Details on this and the different types of sparse matrix used
    are explained in the report. Graph indices removed from the pool when used to generate
    offspring, and are used to open the numbered graph in the graphs folder. The offspring
    these generate are appended to an array which becomes the return of this function.
"""
def offspring_set(graphs):
    offspring = []
    cross_count = random.randint(2,len(graphs)-2)
    mutate_count = len(graphs) - cross_count

    for i in range(mutate_count):
        graph = random.choice(graphs)
        G = nx.read_adjlist("graphs/"+str(graph)+".txt")
        M = scs.lil_matrix(nx.to_scipy_sparse_matrix(G))
        for i in range(random.randint(1,20)):
            M[random.randint(0,M.shape[0]-1),random.randint(0,M.shape[1]-1)] ^= 1
        H = nx.from_scipy_sparse_matrix(scs.csr_matrix(M))
        offspring.append(H)

    for i in range(int(cross_count/2)):
        x = random.randint(2,8)

        graph1 = random.choice(graphs)
        graph2 = random.choice(graphs)

        G1 = nx.read_adjlist("graphs/"+str(graph1)+".txt")
        G2 = nx.read_adjlist("graphs/"+str(graph2)+".txt")

        M1 = nx.to_scipy_sparse_matrix(G1)
        M2 = nx.to_scipy_sparse_matrix(G2)

        cuts_h = []
        cuts_i = []
        lim = 0

        for i in range(x,0,-1):
            if i == 1:
                cut = 43
            else:
                cut = random.randint(lim+1,43-i)
                if cut == lim:
                    cut += 1

            if i % 2 == 0:
                cuts_h.append(M1[range(lim,cut)])
                cuts_i.append(M2[range(lim,cut)])
            else:
                cuts_h.append(M2[range(lim,cut)])
                cuts_i.append(M1[range(lim,cut)])
            lim = cut

        MH = scs.vstack(cuts_h)
        MI = scs.vstack(cuts_i)
        H = nx.from_scipy_sparse_matrix(MH)
        I = nx.from_scipy_sparse_matrix(MI)
        offspring.append(H)
        offspring.append(I)

    return offspring

"""
sort_set():

    no arguments

    return:
        a set of fitness values along with their graph indices sorted by fitness value

    This function imports the cliques file, which is a list of tuples that hold the index
    of the graph along with its fitness value (clique count). Then these are sorted by
    fitness value and returned.
"""
def sort_set():
    f = open("cliques.txt","r")
    cliques_unsorted = []

    for c in f.readlines():
        cliques_unsorted.append(eval(c))

    cliques_sorted = sorted(cliques_unsorted, key=lambda x:x[1])
    f = open("fitness_log.txt","a+")
    f.write(str(cliques_sorted[0][1])+"\n")
    f.close()
    return cliques_sorted

"""
new_set():

    one argument:
        graphs, the set of tuples containing graph indices and fitness values from the
        last generation

    return:
        the next generation of graphs

    This takes the indices of the fitter half of the generation of graphs after being
    sorted in sort_set(), and then these are used to generate offspring via offspring_set().
    The parent indices are then used to import said graphs from the graphs folder, and are
    appended to an array. These two arrays are joined together to make the next generation.
"""
def new_set(graphs):
    parents = [x[0] for x in graphs[:(len(graphs)//2)]]
    offspring = offspring_set(parents)
    parent_graphs = []
    for graph in parents:
        parent_graphs.append(nx.read_adjlist("graphs/"+str(graph)+".txt"))
    new_set = offspring + parent_graphs
    return new_set

"""
give_K5_cliques(G):
    
    one argument:
        G, the graph to have its fitness value found

    return:
        the fitness value (5-clique count) of G

    This enumerates all the cliques of a graph and its complement and filters the list
    by 5-cliques. The length of both lists are summed and returned.
"""
def give_5-cliques(G):
    C = [x for x in list(nx.clique.enumerate_all_cliques(G)) if len(x)==5]
    Gc = nx.complement(G)
    Cc = [x for x in list(nx.clique.enumerate_all_cliques(Gc)) if len(x)==5]
    return (len(C)+len(Cc))

"""
main(size,N):

    two arguments:
        size, the size of an initial data set generated if any
        N, the number of iterations of the algorithm

    no return

    The main loop of the algorithm. This checks if a data set exists, if not it generates
    a set. The main loop gets the sorted list of graph indices through sort_set(). A check
    is made to see if the best graph found has a fitness value of 0, upon which "found.txt"
    is saved as an adjancency matrix of that graph and the loop exists (i.e. this would be
    a (5,5,43)-graph). Otherwise, the next offspring set is generated, the fitness values
    of each are found and these are formed with the index of each graph into a list of tuples
    which form cliques.txt.

    Once the main loop ends, the final generation's cliques.txt file is created and the best
    graph of the generation is found and written as "best.txt".
"""
def main(size,N):
    if not Path("graphs/0.txt").exists():
        generate_set(size)
    for i in range(0,N):
        main_set = sort_set()
        if main_set[0][1] == 0:
            G = nx.read_adjlist("graphs/"+str(main_set[0][0])+".txt")
            nx.write_adjlist(G,"found.txt")
            exit()
        next_set = new_set(main_set)
        cliques = []
        for j in range(len(next_set)):
            nx.write_adjlist(next_set[j],"graphs/"+str(j)+".txt")
            cliques.append((j,give_K5_cliques(next_set[j])))
        f = open("cliques.txt","w+")
        for c in cliques:
            f.write(str(c)+"\n")
        f.close()
    main_set = sort_set()
    best = nx.read_adjlist("graphs/"+str(main_set[0][0])+".txt")
    nx.write_adjlist(best,"best.txt")

# main call
main(1000,500)