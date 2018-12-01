import os
import nltk
from collections import OrderedDict
from more_itertools import locate
from prettytable import PrettyTable


def create_index(src_directory_path, dgaps):
    # Dictionary to store inverted index
    inverted_index = {}
    # stores all terms in each document
    terms_per_document = []
    # stores positions for all terms in each document
    position_index = {}
    # Opening Directory where clean corpus is stored
    for directory in os.walk(src_directory_path):
        for file in directory:
            files_in_directory = file

    counter = 1
    for clean_file in files_in_directory:
        with(open(src_directory_path + '/' + clean_file, 'r+', encoding='utf-8')) as f:

            # stripping .txt from file name
            clean_file = clean_file[:-4]

            # Using nltk library to create terms
            termsList = f.read().split()

            uniqueTerms = set(termsList)

            for uniqueTerm in uniqueTerms:
                length = 0
                if(dgaps):
                    # encoding terms position using dgaps
                    termPositions = encodeDgaps(list((locate(termsList, lambda x: x == uniqueTerm))))
                else:
                    termPositions = list((locate(termsList, lambda x: x == uniqueTerm)))
                if uniqueTerm not in inverted_index:
                    # if term not present, add it in inverted index
                    inverted_index[uniqueTerm] = [[clean_file, len(termPositions)]]
                    position_index[uniqueTerm] = [
                        [clean_file, len(termPositions),termPositions]]
                else:
                    # if term is already present, append current document term details in inverted index
                    inverted_index[uniqueTerm].append([clean_file, len(termPositions)])
                    position_index[uniqueTerm].append([clean_file, len(termPositions),termPositions])

        terms_per_document.append([clean_file, len(uniqueTerms)])
        print("indexed created for file "+ str(counter) +" - " + clean_file + " having terms = " + str(len(uniqueTerms)))
        counter +=1

    # writing inverted index of terms on a text files
    write_inverted_index(terms_per_document, inverted_index, position_index, dgaps)

    # sorting inverted index
    sort_index(inverted_index)

def write_inverted_index(terms_per_document,inverted_index,position_index, dgaps):
    with open('term_count.txt', 'w', encoding='utf-8') as f:
        for term in terms_per_document:
            f.write(str(term) + '\n')

    with open('inverted_index.txt', 'w', encoding='utf-8') as f:
        for key in inverted_index:
            f.write(str(key) + " : " + str(len(inverted_index[key])) + " : "+ str(inverted_index[key]) + "\n")

    if(dgaps):
        f = open('position_inverted_index_dgaps.txt', 'w', encoding='utf-8')
    else:
        f = open('position_inverted_index.txt', 'w', encoding='utf-8')
    for key in position_index:
            f.write(str(key) + " : " + str(position_index[key]) + "\n")

def sort_index(inverted_index):

    # sorted term frequency of terms in descending order
    term_frequency_sorted_index = {}

    # sorted document frequency of terms in descending order
    document_frequency_sorted_index = {}
    for key in inverted_index:
        term_frequency = 0
        document_list = []
        document_count = 0
        for i in range(len(inverted_index[key])):
            # adding term frequency of term from all documents
            term_frequency = term_frequency + inverted_index[key][i][1]
            document_list.append(inverted_index[key][i][0])

            # adding document as document count in document frequency of terms
            document_count = document_count + 1
        term_frequency_sorted_index[key] = term_frequency
        document_frequency_sorted_index[key] = [document_count,document_list]

    # sorting term frequency
    term_frequency_sorted_index = OrderedDict(
        sorted(term_frequency_sorted_index.items(), key=lambda key_value: key_value[1], reverse=True))



    # sorting document frequency
    document_frequency_sorted_index_by_count = OrderedDict(
        sorted(document_frequency_sorted_index.items(),
               key=lambda key_value: key_value[1], reverse=True))
    document_frequency_sorted_index_by_term = OrderedDict(
        sorted(document_frequency_sorted_index.items(),
               key=lambda key_value: key_value[0], reverse=False))


    # coverting indexed terms into table format
    convert_into_table(term_frequency_sorted_index,document_frequency_sorted_index_by_count,document_frequency_sorted_index_by_term)

def convert_into_table(term_frequency_sorted_index,document_frequency_sorted_index_by_count,document_frequency_sorted_index_by_term):
    tf_table = PrettyTable(['term', 'term_frequency'])

    tf_file = open('tf_table.txt', 'w', encoding='utf-8')
    tf_file.write(str("------------- Terms : \tFrequency Count\n\n"))
    for key in term_frequency_sorted_index:
        try:
            tf_file.write(str(key) + "\t" + str(term_frequency_sorted_index[key]) + "\n")
        except:
            print(str(key))
        #tf_table.add_row([key, term_frequency_sorted_index[key]])


    # with open(str(n_gram) + '_tf_table.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(tf_table))
    dfFile =   open('df_table_by_count.txt', 'w', encoding='utf-8')
    dfFile.write(str("------------- Terms : \tDocument Count\t Documents\n\n"))
    for key in document_frequency_sorted_index_by_count:
        dfFile.write(str(key) + ":\t" + str(document_frequency_sorted_index_by_count[key][0]) + "\t" + str(document_frequency_sorted_index_by_count[key][1]) + "\n\n")
    dfFile = open('df_table_by_term.txt', 'w', encoding='utf-8')
    dfFile.write(str("------------- Terms : \tDocument Count\t Documents\n\n"))
    for key in document_frequency_sorted_index_by_term:
        dfFile.write(str(key) + ":\t" + str(document_frequency_sorted_index_by_term[key][0]) + "\t" + str(
            document_frequency_sorted_index_by_term[key][1]) + "\n\n")

# encoding list of positional indexes of a term using dgaps
def encodeDgaps(terms):
    initialValue = 0
    dgaps = []

    # encoding term positions using dgaps
    for termPosition in terms:
        dgaps.append(termPosition-initialValue)
        initialValue = termPosition
    return dgaps

# decoding list of positional indexes of a term
def decodeDgaps(terms):
    currentValue = 0
    dgaps = []

    # decoding term positions using dgaps
    for termPosition in terms:
        dgaps.append(termPosition + currentValue)
        currentValue = currentValue + termPosition
    return dgaps

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
    proximityDocs = []
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
                list1 = decodeDgaps(list1)
                list2 = keyword2[2]
                list2 = decodeDgaps(list2)
                findProximityInRange(proximityDocs, k,list1,list2, keyword1[0])

    with open(str(k) + '_proximity_index.txt', 'w', encoding='utf-8') as f:
        for key in proximityDocs:
            f.write(str(key) + "\n")


# validating two terms proximity values is in range or not.
def findProximityInRange(proximityList, k,keywordPosition1,keywordPosition2, doc):
    positionList = []
    for keywordPos1 in keywordPosition1:
        for keywordPos2 in keywordPosition2:

            # if both keywords are in proximity of each other using k
            if(abs(keywordPos1 - keywordPos2) <= k):
                positionList.append(str(keywordPos1) + " " + str(keywordPos2))

    if(len(positionList) > 0):
        proximityList.append(str(doc) + ": " + str(positionList))


