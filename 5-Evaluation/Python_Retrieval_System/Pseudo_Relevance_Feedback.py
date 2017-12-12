from Corpus_Parser import CorpusParser
import os
from Term_Association import dice_coefficient, mutual_information
from Inverted_Index_Operation import InvertedIndexOperation

"""
Author: Shihao Wang
This class transfers the original query into extended query with more highly relevant terms
extracted from relevant documents.
Constructor Template:
PseudoRelevanceFeedback(query, top_doc_num, top_term_num, term_association, system_name)
query: dict
top_doc_num: int, the number restriction of the relevant document
top_term_num: int, the number restriction of the term to be used in query expansion
term_association: string,  the name of measure, the dictionary is 'association_measure'
system_name: string, the system name which user do query refinement for

"""
association_measure = {"dice": dice_coefficient, "mim": mutual_information}


class PseudoRelevanceFeedback:
    def __init__(self, query, top_doc_num, top_term_num, term_association, system_name):
        self.extend_query = query.copy()
        clean_token_list = CorpusParser().clean_token_list
        top_rank_docs = []
        # read top ranking results from I/O
        with open(os.getcwd() + '/Results/' + system_name + '.txt', 'r') as outfile:
            for i in range(top_doc_num):
                index = int(outfile.readline().split(" ")[2][5:9])
                top_rank_docs.append(index)
        self.relevance_corpus = {}
        self.corpus_term_set = set()
        self.query_terms = query.keys()
        # construct our candidate term set
        for doc in top_rank_docs:
            for item in clean_token_list:
                if item[0] == doc:
                    self.relevance_corpus[doc] = item[1]
                    for term in item[1]:
                        self.corpus_term_set.add(term)
        score_list = []
        for term1 in list(self.corpus_term_set):
            score = 0
            for term2 in self.query_terms:
                score += association_measure.get(term_association)(
                    term1, term2, self.relevance_corpus.values(), window=5)

            score_list.append((term1, score))
        sorted_score_list = sorted(score_list, key=lambda x: x[1], reverse=True)
        # filter repeated and common words from expansion
        count, index = 0, 0
        while count < top_term_num and index < len(sorted_score_list):
            if sorted_score_list[index][0] not in self.extend_query and \
                            sorted_score_list[index][0] not in InvertedIndexOperation.get_stopping_words():
                self.extend_query[sorted_score_list[index][0]] = 1
                count += 1
            index += 1
