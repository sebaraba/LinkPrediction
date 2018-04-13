import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

class Recommender(object):

    #Contructor of the class;
    def __init__(self, dataset):
        self.dataset = dataset
        self.networkG = nx.Graph()        
        self.buyers = []
        self.items = []
        self.edges = []
        self.pairs = []
        self.weights = {}

        print('Entered constructor:')
        self.loadDatasets(self.dataset)

    def loadDatasets(self, selectedDataset):
        dataSetsLists = ['', 'events_sorted.csv', 'data.csv', 'test_csv.csv']
        buyers =[]
        items =[]
        print('Dataset:', dataSetsLists[selectedDataset])
        # Big dataset preparation
        with open('../data/' + dataSetsLists[selectedDataset]) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                if selectedDataset == 3 or selectedDataset == 2:
                    if row[1] != '' and row[6] != '' and row[1] != ' ' and row[6] != ' ':
                        buyers.append(row[6])
                        items.append(row[1])
                if selectedDataset == 1:
                    if row[1] != '' and row[3] != '' and row[1] != ' ' and row[3] != ' ':
                        buyers.append(row[1])
                        items.append(row[3])
        self.generateNetworkG(buyers, items)


    #This method recieves buyers and items lists and generates the bipartite graph from it.
    def generateNetworkG(self, buyers, items):
        print('Generating Network, Loading ...')
        item_wieghts = {}

        # Prepare both sides of nodes and the edges:
        edges = zip(buyers, items)
        buyers = list(set(buyers))
        items = list(set(items))

        # Generate the bipartite graph using the info above
        Gtemp = nx.Graph()
        Gtemp.add_nodes_from(buyers, bipartite = 0)
        Gtemp.add_nodes_from(items, bipartite = 1)
        Gtemp.add_edges_from(edges)

        # Compute degree of item nodes
        for item in items:
            item_wieghts.update({item: Gtemp.degree(item)})
        
        # Initialise state with obtained values
        self.weights = item_wieghts
        self.networkG = Gtemp
        self.buyers = buyers
        self.items = items
        self.edges = edges
        self.pairs = self.pairBuyerNodes(items, buyers)

        #Testing Prints:
        print('Loaded!')
        print('Number of item nodes:', len(items))
        print('Number of buyer nodes:', len(items))
        print('Number of interactions:', len(edges))

        bestSimilarityScores = self.commonNeighborsIndex(self.pairs)
        self.computationOnItemNodes(bestSimilarityScores)



    # The following methods creates a list of pairs of buyers;
    # The list will be fed  intto the link prediction index algorithm;
    def pairBuyerNodes(self, items, buyers):
        pairs = []

        # This is V2 of the algorithm; It considers for next step only buyers that have at least on common neighbour. 
        # This common neighbour is the item, whoes degree is checked. However if an item has more than a certain number of 
        # neighbours than it means it is not so relevant for finding similarities, so it is discarded;
        for item in items:
            neighbours = self.networkG.neighbors(item)
            neighbours = list(neighbours)
            if len(neighbours) > 1 and len(neighbours) < 10:
                for i in range(0, len(neighbours)):
                    firstNode = neighbours[i]
                    for j in range(i+1, len(neighbours)):
                        if buyers[j] != neighbours[i]:
                            secondNode = neighbours[j]
                            pairs.append((firstNode, secondNode))
        pairs = list(set(pairs))
                

        # This is V1 of the function        
        # Define tuples of nodes to feed Common Neighbors Algorithm
        # for i in range(0, len(buyers)):
        #     firstNode = buyers[i]
        #     for j in range(i+1, len(buyers)):
        #         if buyers[j] != buyers[i]:
        #             secondNode = buyers[j]
        #             pairs.append((firstNode, secondNode))
        
        print(len(pairs))
        return(pairs)


    # The following part iterates over a list containing all nodes respecting the condition: |commonNeighbors| > 5
    # We find items that both common neighbors have bought
    # We search for items that one node bougth but the other did not
    # Then we compute the degree of those item nodes
    # Finally we get the item with max degree and predict it to the other user
    def computationOnItemNodes(self, bestSimilarityScores):
        predictionsList = []
        for entry in bestSimilarityScores:
            buyer1, buyer2, cnn = entry
            
            buyer1Edges = self.networkG[buyer1]
            buyer2Edges = self.networkG[buyer2]
            items1 = [obj for obj in buyer1Edges if obj not in buyer2Edges]
            items2 = [obj for obj in buyer2Edges if obj not in buyer1Edges]

            # print(items1)
            # print(set(items1) == set(items2))
            if len(items1):
                maxDegree1 = 0
                for item in items1:
                    if item in self.items:
                        if self.weights[item] > maxDegree1:
                            maxDegree1 = self.weights[item]
                            maxDegreeID1 = item

            if len(items2):
                maxDegree2 = 0
                for item in items2:
                    if item in self.items:
                        if self.weights[item] > maxDegree2:
                            maxDegree2 = self.weights[item]
                            maxDegreeID2 = item
            
            predictionsList.append((buyer1, maxDegreeID1))
            predictionsList.append((buyer2, maxDegreeID2))

            # if items1 != []:
            #     itemsBuyer1Degree = self.networkG.degree(items1)
            #     predictionBuyer1 = max(itemsBuyer1Degree, key = lambda itemsBuyer1Degree:itemsBuyer1Degree[1])
            # else:
            #     predictionBuyer1 = ('', 0)
            # if items2 != []:
            #     itemsBuyer2Degree = self.networkG.degree(items2)
            #     predictionBuyer2 = max(itemsBuyer2Degree, key = lambda itemsBuyer1Degree:itemsBuyer2Degree[1])
            # else:
            #     predictionBuyer2 = ('', 0)


            # if predictionBuyer1[1] > predictionBuyer2[1]:
            #     predictionsList.append((buyer1, predictionBuyer1[0]))
            # else:
            #     predictionsList.append((buyer2, predictionBuyer2[0]))


        predictionsList = list(set(predictionsList))
        for entry in predictionsList:
            print(entry)

    # Compute Common Neighbors Algorithm for Gtemp's nodes 
    # Pick only nodes which exceed e cartain trashold for the number of CNN
    def commonNeighborsIndex(self, buyerPairs):
        bestSimilarityScores = []
        commonNeighbors = []
        for entry in buyerPairs:
            buyer1, buyer2 = entry
            entry = (buyer1, buyer2, len(list(nx.common_neighbors(self.networkG, buyer1, buyer2))))
            commonNeighbors.append(entry)

        for entry in commonNeighbors:
            if entry[2] > 5:
                bestSimilarityScores.append(entry)

        return(list(set(bestSimilarityScores)))


    # Compute the resource allocation index for the Gtemp Graph
    def resourceAllocationIndex(self, buyerPairs):
        # Sort the allocatio indexes in ascending order.
        allocation = nx.resource_allocation_index(self.networkG, buyerPairs)
        allocation = [entry for entry in allocation if entry[2] > 1.5]
        allocation = list(set(allocation))

        #Print allocation indexes
        for entry in allocation:
            u, v, p = entry
            print('Node pair: [', u,']','[', v,'] -> ', 'Index = ' , p)


    def jaccardIndex(self, buyerPairs):
        jaccard = nx.jaccard_coefficient(self.networkG, buyerPairs)
        jaccard = [entry for entry in jaccard if entry[2] > 0.1]
        jaccard = list(set(jaccard))

        #Print jaccard indexes
        for entry in jaccard:
            u, v, p = entry
            print('Node pair: [', u,']','[', v,'] -> ', 'Index = ' , p)

if __name__ == '__main__':
    print(str(sys.argv[1]))
    Recommender(int(sys.argv[1]))