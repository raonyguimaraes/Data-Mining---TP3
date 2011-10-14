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

DISTANCE_THRESHOLD = 0.34
#DISTANCE_THRESHOLD = 0.34
DISTANCE = jaccard_distance
SAMPLE_SIZE = 1000
print "Sample Size:"+str(SAMPLE_SIZE)

# Define a scoring function
def score(tag1, tag2):
  return DISTANCE(set(tag1.split()), set(tag2.split()))

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
  tags = line
  for tag in tags:
    all_tags.append(tag)
    fdist.inc(tag)

print 'finished reading file!'

print str(len(all_tags))+" tags"
print str(len(musics))+" musics"

print "Removing Duplicates..."

unique_tags = []
unique_musics = []

for tag in all_tags:
  if tag not in unique_tags:
    unique_tags.append(tag)

print str(len(all_tags))+"unique tags"

for music in musics:
  if music not in unique_musics:
    unique_musics.append(music)
    
print str(len(unique_musics))+"unique musics"

die()

#frequency of tag

top50_frequency = fdist.values()[:50]
top50 = fdist.keys()[:50]
print "Most 50 frequent tags"
print top50
print top50_frequency



#using pretty table
pt = PrettyTable(fields=['Tag', 'Freq'])
pt.set_field_align('Tag', 'l')
#get the terms more frequent them one
#[pt.add_row([tag, freq]) for (tag, freq) in fdist.items() if freq > 1]
#get all the terms
[pt.add_row([tag, freq]) for (tag, freq) in fdist.items()]
#[:50]
pt.printt()

#sort_list = fdist.keys()
#print sort_list

###############Cluster tags USING Random
#print "Clustering Tags"
#clusters = {}
##for each tag
#for tag1 in all_tags:
  #clusters[tag1] = []
  #for sample in range(SAMPLE_SIZE):
    #tag2 = all_tags[random.randint(0, len(all_tags)-1)]
    ##for tag2 in all_tags:
    #if tag2 in clusters[tag1] or clusters.has_key(tag2) and tag1 in clusters[tag2]:
      #continue
    #distance = DISTANCE(set(tag1.split()), set(tag2.split()))
    #if distance < DISTANCE_THRESHOLD:
      #clusters[tag1].append(tag2)
      
      

#Flatten out clusters
#clusters = [clusters[tag] for tag in clusters if len(clusters[tag]) > 1]

############Cluster tags using Hierarquical Cluster
## Feed the class your data and the scoring function
#hc = HierarchicalClustering(all_tags, score)
## Cluster the data according to a distance threshold
#clusters = hc.getlevel(DISTANCE_THRESHOLD)

## Remove singleton clusters
#clusters = [c for c in clusters if len(c) > 1]

#print "Number of clusters for tags:"+str(len(clusters))

#print "Clustering Musics"      
## Round up musics who are in these clusters and group them together
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




