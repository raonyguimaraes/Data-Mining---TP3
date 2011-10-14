#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import nltk
import unicodedata
import re
import json
import shutil
import webbrowser
from nltk.metrics.distance import masi_distance
from cluster import HierarchicalClustering

HTML_TEMPLATE = '../web_code/protovis/linkedin_tree.html'

# Another option for a template
HTML_TEMPLATE = '../web_code/protovis/linkedin_dendogram.html'

OUT = os.path.basename(HTML_TEMPLATE)



DISTANCE_THRESHOLD = 0.34

DISTANCE = masi_distance

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

######## Begin: HAC ########

# Define a scoring function


def score(title1, title2):
    return DISTANCE(set(title1.split()), set(title2.split()))


# Feed the class your data and the scoring function

hc = HierarchicalClustering(all_tags, score)

# Cluster the data according to a distance threshold

clusters = hc.getlevel(DISTANCE_THRESHOLD)

# Remove singleton clusters
# clusters = [c for c in clusters if len(c) > 1]

######## End: HAC ########

# Round up contacts who are in these clusters and group them together

clustered_contacts = {}
for cluster in clusters:
    clustered_contacts[tuple(cluster)] = []
    for contact in contacts:
        for title in contact['Job Titles']:
            if title in cluster:
                clustered_contacts[tuple(cluster)].append('%s %s.'
                        % (contact['First Name'], contact['Last Name'][0]))

json_output = {}
for titles in clustered_contacts:

    descriptive_terms = set(titles[0].split())
    for title in titles:
        descriptive_terms.intersection_update(set(title.split()))

    json_output[', '.join(descriptive_terms)[:30]] = dict([(c, None) for c in
            clustered_contacts[titles]])

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