import os
import math
from collections import OrderedDict

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source file of inverted unigram index
invertedIndexFile = current_directory + "/inverted_index.txt"

# source file of unigram term count of documents
termCountFile = current_directory + "/term_count.txt"

# value of mu
mu = 1500

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}

def main(queryId, query,dir):
    bm25(queryId, query,dir)

# reading term count from a file
def readTermCount():
    f = open(termCountFile, 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    for term in terms:
        if term:
            term = term.replace("[","").replace("]","")
            term_count_dict[term.split(",")[0].replace("'","").rstrip()] = int(term.split(",")[-1])


# reading word and their respective documents from a file
def readInvertedIndex():
    f = open(invertedIndexFile, 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    for term in terms:
        if term:
            docs = eval(term.split(":")[2])
            inverted_index_dict[term.split(":")[0].rstrip()] = docs

# calculating lm dirichlet smoothing
def bm25(queryId, query, dir):
    readTermCount()
    readInvertedIndex()

    # splitting search query into terms separated by space
    query_terms = query.split(" ")
    q_dict = {}
    score_dict = {}

    for q in query_terms:
        docs = inverted_index_dict.get(q)
        # number of times query word occur in a collection
        c_qi = 0

        for doc in docs:
            count = doc[1]
            c_qi = count + c_qi
        q_dict[q] = c_qi

    term_count_docs = {}

    # number of word occurrences in a collection
    word_count = 0
    for word in inverted_index_dict:
        docs = inverted_index_dict.get(word)
        for doc in docs:
            currentCount = term_count_docs.get(doc[0])
            if(currentCount):
                term_count_docs[doc[0]] = term_count_docs.get(doc[0]) + doc[1]
                word_count = word_count + doc[1]
            else:
                term_count_docs[doc[0]] = doc[1]
                word_count = word_count + doc[1]
    for every_doc in term_count_dict:
        # total number of terms in a document i.e. |D|
        term_count = term_count_docs.get(every_doc)
        score = 0
        for q in query_terms:
            docs = inverted_index_dict.get(q)
            fqi_D = 0
            for doc in docs:
                if(doc[0] == every_doc):
                    # frequency of query word in a document (fqi D)
                    fqi_D = doc[1]

            #lm dirichlet smoothing
            partial_score = (fqi_D + (mu * (q_dict.get(q) / word_count))) / (term_count + mu)
            # adding score in existing score for document
            score = score + math.log10(partial_score)

        score_dict[every_doc] = score
        # sorting document based on score in descending order
        score_dict = OrderedDict(sorted(score_dict.items(), key=lambda key_value: key_value[1], reverse=True))

    query = query.replace(" ","_")
    # writing output in a file
    f = open(dir + "/" + query + "_lm_dirichlet.txt" , 'w+', encoding='utf-8')
    count = 1
    for s in score_dict:
        f.write(str(queryId) + " Q0 " + str(s) + " " + str(count) + " " + str(score_dict[s]) + " LM_Dirichlet " + "\n")
        if(count == 100):
            break;
        count+=1
