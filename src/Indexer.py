import os
from collections import OrderedDict
from more_itertools import locate


def create_index(src_directory_path, file_names, top_k):
    # Dictionary to store inverted index
    inverted_index = {}
    # stores all terms in each document
    terms_per_document = []
     
    # stores positions for all terms in each document
    position_index = {} 
     
    files_in_directory=[]
    
    if len(file_names) == 0:
        # Opening Directory where clean corpus is stored
        for directory in os.walk(src_directory_path):
            for file in directory:
                files_in_directory = file
    else:
        files_in_directory = file_names

    #counter = 1
    for clean_file in files_in_directory:
        if(len(file_names) != 0):
            clean_file += '.txt' 
            
        with(open(src_directory_path + '/' + clean_file, 'r+', encoding='utf-8')) as f:

            # stripping .txt from file name
            clean_file = clean_file[:-4]

            # Using nltk library to create terms
            terms_list = f.read().split()

            unique_terms = set(terms_list)

            for unique_term in unique_terms:
                term_positions = list((locate(terms_list, lambda x: x == unique_term)))
                if unique_term not in inverted_index:
                    # if term not present, add it in inverted index
                    inverted_index[unique_term] = [[clean_file, len(term_positions)]]
                    position_index[unique_term] = [[clean_file, len(term_positions),term_positions]]
                    
                else:
                    # if term is already present, append current document term details in inverted index
                    inverted_index[unique_term].append([clean_file, len(term_positions)])
                    position_index[unique_term].append([clean_file, len(term_positions),term_positions])
                    

        terms_per_document.append([clean_file, len(unique_terms)])
        #print("indexed created for file "+ str(counter) +" - " + clean_file + " having terms = " + str(len(unique_terms)))
        #counter +=1

    if(len(file_names) == 0):
        write_inverted_index(inverted_index)
        write_positional_index(position_index)
        write_term_count(terms_per_document)

    # sorting inverted index
    doc_sorted_by_term_count = sort_index(inverted_index)
    
    # terms to be taken into consideration for query expansion
    term_count = 0
    
    query_ref_string = ""
    
    for term in doc_sorted_by_term_count.keys():
        counter = 0
        while counter < doc_sorted_by_term_count[term][0]:
            query_ref_string += str(term) + " "
            counter += 1
        
        term_count += 1
        if(term_count == top_k):
            break
    
    
    #print(query_ref_string)
    return query_ref_string
    

def sort_index(inverted_index):

    # sorted document frequency of terms in descending order
    document_frequency_sorted_index = {}
    for key in inverted_index:

        document_list = []
        document_count = 0
        for i in range(len(inverted_index[key])):
            document_list.append(inverted_index[key][i])

            # adding document as document count in document frequency of terms
            document_count = document_count + 1
        document_frequency_sorted_index[key] = [document_count,document_list]


    # sorting document frequency
    document_frequency_sorted_index_by_count = OrderedDict(
        sorted(document_frequency_sorted_index.items(),
               key=lambda key_value: key_value[1], reverse=True))
    
    return document_frequency_sorted_index_by_count


def write_inverted_index(inverted_index):
    
    with open('inverted_index.txt', 'w', encoding='utf-8') as f:
        for key in inverted_index:
            f.write(str(key) + " : " + str(len(inverted_index[key])) + " : "+ str(inverted_index[key]) + "\n")


def write_positional_index(position_index):
    
    f = open('position_inverted_index.txt', 'w', encoding='utf-8')
    for key in position_index:
            f.write(str(key) + " : " + str(position_index[key]) + "\n")


def write_term_count(terms_per_document):
    with open('term_count.txt', 'w', encoding='utf-8') as f:
        for term in terms_per_document:
            f.write(str(term) + '\n')     
            
# finding proximity of two terms using k.It is not case sensitive and order does not matter.
def find_proximity(src_directory_path, k, keyword1, keyword2):

    keyword1 = keyword1.lower()
    keyword2 = keyword2.lower()

    # two keywords cannot be same
    if(keyword1 == keyword2):
        return

    f = open(src_directory_path + '1_position_inverted_index_dgaps.txt', 'r+', encoding='utf-8')
    input = f.read();
    terms = input.split("\n");
    keyword1docs = ""
    keyword2docs = ""
    proximity_docs = []
    for term in terms:
        keyword = term.split(":")[0].rstrip()
        print("checking at keyword - " + keyword)
        if(keyword == keyword1):
            keyword1docs = eval(term.split(":")[1])
        if(keyword == keyword2):
            keyword2docs = eval(term.split(":")[1])

    for keyword1 in keyword1docs:
        for keyword2 in keyword2docs:
            if(keyword1[0] == keyword2[0]):
                list1 = keyword1[2]
                list2 = keyword2[2]
                find_proximity_in_range(proximity_docs, k,list1,list2, keyword1[0])

    with open(str(k) + '_proximity_index.txt', 'w', encoding='utf-8') as f:
        for key in proximity_docs:
            f.write(str(key) + "\n")


# validating two terms proximity values is in range or not.
def find_proximity_in_range(proximity_list, k,keyword_position1,keyword_position2, doc):
    position_list = []
    for keyword_pos1 in keyword_position1:
        for keyword_pos2 in keyword_position2:

            # if both keywords are in proximity of each other using k
            if(abs(keyword_pos1 - keyword_pos2) <= k):
                position_list.append(str(keyword_pos1) + " " + str(keyword_pos2))

    if(len(position_list) > 0):
        proximity_list.append(str(doc) + ": " + str(position_list))




#create_index(os.getcwd()+'/sample', [], 5)

