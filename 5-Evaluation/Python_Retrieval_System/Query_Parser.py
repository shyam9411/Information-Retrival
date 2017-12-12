import os
import copy
from Corpus_Parser import CorpusParser
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
from Inverted_Index_Operation import InvertedIndexOperation

"""
Author: Shihao Wang
This class is used to build data structure of the query.
The structure of a query would be:
(queryID, {term:tf, term:tf ...})
It supports two text format (TREC and simple text format) like the files provides.

"""


class QueryParser:
    def __init__(self, filename, TREC_format, stopping, case_folding=True, punctuation=True):
        self.filename = filename
        self.stopping = stopping
        self.case_folding = case_folding
        self.punctuation = punctuation
        self.clean_query_list = []
        if TREC_format:
            self.TREC_parser()
        else:
            self.simple_parser()
        if stopping:
            self.remove_stopping_words()
        self.query_with_proximity = copy.deepcopy(self.clean_query_list)
        for query in self.clean_query_list:
            query_dict = defaultdict(int)
            for term in query[1]:
                query_dict[term] += 1
            query[1] = query_dict

    def TREC_parser(self):
        with open(os.getcwd() + "/Query/" + self.filename, "r") as f:
            text = f.read()
            token_list = text.replace("\n", " ").replace("</DOC>", "").split("<DOC>")[1:]
            for i in range(len(token_list)):
                token_list[i] = token_list[i].replace("<DOCNO>", "").split("</DOCNO>")
                query_index = int(token_list[i][0])
                token_list[i] = token_list[i][1]
                if self.case_folding:
                    token_list[i] = token_list[i].lower()
                token_list[i] = word_tokenize(token_list[i])
                token_list[i] = [item for item in filter(CorpusParser.is_not_null, token_list[i])]
                if self.punctuation:
                    token_list[i] = [item for item in filter(CorpusParser.is_not_useless_punctuation, token_list[i])]
                self.clean_query_list.append([int(query_index), token_list[i]])
                # code for transfer TREC queries into simple text queries.
                # s = " ".join(token_list[i])
                # with open(os.getcwd() + '/Query/processed.cacm.query.txt', 'w') as outfile:
                #     outfile.write(s + '\n')

    def simple_parser(self):
        with open(os.getcwd() + "/Query/" + self.filename, "r") as f:
            index = 1
            for line in f.readlines():
                if self.case_folding:
                    line = line.lower()
                token_list = word_tokenize(line)
                token_list = [item for item in filter(CorpusParser.is_not_null, token_list)]
                if self.punctuation:
                    token_list = [item for item in filter(CorpusParser.is_not_useless_punctuation, token_list)]
                self.clean_query_list.append([index, token_list])
                index += 1

    # This function removes all stopping word in common_words.txt from query text.
    def remove_stopping_words(self):
        common_words_list = InvertedIndexOperation.get_stopping_words()
        for i in range(len(self.clean_query_list)):
            tmp_token_list = []
            for term in self.clean_query_list[i][1]:
                if term not in common_words_list:
                    tmp_token_list.append(term)
            self.clean_query_list[i][1] = tmp_token_list

    def build_proximity_query(self):
        for query in self.query_with_proximity:
            bi_gram = nltk.ngrams(query[1], 2)
            query.append(list(bi_gram))

if __name__ == '__main__':
    # Runnable Demo
    # To show the data
    qp = QueryParser("cacm.query.txt", stopping=False, TREC_format=True)
    qp.build_proximity_query()
    print(qp.query_with_proximity)