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
        if row[1] != '' and row[2] != '' and row[1] != ' ' and row[2] != ' ':
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


# Compute the resource allocation index for the Gtemp Graph
allocation = nx.resource_allocation_index(Gtemp, testCommonNeighbors)

# Sort the allocatio indexes in ascending order.
def takeThird(elem):
    return elem[2]


allocation = sorted(allocation, key = takeThird, reverse = True)
allocation = [al for al in allocation if al[2] > 1]

# Print allocation indexes
# for entry in allocation:
#     u, v, p = entry
#     print('Node pair: [', u,']','[', v,'] -> ', 'Index = ' , p)

predictions = []



# We find all items that bouth buyers have bought
# We search for items that one node bougth but the other did not
# Then we compute the degree of those item nodes
# Finally we get the item with max degree and predict it to the other user
for entry in allocation:
    buyer1, buyer2, res_aloc = entry

    buyer1Edges = Gtemp[buyer1]
    buyer2Edges = Gtemp[buyer2]

    items1 = [edge for edge in buyer1Edges if edge not in buyer2Edges]
    items2 = [edge for edge in buyer2Edges if edge not in buyer2Edges]

    if items1 != []:
        itemsBuyer1Degree = Gtemp.degree(items1)
        buyer1Candidate = max(itemsBuyer1Degree, key = lambda itemsBuyer1Degree:itemsBuyer1Degree[1])
    else:
        buyer1Candidate = ('', 0)
    if items2 != []:
        itemsBuyer2Degree = Gtemp.degree(items2)
        buyer2Candidate = max(itemsBuyer2Degree, key = lambda itemsBuyer1Degree:itemsBuyer2Degree[1])
    else:
        buyer2Candidate = ('', 0)


    if buyer1Candidate[1] > buyer2Candidate[1]:
        predictions.append((buyer1, buyer1Candidate[0]))
    else:
        predictions.append((buyer2, buyer2Candidate[0]))



print(predictions)
