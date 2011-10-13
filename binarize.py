#!/usr/bin/python
# -*- coding: utf-8 -*-


import unicodedata
import re
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

#fdist = nltk.FreqDist()
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
    #fdist.inc(tag)


print 'finished reading file'
print str(len(all_tags))+" tags"
print str(len(musics))+" musics"



#Remove duplicated for tags
unic_tags = []
for tag in all_tags:
  if tag not in unic_tags:
    unic_tags.append(tag)
    
unic_musics = []    
for music in musics:
    if music not in unic_musics:
      unic_musics.append(music)

print str(len(unic_tags))+" unique tags"
print str(len(unic_musics))+" unique musics"

print ",".join(unic_tags)


for music in unic_musics:
  music_string = []
  for tag in unic_tags:
    if tag in music:
      music_string.append("1")
    else:
      music_string.append("0")
  #print "Music has "+str(len(music_string))+" tags"
  string = ",".join(music_string) 
  print string #"%s,%s" % (count, string)   
    
  