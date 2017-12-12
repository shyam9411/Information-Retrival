import math
from Inverted_Index_Operation import InvertedIndexOperation

"""
Author: Shihao Wang
# This class realize the retrieval model BM25
# and use it to search wiki pages according to the user query
# Constructor Template:
#     bm = BM25(query, stemming_corpus=False)
# Interpretation:
#     query: (int, dict), the keys are terms in given query
#            and values are term frequency in given query
#     stemming_corpus: Boolean, True iff the stemmed corpus is used.
"""


class BM25:
    def __init__(self, query, stemming_corpus=False):
        # parameters in BM25 model
        self.query = query[1]
        self.query_id = query[0]
        self.b = 0.75
        self.k1 = 1.2
        self.k2 = 100
        self.stemming_corpus = stemming_corpus
        if stemming_corpus:
            self.N = InvertedIndexOperation.get_stem_corpus_size()
            self.avdl = InvertedIndexOperation.stem_get_average_doc_length()
            self.df_table = InvertedIndexOperation.stem_get_df()
            self.inverted_index = InvertedIndexOperation.stem_get_inverted_index()
        else:
            self.N = InvertedIndexOperation.get_corpus_size()
            self.avdl = InvertedIndexOperation.get_average_doc_length()
            self.df_table = InvertedIndexOperation.get_df()
            self.inverted_index = InvertedIndexOperation.get_inverted_index()
        self.relevance = InvertedIndexOperation.load_relevance_info()
        self.R = len(self.relevance[self.query_id])
        # these three parameters are related with documents
        # use function set_doc to initialize them
        self.doc_id = -1
        self.dl = -1
        self.K = -1

    # This function returns the score of given document for given query
    def get_score(self):
        score = 0
        for term in self.query:
            # handle with unseen terms
            if term not in self.inverted_index.keys():
                continue
            df = self.df_table[term][1]
            tf_i = self.get_tf_i(term, self.doc_id)
            qf_i = self.query[term]
            r_i = self.get_r_i(term)
            if tf_i:
                f = (r_i + 0.5)*(self.N - df - self.R + r_i + 0.5) / ((self.R - r_i + 0.5) * (df - r_i + 0.5))
                score += math.log(f) * (self.k1+1) * tf_i * (self.k2 + 1) * qf_i / ((self.k2 + qf_i) * (self.K + tf_i))
        return score

    # This function returns the number of relevant documents containing given term
    def get_r_i(self, term):
        relevance_docs = self.relevance[self.query_id]
        count = 0
        for doc_id in relevance_docs:
            for posting in self.inverted_index[term]:
                if posting[0] == doc_id:
                    count += 1
        return count

    # This function returns the term frequency of given term in given document
    def get_tf_i(self, term, doc_id):
        for item in self.inverted_index[term]:
            if item[0] == doc_id:
                return item[1]
        return 0

    # This function returns the K value, which is a parameter in BM25
    def get_k(self):
        return self.k1 * ((1 - self.b) + self.b * self.dl / self.avdl)

    # This function is used to initialize document-related parameters in BM25 model
    def set_doc(self, new_doc_id):
        self.doc_id = new_doc_id
        if self.stemming_corpus:
            self.dl = InvertedIndexOperation.stem_get_doc_length(new_doc_id)
        else:
            self.dl = InvertedIndexOperation.get_doc_length(new_doc_id)
        self.K = self.get_k()

