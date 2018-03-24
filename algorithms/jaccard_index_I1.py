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

testJaccardIndex = []

# Define tuples of nodes to feed Common Neighbors Algorithm
for i in range(0, len(buyers) - 1):
    firstNode = buyers[i];
    for j in range(i+1, len(buyers)):
        if buyers[j] != buyers[i]:
            secondNode = buyers[j];
            testJaccardIndex.append((firstNode, secondNode))


# Define Lables for the nodes
# This is a feature that helps more on the algorithms testing part.
lables = []
for node in buyers:
    lables.append(node)
for node in items:
    lables.append(node)


# Compute Common Neighbors Algorithm for Gtemp's nodes
# Pick only nodes which exceed e cartain trashold for the number of CNN
bestJaccardCandidates = []


jaccardCoeff = nx.jaccard_coefficient(Gtemp, testJaccardIndex)
for entry in jaccardCoeff:
    if entry[2] > 0.12:
        # print(entry)
        # input()
        bestJaccardCandidates.append(entry)
print(len(bestJaccardCandidates))


# Compute node degree for different items of the common neighbors:

# for entry in bestJaccardCandidates:
#     print(entry)



items1 = []
items2 = []

predictionsList = []


# The following part iterates over a list containing all nodes respecting the condition: |commonNeighbors| > 5
# We find items that both common neighbors have bought
# We search for items that one node bougth but the other did not
# Then we compute the degree of those item nodes
# Finally we get the item with max degree and predict it to the other user
for entry in bestJaccardCandidates:
    buyer1, buyer2, res_aloc = entry


    buyer1Edges = Gtemp[buyer1]
    buyer2Edges = Gtemp[buyer2]

    # print(len(buyer1Edges))
    # input()

    items1 = [edge for edge in buyer1Edges if edge not in buyer2Edges]
    items2 = [edge for edge in buyer2Edges if edge not in buyer1Edges]

    print(items1, 'items1, items2', items2)
    if items1 != []:
        itemsBuyer1Degree = Gtemp.degree(items1)
        buyer1Candidate = max(itemsBuyer1Degree, key = lambda itemsBuyer1Degree:itemsBuyer1Degree[1])
        print("Buyer 1 candidate:",  buyer1Candidate)
    else:
        buyer1Candidate = ('', 0)
    if items2 != []:
        itemsBuyer2Degree = Gtemp.degree(items2)
        buyer2Candidate = max(itemsBuyer2Degree, key = lambda itemsBuyer2Degree:itemsBuyer2Degree[1])
        print("Buyer 2 candidate:",  buyer2Candidate)

    else:
        buyer2Candidate = ('', 0)

    input()

    if buyer1Candidate[1] > buyer2Candidate[1]:
        predictionsList.append((buyer1, buyer1Candidate[0]))
    else:
        predictionsList.append((buyer2, buyer2Candidate[0]))



for entry in predictionsList:
    if entry[0] in buyers:
        if entry[1] in items:
            print(entry)
            input()





# for entry in buyer1Edges:
#     for entry1 in buyer2Edges:
#         if entry == entry1:
#             print(True)

# print("second items list")

# for entry in buyer2Edges:
#     print(entry)


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
