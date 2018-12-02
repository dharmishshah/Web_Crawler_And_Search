import os
from bs4 import BeautifulSoup

# It gets a output folder in current source path.
current_directory = os.getcwd()

common_words_file = "../test-collection/common_words"

src_directory = "/cleanCorpus"

dst_directory = "/cleanCorpusWithNoStopwords"


def generate_file_without_stopwords():

    # if destination directory does not exist, then create one
    if not os.path.exists(dst_directory):
        os.mkdir(dst_directory)

    # reading all the files names in a list
    for directory in os.walk(current_directory):
        for file in directory:
            file_names = file
    count = 1

    stopList = getStopWords()

    # parsing each file from the directory
    for file in file_names:
        with open(file, 'r+', encoding='utf-8') as f:
            processed_text = f.read()

            for stopword in stopList:
                if stopword in processed_text:
                    processed_text = processed_text.replace(stopword,"")

            fileName = str(file).split(".")[0]
            with open(dst_directory + fileName + ".txt", 'w', encoding='utf-8') as f:
                f.write(processed_text)
            print("Files Processed - " + str(count) + " FileName - " + file)
            count += 1


def getStopWords():
    stopList = []
    with open(common_words_file, 'r+', encoding='utf-8') as f:
        common_words_text = f.read()
        stopList = common_words_text.split("\n")
        return stopList
