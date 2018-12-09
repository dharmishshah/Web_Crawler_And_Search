import os
import re
from bs4 import BeautifulSoup
import Read_data

from collections import OrderedDict

# It gets a output folder in current source path.
current_directory = os.getcwd()

stem_text_file = "./test_collection/cacm_stem.txt"

src_directory = os.getcwd()+"/output_files/clean_corpus/"


def generate_snippet(queryId, query, retrieval_model, window_size):

    snippet = ""
    with open(current_directory + "/results/" + retrieval_model + '/' + str(queryId) + ".txt", 'r+', encoding='utf-8') as f:
        processed_text = f.read()
        files = processed_text.split("\n")

        query = Read_data.remove_punctuation(query)
        query = Read_data.handle_case_folding(query)
        query_terms  = query.split(" ")
        sentences = {}

        destination_file = open(current_directory + "/results/" + retrieval_model + '/' + str(queryId) + "_snippet.html", 'w', encoding='utf-8')

        for file in files:
            destination_file.write("<br>")
            if file:
                file_name = file.split(" ")[2]
                with open(src_directory + file_name + ".txt", 'r+', encoding='utf-8') as file:
                    data = file.read()
                    data_array = data.split(" ")
                    sequence = 0
                    for i in range(len(data_array)):

                        current_array = data_array[i:(i + (window_size))]

                        sentence_value = " ".join(current_array)
                        count = 0
                        for query_term in query_terms:
                            if query_term in current_array:
                                count +=1;
                        sentences[sequence] = [count,sentence_value]
                        sequence+=1

                        # sorting document frequency
                    sentences = OrderedDict(sorted(sentences.items(),key=lambda key_value: key_value[1], reverse=True))
                    count = 1
                    destination_file.write("\n" + file_name + "\n")
                    overlap_position = []
                    destination_file.write("<br>")
                    for sentence in sentences:
                        isOverlapping = False
                        for overlap in overlap_position:
                            if (abs(sentence - overlap)) <= window_size:
                                isOverlapping = True;
                        if not isOverlapping:
                            current_sentence = sentences.get(sentence)[1]
                            current_sent_list = current_sentence.split(" ")
                            for query in query_terms:
                                if query in current_sent_list:
                                    current_sentence = current_sentence\
                                        .replace("<b>" + query + "</b>",query).replace(query, "<b>" + query + "</b>")
                            destination_file.write("..." + current_sentence + "...")
                            overlap_position.append(sentence)
                            if(count == 3):
                                break;
                            count+=1
                    destination_file.write("\n")