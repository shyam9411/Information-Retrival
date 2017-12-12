from __future__ import division
from collections import OrderedDict
import os
import sys
from prettytable import PrettyTable


class Evaluation(object):

    def __init__(self):
        # dict to store relevance information about documents and queries
        self.relevanceInformation = OrderedDict()
        # dict to store retrieval model run information
        self.retrievalModelRunInformation = OrderedDict()
        # dict to store precision data for queries and each document
        self.precisionData = OrderedDict()
        # dict to store recall data for queries and each document
        self.recallData = OrderedDict()
        # dict to store average precision data
        self.averagePrecisionData = {}
        # dict to store reciprocal rank data
        self.reciprocalRankData = {}
        # dict to store precision at K data
        self.precisionAtKData = {}
        # list to store retrieval model names
        self.retrievalModels = []

    # function: clearDictionaries
    # Parameters:
    # Effect:
    #   Removes all the mentioned dictionary entries
    def clearDictionaries(self):
        self.retrievalModelRunInformation.clear()
        self.precisionData.clear()
        self.recallData.clear()
        self.averagePrecisionData.clear()
        self.reciprocalRankData.clear()
        self.precisionAtKData.clear()

    # function: beginTask
    # Parameters:
    # Effect:
    #   starts the evaluation process
    def beginTask(self):
        self.fetchRetrievalModels()
        self.fetchRelevanceData()
        for rm in self.retrievalModels:
            self.clearDictionaries()
            self.fetchRetrievalModelResults(rm)
            self.precision()
            self.recall()
            self.averagePrecision()
            self.reciprocalRank()
            self.precisionAtK()
            self.writeToFile(rm)

    # function: createFile
    # Parameters:
    #   fileName - the name of the file that is to be created
    # Returns:
    #   the name of the file that was created
    # Note: the program creates a directory named "Evaluation"
    # in the directory where the program is running
    def createFile(self, fileName):      
        directory = os.path.dirname(sys.argv[0])
        downloadDir = os.path.join(directory, "Evaluation")
        if not os.path.exists(downloadDir):
            os.makedirs(downloadDir)
        createdFileName = os.path.join(downloadDir, fileName)
        return createdFileName

    # function: writeToFile
    # Parameters:
    #    rm - name of the retrieval model
    # Effects:
    #     Creates a file specific to each retrieval model and stores the results
    def writeToFile(self, rm):
        rmFile = self.createFile(rm)
        fileHandler = open(rmFile, 'w')
        # strips .txt from the model name
        rmName = rm[:-4] + "\n\n"
        fileHandler.write(rmName)  
        for queryID in self.retrievalModelRunInformation:
            # creates a table with columns - Query ID, Document ID, Precision and Recall
            tableData = PrettyTable(["Query ID", "Document ID", "Precision", "Recall"])

            # creates a table with columns - Query ID, Precision @ 5 and Precision @ 20
            tablePatK = PrettyTable(["Query ID", "Precision @ 5", "Precision @ 20"])
            for docID in self.precisionData[queryID]:
                # create a row with Precision and Recall data for a particular document
                tableData.add_row([str(queryID), docID, str(self.precisionData[queryID][docID]),
                                   str(self.recallData[queryID][docID])])

            # create a row with P@K data    
            tablePatK.add_row([str(queryID), str(self.precisionAtKData[queryID]["5"][1]),
                               str(self.precisionAtKData[queryID]["20"][1])])

            fileHandler.write(tableData.get_string())
            fileHandler.write("\n\n")
            fileHandler.write(tablePatK.get_string())
            fileHandler.write("\n\n")

            # write MAP data to the file
            # MAP formula: (Sum of Average Precisions / Number of Vaules)
            log = "\n\nMean Average Precision: \n"
            log += str(sum(self.averagePrecisionData.values())/len(self.averagePrecisionData))

            # write MRR data to the file
            # MRR formula: (Sum of Reciprocal Rank Values / Number of Vaules)
            log += "\n\nMean Reciprocal Rank: \n"
            log += str(sum(self.reciprocalRankData.values())/len(self.reciprocalRankData))
            fileHandler.write(log)
            fileHandler.write("\n\n")
        fileHandler.close()

    # function: fetchRetrievalModels
    # Parameters:
    # Effects:
    #     Fetches retrieval models data from 'result' directory and stores
    #     the information in retrivalModels dict
    def fetchRetrievalModels(self):
        directory = os.path.dirname(sys.argv[0])
        resultsDir = os.path.join(directory, "Results")
        # fetch all the files in the download directory and add them to directoryList
        for o in os.listdir(resultsDir):
            if o.endswith(".txt"):
                self.retrievalModels.append(o)

    # function: fetchRelevanceData
    # Parameters:
    # Effects:
    #     Fetches relevance information data from 'cacm.rek.txt' file and stores
    #     the information in relevanceInformation dict
    def fetchRelevanceData(self):
        directory = os.path.dirname(sys.argv[0])
        relevanceDataPath = directory + "/Relevance/cacm.rel.txt"
        file_handler = open(relevanceDataPath,'r')

        # each line in the file is of the following format:
        # QueryID Q0 DocID IsRelevant Flag => 1 Q0 CACM-1410 1
        for line in file_handler:
            dataSplit = line.split(" ")
            queryID = dataSplit[0] # get the query ID
            docID = dataSplit[2] # get the doc ID
            if queryID in self.relevanceInformation:
                self.relevanceInformation[queryID].append(docID)
            else:
                self.relevanceInformation[queryID] = []
                self.relevanceInformation[queryID].append(docID)

    # function: fetchRetrievalModelResults
    # Parameters:
    #     rmFilePath - the path of the retrieval model file
    # Effects:
    #     Fetches relevance information data from 'cacm.rek.txt' file and stores
    #     the information in relevanceInformation dict
    def fetchRetrievalModelResults(self, rmFileName):
        directory = os.path.dirname(sys.argv[0])
        retrievalModelResultsPath = directory + "/Results/" + rmFileName
        file_handler = open(retrievalModelResultsPath, 'r')

        # each line in the file is of the following format:
        # QueryID Q0 DocID Rank Score SystemName
        for line in file_handler:
            dataSplit = line.split(" ")
            # get the query ID
            queryID = dataSplit[0]
            if queryID in self.relevanceInformation:
                # get the Doc ID
                docID = dataSplit[2]
                if queryID in self.retrievalModelRunInformation:
                    self.retrievalModelRunInformation[queryID].append(docID)
                else:
                    self.retrievalModelRunInformation[queryID] = []
                    self.retrievalModelRunInformation[queryID].append(docID)

    # function: precision
    # Parameters:
    # Effects:
    #     Calculates precision for each document under each query
    #     and stores the information in precisionData dict
    # The formula to calculate precision is:
    #     ((relevant document) intersects (retrieved documents)) / (retrieved documents)
    def precision(self):
        for queryID in self.relevanceInformation:
            if queryID in self.retrievalModelRunInformation:
                retrievedDocumentCount = 0
                relevantDocumentCount = 0
                for docID in self.retrievalModelRunInformation[queryID]:
                    # increment the count whenever a document is encountered
                    retrievedDocumentCount += 1
                    if queryID in self.relevanceInformation:
                        if docID in self.relevanceInformation[queryID]:
                            # increment the count when a relevant document is found
                            relevantDocumentCount += 1
                    if queryID not in self.precisionData:
                        self.precisionData[queryID] = OrderedDict()
                    self.precisionData[queryID][docID] = relevantDocumentCount/retrievedDocumentCount

    # function: recall
    # Parameters:
    # Effects:
    #     Calculates recall for each document under each query
    #     and stores the information in recallData dict
    # The formula to calculate precision is:
    #     ((relevant document) intersects (retrieved documents)) / (relevant documents)
    def recall(self):
        for queryID in self.relevanceInformation:
            if queryID in self.retrievalModelRunInformation:
                relevantDocumentCount = 0
                # get the total number of relevant documents
                totalRelevantDocumentCount = len(self.relevanceInformation[queryID])
                for docID in self.retrievalModelRunInformation[queryID]:
                    if queryID in self.relevanceInformation:
                        if docID in self.relevanceInformation[queryID]:
                            # increment the count whenever a relevant document is found
                            relevantDocumentCount += 1
                    if queryID not in self.recallData:
                        self.recallData[queryID] = OrderedDict()
                    self.recallData[queryID][docID] = relevantDocumentCount/totalRelevantDocumentCount

    # function: averagePrecision
    # Parameters:
    # Effects:
    #     Calculates average precision using precision data calculated in earlier
    #     function and stores the information in averagePrecisionData dict
    # The formula to calculate precision is:
    #     (precision of relevant documents) / (number of common relevant documents)
    def averagePrecision(self):
        for queryID in self.relevanceInformation:
            # get the common documents from relevanceInformation and retrievalModelRunInformation
            # because we are only concerned with documents with relevance judgement information
            commonDocIDs = set(self.relevanceInformation[queryID]).intersection(
                set(self.retrievalModelRunInformation[queryID]))
            if len(commonDocIDs) > 0:
                sum = 0.0
                for docID in commonDocIDs:
                    if docID in self.precisionData[queryID]:
                        sum += self.precisionData[queryID][docID]

                self.averagePrecisionData[queryID] = sum / len(commonDocIDs)

    # function: reciprocalRank
    # Parameters:
    # Effects:
    #     Calculates reciprocal rank for each query ID
    #     and stores the information in reciprocalRankData dict
    # The formula to calculate precision is:
    #     1 / (the index at which the first relevant document is encountered)
    def reciprocalRank(self):
        for queryID in self.relevanceInformation:
            if queryID in self.retrievalModelRunInformation:
                docList = self.recallData[queryID]
                for docID in docList:
                    if docList[docID] != 0:
                        self.reciprocalRankData[queryID] = (1 / (list(docList.keys()).index(docID) + 1))
                        break

    # function: precisionAtK
    # Parameters:
    # Effects:
    #     Calculates precision @ K where K can be any value less than len(precisionData)
    #     and stores the information in precisionAtKData dict
    def precisionAtK(self):
        for queryID in self.relevanceInformation:
            if queryID in self.retrievalModelRunInformation:
                self.precisionAtKData[queryID] = {}
                self.precisionAtKData[queryID]["5"] = list(self.precisionData[queryID].items())[4]
                self.precisionAtKData[queryID]["20"] = list(self.precisionData[queryID].items())[19]
            

if __name__ == "__main__":
    evaluation1 = Evaluation()
    evaluation1.beginTask()
