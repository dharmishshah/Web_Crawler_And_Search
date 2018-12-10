import os
import json
import re
from threading import Thread
from multiprocessing import Pool
from itertools import groupby
from operator import itemgetter
from collections import Counter
from collections import OrderedDict
import math

inverted_index = {}
inverted_index_file_path = '../invertedIndex/position_inverted_index.txt'
queryList_path = '../query/cacm.query.txt'
stop_word_list_path = '../stopWords/common_words'
queryList = []
stop_word_list = []
proximity_window = 10
#bm25 parameters
b = 0.75
k1 = 1.2
k2 = 100


def handle_puctuation_and_newline(sentence):

    sentence = sentence.replace("\n"," ")

    sentence = re.sub(r"( )+", " ", sentence)

    punctuationRemovalListForText = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '_', '=', '{', '}', '[',
                                     ']', ':', ';', '"', '|', '\\\'', ',', '<', '>', '.', '/', '?', '`', '“', '”', '☇',
                                     '′', '～', '☉', '~', '，', '、', '⹁']

    for punctuation in punctuationRemovalListForText:
        sentence = sentence.replace(punctuation,"");

    return sentence


# This is a method to write a JSON file.
def write_json(filename, dict):
    if not os.path.exists("../jsonFiles"):
        os.mkdir("../jsonFiles")
    f = open("../jsonFiles/"+filename+"JSON.json", "w")
    converted_json = json.dumps(dict)
    f.write(converted_json)
    f.close()


def load_inverted_index():
    global inverted_index
    #print("************* LOADING INVERTED INDEX *******************")
    with open(inverted_index_file_path, 'r') as inf:
        for line in inf:
            element = line.split(":");
            inverted_index[element[0].strip()] = eval(element[1])

    #print("finishing inverted index building")


def query_processing(query):

    query_list_temp = query.strip().split("</DOC>")
    for query in query_list_temp:
        query = re.sub(r"<DOC>\n<DOCNO>.*</DOCNO>", "", query)
        if query != "":
            query = handle_puctuation_and_newline(query)
            queryList.append(query.strip().lower())

def load_stop_words():
    with open(stop_word_list_path) as f:
        for line in f:
            stop_word_list.append(line.strip())



def load_query():
    #print("************* LOADING QUERY *******************")
    query = ""
    with open(queryList_path, 'r') as inf:
        for line in inf:
            query = query+line

    query_processing(query)
    #print("finishing query building")


def find_documents_which_has_the_term_passed(term):

    #print("finding document with term "+term)

    if term not in inverted_index.keys():
        return []
    list_of_documents_with_term_present = inverted_index[term]

    list_of_docs = []
    for tuple in list_of_documents_with_term_present:
        list_of_docs.append(tuple[0])

    #print(list_of_docs)

    #print("XXXXXXXXXXXXXfinding document end XXXXXXXXXX  "+term)
    return list_of_docs


def find_position_of_a_term_in_a_file(term, document):
    doc = inverted_index[term]
    if term not in inverted_index.keys():
        return -1
    else:
        for tuple in doc:
            if tuple[0] == document:
                return tuple[2]



def find_intersection_of_files(listOflists):
    result = set(listOflists[0])
    for s in listOflists[1:]:
        result.intersection_update(s)
    return result


def findConsecutiveNumber(listy, lengthOfQuery):
    listy.sort()
    myset = set(listy)
    listy = list(myset)
    number = []
    for k, g in groupby(enumerate(listy), lambda x : x[0] - x[1]):
        number.append(list(map(itemgetter(1), g)))
    returnNumbers = []
    for listelement in number:
        if(len(listelement) >= lengthOfQuery):
            returnNumbers.append(listelement)
    return returnNumbers



def exact_match(query):
    print("************** Executing Exact Match ****************")
    print("the query term being processed is: "+query)
    list_of_query_terms = query.split(" ")
    pool = Pool()
    combinedList = pool.map(find_documents_which_has_the_term_passed, list_of_query_terms)
    pool.close()
    pool.join()
    #print(combinedList)
    result = find_intersection_of_files(combinedList)

    list_of_docuements_containing_the_query_in_eaxct_order = []

    for doc in result:
        combinatrix = {}
        find_consecutive_numbers = []
        for term in list_of_query_terms:
            listPos = find_position_of_a_term_in_a_file(term, doc)
            combinatrix[term] = listPos
            find_consecutive_numbers = find_consecutive_numbers + listPos

        list_of_pos = findConsecutiveNumber(find_consecutive_numbers,len(list_of_query_terms))

        for position in list_of_pos:
            writeToList = True
            for i in range(0, len(list_of_query_terms)):
                if position[i] not in combinatrix[list_of_query_terms[i]]:
                    writeToList = False
            if writeToList:
                list_of_docuements_containing_the_query_in_eaxct_order.append(doc)

    #print("the  document containing query", list_of_docuements_containing_the_query_in_eaxct_order,"\n the length is ", set(list_of_docuements_containing_the_query_in_eaxct_order).__len__())
    exactDocumentList = list(set(list_of_docuements_containing_the_query_in_eaxct_order))



    filename = query[:15].replace(" ", "-")

    f = open("../output/ExactMatch/" + filename + "-Exact-Match", "w")
    f.write("Query: " + query + "\n")
    if len(exactDocumentList) > 0:
        scoreDict = bm25ranking(list_of_query_terms, exactDocumentList)
        counter = 1
        for score in scoreDict.keys():
            if (counter > 100):
                break
            f.write(str(1) + " Q0 " + str(score) + " " + str(counter) + " " + str(scoreDict[score]) + " BM_25 "+ "\n")

            counter += 1

    else:
        f.write("sorry! no match")
        print("sorry! no match")







def exact_match_wrapper():
    for query in queryList:
        exact_match(query)



def best_match_wrapper():
    for query in queryList:
        best_match(query)


def best_match(query):
    print("************** Executing Best Match ****************")
    print("the query term being processed is: " + query)
    list_of_query_terms = query.split(" ")
    pool = Pool()
    combinedList = pool.map(find_documents_which_has_the_term_passed, list_of_query_terms)
    pool.close()
    pool.join()

    combinatrix = []

    for list in combinedList:
        combinatrix = combinatrix + list


    #print("list of docs: ",combinatrix)

    bestMatchDocument = set(combinatrix)

    filename = query[:15].replace(" ", "-")

    f = open("../output/BestMatch/" + filename+"-Best-Match", "w")
    f.write("Query: " + query + "\n")
    if len(bestMatchDocument) > 0:
        scoreDict = bm25ranking(list_of_query_terms, bestMatchDocument)
        counter = 1
        for score in scoreDict.keys():
            if (counter > 100):
                break
            f.write(str(1) + " Q0 " + str(score) + " " + str(counter) + " " + str(scoreDict[score]) + " BM_25 "+ "\n")
            counter += 1

    else:
        f.write("sorry! no match")
        print("sorry! no match")


def proximity_match_wrapper():
    for query in queryList[:1]:
        proximity_match(query)



def bestProximitySearch(document,queryList):
    listOfPos = []
    for queryterm in queryList:
        listOfpositions = find_position_of_a_term_in_a_file(queryterm, document)
        #print(queryterm, " : ", listOfpositions)
        if listOfpositions == None :
            continue
        listOfPos.append(listOfpositions)

    return listOfPos

def listConverter(listOfPositions):

    l = []
    for pos in listOfPositions:
        l = l+pos

    return l


def find_if_proximity2(listofpos):


    for i in range(0, len(listofpos) - 1):
        l1 = listofpos[i]
        l2 = listofpos[i+1]
        temp = checkIfProximity(l1,l2)
        if temp[0]:
            listofpos[i + 1] = temp[1]
            continue
        else:
            return False

    return True


def checkIfProximity(list1,list2):
    listOfProximity = []
    for elem in list1:
        for item in list2:
            if item - elem <=proximity_window and item - elem >= 0:
                listOfProximity.append(item)


    if len(listOfProximity) != 0:
        return True, listOfProximity
    else:
        return False, []

def find_if_proximity(listofpos):
    for i in range(0, len(listofpos) - 1):
        l1 = listofpos[i]
        l2 = listofpos[i+1]
        if checkProximity(l1,l2):
            return True
    return False

def checkProximity(list1,list2):
    for elem in list1:
        for item in list2:
            if item - elem <= proximity_window and item - elem >= 1:
                return True

    return False



def x(term, doc):
    listOflist = inverted_index[term]
    for list in listOflist:
        if list[0] == doc:
            return list[1]

    return 0



def numQueryWordInCollection(list_of_query_terms,collection):

    dict = {}
    for term in list_of_query_terms:
        somenumber = 0
        for doc in collection:
            somenumber = somenumber + x(term,doc)

        dict[term] = somenumber


    return dict



def wordsInCollection(collection):

    dict = {}
    for doc in collection:
        counter = 0
        for key in inverted_index.keys():
            listOflist = inverted_index[key]
            for list in listOflist:
                if list[0] == doc:
                    counter = counter+list[1]

        dict[doc] = counter

    return dict



def list_of_documents_in_collection_in_with_query_term_present(term, collection):
    list_of_docs_in_collection_quey_word_present = []

    if term not in inverted_index.keys():
        return []

    listOflist = inverted_index[term]


    for doc in collection:
        for list in listOflist:
            if list[0] == doc:
                list_of_docs_in_collection_quey_word_present.append(list)

    return list_of_docs_in_collection_quey_word_present


def bm25ranking(list_of_query_terms,collection):
    #number_of_times_query_word_appeared_in_collection = numQueryWordInCollection(list_of_query_terms,collection)

    total_number_of_words_in_collection = wordsInCollection(collection)
    #print(total_number_of_words_in_collection)

    numberOfWordsInCollection = 0
    for keys in total_number_of_words_in_collection:
        numberOfWordsInCollection = numberOfWordsInCollection + total_number_of_words_in_collection[keys]

    average_document_length = numberOfWordsInCollection/ len(total_number_of_words_in_collection.keys())

    score_dict = {}
    for every_doc in collection:
        term_count = total_number_of_words_in_collection[every_doc]
        K = ((1 - b) + b * term_count / average_document_length)
        score = 0
        index = 0
        counts = Counter(list_of_query_terms)
        for q in list_of_query_terms:

            docs = list_of_documents_in_collection_in_with_query_term_present(q, collection)

            query_counts = counts.get(q)
            fqi_d = 0
            doc_len = 0
            if docs:
                doc_len = len(docs)
                for doc in docs:
                    if (doc[0] == every_doc):
                        # frequency of query word in a document (fqi D)
                        fqi_d = doc[1]

            # bm25
            partial_score = - math.log10((doc_len + 0.5) / ((len(total_number_of_words_in_collection.keys()) - doc_len) + 0.5))
            term_frequency_score = (k1 + 1) * fqi_d / (K + fqi_d)
            query_frequency_score = (k2 + 1) * query_counts / (k2 + query_counts)
            score = score + partial_score * term_frequency_score * query_frequency_score
            index += 1
        print("the score of ",every_doc," is: ",score)
        score_dict[every_doc] = score

    score_dict = OrderedDict(sorted(score_dict.items(), key=lambda key_value: key_value[1], reverse=True))
    #print("this is the scores: ",score_dict)

    return score_dict




def proximity_match(query):
    print("************** Executing Proximity Best Match ****************", proximity_window)
    print("the query term being processed is: " + query)
    list_of_query_terms = query.split(" ")
    pool = Pool()
    combinedList = pool.map(find_documents_which_has_the_term_passed, list_of_query_terms)
    pool.close()
    pool.join()

    combinatrix = []

    for list in combinedList:
        combinatrix = combinatrix + list

    listOfuniqueDocuments = set(combinatrix)

    proximityDocumentList = []

    for doc in listOfuniqueDocuments:
        listOPos = bestProximitySearch(doc, list_of_query_terms)
        if len(listOPos) == 1:
            proximityDocumentList.append(doc)
        else:
            if find_if_proximity(listOPos):
                proximityDocumentList.append(doc)

    filename = query[:15].replace(" ", "-")

    f = open("../output/ProximityMatch/" + filename+"-Ordered-Proximity-Match", "w")
    f.write("Query: "+query+"\n")
    if len(proximityDocumentList) > 0:
        scoreDict = bm25ranking(list_of_query_terms, proximityDocumentList)
        counter = 1
        for score in scoreDict.keys():
            if(counter > 100):
                break
            f.write(str(1) + " Q0 " + str(score) + " " + str(counter) + " " + str(scoreDict[score]) + " BM_25 "+ "\n")
            counter += 1

    else:
        f.write("sorry! no match")
        print("sorry! no match")


def do_you_want_to_enter_your_own_query():
    option = input("do you want to enter your own query? y/n\n\n")
    querytext = ""
    if option.lower() == "y":
        querytext = input("enter your query: ")
    elif option.lower() == "n":
        return
    else:
        do_you_want_to_enter_your_own_query()

    return querytext


def documentRetreval():
    global proximity_window
    option = input("\n\nEnter one of the following options:\n1. Exact Match\n2. Best Match\n3. Ordered best	match within proximity N\n4.Exit\n\n")
    if option.lower() == "1":
        query = do_you_want_to_enter_your_own_query()
        if query == None:
            removal_of_stop_words_from_queryList()
            exact_match_wrapper()
        else:
            query = removal_of_stop_words_from_your_own_query(query)
            query = handle_puctuation_and_newline(query)
            query = query.lower()
            exact_match(query)
    elif option.lower() == "2":
        query = do_you_want_to_enter_your_own_query()
        if query == None:
            removal_of_stop_words_from_queryList()
            best_match_wrapper()
        else:
            query = removal_of_stop_words_from_your_own_query(query)
            query = handle_puctuation_and_newline(query)
            query = query.lower()
            best_match(query)
    elif option.lower() == "3":
        proximity = input("Enter the proximity window: ")
        proximity_window = int(proximity)
        query = do_you_want_to_enter_your_own_query()
        if query == None:
            removal_of_stop_words_from_queryList()
            proximity_match_wrapper()
        else:
            query = removal_of_stop_words_from_your_own_query(query)
            query = handle_puctuation_and_newline(query)
            query = query.lower()
            proximity_match(query)
    elif option.lower() == "4":
        return
    else:
        print("Wrong option!")

    documentRetreval()




def removal_of_stop_words_from_your_own_query(query):
    option = input("do you want to remove stop words from your own query? y/n\n\n")
    if option.lower() == "y":
        return remove_stop_words_from_query(query)
    elif option.lower() == "n":
        return query
    else:
        removal_of_stop_words_from_your_own_query()




def remove_stop_words_from_query(query):

    newQuery = ""
    quryLst = query.split(" ")
    for q in quryLst:
        if q not in stop_word_list:
            newQuery = newQuery+q+" "
    return newQuery.strip()


def removal_of_stop_words_from_queryList():
    queryListTemp = []
    global queryList
    option = input("hello user do you want to remove stop words from the query List? y/n\n\n")
    if option.lower() == "y":
        for query in queryList:
            queryListTemp.append(remove_stop_words_from_query(query))

        queryList = queryListTemp;

    elif option.lower() == "n":
        return
    else:
        removal_of_stop_words_from_queryList()


def main():

    thread1 = Thread(target=load_inverted_index)
    thread2 = Thread(target=load_query)
    thread3 = Thread(target=load_stop_words)
    thread1.start()
    thread2.start()
    thread3.start()
    thread2.join()
    thread3.join()
    thread1.join()
    documentRetreval()








if __name__ == '__main__':
    main()