import os
import re
from bs4 import BeautifulSoup

# It gets a output folder in current source path.
current_directory = os.getcwd()

# value of lambda
lambdaValue = 0.35

# dictionary which maintains words as keys and documents as values (including duplicates)
inverted_index_dict = {}

# dictionary which maintains documents as keys and term counts as values (including duplicates)
term_count_dict = {}


# reading term count from a file
def read_term_count(file):
    f = open(file, 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    for term in terms:
        if term:
            term = term.replace("[","").replace("]","")
            term_count_dict[term.split(",")[0].replace("'","").rstrip()] = int(term.split(",")[-1])
    return term_count_dict


# reading word and their respective documents from a file
def read_inverted_index(file):
    f = open(file, 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    for term in terms:
        if term:
            docs = eval(term.split(":")[2])
            inverted_index_dict[term.split(":")[0].rstrip()] = docs
    return inverted_index_dict


# handles punctuation on query text
def remove_punctuation(query_text):
    punctuation_list_text = [',', '.', '!', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', ';', '\'', '/',
                             '\\', '{', '}', ':', '"', '<', '>', '?', '=', '`', '~']
    punctuation_list_digits = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '[', ']', ';', '\'', '/', '\\',
                               '{', '}', ':', '"', '<', '>', '?', '=']
    processed_text_after = ""
    terms_list = query_text.split()
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
        processed_text_after = processed_text_after + ' ' + terms

    processed_text_after = processed_text_after.rstrip()
    processed_text_after = processed_text_after.lstrip()
    return processed_text_after

# handles case folding on query text
def handle_case_folding(query_text):
    query_text = str(query_text).lower()
    return query_text

def getQueries():
    print(0)


def getFileName(src_directory_path, fileName):

    if not os.path.exists(src_directory_path):
        os.mkdir(src_directory_path)

    f = open( src_directory_path + '/' + fileName + '.txt', 'w', encoding='utf-8')

    return f


def get_query(query_file):
    read_doc = open(query_file)
    soup = BeautifulSoup(read_doc.read(), "html.parser")
    doc_arr = soup.findAll("doc")
    query_dic = {}
    for ind_doc in doc_arr:
        soup_ind = BeautifulSoup(str(ind_doc), "html.parser")
        doc_id = str(soup_ind.find("docno").text).strip()
        soup_ind.find("docno").extract()
        query_dic[doc_id] = str(soup_ind.text.replace("\n", " ").strip())
    return query_dic


def get_query_stemmed(query_file):
    return_dictionary = {}
    read_query_arr = open(query_file).read().split("\n")
    i = 1
    for query in read_query_arr:
        return_dictionary[i] = query
        i+=1
    return return_dictionary