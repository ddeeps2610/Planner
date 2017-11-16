#/usr/bin/python

"""
This file defines the cluster class that stores the cluster details.
"""


class Cluster():
  cid = 0
  tf = None
  sentences = None

  def __init__(self, cid):
    self.cid = cid
    self.tf = dict()
    self.sentences = list()

  def addToTerms(self, tf):
    """
    Adds only unique terms to the cluster terms
    terms - list of cluster terms that are generated from new setence.
    """ 
    for term, count in tf.iteritems():
      if term in self.tf.keys():
        self.tf[term] += count
      else:
        self.tf[term] = count

  def addSentenceToCluster(self, sentence):
    """
    Stores the cluster setences.
    sentence - sentence that is to be stored in the cluster
    """
    self.sentences.append(sentence)

