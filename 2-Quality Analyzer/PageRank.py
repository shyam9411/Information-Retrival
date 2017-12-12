from math import log2
import json
import os

# global constant definition
MIN_ITERATION = 4
ZERO = 0
ONE = 1
TWO = 2
TOP_PAGE = 50
# build candidate in_link_dict and out_link_dict through reading files
in_link_file = open(os.getcwd()+'/json_file/dfs_in_link_dict.json', 'r')
out_link_file = open(os.getcwd()+'/json_file/dfs_out_link_dict.json', 'r')
IN_LINK = json.load(in_link_file)
OUT_LINK = json.load(out_link_file)


# PageRank class is used to compute
# the converged page rank values for
# all pages crawled by our former crawlers.
class PageRank:
    def __init__(self, in_link_dict=IN_LINK, out_link_dict=OUT_LINK,
                 damping_factor=0.85, top_page_threshold=MIN_ITERATION):
        self.damping_factor = damping_factor
        self.top_page_threshold = top_page_threshold
        # current page rank vector
        self.current_PR = {}
        # new page rank vector
        self.new_PR = {}
        # self.sink_nodes is the set of all sink nodes
        self.sink_nodes = []
        # self.in_link_dict and self.out_link_dict
        # are recorded the in-link and out-link relationship
        self.in_link_dict, self.out_link_dict = in_link_dict, out_link_dict
        self.page_num = len(self.in_link_dict)
        for page in self.in_link_dict:
            self.current_PR[page] = float(ONE / self.page_num)
            if self.out_link_dict[page] == ZERO:
                self.sink_nodes.append(page)

    # get_perplexity: return the perplexity value
    # of current page rank vector
    def get_perplexity(self):
        h_pr = ZERO
        for pr_value in self.current_PR.values():
            h_pr -= pr_value * log2(pr_value)
        perplexity = TWO ** h_pr
        return perplexity

    # page_rank return the converged
    # page rank values of all pages as a Dict
    def page_rank(self):
        previous_perplexity = self.get_perplexity()
        converged_factor = ZERO
        while converged_factor != MIN_ITERATION:
            print("current perplexity is", self.get_perplexity())
            # print("sum", sum(self.current_PR.values()))
            sink_pr = ZERO
            for page in self.sink_nodes:
                sink_pr += self.current_PR[page]
            for page in self.current_PR:
                # random page jump
                self.new_PR[page] = (ONE-self.damping_factor)/self.page_num
                # page rank value provided by all sink nodes
                self.new_PR[page] += self.damping_factor*sink_pr/self.page_num
                # page rank value provided by all in-links
                for in_link in self.in_link_dict[page]:
                    if self.out_link_dict[in_link] > ZERO:
                        self.new_PR[page] += self.damping_factor*self.current_PR[in_link]/self.out_link_dict[in_link]
            # update page rank vector
            for page in self.current_PR:
                self.current_PR[page] = self.new_PR[page]
            # check converged condition
            if abs(self.get_perplexity() - previous_perplexity) < ONE:
                converged_factor += ONE
                previous_perplexity = self.get_perplexity()
            else:
                converged_factor = ZERO
                previous_perplexity = self.get_perplexity()
        return self.current_PR

    # controller is in charge of
    # 1.sorting pages according to their page rank values
    # 2.store relative files
    def controller(self):
        page_rank_list = sorted(self.page_rank().items(), key=lambda x: x[ONE], reverse=True)
        page_rank_report = open(os.getcwd()+"/report/page_rank_report_G2.txt", "w")
        top_page_rank = open(os.getcwd() + "/report/top_50_pages_G2.txt", "w")
        for i in range(len(page_rank_list)):
            if i < TOP_PAGE:
                top_page_rank.write(str(page_rank_list[i]) + "\n")
            page_rank_report.write(str(page_rank_list[i]) + "\n")
        top_page_rank.close()
        page_rank_report.close()


if __name__ == '__main__':
    # test graph
    # in_link_dict, out_link_dict = {'A': ['D','E','F'],'B':['A','F'],
    #                                'C':['A','B','D'],'D':['B','C'],'E':['B','C','D','F'],
    #                                'F':['A','B','D']}, {'A':3,'B':4,'C':2,'D':4,'E':1,'F':3}
    pr = PageRank()
    pr.controller()






