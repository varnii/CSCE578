#Duncan Harmon
#CSCE578
#Feb 4 2019
#CountReportingVerbs.py
#
#The pupose of this program is to read in all files in a directory, make a list of all tokens and create a list of the most frequent reportingverbs (from the reportingverbs.txt)

import os, sys, operator

def main():

    punctuation = "-....,;:?/\\\"\'()<>!"
    
    studentPath = "../Datastudent/Datastudentata2014sentpos/2014_4_101_400.sentpos/"

    studentFilesL = os.listdir(studentPath)

    #read in the list of reporting verbs and use this to make a dict of the list of reporting verbs
    reportingVerbsDict = {}
    file = open("./reportingverbs.txt","r")
    for line in file:
        if line.endswith('\n'):
            line = line[:-1]
        reportingVerbsDict[line] = 0
    file.close()
    studentrvd = reportingVerbsDict
    #now read through each file in studentFilesL and add to the frequency count of the verbs
    studentTokenCount = 0

    for doc in studentFilesL:
        #print("=======================PRINT===================")
        tempPath = studentPath + doc
        if "FINAL" in tempPath:
            temptup = countReportingVerbs(tempPath,studentrvd,studentTokenCount,punctuation)
            studentrvd = temptup[0]
            studentTokenCount = temptup[1]


    #sorts the dict into a list of tuples sorted on the second value
    for k in studentrvd:
        studentrvd[k]=(1000*studentrvd[k])/studentTokenCount
    sortedsrvd = sorted(studentrvd.items(), key=operator.itemgetter(1))
    print("\n\n-------------\nCOUNT: " + str(studentTokenCount) + "\n-------------")
    for i in range(1,11):
        print("  " + str(sortedsrvd[-i][1])[:10] + " " + str(sortedsrvd[-i][0]))

    COCAPath = "../COCA_acad/COCA_acad_wlp_2009sentpos/COCA_acad_wlp_2009_00.sentpos/"
    COCAFilesL = os.listdir(COCAPath)

    COCArvd = reportingVerbsDict
    COCATokenCount = 0
    doccount = 0;
    for doc in COCAFilesL:
        tempPath = COCAPath+doc
        temptup = countReportingVerbs(tempPath,COCArvd,COCATokenCount,punctuation)
        COCArvd = temptup[0]
        COCATokenCount = temptup[1]
        doccount+=1
        if doccount > 7:
            break

    for k in COCArvd:
        COCArvd[k] = (1000*COCArvd[k]/COCATokenCount)
    sortedCrvd = sorted(COCArvd.items(), key=operator.itemgetter(1))
    print("\n\n-------------\nCOUNT: " + str(COCATokenCount) + "\n-------------")

    for i in range(1,11):
        print("  " + str(sortedCrvd[-i][1])[:10] + " " + str(sortedCrvd[-i][0]))



def countReportingVerbs(p,rvd,tc,punc):#p = path rvd = reportingVerbsDict tc = tokenCount punc = punctuation
    #the goal here is to add to the freqs of doc p to the dict rvd, and increment tc by one for each word we pass
    with open(p,"r") as doc:
        for line in doc:
            lineL = line.split()
            lineL.pop(0)
            lineL.pop(0)
            lineL.pop(0)
            if lineL.pop(0) is "B":
                lineL.pop(0)
                lineL.pop(0)
                for token in lineL:
                    wpos = token.split('_')
                    if wpos[1] not in punc and wpos[0] not in punc:
                        tc+=1
                        if wpos[1][0] is "V" and wpos[0].lower() in rvd:
                            rvd[wpos[0].lower()]+=1


        return rvd,tc


#takes the dict "vdict" and adds any words found in path that match to the freq count and adds 1 to the token count for every word regardless
#def countReportingVerbs(path,vdict,tkcount):







if __name__ == "__main__":
    main()