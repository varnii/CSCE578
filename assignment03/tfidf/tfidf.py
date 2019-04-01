"""
Program to compute tf-idf for words in a set of documents.
This first reads a stoplist into a 'set' and then prints
the frequencies of the stopwords and the real words
separately.
"""
import sys
#from os import listdir
from collections import defaultdict
from glob import glob
from math import log
from math import sqrt

sys.path.append('/Users/buell/Current/PythonUtilities/') # office directory

#pylint: disable=import-error
#pylint: disable=wrong-import-position
from DABUtilities.dabfunctions.checkargs import checkargs
#from DABUtilities.dabfunctions.getfileasset import getfileasset
from DABUtilities.dabfunctions.printoutput import printoutput
from DABUtilities.dabfunctions.dabtimer import DABTimer

#from FYEUtilities.fyexmlize.xmlize import xmlize
#from FYEUtilities.fyeutilities.getfilenames import getfilenames
#from FYEUtilities.fyeutilities.openoutputfile import openoutputfile
#pylint: enable=import-error
#pylint: enable=wrong-import-position


############################################################################
#123456789012345678901234567890123456789012345678901234567890123456789012345
class Globals():
    """ This is the docstring.
    """
    def __init__(self):
        self.filenames = []
        self.punctlist = []

        self.overallwordandposset = set()
        self.stoplist = set()

        self.docs = defaultdict(OneDoc)
        self.docset = defaultdict(set)

        self.sparsematrixbyterm = defaultdict(list)
        self.sparsematrixbydoc = defaultdict(list)

        ########################################################################
        ## Get the stoplist and create a list of punctuation/other symbols.
        thefile = open('../../SourceText/wstoplistNLTK.txt')
        thetext = thefile.read().split()
        for stopword in thetext:
            self.stoplist.add(stopword)
        thefile.close()

        self.punctlist = ['.', '!', '?', ',', ';', ':', '"', "'", \
                                '(', ')', '--', '-', '...']

    ########################################################################
    ## Accessors.
    ########################################################################

    ########################################################################
    ## Mutators and incrementers
    ########################################################################

    ########################################################################
    ## General functions
    ########################################################################
#    ########################################################################
#    ## Print the 'dict' of docs.
#    def printdocs(self):
#        """ This is the docstring.
#        """
#        for docname, doc in sorted(self.docs.items()):
#            sss = 'PRINTDOCS  {:s} {:s}'.format(docname, str(doc))
#            printoutput(sss, OUTFILE)

#    ########################################################################
#    ## Print the 'set' of all the terms in the corpus.
#    def printoveralltermset(self):
#        """ This is the docstring.
#        """
#        for term in sorted(self.overalltermset):
#            sss = 'PRINTSET   {:s}'.format(term)
#            printoutput(sss, OUTFILE)

    ########################################################################
    ## Print the results for each doc for each term.
    def printresults(self, which):
        """ This is the docstring.
        """
        sss = 'LEGEND'
        sss += '\nColumn 0: Filename'
        sss += '\nColumn 1: Raw freq of the term in the doc'
        sss += '\nColumn 2: Total word count for the doc'
        sss += '\nColumn 3: (Raw freq)/(Total word count)'
        sss += '\nColumn 4: Number of unique terms in the doc'
        sss += '\nColumn 5: Number of unique terms in the collection'
        sss += '\nColumn 6: Number of docs in which the term appears'
        sss += '\nColumn 7: idf for this term'
        sss += '\nColumn 8: tf-idf for this term'
        sss += '\nColumn 9: The term'
        printoutput(sss, OUTFILE)

        for filename, onedoc in sorted(self.docs.items()):
            justfilename = filename.split('/')[-1]
            if which == 'ALL':
                thetermlist = onedoc.allterms
            elif which == 'SHORT':
                thetermlist = onedoc.topterms
            else:
                sss = 'ERROR IN PRINTRESULTS {:s}'.format(which)
                printoutput(sss, OUTFILE)
                sys.exit()

            for wordandpos, thisterm in sorted(thetermlist.items()):
                thisterm = onedoc.allterms[wordandpos]

                sss = '{:s} '.format(justfilename)
                sss += '{:7d} '.format(thisterm.rawfreq)
                sss += '{:7d} '.format(onedoc.totalwordcount)
                sss += '{:10.4f} '.format(thisterm.tftf)
                sss += '{:7d} '.format(len(onedoc.wordandposset))
                sss += '{:7d} '.format(len(self.overallwordandposset))
                sss += '{:7d} '.format(len(self.docset[wordandpos]))
                sss += '{:10.4f} '.format(thisterm.idf)
                sss += '{:10.4f} '.format(thisterm.tfidf)
                sss += '{:s} '.format(wordandpos)
                printoutput(sss, OUTFILE)

    ########################################################################
    ## Print the sparse matrix.
    def printsparsematrix(self, which):
        """ This is the docstring.
        """
        if which == 'TERM':
            for key, value in sorted(self.sparsematrixbyterm.items()):
                sss = ''
                for item in value:
                    sss += '   {:5s}:{:6.4f}'.format(item[0], item[3])
                printoutput('MATRIXTERM {:20s} {:s}'.format(key, sss), OUTFILE)
        elif which == 'DOC':
            for key, value in sorted(self.sparsematrixbydoc.items()):
                sss = ''
                for item in value:
                    sss += '   {:5s}:{:6.3f}'.format(item[0], item[3])
                printoutput('MATRIXDOC {:6s} {:s}'.format(key, sss), OUTFILE)

## End of class 'Globals'
############################################################################


############################################################################
#123456789012345678901234567890123456789012345678901234567890123456789012345
## class
class OneDoc():
    """ This is the docstring.
    """
    def __init__(self):
        self.thename = 'dummyname'
        self.totalwordcount = -99
        self.wordandposset = set()
        self.allterms = defaultdict(OneTerm)
        self.topterms = defaultdict(OneTerm)

    ########################################################################
    ## Overloads
    ########################################################################
    def __str__(self):
        """ This is the docstring.
        """
        sss = '{:s} TOTAL:{:6d} UNIQ:{:6d}\n'.format(self.thename, \
                                                     self.totalwordcount, \
                                                     len(self.wordandposset))
        for wordandpos in sorted(self.wordandposset):
            sss += '(WORDPOSSET  {:s})\n'.format(wordandpos)
        for wordandpos, thisterm in sorted(self.allterms.items()):
            sss += '(TERMSALL    {:6d} {:s})\n'.format(thisterm.rawfreq, wordandpos)
        return sss

    ########################################################################
    ## Accessors.
    ########################################################################
    ## accessor
    def gettotalwordcount(self):
        """ This is the docstring.
        """
        count = 0
        for thisterm in self.allterms.values():
            count += thisterm.rawfreq
        return count

    ########################################################################
    ## Mutators and incrementers
    ########################################################################

    ########################################################################
    ## General functions
    ########################################################################
    ########################################################################
    ## Increment the feature counts.
    def filterformostfrequent(self, howmany):
        """ This is the docstring.
        """
        mostfreqlist = []
        for wordandpos, thisterm in self.allterms.items():
            mostfreqlist.append([thisterm.rawfreq, wordandpos, thisterm])
        mostfreqlist = sorted(mostfreqlist)
        mostfreqlist = mostfreqlist[-howmany:]
        for item in mostfreqlist:
            self.topterms[item[1]] = item[2]

## End of class 'OneDoc'
############################################################################


############################################################################
#123456789012345678901234567890123456789012345678901234567890123456789012345
## class
class OneTerm():
    """ This is the docstring.
    """
    def __init__(self):
        self.theterm = 'dummyterm'
        self.rawfreq = 0
        self.tftf = -22.22
        self.idf = -33.33
        self.tfidf = -44.44
        self.docset = set()

    ########################################################################
    ## Overloads
    ########################################################################
    def __str__(self):
        """ This is the docstring.
        """
        sss = '{:20s} '.format(self.theterm)
        sss += ': {:10.4f}'.format(self.tftf)
        sss += ': {:10.4f}'.format(self.idf)
        sss += ': {:10.4f}'.format(self.tfidf)
        sss += ' ('
        for doc in sorted(self.docset):
            sss += ' {:s} '.format(doc)
        sss += ')'
        return sss

    ########################################################################
    ## Accessors.
    ########################################################################
#
    ########################################################################
    ## Mutators and incrementers
    ########################################################################
    ## Add to a docset after trimming away extra text.
    def addtodocset(self, whichdoc):
        """ This is the docstring.
        """
        whichdoc = whichdoc.replace('_FINAL.txt', '')

        whichdoc = whichdoc.replace('zout2014_4_101_000_', '')
        whichdoc = whichdoc.replace('zout2014_4_101_100_', '')
        whichdoc = whichdoc.replace('zout2014_4_101_300_', '')
        whichdoc = whichdoc.replace('zout2014_4_101_400_', '')
        whichdoc = whichdoc.replace('zout2014_4_101_500_', '')
        whichdoc = whichdoc.replace('zout2014_4_101_600_', '')
        self.docset.add(whichdoc)

    ########################################################################
    ## General functions
    ########################################################################

## End of class 'OneTerm'
############################################################################


############################################################################
## Compute the length of a vector in the sparse notation.
def computevectorlength(vectorrow):
    """ This is the docstring.
    """
    sumofsquares = 0.0
    for item in vectorrow:
        weight = item[1]
        addin = weight * weight
        sumofsquares += addin
    length = sqrt(sumofsquares)

    return length

############################################################################
## Compute the doc-doc or term-term similarities using the cosine.
def computecosinecomparison(label, sparsematrix):
    """ This is the docstring.
    """
    doclength = defaultdict(float)
    for key, value in sparsematrix.items():
        doclength[key] = computevectorlength(value)

    for key, value in sorted(doclength.items()):
        sss = '{:s} LENGTH {:20s} {:10.4f}'.format(label, key, value)
        printoutput(sss, OUTFILE)

    cosinedict = defaultdict(list)
    for key1, value1 in sparsematrix.items():
        for key2, value2 in sparsematrix.items():
            # We don't want A versus B and also B versus A,
            # and we don't want A versus A.
            if key2 <= key1:
                continue
            product = 0.0
            sss = '{:s} ONE {:s} {:s}'.format(label, key1, str(value1))
            printoutput(sss, OUTFILE)
            sss = '{:s} TWO {:s} {:s}'.format(label, key2, str(value2))
            printoutput(sss, OUTFILE)
            for item1 in value1:
#                term1 = item1[0]
#                tfidf1 = item1[1]
                for item2 in value2:
#                    term2 = item2[0]
#                    tfidf2 = item2[1]
#                    if term1 == term2:
                    if item1[0] == item2[0]:
#                        addin = tfidf1 * tfidf2
                        addin = item1[1] * item2[1]
                        product += addin
            product = product / doclength[key1]
            product = product / doclength[key2]
            printoutput('{:s} THR {:s} {:s} {:10.4f}\n'.format(label, key1, key2, product), OUTFILE)
            cosinedict[key1].append([key2, product])
            cosinedict[key2].append([key1, product])

    return cosinedict

############################################################################
## Compute the frequencies of nonstopwords and the rest of the basic stuff.
def computetermfreqs(theglobals):
    """ This is the docstring.
    """

    ########################################################################
    ## Read the files and compute the freqs.
    ## Note that we lowercase anything not tagged as an 'NP' of some sort.
    for name in theglobals.filenames:
        if 'FINAL' not in name:  # skip the 'DRAFT' files
            continue
        justfilename = name.split('/')[-1]  # get rid of the path prefix
        thisdoc = OneDoc()
        thefile = open(name)
        for line in thefile:
            if 'FINAL B ' not in line:  # skip the lines without POS
                continue
            lsplit = line.split()
            wordsandpos = lsplit[6:]  # get rid of the non-text metadata

            ################################################################
            ## Here's the loop on word_pos items in the sentence.
            for wordandpos in wordsandpos:
                word = wordandpos.split('_')[0]
                pos = wordandpos.split('_')[1]
                if 'NP' not in pos:
                    word = word.lower()
                    wordandpos = '_'.join([word, pos])
                if skipthistoken(theglobals, wordandpos):
                    continue

                ############################################################
                ## Create a 'OneTerm' if it's not already there.
                if wordandpos not in thisdoc.allterms.keys():
                    thisterm = OneTerm()
                    thisterm.theterm = wordandpos
                else:
                    thisterm = thisdoc.allterms[wordandpos]

                ############################################################
                ## Increment all the things that need to be incremented.
                thisterm.addtodocset(justfilename)
                thisterm.rawfreq += 1

                thisdoc.wordandposset.add(wordandpos)
                thisdoc.allterms[wordandpos] = thisterm

                theglobals.overallwordandposset.add(wordandpos)
                theglobals.docset[wordandpos].add(justfilename)

        ####################################################################
        ## Now update the stuff for 'thisdoc'.
        thisdoc.thename = justfilename
        thisdoc.totalwordcount = thisdoc.gettotalwordcount()
        for term, thisterm in thisdoc.allterms.items():
            thisterm.tftf = float(thisterm.rawfreq) / float(thisdoc.totalwordcount)
            thisdoc.allterms[term] = thisterm
        theglobals.docs[justfilename] = thisdoc

############################################################################
## Compute the tf-idf values.
def computetfidf(theglobals):
    """ This is the docstring.
    """
    for thisdoc in theglobals.docs.values():
        thisdocterms = thisdoc.topterms
#        justfilename = filename.split('/')[-1]
#        print(justfilename)
        thisfilename = thisdoc.thename

        for wordandpos, thisterm in sorted(thisdocterms.items()):
            tftf = float(thisterm.rawfreq)/float(thisdoc.totalwordcount)
            docfreq = len(theglobals.docset[wordandpos])
            bign = len(theglobals.docs)
            idf = log(float(bign)/float(docfreq))
            tfidf = tftf * idf
            thisdoc.topterms[wordandpos].tftf = tftf
            thisdoc.topterms[wordandpos].idf = idf
            thisdoc.topterms[wordandpos].tfidf = tfidf

            skinnyname = skinnythename(thisfilename)
            theglobals.sparsematrixbyterm[wordandpos].append([skinnyname, tftf, docfreq, tfidf])
            theglobals.sparsematrixbydoc[skinnyname].append([wordandpos, tftf, docfreq, tfidf])

############################################################################
## Skinny the name down to just the identifier.
def skinnythename(thename):
    """ This is the docstring.
    """
    newname = thename
    newname = newname.replace('zout2014_4_101_000_', '')
    newname = newname.replace('zout2014_4_101_100_', '')
    newname = newname.replace('zout2014_4_101_300_', '')
    newname = newname.replace('zout2014_4_101_400_', '')
    newname = newname.replace('zout2014_4_101_500_', '')
    newname = newname.replace('zout2014_4_101_600_', '')
    newname = newname.replace('_FINAL.txt', '')
    return newname

############################################################################
## Test whether we skip this token or not.
def skipthistoken(theglobals, token):
    """ This is the docstring.
    """
    skipthis = False

    word = token.split('_')[0]
    pos = token.split('_')[1]
    if (word in theglobals.stoplist) or \
       (('NP' not in pos) and (word.lower() in theglobals.stoplist)) or \
       (word in theglobals.punctlist) or \
       (pos in theglobals.punctlist) or \
       ('NULL' in pos) or \
       (token == "'s_GE"):
        skipthis = True

    return skipthis

############################################################################
## Main main MAIN function
def main(pathtodata):
    """ This is the docstring.
    """

    ########################################################################
    ## Measure process and wall clock times.
    dabtimer = DABTimer()
    logstring = dabtimer.timecall('BEGINNING')
    printoutput(logstring, LOGFILE)

    theglobals = Globals()

    theglobals.filenames = glob(pathtodata + '/*')

    ########################################################################
    ## Compute the term frequencies in each file.
    computetermfreqs(theglobals)

    ########################################################################
    ## Filter from all the terms to only the most frequent.
    for onedoc in theglobals.docs.values():
        onedoc.filterformostfrequent(10)

    ########################################################################
    ## Compute the tfidf and the sparse matrices along the way.
    computetfidf(theglobals)

    ########################################################################
    ## Print the results.
    theglobals.printresults('SHORT')

    ########################################################################
    ## Now compute and print the cosine comparisons.
    cosinedict = computecosinecomparison('DOCDOC', theglobals.sparsematrixbydoc)
    for key, value in sorted(cosinedict.items()):
        sss = 'DOCDOC {:7s} '.format(key)
        for item in sorted(value):
            if item[1] >= 0.50:
                sss += ' ({:6s} {:8.4f})'.format(item[0], item[1])
        printoutput(sss, OUTFILE)

    cosinedict = computecosinecomparison('TERMTERM', theglobals.sparsematrixbyterm)
    for key, value in sorted(cosinedict.items()):
        sss = 'TERMTERM {:15s} '.format(key)
        for item in sorted(value):
            if item[1] >= 0.90:
                sss += ' ({:6s} {:8.4f})'.format(item[0], item[1])
        printoutput(sss, OUTFILE)

    logstring = dabtimer.timecall('ENDING')
    printoutput(logstring, LOGFILE)

############################################################################
## main Main MAIN
checkargs(3, 'python a.out pathtodata outfile logfile')
OUTFILE = open(sys.argv[2], 'w')
LOGFILE = open(sys.argv[3], 'w')
main(sys.argv[1])
