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
# Gtest = nx.Graph()
#
# Gtest.add_nodes_from(buyers)
# Gtest.add_nodes_from(items)
#
# edges = zip(buyers, items)
#
# Gtest.add_edges_from(edges)
#
# color_map = []
# for node in Gtest:
#     if node in buyers:
#         color_map.append('blue')
#     else: color_map.append('green')
#
# nx.draw(Gtest, node_color = color_map ,with_lables = True)
# plt.draw()
# plt.show()

## THIS IS WHERE I START WORKING WITH THE LINK PREDICTION ALGORITHMS


nodes1 = [1, 2, 3]
nodes2 = ['A','B','C','D','E']

edges = [(1,'A'),(1,'B'),(1,'C'),(1,'D'),(2,'B'),(2,'C'),(2,'D'),(3,'C'),(3,'D'),(3,'E')]

Gnormal = nx.complete_graph(5)
# Gnormal.add_nodes_from(nodes1)
# Gnormal.add_nodes_from(nodes2)
# Gnormal.add_edges_from(edges)

Gtemp = nx.Graph()

Gtemp.add_nodes_from(nodes1, bipartite = 0)
Gtemp.add_nodes_from(nodes2, bipartite = 1)
Gtemp.add_edges_from(edges)

print(nx.is_connected(Gtemp));

bottom_nodes, top_nodes = bipartite.sets(Gtemp)

lables = []
for node in nodes1:
    lables.append(node)
for node in nodes2:
    lables.append(node)

print(list(top_nodes))

G = bipartite.projected_graph(Gtemp, bottom_nodes)
print(G.edges())

color_map = []

for node in Gtemp:
    if node in nodes1:
        print('Node=>', node)
        color_map.append('blue')
    else:
        print('Node=>', node)
        color_map.append('green')

preds = nx.common_neighbors(Gtemp, 1, 2)

count = 0
print('Common neighbors for nodes 1 and 2')
for p in preds:
    print(p)
    count += 1
print('Number of common neighbors')
print(count)
# u, v, p = preds
#
#
# # for u, v, p in preds:
# #     print('(%d, %d) -> %d' % (u, v, p))
#
# print(u, v, p)
#
# print(preds)
#
# nx.draw(Gnormal, with_labels = True)
# plt.show()

#
pos = {}
pos.update( (n, (1, i)) for i, n in enumerate(nodes1) ) # put nodes from X at x=1
pos.update( (n, (2, i)) for i, n in enumerate(nodes2) ) # put nodes from Y at x=2
nx.draw(Gtemp, node_color = color_map,pos=pos, with_labels =True)
plt.show()



# nx.draw(Gtemp, with_lables = True)
# plt.show()
