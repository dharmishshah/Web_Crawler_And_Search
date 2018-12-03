import os
import re
from bs4 import BeautifulSoup

# It gets a output folder in current source path.

stem_text_file = "./test_collection/cacm_stem.txt"

dst_directory = os.getcwd()+"/output_files/clean_corpus_with_stemming/"


def generate_corpus_from_stem_file():

    # if destination directory does not exist, then create one
    if not os.path.exists(dst_directory):
        os.mkdir(dst_directory)

    with open(stem_text_file, 'r+', encoding='utf-8') as f:
        processed_text = f.read()
        files = processed_text.split("#")

    updated_files = []
    for j in files:
        if j:
            updated_files.append(re.sub("m[\s\d]+#", "m", j).replace("\n", "").lstrip('0123456789.- '))

    count = 1
    for file in updated_files:
        with open(dst_directory + "/" + "CACM-" + str(count).zfill(4) + ".txt", 'w', encoding='utf-8') as f:
            f.write(file)
        print("Files Processed - " + str(count) )
        count += 1