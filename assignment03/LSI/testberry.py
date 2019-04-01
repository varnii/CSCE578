""" This is the docstring.
"""
#import sys

#from numpy import *
from numpy import array
from numpy import compress
from numpy import diag
from numpy import dot
from numpy import size
from numpy import sqrt
from numpy import matmul
from numpy.linalg import svd

from zinberry import *

######################################################################
## COMPUTE THE NORM OF A COLUMN
def columnnorm(subscript, thematrix):
    """ This is the docstring.
    """
    col = getcolumns(subscript, subscript, thematrix)
#    print(col)
    coltrans = col.transpose()
#    print(coltrans)
    coltransdot = dot(coltrans, col)
#    print(coltransdot)
    thenorm = coltransdot[0][0]
    thenorm = sqrt(thenorm)
#    print(norm)
    return thenorm

######################################################################
## COMPUTE COSINE COEFFICIENT OF TWO VECTORS
def cosinecoeff(vector1, vector2):
    """ This is the docstring.
    """
    v1norm = vectornorm(vector1)
    v2norm = vectornorm(vector2)
    cosine = dot(vector1, vector2.transpose()) # must transpose for dot function
    cosine = cosine/(v1norm * v2norm)
    return cosine[0][0]

######################################################################
## GET COLUMNS SELECTED FROM A MATRIX
def createidentity(matrixsize):
    """ This is the docstring.
    """
    thediagonal = []
    for sub in range(0, matrixsize):
        thediagonal.append(1.0)
    ident = diag(thediagonal)
#    print(ident)
    return array(ident)

######################################################################
## GET COLUMNS SELECTED FROM A MATRIX
def getcolumns(begin, end, thematrix):
    """ This is the docstring.
    """
    colcount = thematrix.shape[1]
    compresslist = []
    for sub in range(0, colcount):
        if sub < begin:
            compresslist.append(False)
        if (sub >= begin) and (sub <= end):
            compresslist.append(True)
        if sub > end:
            compresslist.append(False)
    return compress(compresslist, thematrix, axis=1)

######################################################################
## GET ROWS SELECTED FROM A MATRIX
def getrows(begin, end, thematrix):
    """ This is the docstring.
    """
    rowcount = thematrix.shape[0]
    compresslist = []
    for sub in range(0, rowcount):
        if sub < begin:
            compresslist.append(False)
        if (sub >= begin) and (sub <= end):
            compresslist.append(True)
        if sub > end:
            compresslist.append(False)
    return compress(compresslist, thematrix, axis=0)

######################################################################
## NORMALIZE A MATRIX TO HAVE UNIT NORM COLUMNS
def normalize(thematrix):
    """ This is the docstring.
    """
    msum = thematrix.sum(axis=0, dtype='float')
#    printvector("sum", msum)
    rootsum = sqrt(msum)  # numpy sqrt that will work on a vector
    rootsumdivided = rootsum/msum
#    print(rootsumdivided)

    normalizedlist = []
    for i in range(0, thematrix.shape[0]):
        row = getrows(i, i, thematrix)
        newrow = row * rootsumdivided
#      print(str(i) + ": " + str(newrow))
#      printvector(str(i)+": ", newrow[0])
        normalizedlist.append(newrow[0])
    normalizedmatrix = array(normalizedlist)
#    printmat("normalizedm", normalizedm.round(decimals=4))
    return normalizedmatrix

######################################################################
## FORMATTED PRINT OF A MATRIX
def printmat(label, thematrix):
    """ This is the docstring.
    """
    print(label + ' ' + str(thematrix.shape))
    for row in thematrix:
        sss = ''
        rowlength = size(row)
        for i in range(0, rowlength):
            col = row[i]
            sss += '%10.6f' % (col)
        print(sss)
    print()

######################################################################
## FORMATTED PRINT OF A VECTOR
def printvector(label, thevector):
    """ This is the docstring.
    """
    print(label + ' (' + str(size(thevector)) + ')')
    sss = ''
    vlength = size(thevector)
    for i in range(0, vlength):
        col = thevector[i]
        sss += '%10.6f' % (col)
    print(sss)
    print()

######################################################################
## COMPUTE THE NORM OF A VECTOR
def vectornorm(thevector):
    """ This is the docstring.
    """
#    print(col)
    vtrans = thevector.transpose()
#    print(coltrans)
    vvtransdot = dot(thevector, vtrans)
#    print(coltransdot)
    thenorm = vvtransdot[0][0]
    thenorm = sqrt(thenorm)
#    print(thenorm)
    return thenorm

######################################################################
## do the computations from the input data
def main():
    """ This is the docstring.
    """

    ## first we read the input data and convert to arrays for numpy
    input_matrix_a = array(input_a)
    printmat('input_matrix_a', input_matrix_a)

    ## we will want to normalize the A matrix
    normalized_a = normalize(input_matrix_a)
    printmat("normalized_a", normalized_a)

    input_matrix_u = array(input_u)
    printmat('input_matrix_u', input_matrix_u)

    input_matrix_sigma = array(input_sigma)
    printmat('input_matrix_sigma', input_matrix_sigma)

    input_matrix_vt = array(input_vt)
    printmat('input_matrix_vt', input_matrix_vt)

    result1 = matmul(input_matrix_u, input_matrix_sigma)
    result2 = matmul(result1, input_matrix_vt)
    result2 = result2.round(decimals=4)
    printmat('rounded result', result2)

    matrixdifference = normalized_a - result2
    matrixdifference = matrixdifference.round(decimals=4)
    printmat('difference ', matrixdifference)

    ## now trim to rank 7 as per page 53-54 of berry
    matrix_u7 = getcolumns(0, 6, input_matrix_u)
    printmat('matrix_u7', matrix_u7)

    matrix_sigma7 = getrows(0, 6, input_matrix_sigma)
    printmat('matrix_sigma7', matrix_sigma7)

    matrix_vt7 = input_matrix_vt
    printmat('matrix_vt7', matrix_vt7)

    a7_product = dot(matrix_u7, dot(matrix_sigma7, matrix_vt7))
    printmat("a7_product", a7_product)

    a7_productround = a7_product.round(decimals=4)
    printmat("a7_productround", a7_productround)

    ## now trim to rank 4 as per page 56 of berry
    matrix_u4 = getcolumns(0, 3, input_matrix_u)
    printmat('matrix_u4', matrix_u4)

    matrix_sigma4 = getrows(0, 3, input_matrix_sigma)
    matrix_sigma4 = getcolumns(0, 3, matrix_sigma4)
    printmat('matrix_sigma4', matrix_sigma4)

    matrix_vt4 = getrows(0, 3, input_matrix_vt)
    printmat('matrix_vt4', matrix_vt4)

    a4_product = dot(matrix_u4, dot(matrix_sigma4, matrix_vt4))
    printmat("a4_product", a4_product)

    a4_productround = a4_product.round(decimals=4)
    printmat("a4_productround", a4_productround)

    ######################################################################
    ## do the computations from internally computed svd

    ## now do the computations from internally computed svd on the normalized
    svdmatrix_u, svdvector_sigma, svdmatrix_vt = svd(normalized_a)
    printmat("svdmatrix_u", svdmatrix_u)
    svdmatrix_sigma = diag(svdvector_sigma)
    printmat("svdmatrix_sigma", svdmatrix_sigma)
    printmat("svdmatrix_vt", svdmatrix_vt)

    ## trim to rank 7 just because that's the actual rank of the matrix
    svdmatrix_u7 = getcolumns(0, 6, svdmatrix_u)
    printmat("svdmatrix_u7", svdmatrix_u7)

    svdmatrix_sigma7 = svdmatrix_sigma
    printmat("svdmatrix_sigma7", svdmatrix_sigma7)

    svdmatrix_vt7 = getrows(0, 6, svdmatrix_vt)
    printmat("svdmatrix_vt7", svdmatrix_vt7)

    svdproduct7 = dot(svdmatrix_u7, dot(svdmatrix_sigma7, svdmatrix_vt7))
    printmat("svdproduct7", svdproduct7)

#    # now we're going to invert to get the old terms in terms of the new terms
#    for rowsub in range(0, svdproduct7.shape[0]):
#        for colsub in range(0, svdproduct7.shape[1]):
#            if fabs(svdproduct7[rowsub][colsub]) > 0.001:
#                print(rowsub, colsub, svdproduct7[rowsub][colsub])
#
#
#    sys.exit(1)

    ## now do the rank 4 approximation
    matrix_u4 = getcolumns(0, 3, input_matrix_u)
    printmat("U4", matrix_u4)

    matrix_sigma4 = getcolumns(0, 3, input_matrix_sigma)
    matrix_sigma4 = getrows(0, 3, matrix_sigma4)
    printmat("matrix_sigma4", matrix_sigma4)

    matrix_vt4 = getrows(0, 3, input_matrix_vt)
    printmat("matrix_vt4", matrix_vt4)

    product4 = dot(matrix_u4, dot(matrix_sigma4, matrix_vt4))
    printmat("product4", product4)
    printmat("product4", product4.round(decimals=4))

    #i4 = createidentity(4)
    #printmat('four', i4)
    #
    #i9 = createidentity(9)
    #printmat('nine', i9)
    #
    #i2 = createidentity(2)
    #printmat('two', i2)
    #
    #i1 = createidentity(1)
    #printmat('one', i1)

    for i in range(0, normalized_a.shape[1]):
        print(columnnorm(i, normalized_a))

    for i in range(0, product4.shape[1]):
        print(columnnorm(i, product4))

    thematrix = product4
    for querysub in range(0, thematrix.shape[1]):
        query = getcolumns(querysub, querysub, thematrix).transpose()
#        querynorm = vectornorm(query)
        for docsub in range(0, thematrix.shape[1]):
            doc = getcolumns(docsub, docsub, thematrix).transpose()
#            docnorm = vectornorm(doc)
            cosine = cosinecoeff(query, doc)
            print('product4 %4d %4d %10.6f' % (querysub, docsub, cosine))
        print()

    thematrix = svdproduct7
    for querysub in range(0, thematrix.shape[1]):
        query = getcolumns(querysub, querysub, thematrix).transpose()
#        querynorm = vectornorm(query)
        for docsub in range(0, thematrix.shape[1]):
            doc = getcolumns(docsub, docsub, thematrix).transpose()
#            docnorm = vectornorm(doc)
            cosine = cosinecoeff(query, doc)
            print('product7 %4d %4d %10.6f' % (querysub, docsub, cosine))
        print()

    thematrix = product4
    size_of_a = thematrix.shape[0]
    identity = createidentity(size_of_a)
    for querysub in range(0, thematrix.shape[0]):
        query = getcolumns(querysub, querysub, identity).transpose()
        print(query)

######################################################################
## MAIN Main main
main()
