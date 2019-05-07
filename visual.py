"""
This file "visual.py" was made by Jackie Wedgwood for the University of Portsmouth.

This script opens any graph in the format of the friends and strangers' theorem by
colouring edges red and creating blue edges on independent pairs of nodes.

Associated files/folders:
    graph.txt:          adjacency list of graph to be visualised

Notes:
    This is used to construct the visualisation in Appendix C, but otherwise has
    no reported use.

Imported module uses:
    The "networkx" module is used for graph functionality.

    The "matplotlib.pyplot" module is used to visualise graphs.
"""
import networkx as nx
import matplotlib.pyplot as plt

# imports graph
G = nx.read_adjlist("graph.txt")
H = nx.complement(G)

# gets graph layouts
Gpos = nx.spring_layout(G)
Hpos = nx.spring_layout(H)

# gets edgelists
red = [x for x in G.edges]
blue = [x for x in H.edges]

# draws nodes and edges
nx.draw_networkx_nodes(G, Gpos, node_size=50, node_color="black")
nx.draw_networkx_nodes(H, Hpos, node_size=50, node_color="black")
nx.draw_networkx_edges(G, Gpos, edgelist=red, edge_color="red")
nx.draw_networkx_edges(H, Hpos, edgelist=blue, edge_color="blue")

# draws graph
plt.axis("off")
plt.show()
