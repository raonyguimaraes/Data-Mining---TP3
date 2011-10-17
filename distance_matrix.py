#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import re
import random
import nltk
from prettytable import PrettyTable
import numpy as np


from nltk.metrics.distance import jaccard_distance, masi_distance

# Import the goods
from cluster import HierarchicalClustering

DISTANCE_THRESHOLD = 1.0
#DISTANCE_THRESHOLD = 0.34
DISTANCE = jaccard_distance
SAMPLE_SIZE = 1000
print "Sample Size:"+str(SAMPLE_SIZE)

# Define a scoring function
def score(tag1, tag2):
  return DISTANCE(set(tag1.split(",")), set(tag2.split(",")))

def normalize(string):
  #remove acentos e transforma para maiusculas
  clean_string = unicodedata.normalize('NFKD', string.decode('utf-8')).encode('ASCII','ignore').lower()
  #remove repetição de letras
  clean_string  = re.sub(r'([a-z!?.])\1+', r'\1', clean_string)
  #remove traços '
  clean_string  = re.sub(r'-', ' ', clean_string)
  clean_string  = re.sub(r'\'', '', clean_string)
  
  return clean_string.strip()

data_file = open('tags2.txt', 'rb')
data = data_file.readlines()

fdist = nltk.FreqDist()
musics_fdist = nltk.FreqDist()
linecount = 0
all_tags = []
musics = []
for line in data:
  line = normalize(line).split(',')
  new_music_line = []
  #for all the tags from this music
  for music_tag in line:
    #remove duplicated musics
    #if music_tag not in new_music_line:
    new_music_line.append(music_tag)
  musics.append(new_music_line)
  musics_fdist.inc(",".join(new_music_line))
  tags = line
  #for tag in tags:
    #all_tags.append(tag)
    #fdist.inc(tag)

print 'finished reading file!'

#unique_tags = fdist.keys() 
unique_musics = musics_fdist.keys()

#print str(len(all_tags))+" tags being "+str(len(unique_tags))+" uniques"
print str(len(musics))+" musics being "+str(len(unique_musics))+" uniques"

#matrix[][]= [len(unique_musics)][len(unique_musics)]
distMatrix = np.zeros((len(unique_musics), len(unique_musics)))
print len(distMatrix)
#calculate distance matrix for musics
for idx1, music1 in enumerate(unique_musics):
  for idx2, music2 in enumerate(unique_musics):
    print idx1, idx2
    print music1 ,music2
    distMatrix[idx1-1][idx2-1] = 1 - score(music1, music2)

print distMatrix[1]