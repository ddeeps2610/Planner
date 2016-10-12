#/usr/bin/python

"""
This script logs the idea in Ideas.txt file with time stamp.
"""
import datetime
import os,sys

idea = ''.join([word+' ' for word in sys.argv[1:]]) + '\n'
message = str(datetime.datetime.now()) + " " + idea

# Step 1: log the idea 
fp = None
ideaFile = 'Ideas.txt'
inputFile = 'input.txt'
if os.path.exists(ideaFile):
  fp = open(ideaFile, 'ab+')
  fp2 = open(inputFile, 'ab+')
  fp.write(message)
  fp2.write(idea)
else:
  fp = open(filePath, 'wb+')
  fp.write(message)
  fp2 = open(inputFile, 'wb+')
  fp2.write(idea)
fp.close()
fp2.close()

# Step 2: clusterize the idea
from sentenceClusterer import Clusterer
clusterer = Clusterer(train=True)
clusterer.clusterSentence(idea)
