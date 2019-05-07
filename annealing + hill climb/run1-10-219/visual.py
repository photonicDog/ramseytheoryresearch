import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_adjlist("new.txt")
H = nx.complement(G)
Gpos = nx.spring_layout(G)
Hpos = nx.spring_layout(H)
red = [x for x in G.edges]
blue = [x for x in H.edges]
nx.draw_networkx_nodes(G, Gpos, node_size=50, node_color="black")
nx.draw_networkx_nodes(H, Hpos, node_size=50, node_color="black")
nx.draw_networkx_edges(G, Gpos, edgelist=red, edge_color="red")
nx.draw_networkx_edges(H, Hpos, edgelist=blue, edge_color="blue")

plt.axis("off")
plt.show()
