import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite


# We work with two types of nodes:
# 1. Buyer nodes (buyers)
# 2. Item nodes (items)

buyers = []
items = []
period_lasting = []

count_transaction = 0
count_view = 0
count_add_to_cart = 0

count_fourteen = 0
count_fifteen = 0
count_others = 0

# Big dataset preparation
with open('../data/events.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        if row[2] != 'transaction' and row[2] != 'view' and row[2] not in items:
            items.append(row[2])
        if row[2] == 'transaction':
            count_transaction += 1
        elif row[2] == 'view':
            count_view += 1
        else:
            count_add_to_cart += 1

            print('HERE 1')
    
        if int(row[0]) % 10 == 4:
            count_fourteen += 1
            if row[0] not in period_lasting:
                period_lasting.append(row[0])

            print('HERE 2')
        if int(row[0]) % 10 == 5:
            count_fifteen += 1
            if row[0] not in period_lasting:
                period_lasting.append(row[0])

            print('HERE 3')
        if int(row[0]) % 10 != 5 and int(row[0]) % 10 != 4:
            count_others += 1
            if row[0] not in period_lasting:
                period_lasting.append(row[0])

            print('HERE 4')
            input()


print('Transaction in big data', count_transaction)
print('Views in dataset', count_view)
print('What\'s left', count_add_to_cart)

print('Raport view on actual transaction:', count_view/count_transaction)
print('Raport add to cart on transactions:', count_add_to_cart/count_transaction)

print('Count fourteen:', count_fourteen)
print('Count fifteen:', count_fifteen)
print('Count others:', count_others)


# Write transactions info into a new file .txt
# Perform analisys and generate true predictions
# Test predictions on test dataset
# Find out timestamp format!! IT misses sense. We need to find out how much time we have recorded in the file.

for entry in period_lasting:
    print(entry)