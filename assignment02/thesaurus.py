#Duncan Harmon
#CSCE 578 assignment 2
#thesaurus project
#i plan to create a vector space model of each word (treating each entry in the dictionary as a document) and do a cosine comparison between words, setting a threshold, and calling words within that threshold synonyms

import numpy, scipy, os, sys, operator, json
from nltk.tokenize import word_tokenize, wordpunct_tokenize

def main():
    
    #create a list of stopwords to be referrenced when creating a list of keyterms
    stopwordSet = set()
    file = open("./stopwords.txt")
    for line in file:
        stopwordSet.add(line[:-1])
    file.close()



    #print to test stopword
#    for t in stopwordSet:
#        print("\"" + t + "\"")
    
    #read the json and create a dict of term:definition to be edited to work with
    json_file = open("./gcide-dictionary-json-master/json_files/gcide_z.json")
    json_str  = json_file.read()
    termDict = json.loads(json_str)
    json_file.close()
    print(termDict['zambian'])
    print(len(termDict['zambian']))

    newtermDict = {}

    #mutliple definitions were an issue, this appends the number of the definition to each term, "zambian0" and the corresponding definition, "zambian1" and the next definition for the term "zambian"
    for term in termDict:
        n=0
        for d in termDict[term]:
            newtermDict[term+str(n)]=d
            n+=1

    termDict = newtermDict


    #need a function to remove stopwords from definition
    for term in termDict:
        termDict[term] = removeStopwords(termDict[term],stopwordSet)
    print(termDict['zambian0'])
#    definition = removeStopwords("I like pie. Nothing other than pie, apple specifically, will please me to any extent!", stopwordSet)
#    print(definition)



#takes a string -> removes stopwords and tokenizes it
def removeStopwords(definition,stopwordSet):
    defSet = wordpunct_tokenize(definition)
    for t in defSet:
        if t in stopwordSet:
            defSet.remove(t)
    return defSet




if __name__ == "__main__":
    main()
