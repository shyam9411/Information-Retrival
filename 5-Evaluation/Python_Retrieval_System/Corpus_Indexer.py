from Corpus_Parser import CorpusParser
import collections
import os

"""
Author: Shihao Wang
This class is used to generate Inverted Index, token number dictionary,
term frequency table, document frequency table for given corpus.

Constructor Template:
CorpusIndexer(stem_version)
stem_version: Boolean, to control the corpus we used, whether stemmed or not.
using_proximity: Boolean, true if you want to generate inverted index with position information.
"""


class CorpusIndexer:
    def __init__(self, stem_version, using_proximity):
        self.stem_version = stem_version
        # call CorpusParser to obtain the clean token list.
        self.clean_token_list = CorpusParser(stemming=stem_version).clean_token_list
        self.token_num_dict = {}
        self._number_of_tokens()
        self.inverted_index = {}
        self.using_proximity = using_proximity

    # private function
    # this function is used to construct token_num_dict.
    def _number_of_tokens(self):
        for i in range(len(self.clean_token_list)):
            self.token_num_dict[self.clean_token_list[i][0]] = len(self.clean_token_list[i][1])

    # store all dictionary objects in local folder "Inverted_Index"
    def dump_inverted_index(self):
        if self.using_proximity:
            self.inverted_index = self.sort_posting(self.build_inverted_index_with_proximity())
        else:
            self.inverted_index = self.sort_posting(self.build_inverted_index())
        self.save_all_dict()

    # This function generates the inverted index with position information
    # term1: [docID, tf, [p1, p2, ...]]
    def build_inverted_index_with_proximity(self):
        inverted_index = collections.defaultdict(list)
        for doc_index in range(len(self.clean_token_list)):
            for term_index in range(len(self.clean_token_list[doc_index][1])):
                term = self.clean_token_list[doc_index][1][term_index]
                if term in inverted_index:
                    existing = False
                    for posting in inverted_index[term]:
                        if posting[0] == self.clean_token_list[doc_index][0]:
                            posting[1] += 1
                            posting[2].append(term_index)
                            existing = True
                    if not existing:
                        inverted_index[term].append([self.clean_token_list[doc_index][0], 1, [term_index]])
                else:
                    inverted_index[term].append([self.clean_token_list[doc_index][0], 1, [term_index]])
        return inverted_index

    # This function generates the inverted index.
    # term1: [docID, tf]
    def build_inverted_index(self):
        inverted_index = collections.defaultdict(list)
        for doc_index in range(len(self.clean_token_list)):
            for term_index in range(len(self.clean_token_list[doc_index][1])):
                term = self.clean_token_list[doc_index][1][term_index]
                if term in inverted_index:
                    existing = False
                    for posting in inverted_index[term]:
                        if posting[0] == self.clean_token_list[doc_index][0]:
                            posting[1] += 1
                            existing = True
                    if not existing:
                        inverted_index[term].append([self.clean_token_list[doc_index][0], 1])
                else:
                    inverted_index[term].append([self.clean_token_list[doc_index][0], 1])
        return inverted_index

    # generate sorted term frequency table with the following format:
    # (term, tf), (term, tf)...
    def term_frequency_sort(self):
        tf_table = {}
        for key in self.inverted_index:
            tf_sum = 0
            for posting in self.inverted_index[key]:
                tf_sum += posting[1]
            tf_table[key] = tf_sum
        # sort all terms according to tf
        key_value_list = sorted(tf_table.items(), key=lambda tag: tag[1], reverse=True)
        tf_table = {}
        for item in key_value_list:
            tf_table[item[0]] = item[1]
        return tf_table

    # generate sorted document frequency table with the following format:
    # (term, docID, df), (term, docID, df)...
    def doc_frequency_sort(self):
        df_table = {}
        for key in self.inverted_index:
            df = len(self.inverted_index[key])
            doc_list = []
            for posting in self.inverted_index[key]:
                doc_list.append(posting[0])
            df_table[key] = [doc_list, df]
        # sort all terms lexicographically based on terms
        key_value_list = sorted(df_table.items(), key=lambda tag: tag[0])
        df_table = {}
        for item in key_value_list:
            df_table[item[0]] = item[1]
        return df_table

    # dumping all useful dictionary to local files.
    def save_all_dict(self):

        if self.stem_version:
            if self.using_proximity:
                self.save_dict(self.inverted_index, "stem_unigram_inverted_index_with_proximity")
            else:
                self.save_dict(self.inverted_index, "stem_unigram_inverted_index")
            self.save_dict(self.token_num_dict, "stem_token_num_dict")
            self.save_dict(self.term_frequency_sort(), "stem_term_frequency_table")
            self.save_dict(self.doc_frequency_sort(), "stem_doc_frequency_table")
        else:
            if self.using_proximity:
                self.save_dict(self.inverted_index, "unigram_inverted_index_with_proximity")
            else:
                self.save_dict(self.inverted_index, "unigram_inverted_index")
            self.save_dict(self.token_num_dict, "token_num_dict")
            self.save_dict(self.term_frequency_sort(), "term_frequency_table")
            self.save_dict(self.doc_frequency_sort(), "doc_frequency_table")

    # Helper function
    # GIVEN: an inverted index
    # RETURN: the same inverted index but term frequencies are sorted in inverted lists.
    @staticmethod
    def sort_posting(inverted_index):
        for key in inverted_index:
            inverted_index[key] = sorted(inverted_index[key], key=lambda posting: posting[1], reverse=True)
        return inverted_index

    # Helper function, use format control to save dictionary objects to .txt files
    @staticmethod
    def save_dict(content, filename):
        with open(os.getcwd() + "/Inverted_Index/" + filename + ".txt", 'w') as outfile:
            for key in content:
                outfile.write(str(key) + " : " + str(content[key]) + "\n")

if __name__ == '__main__':
    # Running Demo
    # Initialize a new InvertedIndex objects.
    ii1 = CorpusIndexer(False, True)
    ii1.inverted_index = ii1.build_inverted_index_with_proximity()
    # or use ii1.save_all_dict() to dump all dictionaries.
    ii1.save_dict(ii1.inverted_index, "unigram_inverted_index_with_proximity")