#/usr/bin/python

"""
This script clusters the sentences.
"""
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from sets import Set
from cluster import Cluster
import math
from collections import Counter

# This is the global clusters dictionary that contains the id and cluster pair
clusters = dict()

# CID - cluster id
cid = 0


######################### Pre processing functions ###########################
# Step 1: word tokenize
def tokenize(sentence):
  return nltk.word_tokenize(sentence)
  

def lemmatize(words):
  return [lemmatizer.lemmatize(word) for word in words]


def filter(lems):
  """ 
  Removes the stop words from the list of lems sent and returns list of 
  filtered lems.
  """
  if lems != None:
    return [term for term in lems if term not in stopwords.words('english')]
  return None


def cosineSimilarity(terms1, terms2):
  """
  Makes a list of exhaustive unique terms and computes magnitudes and
  dot product and returns the cosine similarity. Max score = 1, min score = 0
  terms 1 - dictionary of sentence1 term frequencies
  terms 2 - dictionary of sentence2 term frequencies
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


def cluster(clusters, terms): 
  """
  Clusters terms of new node with the existing list of clusters. If
  new, adds it to the cluster. Else, returns the cluster id.
  """
  id = 0
  for id, clusterTerms in clusters.iteritems():
    if any(term in clusterTerms for term in terms):
      return id

  clusterTerms[id+1]=terms
  pass


def addNewCluster(clusters, cid, tf, sentence):
  print "Added new cluster for cid: {}".format(cid)
  newCluster = Cluster(cid)
  newCluster.tf = tf
  newCluster.addSentenceToCluster(sentence)
  clusters[cid] = newCluster

def addToCluster(clusters, cid, tf, sentence):
  if cid in clusters.keys():
    clusters.get(cid).addToTerms(tf)
    clusters.get(cid).addSentenceToCluster(sentence)
  else:
    cid = max(clusters.keys()) + 1
    addNewCluster(clusters, cid, tf, sentence)

def clusterize(clusters, tf, sentence):
  print "Clustering sentence: {}".format(sentence)
  bigCID = -1
  bigSimScore = -1

  # First cluster
  if len(clusters) == 0:
    addNewCluster(clusters, 1, tf, sentence)
  
  else:
    for cid, cluster in clusters.iteritems():
      simScore = cosineSimilarity(cluster.tf, tf)
      if simScore > bigSimScore:
        bigSimScore = simScore
        bigCID = cid 
  
    if bigSimScore > 0.4:# Cos 45 = 0.707, cos60 = 0.5
      addToCluster(clusters, bigCID, tf, sentence)
    else:
      # Create a new cluster
      cid = max(clusters.keys()) + 1
      addNewCluster(clusters, cid, tf, sentence)
  
def clusterSentence(sentence):
  global clusters

  words = tokenize(sentence.lower())
  lems = lemmatize(words)
  terms = filter(lems)
  tf = dict(Counter(terms))
  clusterize(clusters, tf, sentence)  

def generateClusters(fileName):
  fp = open(fileName, 'rb+')
  for line in fp:
    clusterSentence(line)
