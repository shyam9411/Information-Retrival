from urllib import request, error
from bs4 import BeautifulSoup
import re
import threading
import time
import datetime
import sys
import os
import json


# global constant definition
MAX_DEPTH = 6
MAX_URL_NUM = 1000
# THREADS_NUM = 1
THREADS_NUM = int(sys.argv[1])
ORG = "http://en.wikipedia.org"
START_URL = "/wiki/Tropical_cyclone"
ZERO = 0
ONE = 1


class BFSCrawler:
    def __init__(self, url_start=START_URL, thread_num=THREADS_NUM, max_url_num=MAX_URL_NUM, max_depth=MAX_DEPTH):
        self.maximum_layer_number = ONE
        self.max_depth = max_depth
        self.max_url_num = max_url_num
        self.url_start = url_start
        self.thread_num = thread_num
        # initialization of special data structures in crawler:
        # frontier,seen, in_link_dict and out_link_dict
        self.frontier_list = [[self.url_start, self.maximum_layer_number]]
        self.seen_list = []
        self.store_in_seen(self.url_start)
        self.in_link_dict, self.out_link_dict = {}, {}
        self.dict_build()

    #   get all link tags (which contain <a>, </a>)
    #   in the page of given url
    @staticmethod
    def get_link(url):
        # the politeness policy
        # time.sleep(1)
        html = request.urlopen(ORG + url)
        bs_obj = BeautifulSoup(html, 'html.parser')
        return bs_obj.find('div', id="bodyContent").find_all('a', href=re.compile("^(/wiki/)((?!:|#)\S)*$"))

    #   save html files that have been crawled
    @staticmethod
    def save_html(url):
        html = request.urlopen(ORG+url).read()
        file = open(os.getcwd()+"/html"+str(url)+".html", "w")
        file.write(str(html, "utf-8"))
        file.close()

    #   return the name of the url.
    #   For example, the name of '/wiki/Tropical_cyclone'
    #   is 'Tropical_cyclone'
    @staticmethod
    def name_of_url(url):
        return url[6:]

    #   update out_link_dict by statistic of
    #   all out-link edges in the in-link graph
    def update_out_link(self):
        for url_list in self.in_link_dict.values():
            for url_name in url_list:
                if url_name in self.out_link_dict:
                    self.out_link_dict[url_name] += ONE

    #   helper function for initialization of
    #   in_link_dict and out_link_dict using refer_wiki
    def dict_build(self):
        file_object = open(os.getcwd() + '/wiki/bfs_refer_wiki.txt')
        for line in file_object:
            self.in_link_dict[line[6:-1]] = set()
            self.out_link_dict[line[6:-1]] = ZERO
        return

    #   combine function of updating seen queue
    #   and store html file
    def store_in_seen(self, url):
        self.seen_list.append(url)
        self.save_html(url)

    #   a BFS-based crawler
    #   RETURN:no return parameter, but in charge of
    #   1. update in_link_dict by checking every new crawled url
    #   2. fill in frontier queue, which is used to crawl new urls
    #   3. fill in seen queue, which is used to store urls crawled and check duplicate
    def wiki_crawler(self):
        current_url = self.frontier_list.pop(ZERO)
        links = self.get_link(current_url[ZERO])
        layer_number = current_url[ONE]
        while layer_number < self.max_depth and len(self.seen_list) < self.max_url_num:
            self.maximum_layer_number = layer_number
            # find all links in current page and add them into frontier queue
            for link in links:
                if 'href' in link.attrs:
                    # [url, layer number of url] is the unit of the frontier
                    self.frontier_list.append([link.attrs['href'], layer_number+1])
                    if self.name_of_url(link.attrs['href']) in self.in_link_dict:
                        self.in_link_dict[self.name_of_url(link.attrs['href'])].add(self.name_of_url(current_url[0]))
            # select next page to be crawled and save it in the seen queue before crawling it
            while current_url[ZERO] in self.seen_list and self.frontier_list:
                current_url = self.frontier_list.pop(ZERO)
            if not self.frontier_list:
                return
            else:
                self.store_in_seen(current_url[ZERO])
                layer_number = current_url[ONE]
                links = self.get_link(current_url[ZERO])
        return

    #   controller is the control function of all crawlers, file i/o and the console outputs
    #   the controller will use multi-threads to build several crawlers to work together.
    #   GIVEN: no given parameter
    #   RETURN: no return parameter. Only several information such as
    #           execution time, maximum depth and matched urls will be printed on the console.
    def controller(self):
        # Initialize
        url_file = open(os.getcwd()+"/wiki/bfs_wiki.txt", "w")
        in_link_file = open(os.getcwd()+"/report/bfs_in_link_graph.txt", "w")
        # call multi-threads
        start_time = datetime.datetime.now()
        t = locals()
        for i in range(self.thread_num):
            t['x%s' % i] = threading.Thread(target=self.wiki_crawler)
            t['x%s' % i].setDaemon(True)
            t['x%s' % i].start()
            t['x%s' % i].join()
        end_time = datetime.datetime.now()
        # Console output
        print("The maximum depth reached is", self.maximum_layer_number)
        print("You use", self.thread_num, "threads to run your crawlers")
        print("The execution time of this crawler is", (end_time - start_time).seconds, "s")
        print("The following are links crawled:")
        # write bfs_wiki.txt
        for wiki_url in self.seen_list:
            url_file.write(wiki_url + "\n")
            print(self.name_of_url(wiki_url))
        url_file.close()
        # write in_link_graph.txt
        for url_name in self.in_link_dict:
            in_link_file.write(url_name+" "+str(self.in_link_dict[url_name]).replace("'", "")
                               .replace(",", "").strip("{}")+"\n")
            self.in_link_dict[url_name] = list(self.in_link_dict[url_name])
        in_link_file.close()
        # write out_link_dict.json and in_link_dict.json
        self.update_out_link()
        with open(os.getcwd()+'/json_file/bfs_out_link_dict.json', 'w') as outfile:
            json.dump(self.out_link_dict, outfile)
        with open(os.getcwd()+'/json_file/bfs_in_link_dict.json', 'w') as outfile:
            json.dump(self.in_link_dict, outfile)


if __name__ == '__main__':
    crawler = BFSCrawler()
    crawler.controller()
