#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import re
import random
import nltk
from prettytable import PrettyTable

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

data_file = open('tags.txt', 'rb')
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
  for tag in tags:
    all_tags.append(tag)
    fdist.inc(tag)

print 'finished reading file!'

unique_tags = fdist.keys() 
unique_musics = musics_fdist.keys()

print str(len(all_tags))+" tags being "+str(len(unique_tags))+" uniques"
print str(len(musics))+" musics "+str(len(unique_musics))+" uniques"


#frequency of tag and musics

#top50_tags = fdist.keys()[:50]
#top50_tags_frequency = fdist.values()[:50]

###################50 Most Frequent Tags
#pt = PrettyTable(fields=['Tag', 'Freq'])
#pt.set_field_align('Tag', 'l')
##get the terms more frequent them one
##[pt.add_row([tag, freq]) for (tag, freq) in fdist.items() if freq > 1]
##get all the terms
#[pt.add_row([tag, freq]) for (tag, freq) in fdist.items()]
##[:50]
#pt.printt()

#################50 Most Frequent Musics
#pt = PrettyTable(fields=['Music', 'Freq'])
#pt.set_field_align('Music', 'l')
##get the terms more frequent them one
##[pt.add_row([tag, freq]) for (tag, freq) in fdist.items() if freq > 1]
##get all the terms
#[pt.add_row([tag, freq]) for (tag, freq) in musics_fdist.items() if freq > 1]
##[:50]
#pt.printt()



###############Cluster tags USING Random
#print "Clustering Tags"
#clusters = {}
##for each tag in unique_tags tags
#for tag1 in unique_tags:
  #clusters[tag1] = []
  ##get a sample of unique_tags the size SAMPLE_SIZE
  ##for sample in range(SAMPLE_SIZE):
  #tag2 = unique_tags[random.randint(0, len(unique_tags)-1)]
  #for tag2 in unique_tags:
    #if tag2 in clusters[tag1] or clusters.has_key(tag2) and tag1 in clusters[tag2]:
      #continue
    #distance = DISTANCE(set(tag1.split()), set(tag2.split()))
    #if distance < DISTANCE_THRESHOLD:
      #clusters[tag1].append(tag2)
##Flatten out clusters
#clusters = [clusters[tag] for tag in clusters if len(clusters[tag]) > 1]

#############Cluster tags using Hierarquical Cluster
## Feed the class your data and the scoring function
#hc = HierarchicalClustering(unique_musics, score)
## Cluster the data according to a distance threshold
#clusters = hc.getlevel(DISTANCE_THRESHOLD)

## Remove singleton clusters
#clusters = [c for c in clusters if len(c) > 1]

#print "Number of clusters for musics:"+str(len(clusters))
#print "Printing Clusters.."

#for cluster in clusters:
  #print len(cluster)
  #for music in cluster:
    #print music


#print "Clustering Musics"      
## Round up unique_musics who are in these clusters and group them together
#clustered_musics = {}
#for cluster in clusters:
  #clustered_musics[tuple(cluster)] = []
  #for idx, music in enumerate(musics):
    #for tag in music:
      #if tag in cluster:
	#clustered_musics[tuple(cluster)].append('%s' % (idx))



#print "Printing Clusters"
##############Printing Cluster Created
#for tags in clustered_musics:
  #common_tags_heading = 'Common Tags: ' + ', '.join(tags)
  #print common_tags_heading
  #descriptive_terms = set(tags[0].split())
  #for tag in tags:
    #descriptive_terms.intersection_update(set(tag.split()))
    #descriptive_terms_heading = 'Descriptive Terms: ' + ', '.join(descriptive_terms)
  #print descriptive_terms_heading
  #print '-' * max(len(descriptive_terms_heading), len(common_tags_heading))
  #print ','.join(clustered_musics[tags])
  #print

  
#calculate distance between musics
#for each music calculate distance beetween this with all the others
#matrix of distance

#cluster


#After clustering, do cluster evaluation
#Calculate intra and inter cluster distances




