import os
from bs4 import BeautifulSoup
import re

# It gets a output folder in current source path.
current_directory = os.getcwd()

def generate_corpus(src_directory_path,dst_directory_path,punctuation,case_folding):

    # if source directory does not exist, then create one
    if not os.path.exists(src_directory_path):
        os.mkdir(src_directory_path)

    # if destination directory does not exist, then create one
    if not os.path.exists(dst_directory_path):
        os.mkdir(dst_directory_path)

    # reading all the files names in a list
    for directory in os.walk(src_directory_path):
        for file in directory:
            file_names = file
    count = 1

    # parsing each file from the directory
    for file in file_names:
        processed_text = process_text(src_directory_path + file)

        # processing text on punctuation
        if(punctuation):
            processed_text = handle_punctuation(processed_text)

        # processing text by doing case folding
        if(case_folding):
            processed_text = handle_case_folding(processed_text)

        file_name = str(file).split(".")[0]
        with open(dst_directory_path + file_name + ".txt", 'w', encoding='utf-8') as f:
            f.write(processed_text)
        print ("Files Processed - "+str(count) + " FileName - " + file)
        count+=1
    print("done generating corpus")

def process_text(file_name):
    with open(file_name, 'r+', encoding='utf-8') as f:
        # parsing html file using beautiful soup
        soup = BeautifulSoup(f.read(), 'html.parser')
        processed_text = ""

        # extracting contents only from paragraph and header tags
        for row in soup.find_all(['p','pre', 'h1', 'h2', 'h3', 'h4','h5', 'h6']):
            # Extraction of the all the useful text and putting storing it
            processed_text = processed_text + '  '.join(row.stripped_strings)

        # removing line separators
        processed_text = str(processed_text).replace('\r\n',' ')
        processed_text = str(processed_text).replace('\n', ' ')
        processed_text = str(processed_text).replace('\t', ' ')

        # Removing all the url's from the text with the help of regular expression
        processed_text = re.sub(r' http\S+', '', processed_text)

    return processed_text

# handles case folding on processed text
def handle_case_folding(processed_text):
    processed_text = str(processed_text).lower()
    return processed_text

# handles punctuation on processed text
def handle_punctuation(processed_text):
    processed_text_after = ""
    punctuation_list_text = [',','.','!','#','$','%','^','&','*','(',')','_','+','[',']',';','\'','/','\\','{','}',':','"','<','>','?','=','`','~', '-']
    punctuation_list_digits =['!','#','$','%','^','&','*','(',')','_','+','[',']',';','\'','/','\\','{','}',':','"','<','>','?','=']

    terms_list = processed_text.split()
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

    return processed_text_after