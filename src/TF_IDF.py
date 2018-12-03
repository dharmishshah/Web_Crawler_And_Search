from src import readData
import os
import math
from collections import OrderedDict
import re

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source file of inverted unigram index
inverted_index_data = current_directory + "/inverted_index.txt"

# source file of unigram term count of documents
term_count_data = current_directory + "/term_count.txt"

# value of lambda
lambdaValue = 0.35

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}

def main(queryId, query,dir):
    tf_idf(queryId, query,dir)

# calculating lm dirichlet smoothing
def tf_idf(queryId, query, dir):
    term_count_dict = readData.read_term_count()
    inverted_index_dict = readData.read_inverted_index()
    query = readData.remove_punctuation(query)
    query = readData.handle_case_folding(query)
    # splitting search query into terms separated by space
    query_terms = query.split(" ")

    q_dict = {}
    score_dict = {}

    term_count_docs = {}

    num_of_docs = len(term_count_dict)

    for every_doc in term_count_dict:
        # total number of terms in a document i.e. |D|
        term_count = term_count_docs.get(every_doc)
        score = 0
        for q in query_terms:
            docs = inverted_index_dict.get(q)
            fqi_D = 0
            if docs:
                for doc in docs:
                    if(doc[0] == every_doc):
                        # frequency of query word in a document (fqi D)
                        fqi_D = doc[1]

            #tf.idf
            if docs:
                score = score + (fqi_D * math.log10(num_of_docs/len(docs)))
        score_dict[every_doc] = score
    # sorting document based on score in descending order
    score_dict = OrderedDict(sorted(score_dict.items(), key=lambda key_value: key_value[1], reverse=True))

    query = query.replace(" ","_")
    # writing output in a file
    f = open(dir + "/" + str(queryId) + "_tf_idf.txt" , 'w+', encoding='utf-8')
    count = 1
    for s in score_dict:
        f.write(str(queryId) + " Q0 " + str(s) + " " + str(count) + " " + str(score_dict[s]) + " TF_IDF "
                + "\n")
        if(count == 100):
            break;
        count+=1

