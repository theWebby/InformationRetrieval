import math
import operator
import numpy as np

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        
        # Calculate the number of documents when we make the retriever class
        allDocIDs = []
        termDictionarys = self.index.values()
        for dictionary in termDictionarys:
            allDocIDs.extend(dictionary.keys())
        self.numberOfDocuments = len(set(allDocIDs))


    # return 10 document id's that are most relevant to the query 
    def forQuery(self,query):
        queryTerms = sorted(query.keys())

        candidateDocIDs = self.getCandidates(query, queryTerms)
        queryVector = self.createQueryVector(query, queryTerms)
        documentVectors = self.createDocumentVectors(query, queryTerms, candidateDocIDs)
        results = self.findAngles(queryVector, documentVectors)
        
        # takes 10 IDs from results {results = [(docID, angle)]}
        return [i[0] for i in results[:10]]

    
    # create a vector representing the query
    def createQueryVector(self, query, queryTerms):
        queryVector = []

        if self.termWeighting == 'binary':
            return [1] * len(query)
        elif (self.termWeighting == 'tf'):
            for queryTerm in queryTerms:
                queryVector.append(query.get(queryTerm))
        else:
            for queryTerm in queryTerms: # for each search term
                termDocumentFrequencies = self.index.get(queryTerm) # get all the documents this term appears in
                documentFrequency = 0
                if termDocumentFrequencies != None: # if there are documents containing this term
                    documentFrequency = len(termDocumentFrequencies)
                    termFrequency = query.get(queryTerm)
                    queryVector.append(self.tfidf(termFrequency, documentFrequency)) #find tfidf for this term

        return queryVector


    def createDocumentVectors(self, query, queryTerms, candidateDocIDs):
        # Get all terms in the query and prepare doc vectors and results dictionaries
        documentVectors = {}

        for docID in candidateDocIDs:
            documentVectors[docID] = [0] * len(queryTerms)
            for termID, term in enumerate(queryTerms):
                docsContainingTerm = self.index.get(term, None)
                if (docsContainingTerm != None) and (docID in docsContainingTerm.keys()):
                    if self.termWeighting == 'binary':
                        documentVectors[docID][termID] = 1#docsContainingTerm[docID]
                    elif self.termWeighting == 'tf':
                        documentVectors[docID][termID] = docsContainingTerm[docID]
                    else:
                        termFrequency = docsContainingTerm[docID]
                        documentFrequency = len(self.index.get(term))
                        documentVectors[docID][termID] = self.tfidf(termFrequency, documentFrequency) # TODO - check docs containing term

        
        return documentVectors

    # tfidf calculation with smothing techniques applied (http://www.ipcsit.com/vol47/009-ICCTS2012-T049.pdf)
    def tfidf(self, termFrequency, documentFrequency):
        return (math.log(1 + termFrequency) * (math.log(1 + self.numberOfDocuments / documentFrequency)))


    # returns a list of documents that contain at least one query term
    def getCandidates(self, query, queryTerms):
        candidates = []

        for term in queryTerms:
            termDocIDs = self.index.get(term, None) #get all of the document IDs that contain this term
            if termDocIDs != None:
                candidates.extend(list(termDocIDs.keys()))

        #converts to a distinct set and back to a list        
        return list(set(candidates))

    
    # finds the angles between all documents and the query - correlating to results
    def findAngles(self, queryVector, documentVectors):
        results = {}
        for docId in documentVectors:
            results[docId] = self.angleBetween(queryVector, documentVectors.get(docId))
        
        return list(reversed(sorted(results.items(), key=operator.itemgetter(1))))
        


    # Finds the angle between 2 n dimensional vectors
    def angleBetween(self, v1, v2):
        numerator = 0
        d1 = 0
        d2 = 0
        denom1 = 0
        denom2 = 0
        
        # TODO - This can be done while processing - refactor
        for i in range(0, len(v1)):
            numerator += v1[i] * v2[i]
            d1 += v1[i]**2
            d2 += v2 [i]**2
        denom1 = math.sqrt(d1)
        denom2 = math.sqrt(d2)
        denominator = denom1 * denom2

        # TODO - denominator should never be zero because of getCandidates??
        if denominator == 0:
            return 0
        else:
            return numerator / denominator
