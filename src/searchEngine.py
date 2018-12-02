from src import generateCorpus, indexer, JM_Query_Likelihood, TF_IDF, BM25, stopper
import os
from bs4 import BeautifulSoup

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source directory of all output files
src_directory_path = current_directory + "/outputFiles/corpus/"


# destination directory of all output files after cleaning
dst_directory_path = current_directory + "/outputFiles/cleanCorpus/"

def main():

    stopper.generate_file_without_stopwords()

    # generating corpus from raw documents, applying punctuation removal and case folding
    #generateCorpus.generateCorpus(src_directory_path,dst_directory_path,True,True)

    # indexing for unigram with dgaps
    #indexer.create_index(dst_directory_path, True)

    # indexing for unigram without dgaps
    #indexer.create_index(dst_directory_path, False)

    #ranking using JM Query likelihood
    # JM_Query_Likelihood.jm_query_likelihood(1,"What articles exist which deal with TSS (Time Sharing System), an"
    # + "operating system for IBM computers?",current_directory)
    #
    # #ranking using tf idf
    # TF_IDF.tf_idf(1,"What articles exist which deal with TSS (Time Sharing System), an"
    # + "operating system for IBM computers?",current_directory)

    # ranking using bm 25
    # BM25.bm25(1, "What articles exist which deal with TSS (Time Sharing System), an"
    #               + "operating system for IBM computers?", current_directory)

main()