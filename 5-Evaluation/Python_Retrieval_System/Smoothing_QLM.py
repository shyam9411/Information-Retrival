import math
from Inverted_Index_Operation import InvertedIndexOperation

"""
Author: Shihao Wang
This class realize a smoothing query likelihood model using J-M smoothing
Constructor Template:
SmoothingQLM(query, stemming_corpus=False)
Interpretation:
query: dict
stemming_corpus: boolean, true iff the stemming corpus is used.
"""


class SmoothingQLM:
    def __init__(self, query, stemming_corpus=False):
        self.query = query[1]
        self.query_id = query[0]
        self.stemming_corpus = stemming_corpus
        self.smoothing_factor = 0.35
        if self.stemming_corpus:
            self.token_dict = InvertedIndexOperation.stem_get_token_num()
            self.tf_table = InvertedIndexOperation.stem_get_tf()
            self.inverted_index = InvertedIndexOperation.stem_get_inverted_index()
        else:
            self.token_dict = InvertedIndexOperation.get_token_num()
            self.tf_table = InvertedIndexOperation.get_tf()
            self.inverted_index = InvertedIndexOperation.get_inverted_index()
        self.corpus_term_occurrence = self.get_corpus_term_occurrence()
        self.dl = -1
        self.doc_id = -1

    def get_score(self):
        score = 0
        for term in self.query:
            # handle with unseen terms
            if term not in self.inverted_index.keys():
                continue
            tf_i = self.get_tf_i(term, self.doc_id)
            c_i = self.tf_table[term]
            score += math.log((1-self.smoothing_factor) * tf_i / self.dl +
                              self.smoothing_factor * c_i / self.corpus_term_occurrence)
        return score

    def get_tf_i(self, term, doc_id):
        for item in self.inverted_index[term]:
            if item[0] == doc_id:
                return item[1]
        return 0

    def get_corpus_term_occurrence(self):
        term_sum = 0
        for doc in self.token_dict:
            term_sum += self.token_dict[doc]
        return term_sum

    def set_doc(self, new_doc_id):
        self.doc_id = new_doc_id
        if self.stemming_corpus:
            self.dl = InvertedIndexOperation.stem_get_doc_length(new_doc_id)
        else:
            self.dl = InvertedIndexOperation.get_doc_length(new_doc_id)
