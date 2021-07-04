import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite


# The following class comprises a recommender system that uses 
# similarity based link prediction algorithms to find the recommended items. 
# Running instructions:
# The command takes three arguments: 
#       1. The dataset: sroted_evetns.csv, data.csv. test_csv.csv;
#       2. The algorithm: common_neighbours, resource_allocation, jaccard_coefficient;
#       3. The threshold: variable depending on the algorithm;
# An example a call of the recommender system: 
# python recommender.py data.csv common_neighbours 600
class Recommender(object):

    # The constructor initialises the state variables with the given values for: dataset, algorithm and threshold.
    # The functionCalls method calls all other needed functions in order to obtain the predictions with respects 
    # to the given arguments.
    def __init__(self, dataset, algorithm, threshold):
        print('Entered constructor:')
        self.algorithm = algorithm
        self.threshold = threshold
        self.dataset = dataset

        self.networkG = nx.Graph()        
        self.buyers = []
        self.items = []
        self.edges = []
        self.pairs = []
        self.weights = {}
        self.functinCalls()

    # Depending on the chosen algorithm and dataset, 
    # this method computes the predictions based on different link prediction approaches.
    def functinCalls(self):
        self.loadDatasets()

        if self.algorithm == 'common_neighbours':
            bestSimilarityScores = self.commonNeighborsIndex(self.pairs)
            self.computationOnItemNodes(bestSimilarityScores)

        if self.algorithm == 'resource_allocation':
            bestSimilarityScores = self.resourceAllocationIndex(self.pairs)
            self.computationOnItemNodes(bestSimilarityScores)

        if self.algorithm == 'jaccard_coefficient':
            bestSimilarityScores = self.jaccardCoefficientIndex(self.pairs)
            self.computationOnItemNodes(bestSimilarityScores)


    # This function opens the csv file containing the transaction data.
    # The lists containing item nodes, buyer node are generated.
    def loadDatasets(self):
        print('Loading ' + self.dataset + ' ...')
        buyers =[]
        items =[]

        with open('../data/' + self.dataset) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            next(readCSV, None)
            for row in readCSV:
                if self.dataset == 'trainingDataset1.csv':
                    if row[1] != '' and row[6] != '' and row[1] != ' ' and row[6] != ' ':
                        buyers.append(row[6])
                        items.append(row[1])
                if self.dataset == 'trainingDataset2.csv':
                    if row[1] != '' and row[3] != '' and row[1] != ' ' and row[3] != ' ':
                        buyers.append(row[1])
                        items.append(row[3])
        print('Dataset Loaded!')
        print('\n')
        
        self.generateNetworkG(buyers, items)


    # This method recieves as parameters the lists of buyers and items.
    # It creates the list of edges, by binding one item to one buyer as specified in the csv file. 
    # Following it generates the bipartite graph and performs some basic analysis.
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

        temp = Gtemp.degree()
        maximum = 0
        summ = 0
        count = 0
        for el in temp:
            if el[1] > maximum:
                maximum = el[1]
            summ += el[1]
            count += 1


        # print('Average network degree:',summ/count)
        print('Max degree:', maximum)
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

        # Basic Information
        print('Loaded Network with the following characteristics!')
        print('Number of item nodes:', len(items))
        print('Number of buyer nodes:', len(buyers))
        print('Number of interactions:', len(edges))
        print('\n')
        


    # The following method creates a list of pairs of buyers;
    # The list will be fed  into one of the link prediction index algorithms;
    def pairBuyerNodes(self, items, buyers):
        pairs = []
        print('Paring Buyer nodes ...')
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
        print('Pairs generated!')
        print('\n')
        
        
        return(pairs)



    # The following part iterates over a list containing all nodes respecting the condition: |commonNeighbors| > 5
    # We find items that both common neighbors have bought
    # We search for items that one node bougth but the other did not
    # Then we compute the degree of those item nodes
    # We get the item with max degree and predict it to the other user
    # Enventually the predictions are created buinding the similar buyers to thei best items
    def computationOnItemNodes(self, bestSimilarityScores):
        predictionsList = []
        print('Started Computations on item nodes:')
        for entry in bestSimilarityScores:
            buyer1, buyer2, cnn = entry
            maxDegree1 = ''
            maxDegree2 = ''

            buyer1Edges = self.networkG[buyer1]
            buyer2Edges = self.networkG[buyer2]
            items1 = [obj for obj in buyer1Edges if obj not in buyer2Edges]
            items2 = [obj for obj in buyer2Edges if obj not in buyer1Edges]


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
            
            if maxDegree1 != '':
                predictionsList.append((buyer1, maxDegreeID1))
            if maxDegree2 != '':
                predictionsList.append((buyer2, maxDegreeID2))
        print('Computations Done!')
        print('\n')
        
        print('Computing Predictions ...')
        predictionsList = list(set(predictionsList))

        if len(predictionsList):
            for entry in predictionsList:
                print('Prediction:', entry)
        else:
            print('\n')
            print('Not enough data to build predictions, try chainging the threshold value.')


    # Compute Common Neighbors Algorithm for Gtemp's nodes 
    # Pick only nodes which exceed e cartain trashold for the number of CNN
    def commonNeighborsIndex(self, buyerPairs):
        print('Computing Similarity Scors using Common Neighborus Index ...')
        bestSimilarityScores = []
        commonNeighbors = []
        for entry in buyerPairs:
            buyer1, buyer2 = entry
            entry = (buyer1, buyer2, len(list(nx.common_neighbors(self.networkG, buyer1, buyer2))))
            commonNeighbors.append(entry)

        for entry in commonNeighbors:
            if entry[2] > self.threshold:
                bestSimilarityScores.append(entry)
        print('Computation Done!')
        print('\n')
        
        return(list(set(bestSimilarityScores)))



    # Compute the resource allocation index for the selected network
    # Return a list of nodes that exceed the threshold
    def resourceAllocationIndex(self, buyerPairs):
        # Sort the allocatio indexes in ascending order.
        print('Computing Similarity Scors using Resource Allocation Index ...')        
        allocation = nx.resource_allocation_index(self.networkG, buyerPairs)
        allocation = [entry for entry in allocation if entry[2] > self.threshold]
        allocation = list(set(allocation))

        print('Computation Done!')
        print('\n')

        return(list(set(allocation)))


    # Compute the jaccard index for the selected network
    # Return a list of nodes that exceed the threshold
    def jaccardCoefficientIndex(self, buyerPairs):
        print('Computing Similarity Scors using Jaccard Coefficient Index ...')     
        jaccard = nx.jaccard_coefficient(self.networkG, buyerPairs)
        jaccard = [entry for entry in jaccard if entry[2] > self.threshold]
        jaccard = list(set(jaccard))

        print('Computation Done!')
        print('\n')

        return(jaccard)
        

        


if __name__ == '__main__':
    Recommender(str(sys.argv[1]), str(sys.argv[2]), float(sys.argv[3]))