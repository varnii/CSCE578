#Duncan Harmon
#SVDonDocs.py
#
#Purpose of this program is to do a tf.idf on documents and then to do an
#SVD on the matrix of documents
#
#afterwards i will run a clustering algorithm (probably kmeans) to cluster the data
#
#29/03/2019

import sys
import os
from collections import defaultdict
from glob import glob
from math import log
from math import sqrt
from numpy import zeros
from numpy import array
from numpy import compress
from numpy import diag
from numpy import dot
from numpy import size
from numpy import sqrt
from numpy import matmul
from numpy.linalg import svd
from numpy.linalg import norm
from matplotlib import pyplot
from sklearn.manifold import MDS

#from nltk.tokenize import word_tokenize, wordpunct_tokenize

#from input import *


def getcolumns(begin, end, m):
    colcount = m.shape[1]
    compresslist = []
    for sub in range(0, colcount):
        if sub < begin:
            compresslist.append(False)
        if (sub >= begin) and (sub <= end):
            compresslist.append(True)
        if sub > end:
            compresslist.append(False)
    return compress(compresslist, m, axis=1)

def getrows(begin, end, m):
    rowcount = m.shape[0]
    compresslist = []
    for sub in range(0, rowcount):
        if sub < begin:
            compresslist.append(False)
        if (sub >= begin) and (sub <= end):
            compresslist.append(True)
        if sub > end:
            compresslist.append(False)
    return compress(compresslist, m, axis=0)

def normalize(m):
    msum = m.sum(axis=0, dtype='float')
    rootsum = sqrt(msum)
    scalar = rootsum/msum

    normalizedlist = []
    for i in range(0,  m.shape[0]):
        row = getrows(i,i, m)
        newrow = row * scalar
        normalizedlist.append(newrow[0])
    normalized_m = array(normalizedlist)
    return normalized_m

#prints in a format ready to be imported by python
def printmat(label,  m):
    print('\n\n\n####################################################################\n### ' + label + '.shape: ' + str( m.shape))
    rowcount = len( m)
    sss = label + ' = [['
    for i in range(0,rowcount):
        row =  m[i]
        rowlen = len(row)
        if i > 0:
            sss+='\t ['
        for j in range(0,rowlen):
            sss+='%.6f' % (row[j])
            if j==rowlen-1:
                sss+=']'
            else:
                sss+=','

        if i==rowcount-1:
            sss+=']'
        else:
            sss+=','
        print(sss)
        sss = ''


def dimRed(rank,u,s,vt):
    u = getcolumns(0,rank,u)
    s = getcolumns(0,rank,s)
    s = getrows(0,rank,s)
    vt = getrows(0,rank,vt)
    return u,s,vt

#DBSCAN
#http://en.wikipedia.org/wiki/DBSCAN
def DBSCAN(DB, eps, minPts):
    '''
    Returns a list of labels for each point corresponding to the cluster number
    noise is labeled as -1
    cluster labels start at 1
    '''

    clusterC = 0
    label = [0]*len(DB)
    for p in range(0,len(DB)):
        if label[p] != 0:
            continue
        N = rangeQuery(DB, p, eps)
        if len(N) < minPts:
            label[p] = -1
            continue
        clusterC += 1
        label[p] = clusterC
        i = 0
        while i < len(N):
            q = N[i]

            if label[q]==-1:
                label[q]=clusterC
            elif label[q]==0:
                label[q]=clusterC
                #if q has enough neighbors, use it to expand the cluster
                qN = rangeQuery(DB, q, eps)

                if len(qN) >= minPts:
                    N += qN
            i+=1

    return label

def rangeQuery(DB, p, eps):
    N = []
    for q in range(0,len(DB)):
        if norm(DB[p]-DB[q]) < eps:
            N.append(q)
    return N


def main(doRead,pna,doSVD,psvd,doCalc,inrank,inepsilon,inminpts):
    dirpath = "./2014_4_101_000.stanford/"
    filename = "2014_4_101_000_0xxfinaly.txt.conll"
#    print(inrank)
    stopwordSet = set()
    file = open("./stopwords.txt")
    for line in file:
        stopwordSet.add(line[:-1])
    file.close()
    ##initialize dict of all terms
    
    if doCalc:

        wordToIndex = {}
        docToIndex  = {}
        indexToDoc  = {}
        docToDict   = {}
        wordoffset  = 0
        docoffset   = 0

        if doRead:
#            print('#READING DATA#')
            for filename in glob(os.path.join(dirpath,'*.txt.conll')):
                file = open(filename)
                filename = filename.replace('./2014_4_101_000.stanford/2014_4_101_000_','')
                filename = filename.replace('.txt.conll','')
                filename = filename.replace('final','_f_')
                filename = filename.replace('draft','_d_')
                docToIndex[filename] = docoffset
                indexToDoc[docoffset] = filename
                docoffset+=1
                WordToFreq = {}
                #add all nonstop words to wordToIndex, WordToFreq
                #the freqs will be put in a a vector doc[index] = freq which will be put in a vector matrix_a[doc]
                for line in file:
                    line = line.split()
                    if len(line) != 0:
                        word = line[2]
                        if word not in stopwordSet:
                            if word not in wordToIndex.keys():
                                #create a dict of word to index so we know which dimension to increase when we go through
                                wordToIndex[word] = wordoffset
                                wordoffset+=1
                                WordToFreq[word] = 1
                            else:
                                if word not in WordToFreq.keys():
                                    WordToFreq[word] = 1
                                else:
                                    WordToFreq[word] += 1
                docToDict[filename] = WordToFreq
                file.close()
            matrix_a = zeros((docoffset,wordoffset))

            for doc in docToDict:
                doci = docToIndex[doc]
                for word in docToDict[doc]:
                    wordi = wordToIndex[word]
                    matrix_a[doci][wordi] = docToDict[doc][word]
            normalized_matrix_a = normalize(matrix_a)
        else:
#            print('#NOT READING DATA\n#COPYING FROM \'input.py\'#')
            normalized_matrix_a = input_normalized_a


    #    print("row#:\t"+str(len(docToIndex))+"\t: "+str(docoffset))
    #    print("col#:\t"+str(len(wordToIndex))+"\t: "+str(wordoffset))
        
        

    #    if pia:
    #        printmat('matrix_a',matrix_a)

#        if pna:
#            printmat('normalized_a',normalized_matrix_a)

#        print('###make zero matrices')
        matrix_u = zeros((1,1))
        matrix_s = zeros((1,1))
        matrix_vt = zeros((1,1))

        if doSVD:
            #print('#doSVD = 1')
            matrix_u,vector_s,matrix_vt = svd(normalized_matrix_a)
            matrix_s = diag(vector_s)
#            if psvd:
#                printmat('matrix_u',matrix_u)
#                printmat('matrix_s',matrix_s)
#                printmat('matrix_vt',matrix_vt)
        else:
            #print('#doSVD = 0')
            matrix_u  = input_matrix_u
            matrix_s  = input_matrix_s
            matrix_vt = input_matrix_vt
########################################################################################
        rank = inrank
########################################################################################
        print('#rank: ' + str(rank))

        matrix_u  = getcolumns(0,rank,matrix_u)
        matrix_s  = getcolumns(0,rank,matrix_s)
        matrix_s  = getrows(0,rank,matrix_s)
        matrix_vt = getrows(0,rank,matrix_vt)

        #printmat('redmatrix_u',matrix_u)
        #printmat('redmatrix_s',matrix_s)
        #printmat('redmatrix_vt',matrix_vt)

        matrix_product = dot(matrix_u, dot(matrix_s,matrix_vt))

        #printmat('product',matrix_product)

    #    testmat = zeros((10,10))
    #    printmat('test',testmat)


        ###NEED TO MDS###
        scale = MDS(n_components=2,n_init=200,max_iter=3000)



        print("\n\n################################")
#        print("## xd -> 2d\n")
        print("#pre-transform shape:  " + str(matrix_product.shape) + "\n")


        matrix_product_2d = scale.fit_transform(matrix_product)
        
        print("#post-transform shape: " + str(matrix_product_2d.shape) + "\n")

        #printmat('projected_product',matrix_product_2d)
    else:
        matrix_product_2d = array(input_2d)

    ##calculate xmaxmin and ymaxmin

   
    colorspec = {}
    colorspec[-1]   ='k'
    colorspec[-2]   ='r'
    colorspec[0]    ='b'
    colorspec[1]    ='g'
    colorspec[2]    ='r'
    colorspec[3]    ='c'
    colorspec[4]    ='m'
    colorspec[5]    ='y'

    shapespec = {}
    shapespec[-1]   ='o'
    shapespec[-2]   ='x'
    shapespec[0]    ='o'
    shapespec[1]    ='v'
    shapespec[2]    ='s'
    shapespec[3]    ='p'
    shapespec[4]    ='*'
    shapespec[5]    ='+'
    shapespec[6]    ='d'

    fig1 = pyplot.figure("full_dimension_clustering",figsize=[12.8,9.6],dpi=100)

    clusters = DBSCAN(matrix_product,inepsilon,inminpts)

    CMAX = 0

    for i in range(0,len(matrix_product_2d)):
        C = clusters[i]
        CMAX = max(C,CMAX)
        X = matrix_product_2d[i,0]
        Y = matrix_product_2d[i,1]
        if C == -1:
            CS = str(colorspec[-1]+shapespec[-1])
            pyplot.plot(X,Y,CS)
        elif C == 0:
            CS = str(colorspec[-2]+shapespec[-2])
            pyplot.plot(X,Y,CS)
        else:
            CS = str(colorspec[C%6]+shapespec[int(C/6)])
            pyplot.plot(X,Y,CS)


    print("\n\n#number of clusters: " + str(CMAX))
    print("#epsilon:\t"+str(inepsilon))
    print("#minPts:\t"+str(inminpts))
    print("")
    pyplot.show()

    print("#docs in each cluster for comparison: ")
    for i in range(-1,CMAX+1):
        if i == -1:
            print("\t#NOISE:")
        elif i == 0:
            print("\t#ERROR:")
        else:
            print("\t#CLUSTER_"+str(i))
        for j in range(0,len(clusters)):
            if clusters[j] == i:
                print("\t#  \'" + indexToDoc[j]+"\'")




if __name__ == '__main__':
    main(1,1,1,0,1,int(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]))