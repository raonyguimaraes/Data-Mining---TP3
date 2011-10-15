#!/usr/bin/python
# -*- coding: utf-8 -*-


import unicodedata
import re
import nltk


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




#print str(len(unique_tags))+" unique tags"
#print str(len(unique_musics))+" unique musics"

print ",".join(unique_tags)

for music in unique_musics:
  music_string = []
  music_tags = music.split(",")
  for tag in unique_tags:
    if tag in music_tags:
      music_string.append("1")
    else:
      music_string.append("0")
  #print "Music has "+str(len(music_string))+" tags"
  string = ",".join(music_string) 
  print string #"%s,%s" % (count, string)