import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite


buyers = []
items = []
# Big dataset preparation
with open('../data/test_csv.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        buyers.append(row[6])
        items.append(row[1])

edges = zip(buyers, items)

buyers = list(set(buyers))
items = list(set(items))


# Generate a normal networkx Graph
# Populate with the predefined nodes and edges
Gtemp = nx.Graph()
Gtemp.add_nodes_from(buyers, bipartite = 0)
Gtemp.add_nodes_from(items, bipartite = 1)
Gtemp.add_edges_from(edges)

print(nx.is_connected(Gtemp))

# Create a bipartite graph from the Gtemp classic graph
# bottom_nodes, top_nodes = bipartite.sets(Gtemp)
# G = bipartite.projected_graph(Gtemp, bottom_nodes)

allCommon = []

# Define tuples of nodes1 to feed Common Neighbors Algorithm
for i in range(0, len(buyers) - 1):
    firstNode = buyers[i];
    for j in range(i+1, len(buyers)):
        if buyers[j] != buyers[i]:
            secondNode = buyers[j];
            allCommon.append((firstNode, secondNode))


# Define Lables for the nodes
# This is a feature that helps more on the algorithms testing part.
lables = []
for node in buyers:
    lables.append(node)
for node in items:
    lables.append(node)


# Define Colors for algorithms testing
color_map = []
for node in Gtemp:
    if node in buyers:
        color_map.append('blue')
    else:
        color_map.append('green')



# Compute Common Neighbors Algorithm for Gtemp's nodes
# Pick only nodes which exceed e cartain trashold for the number of CNN
bestResults = []

commonNeighbours = [(cn[0], cn[1], len(list(nx.common_neighbors(Gtemp, cn[0], cn[1])))) for cn in allCommon]
for entry in commonNeighbours:
    if entry[2] > 3:
        bestResults.append(entry)


# Compute node degree for common items of the common neighbors:
print(Gtemp.degree(buyers[0]))

degreeList = []

degreeDict = nx.degree(Gtemp)


for (node, degree) in degreeDict:
    if node in items:
        if degree > 5:
            print('degree: ', degree)
            degreeList.append((node, degree))


print(degreeList)

# print(len(buyers))
# print(len(items))
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
# pos.update( (n, (1, i)) for i, n in enumerate(buyers) ) # put nodes from X at x=1
# pos.update( (n, (2, i)) for i, n in enumerate(items) ) # put nodes from Y at x=2
# nx.draw(Gtemp, node_color = color_map,pos=pos, with_labels =True)
# plt.show()
