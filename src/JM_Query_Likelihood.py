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

dst_directory = current_directory + "/results/jm_query_likelihood/"


# calculating lm dirichlet smoothing
def jm_query_likelihood(queryId, query, isStemming,isStopping):
    global inverted_index_data,term_count_data, dst_directory
    query = Read_data.remove_punctuation(query)
    query = Read_data.handle_case_folding(query)
    # splitting search query into terms separated by space
    query_terms = query.split(" ")

    # writing output in a file
    f = Read_data.getFileName(dst_directory, str(queryId))

    if isStemming:
        inverted_index_data = current_directory + "/indexes/inverted_index_stemmed.txt"
        term_count_data = current_directory + "/indexes/term_count_stemmed.txt"
        dst_directory = current_directory + "/results/jm_query_likelihood_stemmed"
        f = Read_data.getFileName(dst_directory, str(queryId))

    if isStopping:
        inverted_index_data = current_directory + "/indexes/inverted_index_stopped.txt"
        term_count_data = current_directory + "/indexes/term_count_stopped.txt"
        dst_directory = current_directory + "/results/jm_query_likelihood_stopped"
        f = Read_data.getFileName(dst_directory, str(queryId))

    term_count_dict = Read_data.read_term_count(term_count_data)
    inverted_index_dict = Read_data.read_inverted_index(inverted_index_data)

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

            #lm dirichlet smoothing
            partial_score = ( (1 - lambdaValue) * (fqi_D / term_count) + lambdaValue * (q_dict.get(q) / word_count))

            # adding score in existing score for document
            if partial_score != 0:
                score = score + math.log10(partial_score)
        score_dict[every_doc] = score
    # sorting document based on score in descending order
    score_dict = OrderedDict(sorted(score_dict.items(), key=lambda key_value: key_value[1], reverse=True))

    query = query.replace(" ","_")
    count = 1
    for s in score_dict:
        f.write(str(queryId) + " Q0 " + str(s) + " " + str(count) + " " + str(score_dict[s]) + " JM_Query_Likelihood "
                + "\n")
        if(count == 100):
            break;
        count+=1
    f.close()
