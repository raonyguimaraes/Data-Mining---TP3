#!/usr/bin/python
# -*- coding: utf-8 -*-


import unicodedata
import re

import nltk
from prettytable import PrettyTable

from nltk.metrics.distance import jaccard_distance, masi_distance

DISTANCE_THRESHOLD = 0.34
#DISTANCE_THRESHOLD = 0.34
DISTANCE = masi_distance

# Import the goods
from cluster import HierarchicalClustering


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
  musics.append(line)
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


print "Clustering Musics"      

# Define a scoring function
def score(music1, music2):
  return DISTANCE(set(music1), set(music2))

# Feed the class your data and the scoring function
hc = HierarchicalClustering(musics, score)
# Cluster the data according to a distance threshold
clusters = hc.getlevel(DISTANCE_THRESHOLD)

# Remove singleton clusters
clusters = [c for c in clusters if len(c) > 1]


######## End: HAC ########

# Round up musics who are in these clusters and group them together

clustered_musics = {}

for cluster in clusters:
  clustered_musics[tuple(cluster)] = []
  for idx, music in enumerate(musics):
    for tag in music:
      if tag in cluster:
	clustered_musics[tuple(cluster)].append('%s' % (idx))
	
	

json_output = {}
for tags in clustered_musics:

    descriptive_terms = set(tags[0].split())
    for title in tags:
        descriptive_terms.intersection_update(set(title.split()))

    json_output[', '.join(descriptive_terms)[:30]] = dict([(c, None) for c in
            clustered_musics[tags]])


if not os.path.isdir('out'):
    os.mkdir('out')

# HTML_TEMPLATE references some dependencies that we need to
# copy into out/

shutil.rmtree('out/protovis-3.2', ignore_errors=True)

shutil.copytree('../web_code/protovis/protovis-3.2',
                'out/protovis-3.2')

html = open(HTML_TEMPLATE).read() % (json.dumps(json_output),)
f = open(os.path.join(os.getcwd(), 'out', OUT), 'w')
f.write(html)
f.close()

print 'Data file written to: %s' % f.name

# Open up the web page in your browser

webbrowser.open('file://' + f.name)