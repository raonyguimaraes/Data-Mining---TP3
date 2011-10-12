#!/usr/bin/python
# -*- coding: utf-8 -*-


import unicodedata
import re

#import nltk
#from prettytable import PrettyTable


def clean_string(string):
  #remove acentos e transforma para maiusculas
  clean_string = unicodedata.normalize('NFKD', string.decode('utf-8')).encode('ASCII','ignore').lower()
  #remove repetição de letras
  clean_string  = re.sub(r'([a-z!?.])\1+', r'\1', clean_string)
  return clean_string

data_file = open('tags.txt', 'rb')
data = data_file.readlines()

linecount = 0
tags_list = []
for line in data:
  line = clean_string(line)
  tags = line.split()
  #linecount=linecount+1
  #print linecount
  for tag in tags:
    tags_list.append(tag)

print 'finished reading file'
print len(tags_list)
new_tags_list = []
for tag in tags_list:
  if tag not in new_tags_list:
    new_tags_list.append(tag)
    
print len(new_tags_list)
print new_tags_list