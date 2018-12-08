from collections import Counter
from collections import OrderedDict
import math
import os
import Read_data


# The current working directory
current_directory = os.getcwd()

# source file of inverted unigram index
inverted_index_data = current_directory + "/indexes/inverted_index_clean.txt"

# source file of unigram term count of documents
term_count_data = current_directory + "/indexes/term_count_clean.txt"

dst_directory = current_directory + "/results/bm_25/"


#bm25 parameters
b = 0.75
k1 = 1.2
k2 = 100

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}

# calculating lm dirichlet smoothing
def bm25(query_id, query, isStemming, isStopping):
    global inverted_index_data,term_count_data, dst_directory

    reset_dir()

    query = Read_data.remove_punctuation(query)
    query = Read_data.handle_case_folding(query)
    # splitting search query into terms separated by space
    query_terms = query.split(" ")


    if isStemming:
        inverted_index_data = current_directory + "/indexes/inverted_index_stemmed.txt"
        term_count_data = current_directory + "/indexes/term_count_stemmed.txt"
        dst_directory = current_directory + "/results/bm_25_stemmed"
        f = Read_data.getFileName(dst_directory, str(query_id))
    elif isStopping:
        inverted_index_data = current_directory + "/indexes/inverted_index_stopped.txt"
        term_count_data = current_directory + "/indexes/term_count_stopped.txt"
        dst_directory = current_directory + "/results/bm_25_stopped"
        f = Read_data.getFileName(dst_directory, str(query_id))
    elif 'prf' in str(query_id):
        f = Read_data.getFileName(current_directory + "/results/prf", query_id.split('_')[0])
    else:
        f = Read_data.getFileName(dst_directory, str(query_id))

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
            current_count = term_count_docs.get(doc[0])
            if(current_count):
                term_count_docs[doc[0]] = term_count_docs.get(doc[0]) + doc[1]
                word_count = word_count + doc[1]
            else:
                term_count_docs[doc[0]] = doc[1]
                word_count = word_count + doc[1]

    average_document_length = word_count / len(term_count_dict)

    counter = 1
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
            fqi_d = 0
            doc_len = 0
            if docs:
                doc_len = len(docs)
                for doc in docs:
                    if(doc[0] == every_doc):
                        # frequency of query word in a document (fqi D)
                        fqi_d = doc[1]

            #bm25
            partial_score = - math.log10((doc_len + 0.5) / ((len(term_count_dict) - doc_len) + 0.5))
            term_frequency_score = (k1 + 1) * fqi_d / (K + fqi_d)
            query_frequency_score = (k2+1) * query_counts/(k2+query_counts)
            score = score + partial_score * term_frequency_score * query_frequency_score
            index+=1

        score_dict[every_doc] = score
        print("bm25 calculated for - " + every_doc + ' for query ' + str(query_id))

    # sorting document based on score in descending order
    score_dict = OrderedDict(sorted(score_dict.items(), key=lambda key_value: key_value[1], reverse=True))

    query = query.replace(" ","_")

    count = 1
    for s in score_dict:
        f.write(str(query_id) + " Q0 " + str(s) + " " + str(count) + " " + str(score_dict[s]) + " BM_25 "
                + "\n")
        if(count == 100):
            break;
        count+=1
    f.close()

    
    return score_dict


def reset_dir():
    global dst_directory, inverted_index_data, term_count_data
    # source file of inverted unigram index
    inverted_index_data = current_directory + "/indexes/inverted_index_clean.txt"
    # source file of unigram term count of documents
    term_count_data = current_directory + "/indexes/term_count_clean.txt"
    dst_directory = current_directory + "/results/bm_25/"