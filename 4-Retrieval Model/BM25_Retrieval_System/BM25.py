import math
from Inverted_Index_Operation import InvertedIndexOperation
from Query_Parser import QueryParser

"""
# This class realize the retrieval model BM25
# and use it to search wiki pages according to the user query
# Constructor Template:
#     bm = BM25(query, doc)
# Interpretation:
#     query: dict, the keys are terms in given query
#            and values are term frequency in given query
#     doc: the id of document to be retrieved.
"""


class BM25:
    def __init__(self, query):
        # parameters in BM25 model
        self.query = query
        self.b = 0.75
        self.k1 = 1.2
        self.k2 = 100
        self.N = 1000
        self.avdl = iio.get_average_doc_length()
        self.tf_table = iio.get_tf()
        self.df_table = iio.get_df()
        # these three parameters are related with documents
        # use function set_doc to initialize them
        self.doc_id = -1
        self.dl = -1
        self.K = -1

    # This function returns the score of given document for given query
    def get_score(self):
        score = 0
        for term in self.query:
            df = self.df_table[term][1]
            tf_i = self.get_tf_i(term, self.doc_id)
            qf_i = self.query[term]
            if tf_i:
                f = ((self.k1+1) * tf_i * (self.k2 + 1) * qf_i * (self.N - df + 0.5))\
                    / ((df + 0.5) * (self.k2 + qf_i) * (self.K + tf_i))
                score += math.log(f)
        return score

    # This function returns the term frequency of given term in given document
    def get_tf_i(self, term, doc_id):
        for item in self.tf_table[term]:
            if item[0] == doc_id:
                return item[1]
        return 0

    # This function returns the K value, which is a parameter in BM25
    def get_k(self):
        return self.k1 * ((1 - self.b) + self.b * self.dl / self.avdl)

    # This function is used to initialize document-related parameters in BM25 model
    def set_doc(self, new_doc_id):
        self.doc_id = new_doc_id
        self.dl = iio.get_doc_length(new_doc_id)
        self.K = self.get_k()

"""
main function.
Input: a query with string type that user input from console
Where: if user inputs 'q' as a query, then the main function quit.
Output: top 100 results with format control
"""
if __name__ == '__main__':
    iio = InvertedIndexOperation()
    top_results = 100
    query_id = 0
    # retrieval program terminals until a 'q' is the input.
    print("Welcome to BM25-based Information Search Engine, please input your query:")
    q = input()
    while q != 'q':
        query_id += 1
        q = QueryParser(q)
        # filter all related documents with given query
        candidate_doc = iio.find_candidate_doc(q.query)
        score_list = {}
        bm = BM25(q.query)
        for doc in candidate_doc:
            # reset BM25 object for another doc
            bm.set_doc(doc)
            score_list[iio.to_doc_name(doc)] = bm.get_score()
            print(iio.to_doc_name(doc) + "'s score is "+str(score_list[iio.to_doc_name(doc)]))
        rank_list = sorted(score_list.items(), key=lambda x: x[1], reverse=True)
        # output under format control
        for i in range(top_results):
            print(str(query_id)+" "+"Q0"+" "+str(
                rank_list[i][0])+" "+str(i+1)+" "+str(rank_list[i][1])+" "+"BM25_Unigram_Stopping_Case-folded")
        print("Welcome to BM25-based Information Search Engine, please input your query:")
        q = input()
