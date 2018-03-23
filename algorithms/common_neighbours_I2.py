import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite


# We work with two types of nodes:
# 1. Buyer nodes (buyers)
# 2. Item nodes (items)

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


# Create a bipartite graph from the Gtemp classic graph
# bottom_nodes, top_nodes = bipartite.sets(Gtemp)
# G = bipartite.projected_graph(Gtemp, bottom_nodes)

testCommonNeighbors = []

# Define tuples of nodes to feed Common Neighbors Algorithm
for i in range(0, len(buyers) - 1):
    firstNode = buyers[i];
    for j in range(i+1, len(buyers)):
        if buyers[j] != buyers[i]:
            secondNode = buyers[j];
            testCommonNeighbors.append((firstNode, secondNode))


# Define Lables for the nodes
# This is a feature that helps more on the algorithms testing part.
lables = []
for node in buyers:
    lables.append(node)
for node in items:
    lables.append(node)


# Compute Common Neighbors Algorithm for Gtemp's nodes
# Pick only nodes which exceed e cartain trashold for the number of CNN
bestCommonNeighbors = []

commonNeighbors = [(cn[0], cn[1], len(list(nx.common_neighbors(Gtemp, cn[0], cn[1])))) for cn in testCommonNeighbors]
for entry in commonNeighbors:
    if entry[2] > 5:
        bestCommonNeighbors.append(entry)


# Compute node degree for different items of the common neighbors:

items1 = []
items2 = []

predictionsList = []


# The following part iterates over a list containing all nodes respecting the condition: |commonNeighbors| > 5
# We find items that both common neighbors have bought
# We search for items that one node bougth but the other did not
# Then we compute the degree of those item nodes
# Finally we get the item with max degree and predict it to the other user
for entry in bestCommonNeighbors:
    buyer1, buyer2, cnn = entry
    commonNeighboursList = nx.common_neighbors(Gtemp, buyer1, buyer2)

    buyer1Edges = Gtemp[buyer1]
    buyer2Edges = Gtemp[buyer2]
    items1 = [obj for obj in buyer1Edges if obj not in buyer2Edges]
    items2 = [obj for obj in buyer2Edges if obj not in buyer1Edges]

    # print(items1)
    # print(set(items1) == set(items2))

    itemsBuyer1Degree = Gtemp.degree(items1)
    itemsBuyer2Degree = Gtemp.degree(items2)

    predictionBuyer1 = max(itemsBuyer1Degree, key = lambda itemsBuyer1Degree:itemsBuyer1Degree[1])
    predictionBuyer2 = max(itemsBuyer2Degree, key = lambda itemsBuyer2Degree:itemsBuyer2Degree[1])

    if predictionBuyer1[1] > predictionBuyer2[1]:
        predictionsList.append((buyer1, predictionBuyer1[0]))
    else:
        predictionsList.append((buyer2, predictionBuyer2[0]))



print(set(predictionsList))



# DISPLAY THE RESULTING GRAPH (ONLY TESTING PUR)


# Define Colors for algorithms testing
# color_map = []
# for node in Gtemp:
#     if node in buyers:
#         color_map.append('blue')
#     else:
#         color_map.append('green')


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
