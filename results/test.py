#!/usr/bin/python
# -*- coding: utf-8 -*-

#Now, let's generate vectors x and y in R, do a scatter plot, fit a least-squares line, etc.:

#from rpy2.robjects import r
#from rpy2 import robjects
#from rpy2.robjects import Formula
#from rpy2.robjects.vectors import IntVector, FloatVector
#from rpy2.robjects.lib import grid
#from rpy2.robjects.packages import importr

#r('x <- rnorm(100)')  # generate x at R
#r('y <- x + rnorm(100,sd=0.5)')  # generate y at R
#r('plot(x,y)')  # have R plot them
#r('lmout <- lm(y~x)')  # run the regression
#r('print(lmout)')  # print from R
#loclmout = r('lmout') # download lmout from R to Python
#print loclmout  # print locally
#print loclmout.r['coefficients']  # print one component
#Now let's apply some R operations to some Python variables:

#u = range(10)  # set up another scatter plot, this one local
#e = 5*[0.25,-0.25]
#v = u[:]
#for i in range(10): v[i] += e[i]
#r.plot(u,v)
#r.assign('remoteu',u)  # ship local u to R
#r.assign('remotev',v)  # ship local v to R
#r('plot(remoteu,remotev)')  # plot there

