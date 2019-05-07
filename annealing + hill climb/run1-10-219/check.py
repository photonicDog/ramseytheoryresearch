import networkx as nx

def give_K5_cliques(G):
    C = [x for x in list(nx.clique.enumerate_all_cliques(G)) if len(x)==5]
    Gc = nx.complement(G)
    Cc = [x for x in list(nx.clique.enumerate_all_cliques(Gc)) if len(x)==5]
    return(len(C)+len(Cc))

def main():
    G = nx.read_adjlist("new.txt")
    print(str(give_K5_cliques(G)))