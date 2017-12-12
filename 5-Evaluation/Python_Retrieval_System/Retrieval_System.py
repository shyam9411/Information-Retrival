from Query_Parser import QueryParser
from BM25 import BM25
from TF_IDF import TfIdf
from Smoothing_QLM import SmoothingQLM
from Inverted_Index_Operation import InvertedIndexOperation
from Pseudo_Relevance_Feedback import PseudoRelevanceFeedback
import os

"""
Author: Shihao Wang
The class is the entrance of this retrieval system.
Constructor Template:
RetrievalSystem(query_file, TREC_format, stopping, retrieval_model, stemming_corpus=False,
                query_refinement=False)
Interpretation:
query_file: string, the name of a file contains all queries
TREC_format: boolean, whether the query file is organized as TREC format
stopping: boolean , whether using stopping
retrieval_model: string, the name of rm user wants to use to do this searching.
stemming_corpus: boolean, true iff the stemming corpus is used.
query_refinement: boolean, true iff query refinement is used.
"""
model_lib = {'BM25': BM25, 'tf-idf': TfIdf, 'SmoothingQLM': SmoothingQLM}


class RetrievalSystem:
    def __init__(self, query_file, TREC_format, stopping, retrieval_model, stemming_corpus=False,
                 query_refinement=False):
        self.query_list = QueryParser(query_file, stopping=stopping, TREC_format=TREC_format).clean_query_list
        self.retrieval_model = retrieval_model
        self.stemming_corpus = stemming_corpus
        self.query_refinement = query_refinement
        self.top_results = 100
        self.system_name = self.retrieval_model
        if stopping:
            self.system_name += "_Stopping"
        if stemming_corpus:
            self.system_name += "_Stemming"
        self.system_name += "_Unigram_Case-folded"
        if self.query_refinement:
            self.system_name += "_QueryRefine"

    def retrieval_process(self):
        for query in self.query_list:
            query_id = query[0]
            if self.query_refinement:
                query_terms = PseudoRelevanceFeedback(query[1], 10, 10, 'dice', self.system_name[:-12]).extend_query
            else:
                query_terms = query[1]
            # filter all related documents with given query
            candidate_doc = InvertedIndexOperation.find_candidate_doc(query_terms)
            score_list = {}
            rm = model_lib.get(self.retrieval_model)((query_id, query_terms), self.stemming_corpus)
            for doc in candidate_doc:
                # reset retrieval model for another doc
                rm.set_doc(doc)
                score_list[InvertedIndexOperation.to_doc_name(doc)] = rm.get_score()
                print(InvertedIndexOperation.to_doc_name(doc) + "'s score is "
                      + str(score_list[InvertedIndexOperation.to_doc_name(doc)]))
            rank_score_list = sorted(score_list.items(), key=lambda x: x[1], reverse=True)
            # output under format control
            with open(os.getcwd() + '/Results/' + self.system_name + '.txt', 'a') as outfile:
                for i in range(self.top_results):
                    outfile.write(str(query_id) + " " +
                                  "Q0" + " " + str(rank_score_list[i][0]) +
                                  " " + str(i + 1) + " " + str(rank_score_list[i][1]) +
                                  " " + self.system_name + "\n")

# """
# main function.
# User do the searching by creating a RetrievalSystem object
# and call its retrieval_process function.
# """
if __name__ == '__main__':
    rs = RetrievalSystem("cacm.query.txt", TREC_format=True, stopping=False, retrieval_model='BM25',
                         stemming_corpus=False, query_refinement=True)
    rs.retrieval_process()
