import os
import BM25, Indexer


# the current working directory
current_dir = os.getcwd()

# docs that are to be considered relevant
top_k = 1
relevant_docs_dic = {}

# method to retrieve top documents using pseudo relevance feedback 
def calculate_score(query_id,original_query_text):
    
    # first run 
    # to fetch relevant results using bm25 function
    score_dict = BM25.bm25(query_id, original_query_text, False, False)

     # the top_k files to be searched for relevant words
    file_names = []

    k = 0
    for doc in score_dict.keys():

        file_names.append(doc)

        k += 1
        if(k == top_k):
            break

    print(file_names)
    
    # global relevant_docs_dic
    # get_relevant_docs()
    # file_names = relevant_docs_dic[query_id]
    
    # new query to be appended to original query for fetching highly relevant results
    refined_query = Indexer.create_index('./output_files/clean_corpus_with_no_stopwords', file_names, top_k, "clean")
    
    # expanding the query
    new_query = original_query_text + " " +refined_query
    
    print(new_query)
    print()
    
    
    # second_run
    # to fetch the relevant documents to be shown to the user sorted by their relevance
    score_dict = BM25.bm25(str(query_id)+"_prf", new_query, False, False)


def get_relevant_docs():
    
    global relevant_docs_dic
    
    with open('./test_collection/cacm.rel.txt', 'r+') as rel_file:
        line_data = rel_file.read().split('\n') 
        
        for line in line_data:
            if(len(line) == 0):
                continue
            parts = line.split(' ')
            query_id = parts[0]
            
            rel_doc_name = parts[2]
            
            if query_id not in relevant_docs_dic.keys():
                relevant_docs_dic[query_id] = [rel_doc_name]
            else:
                doc_list = relevant_docs_dic[query_id]
                doc_list.append(rel_doc_name)
                relevant_docs_dic.update({query_id : doc_list})


# calculate_score(1, "What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?")