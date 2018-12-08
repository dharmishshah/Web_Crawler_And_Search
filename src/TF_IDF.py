from src import Read_data
import os
import math
from collections import OrderedDict
import re

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source file of inverted unigram index
inverted_index_data = current_directory + "/indexes/inverted_index_clean.txt"

# source file of unigram term count of documents
term_count_data = current_directory + "/indexes/term_count_clean.txt"

# value of lambda
lambdaValue = 0.35

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}

dst_directory = current_directory + "/results/tf_idf/"

def main(queryId, query,dir):
    tf_idf(queryId, query,dir)

# calculating lm dirichlet smoothing
def tf_idf(queryId, query, isStemming, isStopping):
    global term_count_data,inverted_index_data,dst_directory
    query = Read_data.remove_punctuation(query)
    query = Read_data.handle_case_folding(query)
    # splitting search query into terms separated by space
    query_terms = query.split(" ")

    # writing output in a file
    f = Read_data.getFileName(dst_directory, str(queryId))

    if isStemming:
        inverted_index_data = current_directory + "/indexes/inverted_index_stemmed.txt"
        term_count_data = current_directory + "/indexes/term_count_stemmed.txt"
        dst_directory = current_directory + "/results/tf_idf_stemmed"
        f = Read_data.getFileName(dst_directory, str(queryId))

    if isStopping:
        inverted_index_data = current_directory + "/indexes/inverted_index_stopped.txt"
        term_count_data = current_directory + "/indexes/term_count_stopped.txt"
        dst_directory = current_directory + "/results/tf_idf_stopped"
        f = Read_data.getFileName(dst_directory, str(queryId))

    term_count_dict = Read_data.read_term_count(term_count_data)
    inverted_index_dict = Read_data.read_inverted_index(inverted_index_data)

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
    count = 1
    for s in score_dict:
        f.write(str(queryId) + " Q0 " + str(s) + " " + str(count) + " " + str(score_dict[s]) + " TF_IDF "
                + "\n")
        if(count == 100):
            break;
        count+=1
    f.close()

