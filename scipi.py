#!/usr/bin/python
# -*- coding: utf-8 -*-

import scipy
import pylab
import matplotlib
import scipy.cluster.hierarchy as sch

# Generate features and distance matrix.
SAMPLE_SIZE = 40
x = scipy.rand(SAMPLE_SIZE)
D = scipy.zeros([SAMPLE_SIZE,SAMPLE_SIZE])
for i in range(SAMPLE_SIZE):
    for j in range(SAMPLE_SIZE):
        D[i,j] = abs(x[i] - x[j])

# Compute and plot dendrogram.
fig = pylab.figure()
axdendro = fig.add_axes([0.09,0.1,0.2,0.8])
Y = sch.linkage(D, method='single')

Z = sch.dendrogram(Y, orientation='right')

axdendro.set_xticks([])
axdendro.set_yticks([])

# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.8])
index = Z['leaves']
D = D[index,:]
D = D[:,index]
im = axmatrix.matshow(D, aspect='auto', origin='lower')
axmatrix.set_xticks([])
axmatrix.set_yticks([])

# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.8])
pylab.colorbar(im, cax=axcolor)
fig.savefig('dendrogram.png')