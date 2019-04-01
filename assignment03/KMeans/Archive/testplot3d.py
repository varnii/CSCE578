import sys
import random

import pylab
#from pylab import plot,show
#from numpy import vstack
from numpy import array
from math import sqrt
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

from utilspackage import *

######################################################################
## assign initial centroids
def assignInitialCentroids(howMany):
    centroids = []
    for num in range(1, 2*howMany, 2):
        centroids.append([(num+0.0)/(2.0*howMany),0.5,0.5])
    return centroids

######################################################################
## assign points to a cluster/centroid
## Parameters:
##     data : the list of points
##     centroids : the centroids
def assignPointsToCluster(data, centroids):
    clusterIndex = []
    for point in data:
        clusterIndex.append(getCentroidForPoint(point, centroids))
#    printList('INDEX', clusterIndex))
    return clusterIndex

######################################################################
## compute new centroids
## Parameters:
##     data : the list of points
##     centroids : the centroids
##     clusterIndex : the list of centroid subscripts for each point
## Returns:
##     the list of the new centroids
def computeNewCentroids(data, centroids, clusterIndex):
    newCentroids = []
    sumDistChange = 0.0
    for centroidSub in range(0, len(centroids)):
        print('COMPUTE CENTROID ', centroidSub)
        xAverage = 0.0
        yAverage = 0.0
        clusterCount = 0
        for pointSub in range(0, len(data)):
            if clusterIndex[pointSub] == centroidSub:
                xAverage += data[pointSub][0]
                yAverage += data[pointSub][1]
                clusterCount += 1
        xValue = xAverage/clusterCount
        yValue = yAverage/clusterCount
        print('COORDS ', xValue, yValue)
        newCentroids.append([xValue, yValue])
        sumDistChange += getDistance(centroids[centroidSub], newCentroids[centroidSub])

    return sumDistChange, newCentroids

######################################################################
## assign a point to a centroid
## Parameters:
##     point : the point
##     centroids : the centroids
def getCentroidForPoint(point, centroids):
    mindist = 9999999.99
    minsub = 9999999
#    print('\n')
    for sub in range(0, len(centroids)):
        cent = centroids[sub]
        dist = getDistance(point, cent)
#        print(sub, mindist, dist)
        if dist < mindist:
            mindist = dist
            minsub = sub

#    print('RETURN', minsub, mindist)
#    print('\n')
    return minsub

######################################################################
## compute a distance between two points
## Parameters:
##     p1 : point 1
##     p2 : point 2
## Returns:
##     the distance between the points
def getDistance(p1, p2):
    xdist =  p1[0] - p2[0]
    ydist =  p1[1] - p2[1]
    zdist =  p1[2] - p2[2]
    dist = sqrt(xdist*xdist + ydist*ydist + zdist*zdist)
    return dist

######################################################################
## plot data and centroids
## Parameters:
##     data : the list of points
##     centroids : the centroids
##     clusterIndex : the list of centroid subscripts for each point
def plotDataAndCentroids(data, centroids, clusterIndex):
    colors = ['xk', '+r', 'og', '^m', 'xb', '+y', 'oc', '^w']
    for sub in range(0, len(data)):
        point = data[sub]
        pylab.plot3d(point[0], point[1], point[2], colors[clusterIndex[sub]])

    for cent in centroids:
        plot3d(cent[0], cent[1], cent[2], 'sg')

######################################################################
## MAIN CODE STARTS HERE

data = []
for i in range(0,100):
    x = random.random()
    y = random.random()
    z = random.random()
    if 0 == i%2:
        x += 1.0
        y += 1.0
        z += 1.0
    data.append([x,y,z])

printList('DATA', data)

######################################################################
## INITIAL ASSIGNMENT OF CENTROIDS
centroids = assignInitialCentroids(2)
printList('\nONE CENTROIDS', centroids)

######################################################################
## ITERATION ONE: cluster, plot
clusterIndex = assignPointsToCluster(data, centroids)
print('INDEX', clusterIndex)

plotDataAndCentroids(data, centroids, clusterIndex)
print('FIRST IMAGE OF RANDOM CLUSTERS')
show()

sys.exit(1)

iteration = 0
distChange = 9999999.0
while distChange > 0.1:
    iteration += 1
    ######################################################################
    ## ITERATION: compute centroids, cluster, and plot
    distChange, centroids = computeNewCentroids(data, centroids, clusterIndex)
    print('\nITER: %d CENTROIDS' % (iteration))
    printList('CENTROIDS', centroids)
    print('DISTCHANGE ', distChange)
    
    clusterIndex = assignPointsToCluster(data, centroids)
    print('INDEX', clusterIndex)

    plotDataAndCentroids(data, centroids, clusterIndex)
    show()

######################################################################
## REPLOT BECAUSE THE PROGRAM HAS A GLITCH 
print('AFTER FINDING CENTROIDS')
plotDataAndCentroids(data, centroids, clusterIndex)
show()

inCluster = []
outOfCluster = []
for pointSub1 in range(0, len(data)-1):
    p1 = data[pointSub1]
    for pointSub2 in range(pointSub1+1, len(data)):
        p2 = data[pointSub2]
        dist = getDistance(p1, p2)
        if clusterIndex[pointSub1] == clusterIndex[pointSub2]:
            inCluster.append([clusterIndex[pointSub1], dist])
        else:
            outOfCluster.append([clusterIndex[pointSub1], dist])
       
colors = ['xk', '+r', 'og', '^m', 'xb', '+y', 'oc', '^w']
for point in inCluster:
    plot(random.random(), point[1], colors[0])
#    plot(point[0],point[1], colors[clusterIndex[sub]])

for point in outOfCluster:
    plot(random.random()+1.0, point[1], colors[1])
#    plot(point[0],point[1], colors[clusterIndex[sub]])

show()

sys.exit(1)
    
######################################################################
## DISCARDED CODE STORED HERE FOR REFERENCE

######################################################################
## OLD CODE STARTS HERE

# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(data,2)
# assign each sample to a cluster
idx,_ = vq(data,centroids)

# some plotting using numpy's logical indexing
plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()

# now with K = 3 (3 clusters)
centroids,_ = kmeans(data,3)
idx,_ = vq(data,centroids)

plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or',
     data[idx==2,0],data[idx==2,1],'og') # third cluster points
plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
show()
