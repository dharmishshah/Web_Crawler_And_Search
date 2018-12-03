import os
from src import BM25
from src import Indexer


# the current working directory
current_dir = os.getcwd()

# docs that are to be considered relevant
top_k = 1


# method to retrieve top documents using pseudo relevance feedback 
def calculate_score(query_id,original_query_text):
    
    # first run 
    # to fetch relevant results using bm25 function 
    score_dict = BM25.bm25(query_id, original_query_text)
    
    
    # the top_k files to be searched for relevant words
    file_names = []
    
    k = 0
    for doc in score_dict.keys():
        
        file_names.append(doc)
        
        k += 1
        if(k == top_k):
            break
    
    #print(file_names)
    
    
    # new query to be appended to original query for fetching highly relevant results
    refined_query = Indexer.create_index('./output_files/clean_corpus_with_no_stopwords', file_names, top_k)
    
    # expanding the query
    new_query = original_query_text + " " +refined_query
    
    print(new_query)
    print()
    
    
    # second_run
    # to fetch the relevant documents to be shown to the user sorted by their relevance
    score_dict = BM25.bm25(str(query_id)+"_new", new_query)
        

calculate_score(1, "What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?")