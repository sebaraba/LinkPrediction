import networkx as nx
import matplotlib.pyplot as plt
import csv
from networkx.algorithms import bipartite


# We work with two types of nodes:
# 1. Buyer nodes (buyers)
# 2. Item nodes (items)

# buyers = []
# items = []
# period_lasting = []

# count_transaction = 0
# count_view = 0
# count_add_to_cart = 0

# count_fourteen = 0
# count_fifteen = 0
# count_others = 0

# distinct_buyers = []
# distinct_items = []
# distinct_invoice = []
# count = 0
# # Big dataset preparation
# with open('../data/swarovski.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     next(readCSV, None)
#     for row in readCSV:
#         count +=1
#         if row[1] not in distinct_buyers:
#             distinct_buyers.append(row[1])
#         if row[3] not in distinct_items:
#             distinct_items.append(row[3])


# print(count)
# print(len(distinct_buyers))
# print(len(distinct_items))
                



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
# This function opens the csv file containing the transaction data.
# The lists containing item nodes, buyer node are generated.

buyers =[]
items =[]
datesAvailable = []
count = 0
lastDate = ''
with open('../data/data.csv') as csvfile:
    with open('../data/trainingDataset1.csv', 'w+') as csvfile1:
        with open('../data/testDataset1.csv', 'w+') as csvfile2:
            readCSV = csv.reader(csvfile, delimiter=',') 
            next(readCSV, None)
            
            trainingDataset1 = csv.writer(csvfile1, delimiter=',')
            testDataset1 = csv.writer(csvfile2, delimiter=',')
            
            for row in readCSV:
                count += 1
                if count < 370000:

                    trainingDataset1.writerow(row)
                else:
                    testDataset1.writerow(row)

            print(sum(1 for row in csvfile1))
            print(sum(1 for row in csvfile2))
                    

print('Dataset Loaded!')
print('\n')



# print(count)
# count = 0

# with open('../data/trainingDataset.csv') as csvfile:
#     reader = csv.reader(csvfile, delimiter=' ')
#     with open('../data/trainingDataset1.csv', 'w+') as csvfile1:
#         writerTraining = csv.writer(csvfile1)
#         for row in reader:
#             if count < 370000:
#                 writerTraining.writerow(row)
#             else:
#                 break
#     with open('../data/testDataset1.csv')

# This method recieves as parameters the lists of buyers and items.
# It creates the list of edges, by binding one item to one buyer as specified in the csv file. 
# Following it generates the bipartite graph and performs some basic analysis.
# def generateNetworkG(self, buyers, items):
#     print('Generating Network, Loading ...')
#     item_wieghts = {}

#     # Prepare both sides of nodes and the edges:
#     edges = zip(buyers, items)
#     buyers = list(set(buyers))
#     items = list(set(items))

#     # Generate the bipartite graph using the info above
#     Gtemp = nx.Graph()
#     Gtemp.add_nodes_from(buyers, bipartite = 0)
#     Gtemp.add_nodes_from(items, bipartite = 1)
#     Gtemp.add_edges_from(edges)

#     temp = Gtemp.degree()
#     maximum = 0
#     summ = 0
#     count = 0
#     for el in temp:
#         if el[1] > maximum:
#             maximum = el[1]
#         summ += el[1]
#         count += 1


#     print('Average network degree:',summ/count)
#     print('Max degree:', maximum)
#     # Compute degree of item nodes
#     for item in items:
#         item_wieghts.update({item: Gtemp.degree(item)})


#     # Basic Information
#     print('Loaded Network with the following characteristics!')
#     print('Number of item nodes:', len(items))
#     print('Number of buyer nodes:', len(buyers))
#     print('Number of interactions:', len(edges))
#     print('\n')
    