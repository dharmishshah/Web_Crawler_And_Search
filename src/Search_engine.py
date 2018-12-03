from src import JM_Query_Likelihood, TF_IDF, BM25
from src import Indexer
from src import Stopper
from src import Generate_corpus
import os
from bs4 import BeautifulSoup

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source directory of all output files
src_directory_path = current_directory + "/test_collection/corpus/"


# destination directory of all output files after cleaning
dst_directory_path = current_directory + "/output_files/clean_corpus/"

def main():

    Stopper.generate_corpus_without_stop_words()

    #generating corpus from raw documents, applying punctuation removal and case folding
    # Generate_corpus.generate_corpus(src_directory_path,dst_directory_path,True,True)
    #
    # #indexing for unigram with dgaps
    # Indexer.create_index(dst_directory_path, True, 100)
    #
    # #indexing for unigram without dgaps
    # Indexer.create_index(dst_directory_path, False, 100)
    #
    # #ranking using JM Query likelihood
    # JM_Query_Likelihood.jm_query_likelihood(1,"What articles exist which deal with TSS (Time Sharing System), an"
    # + "operating system for IBM computers?",current_directory)
    #
    # #ranking using tf idf
    # TF_IDF.tf_idf(1,"What articles exist which deal with TSS (Time Sharing System), an"
    # + "operating system for IBM computers?",current_directory)
    #
    # #ranking using bm 25
    # BM25.bm25(1, "What articles exist which deal with TSS (Time Sharing System), an"
    #               + "operating system for IBM computers?")

main()