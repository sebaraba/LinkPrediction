import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite


# We work with two types of nodes:
# 1. Buyer nodes (buyers)
# 2. Item nodes (items)

buyers = []
items = []

count_accuired = 0
count_view = 0
random_count = 0


# Big dataset preparation
with open('../data/events.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        if row[2] != 'transaction' and row[2] != 'view' and row[2] not in items:
            items.append(row[2])
        if row[2] == 'transaction':
            count_accuired += 1
        elif row[2] == 'view':
            count_view += 1
        else:
            random_count += 1


print('Transaction in big data', count_accuired)
print('Views in dataset', count_view)
print('What\'s left', random_count)

for entry in items:
    print(entry)
    input()