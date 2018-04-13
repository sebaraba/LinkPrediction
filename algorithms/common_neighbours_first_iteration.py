import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite


# Define Nodes

nodes1 = [1, 2, 3]
nodes2 = ['A','B','C','D','E']

# Define Edges
edges = [(1,'A'),(1,'B'),(1,'C'),(1,'D'),(2,'B'),(2,'C'),(2,'D'),(3,'C'),(3,'D'),(3,'E')]


# Generate a normal networkx Graph
# Populate with the predefined nodes and edges
Gtemp = nx.Graph()
Gtemp.add_nodes_from(nodes1, bipartite = 0)
Gtemp.add_nodes_from(nodes2, bipartite = 1)
Gtemp.add_edges_from(edges)

# Create a bipartite graph from the Gtemp classic graph
bottom_nodes, top_nodes = bipartite.sets(Gtemp)
G = bipartite.projected_graph(Gtemp, bottom_nodes)

allCommon = []


# Define tuples of nodes1 to feed Common Neighbors Algorithm
for i in range(0, len(nodes1) - 1):
    firstNode = nodes1[i]
    for j in range(i+1, len(nodes1)):
        secondNode = nodes1[j]
        allCommon.append((firstNode, secondNode))


# Define Lables for the nodes
# This is a feature that helps more on the algorithms testing part.
lables = []
for node in nodes1:
    lables.append(node)
for node in nodes2:
    lables.append(node)


# Define Colors for algorithms testing
color_map = []
for node in Gtemp:
    if node in nodes1:
        color_map.append('blue')
    else:
        color_map.append('green')



# Compute Common Neighbors Algorithm for Gtemp's nodes
commonNeighbours = [(cn[0], cn[1], len(list(nx.common_neighbors(Gtemp, cn[0], cn[1])))) for cn in allCommon]
print(commonNeighbours)

# Generate common neighbors as Test
# preds = nx.common_neighbors(Gtemp, 1, 2)
# count = 0
# print('Common neighbors for nodes 1 and 2')
# for p in preds:
#     print(p)
#     count += 1
# print('Number of common neighbors')
# print(count)

# Display the graph
# pos = {}
# pos.update( (n, (1, i)) for i, n in enumerate(nodes1) ) # put nodes from X at x=1
# pos.update( (n, (2, i)) for i, n in enumerate(nodes2) ) # put nodes from Y at x=2
# nx.draw(Gtemp, node_color = color_map,pos=pos, with_labels =True)
# plt.show()
