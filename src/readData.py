import os
import re

# It gets a output folder in current source path.
current_directory = os.getcwd()

# source file of inverted unigram index
invertedIndexFile = current_directory + "/inverted_index.txt"

# source file of unigram term count of documents
termCountFile = current_directory + "/term_count.txt"

# value of lambda
lambdaValue = 0.35

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}


# reading term count from a file
def readTermCount():
    f = open(termCountFile, 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    for term in terms:
        if term:
            term = term.replace("[","").replace("]","")
            term_count_dict[term.split(",")[0].replace("'","").rstrip()] = int(term.split(",")[-1])
    return term_count_dict


# reading word and their respective documents from a file
def readInvertedIndex():
    f = open(invertedIndexFile, 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    for term in terms:
        if term:
            docs = eval(term.split(":")[2])
            inverted_index_dict[term.split(":")[0].rstrip()] = docs
    return inverted_index_dict


# handles punctuation on query text
def remove_punctuation(queryText):
    punctuation_list_text = [',', '.', '!', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', ';', '\'', '/',
                             '\\', '{', '}', ':', '"', '<', '>', '?', '=', '`', '~']
    punctuation_list_digits = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', ';', '\'', '/', '\\',
                               '{', '}', ':', '"', '<', '>', '?', '=']
    processedTextAfter = ""
    terms_list = queryText.split()
    for terms in terms_list:
        # Case on whether digit is included
        if re.search(r'\d', terms):
            # Removing all the punctuations from the digit punctuation list
            for punctuations in punctuation_list_digits:
                terms = terms.replace(punctuations, '')
        else:
            # Removing all the punctuations from the text punctuation list
            for punctuations in punctuation_list_text:
                terms = terms.replace(punctuations, '')
        # text after punctuation handling
        processedTextAfter = processedTextAfter + ' ' + terms

    processedTextAfter = processedTextAfter.rstrip()
    processedTextAfter = processedTextAfter.lstrip()
    return processedTextAfter

# handles case folding on query text
def handleCaseFolding(query_text):
    query_text = str(query_text).lower()
    return query_text