from src import readData
import os
import math
from collections import OrderedDict
import re
from collections import Counter

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source file of inverted unigram index
invertedIndexFile = current_directory + "/inverted_index.txt"

# source file of unigram term count of documents
termCountFile = current_directory + "/term_count.txt"

#bm25 parameters
b = 0.75
k1 = 1.2
k2 = 100

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}

# calculating lm dirichlet smoothing
def bm25(queryId, query, dir):
    term_count_dict = readData.readTermCount()
    inverted_index_dict = readData.readInvertedIndex()
    query = readData.remove_punctuation(query)
    query = readData.handleCaseFolding(query)
    # splitting search query into terms separated by space
    query_terms = query.split(" ")

    q_dict = {}
    score_dict = {}

    for q in query_terms:
        docs = inverted_index_dict.get(q)
        # number of times query word occur in a collection
        c_qi = 0

        if docs:
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

    average_document_length = word_count / len(term_count_dict)

    for every_doc in term_count_dict:
        # total number of terms in a document i.e. |D|
        term_count = term_count_docs.get(every_doc)

        K = ((1 - b) + b * term_count/average_document_length)

        score = 0
        index = 0
        counts = Counter(query_terms)
        for q in query_terms:
            docs = inverted_index_dict.get(q)
            query_counts = counts.get(q)
            fqi_D = 0
            if docs:
                for doc in docs:
                    if(doc[0] == every_doc):
                        # frequency of query word in a document (fqi D)
                        fqi_D = doc[1]

            #bm25
            doc_len = 0
            if docs:
                doc_len = len(docs)
            partial_score = - math.log10(doc_len + 0.5 / ((len(term_count_dict) - doc_len) + 0.5))
            term_frequency_score = (k1 + 1) * fqi_D / (K + fqi_D)
            query_frequency_score = (k2+1) * query_counts/(k2+query_counts)
            score = score + partial_score * term_frequency_score * query_frequency_score
            index+=1

        score_dict[every_doc] = score
    # sorting document based on score in descending order
    score_dict = OrderedDict(sorted(score_dict.items(), key=lambda key_value: key_value[1], reverse=True))

    query = query.replace(" ","_")
    # writing output in a file
    f = open(dir + "/" + str(queryId) + "_bm_25.txt" , 'w+', encoding='utf-8')
    count = 1
    for s in score_dict:
        f.write(str(queryId) + " Q0 " + str(s) + " " + str(count) + " " + str(score_dict[s]) + " JM_Query_Likelihood "
                + "\n")
        if(count == 100):
            break;
        count+=1

