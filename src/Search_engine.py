
import JM_Query_Likelihood, TF_IDF, BM25
import Indexer
import Stopper
import Stemmer
import Snippet_generation
import Generate_corpus
import os
from bs4 import BeautifulSoup
import Pseudo_rel_feedback

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source directory of all output files
src_directory_path = current_directory + "/test_collection/corpus/"


# destination directory of all output files after cleaning
dst_directory_path = current_directory + "/output_files/clean_corpus/"

def main():


    #generating corpus from raw documents, applying punctuation removal and case folding
    #Generate_corpus.generate_corpus(src_directory_path,dst_directory_path,True,True)

    # generating corpus with no stopwords
    #Stopper.generate_corpus_without_stop_words()

    # generating corpus with stemming
    #Stemmer.generate_corpus_from_stem_file()


    #indexing for unigram with dgaps
    Indexer.create_index('./output_files/clean_corpus', [], 0, "clean")

    # indexing for unigram with dgaps
    Indexer.create_index('./output_files/clean_corpus_with_no_stopwords', [], 0, "stopped")

    # indexing for unigram with dgaps
    Indexer.create_index('./output_files/clean_corpus_with_stemming', [], 0, "stemmed")


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



    # Pseudo_rel_feedback.calculate_score(1, "What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?")

    # snippet generation for retrieval models
    # Snippet_generation.generate_snippet(1,"What articles exist which deal with TSS (Time Sharing System), an"
    #  + "operating system for IBM computers?","bm_25",5)
    #
    # Snippet_generation.generate_snippet(1, "What articles exist which deal with TSS (Time Sharing System), an"
    #                                     + "operating system for IBM computers?", "jm_query_likelihood", 5)
    #
    # Snippet_generation.generate_snippet(1, "What articles exist which deal with TSS (Time Sharing System), an"
    #                                     + "operating system for IBM computers?", "tf_idf", 5)

main()