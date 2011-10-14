#!/usr/bin/python
# -*- coding: utf-8 -*-


import unicodedata
import re

import nltk
from prettytable import PrettyTable

from nltk.metrics.distance import jaccard_distance, masi_distance

DISTANCE_THRESHOLD = 0.20
#DISTANCE_THRESHOLD = 0.34
DISTANCE = jaccard_distance

def clean_string(string):
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
linecount = 0
all_tags = []
musics = []
for line in data:
  line = clean_string(line).split(',')
  new_music_line = []
  for music_tag in line:
    if music_tag not in new_music_line:
      new_music_line.append(music_tag)
  musics.append(new_music_line)
  tags = line
  for tag in tags:
    all_tags.append(tag)
    fdist.inc(tag)

print 'finished reading file'
print str(len(all_tags))+" tags"
print str(len(musics))+" musics"

#frequency of tag

#top50_frequency = fdist.values()[:50]
#top50 = fdist.keys()[:50]
#print "Most 50 frequent terms"
#print top50
#print top50_frequency



#using pretty table
#pt = PrettyTable(fields=['Tag', 'Freq'])
#pt.set_field_align('Tag', 'l')
#[pt.add_row([tag, freq]) for (tag, freq) in fdist.items() if freq > 1]
##[:50]
#pt.printt()

#sort_list = fdist.keys()
#print sort_list

###############Cluster tags
print "Clustering Tags"
clusters = {}
for tag1 in all_tags:
  clusters[tag1] = []
  for tag2 in all_tags:
    if tag2 in clusters[tag1] or clusters.has_key(tag2) and tag1 in clusters[tag2]:
      continue
    distance = DISTANCE(set(tag1.split()), set(tag2.split()))
    if distance < DISTANCE_THRESHOLD:
      clusters[tag1].append(tag2)




# Flatten out clusters
clusters = [clusters[tag] for tag in clusters if len(clusters[tag]) > 1]


print "Number of clusters for tags:"+str(len(clusters))

print "Clustering Musics"      
# Round up musics who are in these clusters and group them together
clustered_musics = {}
for cluster in clusters:
  clustered_musics[tuple(cluster)] = []
  for idx, music in enumerate(musics):
    for tag in music:
      if tag in cluster:
	clustered_musics[tuple(cluster)].append('%s' % (idx))



print "Printing Clusters"
#############Printing Cluster Created
for tags in clustered_musics:
  common_tags_heading = 'Common Tags: ' + ', '.join(tags)
  print common_tags_heading
  descriptive_terms = set(tags[0].split())
  for tag in tags:
    descriptive_terms.intersection_update(set(tag.split()))
    descriptive_terms_heading = 'Descriptive Terms: ' + ', '.join(descriptive_terms)
  print descriptive_terms_heading
  print '-' * max(len(descriptive_terms_heading), len(common_tags_heading))
  print ','.join(clustered_musics[tags])
  print

#calculate distance between musics
#for each music calculate distance beetween this with all the others
#matrix of distance


#cluster



