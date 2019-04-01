import sys
import random

from pylab import plot,show
from numpy import vstack,array
from math import sqrt
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

from utilspackage import *

######################################################################
## assign initial centroids
def assigninitialcentroids(howmany):
    centroids = []
    for num in range(1, 2*howmany, 2):
        centroids.append([(num+0.0)/(2.0*howmany),0.5])
    return centroids

######################################################################
## assign points to a cluster/centroid
## Parameters:
##     data : the list of points
##     centroids : the centroids
def assignpointstocluster(data, centroids):
    clusterindex = []
    for point in data:
        clusterindex.append(getcentroidforpoint(point, centroids))
#    printlist('INDEX', clusterindex)
    return clusterindex

######################################################################
## compute new centroids
## Parameters:
##     data : the list of points
##     centroids : the centroids
##     clusterindex : the list of centroid subscripts for each point
## Returns:
##     the sum of the distances from the old to the new centroids
##     the list of the new centroids
def computenewcentroids(data, centroids, clusterindex):
    newcentroids = []
    sumdistchange = 0.0
    for centroidsub in range(0, len(centroids)):
        print('COMPUTE CENTROID ', centroidsub)
        xaverage = 0.0
        yaverage = 0.0
        clustercount = 0
        for pointsub in range(0, len(data)):
            if clusterindex[pointsub] == centroidsub:
                xaverage += data[pointsub][XCOORD]
                yaverage += data[pointsub][YCOORD]
                clustercount += 1
        xvalue = xaverage/clustercount
        yvalue = yaverage/clustercount
        print('COORDS ', xvalue, yvalue)
        newcentroids.append([xvalue, yvalue])
        sumdistchange += getdistance(centroids[centroidsub], \
                                     newcentroids[centroidsub])

    return sumdistchange, newcentroids

######################################################################
## compute a distance between two points
## Parameters:
##     p1 : point 1
##     p2 : point 2
## Returns:
##     the distance between the points
def getdistance(p1, p2):
    xdist =  p1[XCOORD] - p2[XCOORD]
    ydist =  p1[YCOORD] - p2[YCOORD]
    dist = sqrt(xdist*xdist + ydist*ydist)
    return dist

######################################################################
## assign a point to a centroid
## Parameters:
##     point : the point
##     centroids : the centroids
def getcentroidforpoint(point, centroids):
    mindist = 9999999.99
    minsub = 9999999
#    print '\n'
    for sub in range(0, len(centroids)):
        cent = centroids[sub]
        dist = getdistance(point, cent)
#        print sub, mindist, dist
        if dist < mindist:
            mindist = dist
            minsub = sub

#    print 'RETURN', minsub, mindist
#    print '\n'
    return minsub

######################################################################
## plot data and centroids
## Parameters:
##     data : the list of points
##     centroids : the centroids
##     clusterindex : the list of centroid subscripts for each point
def plotdataandcentroids(data, centroids, clusterindex):
    colors = ['xk', '+r', 'og', '^m', 'xb', '+y', 'oc', '^w']
    for sub in range(0, len(data)):
        point = data[sub]
        plot(point[XCOORD],point[YCOORD], colors[clusterindex[sub]])

    for cent in centroids:
        plot(cent[XCOORD], cent[YCOORD], 'sg')

######################################################################
## Print a list.
## We print essentially unformatted, but we allow for formatting.
##
## Parameters:
##     label : the label to print at the head of the output
##     thelist : the list to print
##
def printlist(label, thelist):
    print('%s' % (str(label)))
    for item in thelist:
        print('%s' % (str(item)))
    return

######################################################################
## MAIN CODE STARTS HERE
def main():

    ##################################################################
    ## CREATE SOME RANDOM DATA
    data = []
    for i in range(0,100):
        x = random.random()
        y = random.random()
        if 0 == i%2:
            x += 1.0
            y += 1.0
        data.append([x,y])
    printlist('DATA', data)

    ##################################################################
    ## INITIAL ASSIGNMENT OF CENTROIDS
    centroids = assigninitialcentroids(2)
    printlist('\nINITIAL CENTROIDS', centroids)

    ##################################################################
    ## ITERATION ONE: cluster, plot
    clusterindex = assignpointstocluster(data, centroids)
    print('FIRST INDEX', clusterindex)

    plotdataandcentroids(data, centroids, clusterindex)
    print('FIRST IMAGE OF RANDOM CLUSTERS')
    show()

    iteration = 0
    distchange = 9999999.0
    while distchange > 0.1:
        iteration += 1
        ##############################################################
        ## ITERATION: compute centroids, cluster, and plot
        distchange, centroids = computenewcentroids(data, centroids, \
                                                    clusterindex)
        print('\nITER: %d CENTROIDS' % (iteration))
        printlist('CENTROIDS', centroids)
        print('DISTCHANGE ', distchange)
    
        clusterindex = assignpointstocluster(data, centroids)
        print('INDEX', clusterindex)

        plotdataandcentroids(data, centroids, clusterindex)
        show()

######################################################################
## MAIN Main main
XCOORD = 0
YCOORD = 1
main()

