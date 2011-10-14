#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.metrics.distance import jaccard_distance, masi_distance


#from numpy import array
#from nltk import cluster
from nltk.cluster import euclidean_distance
#vectors = [array(f) for f in [[3, 3], [1, 2], [4, 2], [4, 0]]]
#clusterer = cluster.KMeansClusterer(2, euclidean_distance, repeats=10)
#print clusterer.cluster(vectors, True) 


# Define a scoring function
def score(tag1, tag2):
  return jaccard_distance(set(tag1[0]), set(tag2[0]))


from nltk import cluster
import numpy

vectors = [numpy.array(f) for f in [[2, 1], [1, 3], [4, 7], [6, 7]]]
#vectors = [["car", "bar"], ["bar", "car"], ["bar", "car"], ["car", "bar"]]
#means = [[4, 3], [5, 5]]

clusterer = cluster.KMeansClusterer(2, euclidean_distance) #, initial_means=means
clusters = clusterer.cluster(vectors, True, trace=True)

print 'Clustered:', vectors
print 'As:', clusters
print 'Means:', clusterer.means()
print

#vectors = [numpy.array(f) for f in [[3, 3], [1, 2], [4, 2], [4, 0], [2, 3], [3, 1]]]

## test k-means using the euclidean distance metric, 2 means and repeat
## clustering 10 times with random seeds

#clusterer = cluster.KMeansClusterer(2, euclidean_distance, repeats=10)
#clusters = clusterer.cluster(vectors, True)
#print 'Clustered:', vectors
#print 'As:', clusters
#print 'Means:', clusterer.means()
#print

## classify a new vector
#vector = numpy.array([3, 3])
#print 'classify(%s):' % vector,
#print clusterer.classify(vector)
#print

