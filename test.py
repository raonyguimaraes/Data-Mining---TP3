#!/usr/bin/python
# -*- coding: utf-8 -*-

#from nltk.metrics.distance import jaccard_distance, masi_distance
#from prettytable import PrettyTable
#fields = ['X', 'Y', 'Jaccard(X,Y)', 'MASI(X,Y)']
#pt = PrettyTable(fields=fields)
#[pt.set_field_align(f, 'l') for f in fields]
#for z in range(4):
  #X = set()
  #for x in range(z, 4):
    #Y = set()
    #for y in range(1, 3):
      #X.add(x)
      #Y.add(y)
      #pt.add_row([list(X), list(Y), round(jaccard_distance(X, Y), 2),round(masi_distance(X, Y), 2)])
#pt.printt()


#A = [1,2,3]
#B = [2,3,4]

#X = set(A)
#Y = set(B)

#distance = round(jaccard_distance(X, Y), 2)
#print distance

ints = ["A", "2", "HJHAS"]
for idx, val in enumerate(ints):
    print idx, val