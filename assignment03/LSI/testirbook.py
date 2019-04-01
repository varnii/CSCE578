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

from zinirbook import *

######################################################################
## do the computations from the input data
arrC = array(C)
printMat('matrix C', arrC)
#
arrxU = array(xU)
printMat('matrix xU', arrxU)
#
arrxS = array(xS)
printMat('matrix xS', arrxS)
#
arrxVT = array(xVT)
printMat('matrix xVT', arrxVT)
#
arrxUtrim = getColumns(0, 1, arrxU)
printMat("arrxUtrim", arrxUtrim)
arrxStrim = getColumns(0, 1, arrxS)
arrxStrim = getRows(0, 1, arrxStrim)
printMat("arrxStrim", arrxStrim)
arrxVTtrim = getRows(0, 1, arrxVT)
printMat("arrxVTtrim", arrxVTtrim)
#
xprod = dot(arrxUtrim, dot(arrxStrim, arrxVTtrim))
printMat("xprod", xprod)


######################################################################
## do the computations from internally computed svd
U,Svector,VT = svd(C)
printMat("U", U)
S = diag(Svector)
printMat("S", S)
printMat("VT", VT)
VTtrim = getRows(0, 4, VT)
printMat("VTtrim", VTtrim)

prod = dot(U, dot(S, VTtrim))
printMat("prod", prod)
#
#

Utrim = getColumns(0, 1, U)
printMat("Utrim", Utrim)
Strim = getColumns(0, 1, S)
Strim = getRows(0, 1, Strim)
printMat("Strim", Strim)
VTtrim = getRows(0, 1, VT)
printMat("VTtrim", VTtrim)

prodRed = dot(Utrim, dot(Strim, VTtrim))
printMat("prodRed", prodRed)
printMat("diff", C-prodRed)

Utrim2 = getColumns(0, 1, U)
printMat("Utrim2", Utrim2)
Strim2 = getColumns(0,1, S)
Strim2 = getRows(0,1, Strim2)
printMat("Strim2", Strim2)
VTtrim2 = getRows(0,1, VT)
printMat("VTtrim2", VTtrim2)

prodRed2 = dot(Utrim2, dot(Strim2, VTtrim2))
printMat("prodRed2", prodRed2)
printMat("diff", C-prodRed2)

sbyv = dot(Strim2, VTtrim2)
printMat("sbyv", sbyv)

