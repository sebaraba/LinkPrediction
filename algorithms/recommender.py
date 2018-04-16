import csv
import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import decimal
import numpy as np

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
        self.dataset = dataset        
        self.algorithm = algorithm
        self.threshold = threshold

        print(threshold, 'threshold')

        self.networkG = nx.Graph()        
        self.buyers = []
        self.items = []
        self.edges = []
        self.pairs = []
        self.predictions = []        
        self.weights = {}

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
                if self.dataset == 'test_csv.csv' or self.dataset == 'data.csv' or self.dataset == 'trainingDataset1.csv':
                    if row[1] != '' and row[6] != '' and row[1] != ' ' and row[6] != ' ':
                        buyers.append(row[6])
                        items.append(row[1])
                if self.dataset == 'events_sorted.csv':
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
        # print('Loaded Network with the following characteristics!')
        # print('Number of item nodes:', len(items))
        # print('Number of buyer nodes:', len(buyers))
        # print('Number of interactions:', len(edges))
        # print('\n')
        


    # The following method creates a list of pairs of buyers;
    # The list will be fed  into one of the link prediction index algorithms;
    def pairBuyerNodes(self, items, buyers):
        pairs = []
        # print('Paring Buyer nodes ...')
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
        # print('Pairs generated!')
        # print('\n')
        
        
        return(pairs)



    # The following part iterates over a list containing all nodes respecting the condition: |commonNeighbors| > 5
    # We find items that both common neighbors have bought
    # We search for items that one node bougth but the other did not
    # Then we compute the degree of those item nodes
    # We get the item with max degree and predict it to the other user
    # Enventually the predictions are created buinding the similar buyers to thei best items
    def computationOnItemNodes(self, bestSimilarityScores):
        predictionsList = []
        # print('Started Computations on item nodes:')
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
        # print('Computations Done!')
        # print('\n')
        
        # print('Computing Predictions ...')
        predictionsList = list(set(predictionsList))

        if len(predictionsList):
            self.predictions = predictionsList
            # print('Predictions generated')
        else:
            # print('\n')
            print('Not enough data to build predictions, try chainging the threshold value.')


    # Compute Common Neighbors Algorithm for Gtemp's nodes 
    # Pick only nodes which exceed e cartain trashold for the number of CNN
    def commonNeighborsIndex(self, buyerPairs):
        # print('Computing Similarity Scors using Common Neighborus Index ...')
        bestSimilarityScores = []
        commonNeighbors = []
        for entry in buyerPairs:
            buyer1, buyer2 = entry
            entry = (buyer1, buyer2, len(list(nx.common_neighbors(self.networkG, buyer1, buyer2))))
            commonNeighbors.append(entry)

        for entry in commonNeighbors:
            if entry[2] > self.threshold:
                bestSimilarityScores.append(entry)
        # print('Computation Done!')
        # print('\n')
        
        return(list(set(bestSimilarityScores)))



    # Compute the resource allocation index for the selected network
    # Return a list of nodes that exceed the threshold
    def resourceAllocationIndex(self, buyerPairs):
        # Sort the allocatio indexes in ascending order.
        # print('Computing Similarity Scors using Resource Allocation Index ...')        
        allocation = nx.resource_allocation_index(self.networkG, buyerPairs)
        allocation = [entry for entry in allocation if entry[2] > self.threshold]
        allocation = list(set(allocation))

        # print('Computation Done!')
        # print('\n')

        return(list(set(allocation)))


    # Compute the jaccard index for the selected network
    # Return a list of nodes that exceed the threshold
    def jaccardCoefficientIndex(self, buyerPairs):
        # print('Computing Similarity Scors using Jaccard Coefficient Index ...')     
        jaccard = nx.jaccard_coefficient(self.networkG, buyerPairs)
        jaccard = [entry for entry in jaccard if entry[2] > self.threshold]
        jaccard = list(set(jaccard))

        # print('Computation Done!')
        # print('\n')

        return(jaccard)
        

    def getPreditions(self):
        self.functinCalls()        
        return(self.predictions)


# if __name__ == '__main__':
#   Recommender(str(sys.argv[1]), str(sys.argv[2]), float(sys.argv[3]))




# This second class is a leper for the testing and evaluation parts;
# It calls the recommender class, feeding it different threshold values for each algorithm;
# Analysis are always made on the training datasets;
# All results for each model are stored in three separate lists;
# The next step is to cross examine the prediction lists against the test set;
# A percentage of true prediction against the total number of predictions is output;
# In the final step, the application plots each results;
class resultsVisualisation():
    buyers =[]
    items = []
    edges = []
    minBuyer = 100000000000
    maxBuyer = 0
    random_predictions = [0.0,0.0,0.0,1.5,3.2,4.6,3.421,6.0,2.54,1.0,0.0,0.0,4.324,1.542,0.0]

    # First the testdataset file is opened and the inferred links are stored in the edges list;
    with open('../data/testDataset1.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)
        for row in readCSV:
            if row[1] != '' and row[6] != '' and row[1] != ' ' and row[6] != ' ':
                items.append(row[1])
                buyers.append(row[6])
                

    edges = zip(buyers, items)
    buyers = list(set(buyers))
    items = list(set(items)) 
    randPredictions = []

    # First we used np.arrange() to create the range of numbers; Unfortunately it is not consistent and it doesn't return 
    # the desired values always;
    # The list defines the range of the threshold values to be computed;
    # Resulting predictions are checked and the percentage of true predictions is stored;
    common_neighbours_percentage = []
    common_neighbors_range =[160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440]
    for i in range(160, 460, 20):
        if i > 2:
            rec = Recommender('trainingDataset1.csv', 'common_neighbours', i)
            predictionsList = rec.getPreditions()

            countTotal = 0
            countBad = 0
            countGood = 0
            for item in predictionsList:
                countTotal += 1
                if item in edges:
                    countGood += 1
                else:
                    countBad += 1
            percentage = float(float(countGood)/float(countTotal) * 100)
            print(countTotal, 'Total')
            print(countBad, 'Bad')
            print(countGood, 'Good')
            print(percentage, 'Percentage')
            print('\n')

            common_neighbours_percentage.append(percentage)


    # First we used np.arrange() to create the range of numbers; Unfortunately it is not consistent and it doesn't return 
    # the desired values always;
    # The list defines the range of the threshold values to be computed;
    # Resulting predictions are checked and the percentage of true predictions is stored;
    resource_allocation_range = [2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4]
    resource_allocation_percentage = []
    for i in resource_allocation_range:
        if i > 2:
            recResources = Recommender('trainingDataset1.csv', 'resource_allocation', i)
            predictionsListResources = recResources.getPreditions()

            countTotal = 0
            countBad = 0
            countGood = 0
            for item in predictionsListResources:
                countTotal += 1
                if item in edges:
                    countGood += 1
                else:
                    countBad += 1
            percentage = float(float(countGood)/float(countTotal) * 100)

            print(countTotal, 'Total')
            print(countBad, 'Bad')
            print(countGood, 'Good')
            print(percentage, 'Percentage')
            print('\n')

            resource_allocation_percentage.append(percentage)


    # First we used np.arrange() to create the range of numbers; Unfortunately it is not consistent and it doesn't return 
    # the desired values always;
    # The list defines the range of the threshold values to be computed;
    # Resulting predictions are checked and the percentage of true predictions is stored;
    jaccard_coefficient_percentage = []
    jaccard_coefficient_range = [0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40] 
    for i in jaccard_coefficient_range:
        recJaccard = Recommender('trainingDataset1.csv', 'jaccard_coefficient', i)
        predictionsListJaccard = recJaccard.getPreditions()

        countTotal = 0
        countBad = 0
        countGood = 0

        for item in predictionsListJaccard:
            countTotal += 1
            if item in edges:
                countGood += 1
            else:
                countBad += 1
        percentage = float(float(countGood)/float(countTotal) * 100)
        print(countTotal, 'Total')
        print(countBad, 'Bad')
        print(countGood, 'Good')
        print(percentage, 'Percentage')
        print('\n')

        jaccard_coefficient_percentage.append(percentage)



    tr = [2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4]
    tj = [1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4]
    tc = [160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440] 

    # Fig one plots the results of common neighbours index together with the random predictions results
    fig1, resourcePlot = plt.subplots()
    resourcePlot.plot(tr, resource_allocation_percentage, label='resource allocation')
    resourcePlot.plot(tr, random_predictions, label='random predictions')
    resourcePlot.set(ylabel='Percentage of ture predictions', xlabel='Threshold value variation',
        title='Resource Allocation Performance')
    resourcePlot.grid()
    resourcePlot.legend(bbox_to_anchor=(0., 1.07, 1., .102), loc=3,
            ncol=9, mode="expand", borderaxespad=0.)


    # Fig two plots the results of resource allocation index together with the random predictions results
    fig2, commonPlot = plt.subplots()
    commonPlot.plot(tc, common_neighbours_percentage, label='common neighbours')
    commonPlot.plot(tc, random_predictions, label='random predictions')
    commonPlot.set(ylabel='Percentage of ture predictions', xlabel='Threshold value variation',
        title='Common Neighbours Performance')
    commonPlot.grid()
    commonPlot.legend(bbox_to_anchor=(0., 1.07, 1., .102), loc=3,
            ncol=9, mode="expand", borderaxespad=0.)

    # Fig three plots the results of jaccard index together with the random predictions results
    fig3, jaccardPlot = plt.subplots()
    jaccardPlot.plot(tj, jaccard_coefficient_percentage, label='jaccard index')
    jaccardPlot.plot(tj, random_predictions, label='random predictions')
    jaccardPlot.set(ylabel='Percentage of ture predictions', xlabel='Threshold value variation',
        title='Jaccard Index Performance')
    jaccardPlot.grid()
    jaccardPlot.legend(bbox_to_anchor=(0., 1.07, 1., .102), loc=3,
            ncol=9, mode="expand", borderaxespad=0.)

    plt.show()


    # These were used to save the plots
    # fig1.savefig("resource_plot.png")
    # fig2.savefig("common_plot.png")
    # fig3.savefig("jaccard_plot.png")


