from numpy import *
from numpy.linalg import svd

######################################################################
## GET COLUMNS SELECTED FROM A MATRIX
def getColumns(begin, end, m):
  colcount = m.shape[1]
  compresslist = []
  for i in range(0,colcount):
    if i < begin:
      compresslist.append(False)
    if i >= begin and i <= end:
      compresslist.append(True)
    if i > end:
      compresslist.append(False)
  return compress(compresslist, m, axis=1)

######################################################################
## GET ROWS SELECTED FROM A MATRIX
def getRows(begin, end, m):
  rowcount = m.shape[0]
  compresslist = []
  for i in range(0,rowcount):
    if i < begin:
      compresslist.append(False)
    if i >= begin and i <= end:
      compresslist.append(True)
    if i > end:
      compresslist.append(False)
  return compress(compresslist, m, axis=0)

######################################################################
## FORMATTED PRINT OF A MATRIX 
def printMat(label, m):
  print label + ' ' + str(m.shape)
  for row in m:
    s = ''
    rowlength = size(row)
    for i in range(0,rowlength):
      col = row[i]
      s += '%10.6f' % (col)
    print s
  print

######################################################################
## FORMATTED PRINT OF A VECTOR 
def printVector(label, v):
  print label + ' (' + str(size(v)) + ')'
  s = ''
  vlength = size(v)
  for i in range(0,vlength):
    col = v[i]
    s += '%10.6f' % (col)
  print s
  print

#from zinirbook import *

A = [[2, 0, 8, 6, 0],
     [1, 6, 0, 1, 7],
     [5, 0, 7, 4, 0],
     [7, 0, 8, 5, 0],
     [0,10, 0, 0, 7]]
arrA = array(A)
printMat('matrix A', arrA)

U,Svector,VT = svd(A)
printMat("U", U)
S = diag(Svector)
printMat("S", S)
printMat("VT", VT)

prod = dot(U, dot(S, VT))
printMat("prod", prod)

Utrim = getColumns(0,3, U)
printMat("Utrim", Utrim)
Strim = getColumns(0,3, S)
Strim = getRows(0,3, Strim)
printMat("Strim", Strim)
VTtrim = getRows(0,3, VT)
printMat("VTtrim", VTtrim)

prodRed = dot(Utrim, dot(Strim, VTtrim))
printMat("prodRed", prodRed)
printMat("diff", A-prodRed)

Utrim2 = getColumns(0, 2, U)
printMat("Utrim2", Utrim2)
Strim2 = getColumns(0,2, S)
Strim2 = getRows(0,2, Strim2)
printMat("Strim2", Strim2)
VTtrim2 = getRows(0,2, VT)
printMat("VTtrim2", VTtrim2)

prodRed2 = dot(Utrim2, dot(Strim2, VTtrim2))
printMat("prodRed2", prodRed2)
printMat("diff", A-prodRed2)


U = [[-0.54,  0.07,  0.82],
     [-0.10, -0.59, -0.11],
     [-0.53,  0.06, -0.21],
     [-0.65,  0.07, -0.51],
     [-0.06, -0.80,  0.09]]
arrU = array(U)
printMat("Uorig", arrU)

S = [[17.92,  0.00,  0.00],
     [ 0.00, 15.17,  0.00],
     [ 0.00,  0.00,  3.56]]
arrS = array(S)
printMat("Sorig", arrS)

V = [[-0.46,  0.02, -0.87, -0.00,  0.17],
     [-0.07, -0.76,  0.06,  0.60,  0.23],
     [-0.74,  0.10,  0.28,  0.22, -0.56]]
arrV = array(V)
printMat("Vorig", arrV)

prodOrig = dot(arrU, dot(arrS, arrV))
printMat("prodOrig", prodOrig)
printMat("diff", A-prodOrig)

#matrix A
#5 5
#2  0 8 6 0],
#1  6 0 1 7],
#5  0 7 4 0],
#7  0 8 5 0],
#0 10 0 0 7]]
#matrix U
#5 5
#-0.54  0.07  0.82 -0.11  0.12],
#-0.10 -0.59 -0.11 -0.79 -0.06],
#-0.53  0.06 -0.21  0.12 -0.81],
#-0.65  0.07 -0.51  0.06  0.56],
#-0.06 -0.80  0.09  0.59  0.04]]
#matrix Sigma
#5 5
#17.92  0.00  0.00  0.00  0.00],
# 0.00 15.17  0.00  0.00  0.00],
# 0.00  0.00  3.56  0.00  0.00],
# 0.00  0.00  0.00  1.98  0.00],
# 0.00  0.00  0.00  0.00  0.35]]
#matrix Vtranspose
#5 5
#-0.46  0.02 -0.87 -0.00  0.17],
#-0.07 -0.76  0.06  0.60  0.23],
#-0.74  0.10  0.28  0.22 -0.56],
#-0.48  0.03  0.40 -0.33  0.70],
#-0.07 -0.64 -0.04 -0.69 -0.32]]
#

#arrC = array(C)
#printMat('matrix C', arrC)
#
#arrU = array(U)
#printMat('matrix U', arrU)
#
#arrS = array(S)
#printMat('matrix S', arrS)
#
#arrVT = array(VT)
#printMat('matrix VT', arrVT)
#
#prod1 = dot(arrU, arrS)
#
#prod2 = dot(prod1, arrVT)
#printMat("product 2", prod2)
#
#UU, SS, VV = svd(C)
#
#printMat('matrix UU', UU)
#
#printVector('matrix SS', SS)
#SSmatrix = diag(SS)
#printMat('matrix SS', SSmatrix)
#
#printMat('matrix VV', VV)
#
#VVsubset = getRows(0, UU.shape[0]-1, VV)
#printMat('matrix VVsubset', VVsubset)
#
#prod1 = dot(UU, SSmatrix)
#prod2 = dot(prod1, VVsubset)
#printMat('matrix prod2', prod2)
