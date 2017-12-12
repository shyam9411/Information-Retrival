import os

"""
# A utility class for existing inverted indexes while have formed files
# This class are in charge of:
# 1.load inverted indexes, tf table, df table, token number table
# and id-doc reflection dictionary.
# 2.Compute related parameters that will be useful in BM25 model.
# Constructor template:
# iio = InvertedIndexOperation()
"""


class InvertedIndexOperation:
    # The function is used to recover dictionary dumped
    # by function _save_dict
    # GIVEN: PosInt, n has different values, representing different dictionaries to be loaded.
    #        See comment below.
    @staticmethod
    def load_dict(n):
        load_dict = {}
        # load unigram inverted index
        if n == 1:
            with open(os.getcwd() + "/Inverted_Index/unigram_inverted_index.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        # load unigram term frequency table
        elif n == 2:
            with open(os.getcwd() + "/Inverted_Index/unigram_term_frequency_table.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        # load unigram document frequency table
        elif n == 3:
            with open(os.getcwd() + "/Inverted_Index/unigram_doc_frequency_table.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        # load the dictionary with token numbers of each document.
        elif n == 4:
            with open(os.getcwd() + "/Inverted_Index/token_num_dict.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        # load the docID - docName reflection dictionary.
        elif n == 5:
            with open(os.getcwd() + "/Inverted_Index/id_doc_table.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = key_value_pair[1]
        return load_dict

    # This function returns the document frequency table
    def get_df(self):
        return self.load_dict(3)

    # This function returns the term frequency table
    def get_tf(self):
        return self.load_dict(1)

    # This function returns the document length of given doc
    def get_doc_length(self, doc_id):
        token_dict = self.load_dict(4)
        return token_dict[doc_id][0]

    # This function returns the average document length of the corpus
    def get_average_doc_length(self):
        token_dict = self.load_dict(4)
        token_sum = 0
        for key in token_dict:
            token_sum += token_dict[key][0]
        return float(token_sum)/1000

    # This function returns the a list which contains all documents
    # with at least one term in given query.
    def find_candidate_doc(self, query):
        inverted_index = self.load_dict(1)
        candidate_doc = set()
        for term in query:
            if term in inverted_index:
                for t in inverted_index[term]:
                    candidate_doc.add(t[0])
        return list(candidate_doc)

    # This function returns the name of given document according to doc_id
    def to_doc_name(self, doc_id):
        id_name = self.load_dict(5)
        return id_name[doc_id]
