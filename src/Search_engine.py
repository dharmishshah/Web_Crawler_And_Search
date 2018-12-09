
import JM_Query_Likelihood, TF_IDF, BM25
import Indexer
import Stopper
import Stemmer
import Snippet_generation
import Generate_corpus
import os
import Read_data
from bs4 import BeautifulSoup
import Pseudo_rel_feedback
import Evaluation

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source directory of all output files
src_directory_path = current_directory + "/test_collection/corpus/"


# destination directory of all output files after cleaning
dst_directory_path = current_directory + "/output_files/clean_corpus/"

# destination directory of all output files after cleaning
query_dir = current_directory + "/test_collection/"

def main():


    #generate_corpuses()

    #generate_indexes()

    query_dict = Read_data.get_query(query_dir + "cacm.query.txt")
    for query in query_dict:
        run_bm_25(int(query),query_dict.get(query),False)
        run_jm(int(query), query_dict.get(query), False)
        run_tf_idf(int(query), query_dict.get(query), False)
        print("done for query - " + query)

    # stemmed_query_dict = Read_data.get_query_stemmed(query_dir + "cacm_stem.query.txt")
    # for query in stemmed_query_dict:
    #     run_bm_25(int(query),stemmed_query_dict.get(query),True)
    #     run_jm(int(query), stemmed_query_dict.get(query), True)
    #     run_tf_idf(int(query), stemmed_query_dict.get(query), True)
    #     print("done for stemmed query - " + str(query))


    # run_bm_25()
    # run_jm()
    # run_tf_idf()

#     query_dict = Read_data.get_query(query_dir + "cacm.query.txt")
#     q_id=0
#     for query in query_dict:
#         q_id+=1
#         Pseudo_rel_feedback.calculate_score(q_id, query_dict.get(query))
    
    
#     Evaluation.evaluate_docs()
    


def generate_corpuses():

    # generating corpus from raw documents, applying punctuation removal and case folding
    Generate_corpus.generate_corpus(src_directory_path,dst_directory_path,True,True)

    # generating corpus with no stopwords
    Stopper.generate_corpus_without_stop_words()

    # generating corpus with stemming
    Stemmer.generate_corpus_from_stem_file()


def generate_indexes():
    Indexer.create_index('./output_files/clean_corpus', [], 0, "clean")

    Indexer.create_index('./output_files/clean_corpus_with_no_stopwords', [], 0, "stopped")

    Indexer.create_index('./output_files/clean_corpus_with_stemming', [], 0, "stemmed")


def run_bm_25(queryId, query, is_stem_query):
    # #ranking using bm 25
    if not is_stem_query:
        BM25.bm25(queryId, query, False, False)
        Snippet_generation.generate_snippet(queryId, query, "bm_25", 5)

        BM25.bm25(queryId, query, False, True)
        Snippet_generation.generate_snippet(queryId, query, "bm_25_stopped", 5)

    if is_stem_query:
        BM25.bm25(queryId, query, True, False)
        Snippet_generation.generate_snippet(queryId, query, "bm_25_stemmed", 5)

def run_jm(queryId, query,is_stem_query):
    # #ranking using JM Query likelihood
    JM_Query_Likelihood.jm_query_likelihood(queryId, query, False, False)
    Snippet_generation.generate_snippet(queryId, query, "jm_query_likelihood", 5)

    JM_Query_Likelihood.jm_query_likelihood(queryId, query, False, True)
    Snippet_generation.generate_snippet(queryId, query, "jm_query_likelihood_stopped", 5)

    if is_stem_query:
        JM_Query_Likelihood.jm_query_likelihood(queryId, query, True, False)
        Snippet_generation.generate_snippet(queryId, query, "jm_query_likelihood_stemmed", 5)


def run_tf_idf(queryId, query, is_stem_query):
    # #ranking using tf idf
    TF_IDF.tf_idf(queryId, query, False, False)
    Snippet_generation.generate_snippet(queryId, query, "tf_idf", 5)

    TF_IDF.tf_idf(queryId, query, False, True)
    Snippet_generation.generate_snippet(queryId, query, "tf_idf_stopped", 5)

    if is_stem_query:
        TF_IDF.tf_idf(queryId, query, True, False)
        Snippet_generation.generate_snippet(queryId, query, "tf_idf_stemmed", 5)

main()