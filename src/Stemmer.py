import os
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

