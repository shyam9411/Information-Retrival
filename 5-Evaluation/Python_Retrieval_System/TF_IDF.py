import math
from Inverted_Index_Operation import InvertedIndexOperation

"""
Author: Shihao Wang
This class realize a simple tf-idf model, summing up the score of <term, query>
Constructor Template:
TfIdf(query, stemming_corpus=False)
Interpretation:
query: dict
stemming_corpus: boolean, true iff the stemming corpus is used.
"""


class TfIdf:
    def __init__(self, query, stemming_corpus=False):
        self.query = query[1]
        self.query_id = query[0]
        self.stemming_corpus = stemming_corpus
        if stemming_corpus:
            self.N = InvertedIndexOperation.get_stem_corpus_size()
            self.df_table = InvertedIndexOperation.stem_get_df()
            self.inverted_index = InvertedIndexOperation.stem_get_inverted_index()
        else:
            self.N = InvertedIndexOperation.get_corpus_size()
            self.df_table = InvertedIndexOperation.get_df()
            self.inverted_index = InvertedIndexOperation.get_inverted_index()

        self.dl = -1
        self.doc_id = -1

    def get_score(self):
        score = 0
        for term in self.query:
            # handle with unseen terms
            if term not in self.inverted_index.keys():
                continue
            df = self.df_table[term][1]
            tf_i = self.get_tf_i(term, self.doc_id)
            score += (tf_i/self.dl) * (math.log(self.N/df))
        return score

    def get_tf_i(self, term, doc_id):
        for item in self.inverted_index[term]:
            if item[0] == doc_id:
                return item[1]
        return 0

    def set_doc(self, new_doc_id):
        self.doc_id = new_doc_id
        if self.stemming_corpus:
            self.dl = InvertedIndexOperation.stem_get_doc_length(new_doc_id)
        else:
            self.dl = InvertedIndexOperation.get_doc_length(new_doc_id)