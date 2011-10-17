#!/usr/bin/env python
## -*- coding: utf-8 -*-


# Cluster.py
# Author: RaonyGuimarães

#import the goods!

import unicodedata
import re
import random
import nltk
from prettytable import PrettyTable
from nltk.metrics.distance import jaccard_distance, masi_distance
from numpy import zeros

from cluster import HierarchicalClustering

#CONSTANT VARIABLES
DISTANCE_THRESHOLD = 1.0
#DISTANCE_THRESHOLD = 0.34
DISTANCE = jaccard_distance
SAMPLE_SIZE = 1000

class RCluster:
  
  #define global variables
  
  def __init__(self):
    print "Init"
    
    
    
  def main(self):
    print "Main"
    musics = self.loaddata()
  
  # Calculate Distance Between 2 strings Ex. ['rock', 'rock and roll']
  def distance(self, word1, word2):
    return DISTANCE(set(word1.split()), set(word.split()))
  
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
    data_file = open('tags.txt', 'rb')
    data = data_file.readlines()
    #Load all musics in memory
    for line in data:
      line = self.normalize(line).split(',')
      new_music_line = []
      #for all the tags from this music
      musics.append(new_music_line)
    print 'Finished reading file!'
  
  #Print frequent Items from a list
  #items:musics, size:50, name:Musics
  def freq_dist(self, items, size, name):
    print "hello"
    
    
  
    


if __name__ == "__main__":
    cluster = RCluster()
    cluster.main()