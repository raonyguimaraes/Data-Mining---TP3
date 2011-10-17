#!/usr/bin/env python
## -*- coding: utf-8 -*-


# Cluster.py
# Author: RaonyGuimarães

#import the goods!

import unicodedata
import re
import random
import nltk
import scipy
import matplotlib



from scipy.spatial import distance
import scipy.cluster.hierarchy as sch
import pylab
from hcluster import pdist, linkage, dendrogram, squareform
import numpy

from prettytable import PrettyTable
from nltk.metrics.distance import jaccard_distance, masi_distance
from numpy import zeros
from cluster import HierarchicalClustering
#from cluster import HierarchicalClustering

#CONSTANT VARIABLES
DISTANCE_THRESHOLD = 0.34
#DISTANCE_THRESHOLD = 0.34
DISTANCE = jaccard_distance
SAMPLE_SIZE = 100

class RCluster:
  
  #define global variables
  distances = scipy.zeros([0,0])
  all_items = []
  def __init__(self):
    print "Init"

  def main(self):
    print "Main"
    musics = self.loaddata()
    #print Frequency
    print "Frequency of original data.."
    self.stats(musics)
    samples = self.getsamples(musics, SAMPLE_SIZE)
    print "Frequency of sample data..."
    self.stats(samples)
    
    #print "Group Similar Categories..."
    #self.group_categories(samples, DISTANCE_THRESHOLD)
    #print "Find Similar Musics"
    #self.mostsimilar(samples)

    print "Calculate Distance Matrix..."
    distances = self.distance_matrix(samples)
    #distances = []
    #print "Relevant Musics..."
    #self.mostrelevant(samples)
    print "Cluster Items..."
    self.cluster(samples, distances)
    
    
    #self.freq_dist(samples, 20, "Musics")
      
  # Calculate Distance Between 2 strings Ex. ['rock', 'rock and roll']
  def score(self, idx1, idx2):
    global distances
    #global all_items
    #idx1 = all_items.index(item1)
    #idx2 = all_items.index(item2)
    if idx1 < idx2:
      dist = 1 - distances[idx1][idx2]
    else:
      dist = 1 - distances[idx2][idx1]
    #print "Distance Beeween %s, %s: %s" % (idx1, idx2, dist)
    return dist
  
  # Normalize String
  def normalize(self,string):
    #remove acentos e transforma para maiusculas
    clean_string = unicodedata.normalize('NFKD', string.decode('utf-8')).encode('ASCII','ignore').lower()
    #remove repetição de letras
    clean_string  = re.sub(r'([a-z!?.])\1+', r'\1', clean_string)
    #remove traços '
    clean_string  = re.sub(r'-', ' ', clean_string)
    clean_string  = re.sub(r'\'', '', clean_string)
    
    return clean_string.strip()
  
  #Load data into memory
  def loaddata(self):
    musics = []
    print 'Reading file...'
    data_file = open('sample_100.txt', 'rb')
    data = data_file.readlines()
    #Load all musics in memory
    for line in data:
      line = self.normalize(line).split(',')
      #remove duplicated tags for  the same music
      music_tags = []
      for tag in line:
	if tag not in music_tags:
	  music_tags.append(tag)
      #for all the tags from this music
      musics.append(music_tags)
    print 'Finished reading file!'
    return musics
  
  #Print the most frequent items from a list
  #items:musics, size:50, name:Musics
  def freq_dist(self, items, size, name):
    print "Print the "+str(size)+" most frequent "+str(name)
    fdist = nltk.FreqDist()
    for item in items:
      fdist.inc(",".join(item))
    if not name:
      name = "Item"
    pt = PrettyTable(fields=[name, 'Freq'])
    pt.set_field_align(name, 'l')
    [pt.add_row([tag, freq]) for (tag, freq) in fdist.items()[:size]]
    pt.printt()
    
    
  def getsamples(self, items, size):
    global all_items
    samples = []
    for sample in range (0, size):
      item = items[random.randint(0, len(items)-1)]
      #if item not in samples:
	#print ",".join(item)
      samples.append(item)
    all_items = samples
    
    return samples
  #print stats about items
  def stats(self, items):
    #use fdist to make it fast!
    objects = nltk.FreqDist()
    categories = nltk.FreqDist()
    categories_count = 0
    for item in items:
      objects.inc(",".join(item))
      for category in item:
	categories_count = categories_count + 1
	categories.inc(category)
    print "Objects: "+str(len(items))+" being "+str(len(objects.items()))+" uniques"
    print "Categories: "+str(categories_count)+" being "+str(len(categories.items()))+" uniques"

  def group_categories(self,items, threshold):
    #categories = []
    fdist = nltk.FreqDist()
    for item in items:
      for category in item:
	fdist.inc(category)
    categories = fdist.keys()
    print "Unique Categories: "+str(len(categories))
    
    print "Grouping Categories"
    ##############Greedy approach to Cluster tags
    
    groups = {}
    #for each tag in categories tags
    for tag1 in categories:
      groups[tag1] = []
      for tag2 in categories:
	if tag2 in groups[tag1] or groups.has_key(tag2) and tag1 in groups[tag2]:
	  continue
	distance = DISTANCE(set(tag1.split()), set(tag2.split()))
	if distance < DISTANCE_THRESHOLD:
	  groups[tag1].append(tag2)
    #Flatten out groups
    groups = [groups[tag] for tag in groups if len(groups[tag]) > 1]
    print "Number of groups for categories:"+str(len(groups))
    
    print "Printing Groups..."
    #############Printing Cluster Created
    for idx, tags in enumerate(groups):
      common_tags_heading = 'Common Categories: ' + ', '.join(tags)
      print common_tags_heading
      descriptive_terms = set(tags[0].split())
      for tag in tags:
	descriptive_terms.intersection_update(set(tag.split()))
	descriptive_terms_heading = 'Descriptive Terms: ' + ', '.join(descriptive_terms)
      print descriptive_terms_heading
      print '-' * max(len(descriptive_terms_heading), len(common_tags_heading))
      print ','.join(groups[idx])
      print
  
  def distance_matrix(self, items):
    global distances
    tc = nltk.TextCollection(items)
    td_matrix = {}
    for idx in range(len(items)):
      item = items[idx]
      fdist = nltk.FreqDist(item)
      td_matrix[idx] = {}
      for term in fdist.iterkeys():
	td_matrix[idx][term] = tc.tf_idf(term, item)
    
    # Build vectors such that term scores are in the same positions...
    #distances = {}
    distances = scipy.zeros([len(items),len(items)])

    for idx1 in td_matrix.keys():
      #distances[idx1] = {}
      for idx2 in td_matrix.keys():
	if idx1 <= idx2:
	  terms1 = td_matrix[idx1].copy()
	  terms2 = td_matrix[idx2].copy()
	  # Fill in "gaps" in each map so vectors of the same length can be computed
	  for term1 in terms1:
	    if term1 not in terms2:
	      terms2[term1] = 0
	  for term2 in terms2:
	    if term2 not in terms1:
	      terms1[term2] = 0
	  # Create vectors from term maps
	  v1 = [score for (term, score) in sorted(terms1.items())]
	  v2 = [score for (term, score) in sorted(terms2.items())]
	  score = nltk.cluster.util.cosine_distance(v1, v2)
	  
	  distances[idx1][idx2] = 1 - score
	if idx2 > idx1:
	  distances[idx2][idx1] = distances[idx1][idx2]
	
    print distances	    
    return distances
  
  def mostsimilar(self,items):
    tc = nltk.TextCollection(items)
    # Compute a term-document matrix such that td_matrix[doc_title][term]
    # returns a tf-idf score for the term in the item
    td_matrix = {}
    for idx in range(len(items)):
      item = items[idx]
      fdist = nltk.FreqDist(item)
      td_matrix[idx] = {}
      for term in fdist.iterkeys():
	td_matrix[idx][term] = tc.tf_idf(term, item)
    
    # Build vectors such that term scores are in the same positions...
    distances = {}
    for idx1 in td_matrix.keys():
      #print idx1
      distances[idx1] = {}
      #print distances[idx]
      #(max_score, most_similar) = (0.0, None)
      max_score = 0.0
      most_similar = None
      for idx2 in td_matrix.keys():
	# Take care not to mutate the original data structures
	# since we're in a loop and need the originals multiple times
	terms1 = td_matrix[idx1].copy()
	terms2 = td_matrix[idx2].copy()
	# Fill in "gaps" in each map so vectors of the same length can be computed
	for term1 in terms1:
	  if term1 not in terms2:
	    terms2[term1] = 0
	for term2 in terms2:
	  if term2 not in terms1:
	    terms1[term2] = 0
	# Create vectors from term maps
	v1 = [score for (term, score) in sorted(terms1.items())]
	v2 = [score for (term, score) in sorted(terms2.items())]
	# Compute similarity among items
	#print idx1, idx2
	distances[idx1][idx2] = nltk.cluster.util.cosine_distance(v1, v2)
	
	if idx1 == idx2:
	  continue
	if distances[idx1][idx2] > max_score:
	  max_score = distances[idx1][idx2]
	  most_similar = idx2
	  #(max_score, most_similar) = (distances[idx1][idx2], idx2)
      
      #print most similar documents
      #print most_similar, max_score
      print '''The Most Similar to item %s is
      \t%s
      \tscore %s
      ''' % (idx1, most_similar, max_score)
      #print '''Most similar to %s
      #\t%s (%s)
      #\tscore %s
      #''' % (idx1,
      #most_similar[0], most_similar[1], max_score)
      
	
      
    
  def cluster(self, items, distances):
    D = distances
    
    Y = sch.linkage(D, method='single')#, metric=''
    treshold = 0.5*max(D[:,2])
    treshold = 0
    Z = sch.dendrogram(Y, orientation='top', color_threshold=treshold)
    
    ###print cluster based on a treshold
    
    ###cutoff = 0.5*max(Y[:,2])
    ###cutoff = 0
    ##print "cutt of: %s"+str(cutoff)
    #print "distance"
    #treshold = 0.35
    #print "treshold: "+str(treshold)
    treshold_list = [0.01, 0.03, 0.05, 0.1, 0.8, 0.9, 0.99, 0.95]
    for item in treshold_list:
      print "treshold: "+str(item)
      T = sch.fcluster(Y, item, criterion='distance')  # n
      clusters = self.clusterlists(T)
      print "numero de clusters: %s" % (len(clusters))
    
    #for item in treshold_list:  
      #print item
      #print "distance"
      #T = sch.fcluster(Y, item, criterion='distance' )  # n
      #clusters = self.clusterlists(T)
      #print "numero de clusters: %s" % (len(clusters))
    #for item in treshold_list:  
      #print item
      #print "inconsistent"
      #T = sch.fcluster(Y, item, criterion='inconsistent' )  # n
      #clusters = self.clusterlists(T)
      #print "numero de clusters: %s" % (len(clusters))      
    
      
      
    #print "cluster sizes:", map( len, clusters )
    
    #print "Imprimindo Cluster..."
    
    #count = 1
    #rank_clusters = []
    #for cluster in clusters:
	#print "Cluster %s" % (count)
	#print "Items %s" % (cluster)
	#count = count+1
	#cluster_distance = 0
	#for idx1 in cluster:
	  #print idx1, items[idx1]
	  #for idx2 in cluster:
	    #if idx1 < idx2:
	      
	      ##print distances[0][0]
	      ##print distances[1][1]
	      ##print idx1, idx2
	      #distance = distances[idx1][idx2]
	      #cluster_distance = cluster_distance + distance
	      ##print "Distance: %s" % (distance)
	#print "Cluster Distance: %s" % (cluster_distance)
	  ##print distances[idx]
	  
	  ##calculate similarity beetween clusters
	  
	  
    
    
    
    
    #plot results
    matplotlib.pylab.savefig('dendrogram.png')
    fig = pylab.figure()
    
    axdendro = fig.add_axes([0.09,0.1,0.2,0.8])
    axdendro.set_xticks([])
    axdendro.set_yticks([])

    # Plot distance matrix.
    axmatrix = fig.add_axes([0.3,0.1,0.6,0.8])
    #index = Z['leaves']
    
    #D = D[index,:]
    #D = D[:,index]
    im = axmatrix.matshow(D, aspect='auto', origin='lower')
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])
    # Plot colorbar.
    axcolor = fig.add_axes([0.91,0.1,0.02,0.8])
    pylab.colorbar(im, cax=axcolor)
    fig.savefig('matrix.png')
    
  def clusterlists(self,T):
    """ T = hier.fcluster( Z, t ) e.g. [a b a b a c]
	-> [ [0 2 4] [1 3] [5] ] sorted by len
    """
    clists = [ [] for j in range( max(T) + 1 )]
    for j, c in enumerate(T):
	clists[c].append( j )
    clists.sort( key=len, reverse=True )
    return clists[:-1]  # clip the []


if __name__ == "__main__":
    cluster = RCluster()
    cluster.main()