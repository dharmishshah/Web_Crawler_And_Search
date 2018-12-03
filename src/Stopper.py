import os
from bs4 import BeautifulSoup

# It gets a output folder in current source path.

common_words_file = "./test_collection/common_words"

src_directory = "./output_files/clean_corpus/"

dst_directory = os.getcwd()+"/output_files/clean_corpus_with_no_stopwords/"


def generate_corpus_without_stop_words():

    # if destination directory does not exist, then create one
    if not os.path.exists(dst_directory):
        os.mkdir(dst_directory)

    file_names=[]
    # reading all the files names in a list
    for directory in os.walk(src_directory):
        for file in directory:
            file_names = file
    count = 1

    stop_list = get_stop_words()

    # parsing each file from the directory
    for file in file_names:
        with open(src_directory+file, 'r+', encoding='utf-8') as f:
            processed_text = f.read()

            for stopword in stop_list:
                if stopword in processed_text:
                    processed_text = processed_text.replace(stopword,"")

            file_name = str(file).split(".")[0]
            with open(dst_directory + file_name + ".txt", 'w', encoding='utf-8') as f:
                f.write(processed_text)
            print("Files Processed - " + str(count) + " FileName - " + file)
            count += 1


def get_stop_words():
    stop_list = []
    with open(common_words_file, 'r+', encoding='utf-8') as f:
        common_words_text = f.read()
        stop_list = common_words_text.split("\n")
        
    return stop_list

#generate_corpus_without_stop_words()