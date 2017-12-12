import os
from Query_Parser import QueryParser
from Inverted_Index_Operation import InvertedIndexOperation

"""
Author: Shihao Wang
This class realize a simple proximity dependence model, using the bottom of span distance as score function
(span distance means the length from the first term to the last term). This model consists of two parts,
sequential-pair part and all combination part, occupying the weight 0.2 and 0.8 separately in default.

Constructor Template:
ProximityRetrievalModel(query, window=3, factor=0.8)
query: [queryID, [query_term...], [query_bi-gram...]]
window: int, number of maximum proximity
factor: float, weight of all combination part.
"""


class ProximityRetrievalModel:
    def __init__(self, query, window=3, factor=0.8):
        self.query_index = query[0]
        self.bi_gram_list = query[2]
        self.doc_id = -1
        self.query_term_list = query[1]
        self.window = window
        self.inverted_index = InvertedIndexOperation.get_inverted_index_with_proximity()
        self.factor = factor

    def get_score(self):
        score = 0
        position_info_dict = {}
        position_info_t1, position_info_t2 = [], []
        # compute the score of sequential-pair part
        for bi_gram_pair in self.bi_gram_list:
            if bi_gram_pair[0] in self.inverted_index and bi_gram_pair[1] in self.inverted_index:
                for posting in self.inverted_index[bi_gram_pair[0]]:
                    if posting[0] == self.doc_id:
                        position_info_t1 = posting[2]
                        position_info_dict[bi_gram_pair[0]] = position_info_t1
                for posting in self.inverted_index[bi_gram_pair[1]]:
                    if posting[0] == self.doc_id:
                        position_info_t2 = posting[2]
                        position_info_dict[bi_gram_pair[1]] = position_info_t2
                # check if both term are in the same doc
                if position_info_t1 and position_info_t2:
                    for position in position_info_t1:
                            position_span = [position+i+1 for i in range(self.window)]
                            for pos in position_info_t2:
                                if pos in position_span:
                                    score += float(1)/(pos - position)
            position_info_t1, position_info_t2 = [], []
        # check whether the document has all terms in query
        if len(position_info_dict) != len(self.query_term_list):
                return score * (1 - self.factor)
        # re-construct matching list
        max_index = 0
        for key in position_info_dict:
            tmp = max(position_info_dict[key])
            if tmp > max_index:
                max_index = tmp
        recovery_doc = ["#" for i in range(max_index+1)]
        # # compute the score of all combination part
        for key in position_info_dict:
            for pos in position_info_dict[key]:
                recovery_doc[pos] = key
        score = (1-self.factor) * score + self.factor * self.score_of_all_combination(recovery_doc)
        return score

    # compute score for the combination part of PRM
    def score_of_all_combination(self, doc_list):
        # using a stack to backtrack
        stack = []
        max_score = 0
        i = 0
        j = 0
        while i < len(doc_list) and j < len(self.query_term_list):
            if doc_list[i] == self.query_term_list[j]:
                stack.append([self.query_term_list[j], i])
                j += 1
            if stack and i > stack[-1][1]+3:
                res = stack.pop()
                j -= 1
                i = res[1]
            if len(stack) == len(self.query_term_list):
                if max_score < float(1) / (stack[-1][1] - stack[0][1]):
                    max_score = float(1) / (stack[-1][1] - stack[0][1])
                j = 0
                i = stack[0][1]
                stack = []
            i += 1
        return max_score

    # This function is used to initialize document-related parameters
    def set_doc(self, new_doc_id):
        self.doc_id = new_doc_id

# main function
# control the calculation processing for all queries.
if __name__ == '__main__':
    system_name = 'PRM_Unigram_Case-folded.txt'
    top_results = 100
    stopping_system_name = 'PRM_Stopping_Unigram_Case-folded.txt'
    qp = QueryParser("cacm.query.txt", stopping=True, TREC_format=True)
    qp.build_proximity_query()
    query_list = qp.query_with_proximity
    # test_query = query_list[3]
    # candidate_doc = InvertedIndexOperation.find_candidate_doc(test_query[1])
    # prm = ProximityRetrievalModel(test_query)
    # prm.set_doc(1890)
    # print(prm.get_score())

    for query_item in query_list:
        score_list = {}
        # filter all related documents with given query
        candidate_doc = InvertedIndexOperation.find_candidate_doc(query_item[1])
        prm = ProximityRetrievalModel(query_item)
        for doc in candidate_doc:
            prm.set_doc(doc)
            score_list[InvertedIndexOperation.to_doc_name(doc)] = prm.get_score()
            print(InvertedIndexOperation.to_doc_name(doc) + "'s score is "
                  + str(score_list[InvertedIndexOperation.to_doc_name(doc)]))
        rank_score_list = sorted(score_list.items(), key=lambda x: x[1], reverse=True)
        # output under format control
        with open(os.getcwd() + '/Results/' + stopping_system_name, 'a') as outfile:
            for k in range(top_results):
                outfile.write(str(prm.query_index) + " " +
                              "Q0" + " " + str(rank_score_list[k][0]) +
                              " " + str(k + 1) + " " + str(rank_score_list[k][1]) +
                              " " + stopping_system_name + "\n")
