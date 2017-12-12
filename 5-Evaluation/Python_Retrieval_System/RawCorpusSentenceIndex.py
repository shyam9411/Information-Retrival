import os
from bs4 import BeautifulSoup
from nltk import tokenize

"""
Author: Kartik Dave
Date: 12/5/2017

Program to create index of the raw documents, with identifying the sentences

The input to the program will be the following location of the directory of:
a. Location of the directory where the raw documents are stored

"""


class RawCorpusSentenceIndex:
    documentStoreIndex = {}
    __raw_docs_dir_loc = os.getcwd() + "/Corpus/"

    # Function: __init__
    #
    # Parameters:
    # raw_docs_dir_loc => Location of the directory where the raw documents are stored
    #
    # Effect: Constructor of the class, for getting the file location of the required files
    def __init__(self, raw_docs_dir_loc):
        self.__raw_docs_dir_loc += raw_docs_dir_loc

    # Function: raw_corpus_index_generation
    #
    # Effect: Construction of a file with index for the raw documents.
    # The sentences in the documents are identified and stored
    def raw_corpus_index_generation(self):
        raw_doc_files = []
        # For getting all the names of the file in the directory passed
        for dir_parsing in os.walk(self.__raw_docs_dir_loc):
            for file in dir_parsing:
                raw_doc_files = file
        # For all the raw documents
        for file in raw_doc_files:
            soup = BeautifulSoup(open(self.__raw_docs_dir_loc + file), "html.parser")
            # Taking all the pre tag, as the structure of the html corpus passed
            tuple_test = ()
            for row in soup.find_all('pre'):
                all_text = [x.replace('\n', ' ') for x in row.get_text().split('\n\n')]
                all_text = [x for x in all_text if x]

                temp = []
                for i in range(1, len(all_text)):
                    # Identification of the sentences in the text
                    content_sentence = tokenize.sent_tokenize(all_text[i])
                    for sentence in content_sentence:
                        temp.append(sentence)
                # Tuple with the title of the page
                # and list of all the sentences
                tuple_test = (all_text[0], temp)
            self.documentStoreIndex[file[:-5]] = tuple_test
        # For writing the index inside the file
        with open(os.getcwd() + '/Inverted_Index/docs_sentence_index.txt', 'w', encoding='utf-8') as f:
            f.write(str(self.documentStoreIndex))


# Note :
# the location provided should not include single backslash(\)
# it should either have a common slash(/) or double backslash(//)
#
# Demo Examples:
index_generation = RawCorpusSentenceIndex('cacm/')  # => Please provide the location to the class constructor
index_generation.raw_corpus_index_generation()
