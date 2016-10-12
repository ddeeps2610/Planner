#/usr/bin/python

"""
This script clusters the sentences.
"""
#import nltk
#from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer
#lemmatizer = WordNetLemmatizer()
from sets import Set
from cluster import Cluster
import math
from collections import Counter
import utils
import pickle
import os, sys


class Clusterer():
  # This is the global clusters dictionary that contains the id and cluster pair
  clusters = None

  # CID - cluster id
  newCID = 0

  # clusterized existing input sentences
  trained = False

  # Clusters pickle file name
  clustersPickleFile = 'clusters.pkl'
 
  def __init__(self, train = False):
    """
    Initializes data with existing clusters.
    """
    # Load clusters if there is a clusters.pkl file
    if os.path.exists(self.clustersPickleFile):
        fp = open(self.clustersPickleFile, 'rb+')
        self.clusters = pickle.load(fp)
        fp.close()
      
        # Set the model to trained
        self.trained = True
    else:
        self.clusters = dict()
        if train:
            self.generateClusters('input.txt')

    # Update the new cluster ID
    self.newCID = max(self.clusters.keys())

  def isTrained(self):
    """
    Checks if the clusterized the existing input sentences.
    """
    if self.trained != None:
        return self.trained
    return False

  def cosineSimilarity(self, terms1, terms2):
    """
    Makes a list of exhaustive unique terms and computes magnitudes and
    dot product and returns the cosine similarity. Max score = 1, min score = 0
    terms1 - dictionary of sentence1 term frequencies
    terms2 - dictionary of sentence2 term frequencies
    """
    #print "Computing cosine sim between: \n{} and \n {}".format(terms1, terms2)
    allTerms = Set(terms1.keys() + terms2.keys())
    mag1 = 0
    mag2 = 0
    dotProduct = 0
    for term in allTerms:
        if term in terms1.keys():
            mag1 += math.pow(terms1.get(term), 2)
        if term in terms2.keys():
            mag2 += math.pow(terms2.get(term), 2)
        if term in terms1.keys() and term in terms2.keys():
            dotProduct += terms1.get(term) * terms2.get(term)
        #print "Mag1: {}, Mag2: {}, dotProd: {}".format(mag1, mag2, dotProduct)
    if (mag1 == 0) or (mag2 == 0):
        return 0
    else:
        simScore = dotProduct / (math.sqrt(mag1) * math.sqrt(mag2))
        return simScore



  def addNewCluster(self, tf, sentence):
      """
      Creates a new cluster and adds it to the clusters.
      tf - term frequency counts of the given sentence
      sentence - sentence to be added to the cluster
      """
      self.newCID += 1
      newCluster = Cluster(self.newCID)
      newCluster.tf = tf
      newCluster.addSentenceToCluster(sentence)
      self.clusters[self.newCID] = newCluster
      print "Added new cluster for cid: {}".format(self.newCID)
  
  def addToCluster(self, cid, tf, sentence):
      """
      Adds the sentence to the given cluster.
      cid - cluster id of the cluster to which sentence is added.
      tf - term frequency counts for the given sentence
      sentence - sentence to be clustered.
      """
      print "Adding to existing cluster: ", cid
      if cid in self.clusters.keys():
          self.clusters.get(cid).addToTerms(tf)
          self.clusters.get(cid).addSentenceToCluster(sentence)
      else:
          self.addNewCluster(tf, sentence)
 
  def clusterize(self, tf, sentence):
      """
      clusters the sentence with existing cluster.
      tf - term frequency counts for the given sentence.
      sentence - sentence to be clustered.
      """
      print "\nClustering sentence: {}".format(sentence.strip())
      bigCID = -1
      bigSimScore = -1

      # First cluster
      if len(self.clusters) == 0:
          self.addNewCluster(tf, sentence)
  
      else:
          for cid, cluster in self.clusters.iteritems():
              simScore = self.cosineSimilarity(cluster.tf, tf)
              if simScore > 0:
                  print "cid: {}, simScore: {}".format(cid, simScore)
                  print "cluster sentence: ", cluster.sentences
                  print ""
              if simScore > bigSimScore:
                  bigSimScore = simScore
                  bigCID = cid 
  
          if bigSimScore > 0.4:# Cos 45 = 0.707, cos60 = 0.5
              self.addToCluster(bigCID, tf, sentence)
          else:
              # Create a new cluster
              self.addNewCluster(tf, sentence)
    
  def clusterSentence(self, sentence):
      """
      clusters the given sentence with existing cluster or creates a
      new cluster.
      sentence - sentence to be clustered
      """
      words = utils.tokenize(sentence.lower())
      lems = utils.lemmatize(words)
      terms = utils.filterStopWords(lems)
      tf = dict(Counter(terms))
      self.clusterize(tf, sentence)  
   
      # Every time a new sentence is clusterized, save latest clusters
      self.saveClusters()

  def saveClusters(self):
      """
      Saves the cluster in clusterPickleFile
      """
      fp = open(self.clustersPickleFile, 'wb+')
      pickle.dump(self.clusters, fp)
      fp.close()

  def generateClusters(self, fileName):
      """
      Clusters sentences from a fileName.
      fileName - file that contains sentences to be clustered.
      """
      fp = open(fileName, 'rb+')
      for line in fp:
          self.clusterSentence(line)
      fp.close()    



if __name__ == "__main__":
    fileName = 'input.txt'
    clusterer = Clusterer()
    clusterer.generateClusters(fileName)
