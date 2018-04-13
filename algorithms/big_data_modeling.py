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

distinct_buyers = []
distinct_items = []
distinct_invoice = []
count = 0
# Big dataset preparation
with open('../data/swarovski.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        count +=1
        if row[1] not in distinct_buyers:
            distinct_buyers.append(row[1])
        if row[3] not in distinct_items:
            distinct_items.append(row[3])


print(count)
print(len(distinct_buyers))
print(len(distinct_items))
                



# print('Transaction in big data', count_transaction) 
# print('Views in dataset', count_view)
# print('What\'s left', count_add_to_cart)

# print('Raport view on actual transaction:', count_view/count_transaction)
# print('Raport add to cart on transactions:', count_add_to_cart/count_transaction)

# print('Count fourteen:', count_fourteen)
# print('Count fifteen:', count_fifteen)
# print('Count others:', count_others)


# Write transactions info into a new file .txt
# Perform analisys and generate true predictions
# Test predictions on test dataset
# Find out timestamp format!! IT misses sense. We need to find out how much time we have recorded in the file.
