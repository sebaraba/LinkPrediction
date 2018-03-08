import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite

# with open('test_csv.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     buyers = []
#     items = []
#     for row in readCSV:
#         buyers.append(row[6])
#         items.append(row[1])
#
#
# print(len(buyers))
# print(len(items))
#
#
Gtest = nx.Graph()

nodes = ['A','B','C','D','E','G','H','I']
edges = [('A','B'),('A','C'),('A','D'),('A','G'),('B','C'),('B','D'),('B','I'),('B','H'),('C','D'),('C','H'),('C','E')]

Gtest.add_nodes_from(nodes)


Gtest.add_edges_from(edges)


nx.draw(Gtest, with_labels = True)
plt.draw()
plt.show()
