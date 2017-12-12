import os
from nltk.tokenize import word_tokenize

START_SIGNAL = '#'

"""
Author: Shihao Wang
This class realize the function to transfer the corpus into structured clean tokens.
It supports two parsers for both .html and .txt, which are the file formats in given CACM dataset.

"""


class CorpusParser:
    def __init__(self, stemming=False, case_folding=True, punctuation=True):
        self.stemming = stemming
        self.case_folding = case_folding
        self.punctuation = punctuation
        # The final token list we need for further using, with following structure:
        # [(docID, [doc_terms]) ... ]
        self.clean_token_list = []
        if stemming:
            self.txt_parser()
        else:
            self.html_parser()

    def html_parser(self):
        files = os.listdir(os.getcwd() + "/Corpus/cacm/")
        tag_list = ["<html>", "<pre>", "</html>", "</pre>"]
        for file in files:
            with open(os.getcwd() + "/Corpus/cacm/" + file, "r") as f:
                text = ""
                for line in f.readlines():
                    line = line[:-1]
                    if line not in tag_list and not self.is_digits_line(line):
                        text += line
                        text += " "
                if self.case_folding:
                    text = text.lower()
                token_list = word_tokenize(text)
                if self.punctuation:
                    token_list = [item for item in filter(self.is_not_useless_punctuation, token_list)]
                self.clean_token_list.append((int(file[5:9]), token_list))
        self.clean_token_list = sorted(self.clean_token_list, key=lambda x: x[0])

    def txt_parser(self):
        with open(os.getcwd() + "/Corpus/cacm_stem.txt", "r") as f:
            text = f.read()
            token_list = text.replace("\n", " ").split("#")[1:]
            for i in range(len(token_list)):
                token_list[i] = token_list[i].split(" ")
                if "pm" in token_list[i]:
                    end_index = token_list[i].index("pm") + 1
                    token_list[i] = token_list[i][:end_index]
                elif "am" in token_list[i]:
                    end_index = token_list[i].index("am") + 1
                    token_list[i] = token_list[i][:end_index]
                token_list[i] = [item for item in filter(self.is_not_null, token_list[i])]
                self.clean_token_list.append((int(token_list[i][0]), token_list[i][1:]))
            self.clean_token_list = sorted(self.clean_token_list, key=lambda x: x[0])

    # Helper function to remove useless punctuations
    # GIVEN: StringList, a token list which just is processed by NLTK's word_tokenizer
    # RETURN: StringList, clean token list which remove the useless parts
    @staticmethod
    def is_not_useless_punctuation(term):
        useless_list = [',', '.', ':', ';', '?', '(', ')', '[', ']',
                        '&', '!', '*', '@', '#', '$', '%', '"', '``',
                        "''", "'", '–', '—', '’', '′', '，']
        return term not in useless_list

    # Helper function to judge whether a line contains only spaces and digits.
    # GIVEN: String, a text of certain line.
    # RETURN: True iff it is a digits line.
    @staticmethod
    def is_digits_line(line):
        for i in line:
            if i != '\t' and not i.isdigit():
                return False
        return True

    # Helper function to remove all null characters
    @staticmethod
    def is_not_null(term):
        return term != ''
