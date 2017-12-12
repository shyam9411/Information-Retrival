import os
from collections import defaultdict

"""
Author: Shihao Wang
A utility class for operating inverted indexes and other metadata.

"""


class InvertedIndexOperation:
    # The function is used to recover dictionary dumped
    # by the function _save_dict
    # GIVEN: a file name under the folder /Inverted_Index/
    # RETURN: The dictionary object made of the loaded data.
    @staticmethod
    def load_dict(filename):
        load_dict = {}
        with open(os.getcwd() + "/Inverted_Index/" + filename) as f:
            for line in f.readlines():
                key_value_pair = line.strip("\n").split(" : ")
                load_dict[key_value_pair[0]] = eval(key_value_pair[1])
        return load_dict

    # This function loads token number dictionary
    @staticmethod
    def load_token_dict(filename):
        load_dict = {}
        with open(os.getcwd() + "/Inverted_Index/" + filename) as f:
            for line in f.readlines():
                key_value_pair = line.strip("\n").split(" : ")
                load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        return load_dict

    # This function load the relevance information under the folder /Relevance/
    @staticmethod
    def load_relevance_info():
        load_dict = defaultdict(list)
        with open(os.getcwd() + "/Relevance/cacm.rel.txt") as f:
            for line in f.readlines():
                tokens = line.split(" ")
                load_dict[int(tokens[0])].append(int(tokens[2][5:9]))
        return load_dict

    # This function returns the document frequency table
    @staticmethod
    def get_df():
        return InvertedIndexOperation.load_dict("doc_frequency_table.txt")

    @staticmethod
    def stem_get_df():
        return InvertedIndexOperation.load_dict("stem_doc_frequency_table.txt")

    # This function returns the term frequency table
    @staticmethod
    def get_tf():
        return InvertedIndexOperation.load_dict("term_frequency_table.txt")

    # This function returns the term frequency table of stemming corpus
    @staticmethod
    def stem_get_tf():
        return InvertedIndexOperation.load_dict("stem_term_frequency_table.txt")

    # This function returns the token number dictionary
    @staticmethod
    def get_token_num():
        return InvertedIndexOperation.load_token_dict("token_num_dict.txt")

    # This function returns the token number dictionary of stemming corpus
    @staticmethod
    def stem_get_token_num():
        return InvertedIndexOperation.load_token_dict("stem_token_num_dict.txt")

    # This function returns the inverted index
    @staticmethod
    def get_inverted_index():
        return InvertedIndexOperation.load_dict("unigram_inverted_index.txt")

    # This function returns the inverted index of stemming corpus
    @staticmethod
    def stem_get_inverted_index():
        return InvertedIndexOperation.load_dict("stem_unigram_inverted_index.txt")

    # This function returns the inverted index with position information
    @staticmethod
    def get_inverted_index_with_proximity():
        return InvertedIndexOperation.load_dict("unigram_inverted_index_with_proximity.txt")

    @staticmethod
    # This function returns the document length of given document
    def get_doc_length(doc_id):
        token_dict = InvertedIndexOperation.get_token_num()
        return token_dict[doc_id]

    # This function returns the document length of given document in stemming corpus
    @staticmethod
    def stem_get_doc_length(doc_id):
        token_dict = InvertedIndexOperation.stem_get_token_num()
        return token_dict[doc_id]

    @staticmethod
    # This function returns the average document length of the corpus
    def get_average_doc_length():
        token_dict = InvertedIndexOperation.get_token_num()
        token_sum = 0
        for key in token_dict:
            token_sum += token_dict[key]
        return float(token_sum)/len(token_dict)

    # This function returns the average document length of the stemming corpus
    @staticmethod
    def stem_get_average_doc_length():
        token_dict = InvertedIndexOperation.stem_get_token_num()
        token_sum = 0
        for key in token_dict:
            token_sum += token_dict[key]
        return float(token_sum)/len(token_dict)

    @staticmethod
    # This function returns the a list of documents,
    # each of which contains at least one overlapping term with the query
    def find_candidate_doc(query):
        inverted_index = InvertedIndexOperation.get_inverted_index()
        candidate_doc = set()
        for term in query:
            if term in inverted_index:
                for t in inverted_index[term]:
                    candidate_doc.add(t[0])
        return list(candidate_doc)

    # Find candidate documents from stemming corpus
    @staticmethod
    def stem_find_candidate_doc(query):
        inverted_index = InvertedIndexOperation.stem_get_inverted_index()
        candidate_doc = set()
        for term in query:
            if term in inverted_index:
                for t in inverted_index[term]:
                    candidate_doc.add(t[0])
        return list(candidate_doc)

    # This function returns the term occurrence of the whole corpus
    @staticmethod
    def get_corpus_size():
        return len(InvertedIndexOperation.get_token_num())

    # This function returns the term occurrence of the whole stemming corpus
    @staticmethod
    def get_stem_corpus_size():
        return len(InvertedIndexOperation.stem_get_token_num())

    @staticmethod
    # This function returns the name of given document according to doc_id
    def to_doc_name(doc_id):
        left_zero = 4 - len(str(doc_id))
        pre = ""
        for i in range(left_zero):
            pre += "0"
        return "CACM-" + pre + str(doc_id)

    # This function returns the list of relevant documents with the given query
    @staticmethod
    def get_relevance_docs(query_id):
        relevance_info = InvertedIndexOperation.load_relevance_info()
        if query_id in relevance_info:
            return relevance_info[query_id]

    # This function returns all stopping words from common_words.txt
    @staticmethod
    def get_stopping_words():
        with open(os.getcwd() + "/Query/common_words.txt", "r") as f:
            text = f.read()
            common_words_list = text.split('\n')[:-1]
        return common_words_list
