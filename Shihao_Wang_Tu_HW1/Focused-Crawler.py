from urllib import request
from bs4 import BeautifulSoup
import copy
import re
import threading
import time
import sys
import datetime
#  A package used to extract the similar words and conduct stemming process
from nltk.corpus import wordnet as wn
import nltk as nk


#   global constant definition
MAX_DEPTH = 6
MAX_URL_NUM = 200
THREADS_NUM = int(sys.argv[2])
#   global variable definition
maximum_layer_number = 1
lancaster = nk.LancasterStemmer()


#   get all link tags (which contain <a>, </a>) in the page of given url
def get_link(url):
    # the politeness policy
    time.sleep(1)
    org = "http://en.wikipedia.org"
    html = request.urlopen(org + url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    return bs_obj.find('div', id="bodyContent").find_all('a', href=re.compile("^(/wiki/)((?!:|#)\S)*$"))


#   find all stemming words of given keyword, return the union set of stemming words and origin words
def find_stemming_sets(word_list):
    stem_word_list = copy.deepcopy(word_list)
    for word in word_list:
        stem_word_list.append(lancaster.stem(word))
    return stem_word_list


#   find all synonyms of given keyword
def find_synonym_sets(key_word):
    synonym_sets = wn.synsets(key_word)
    sys_words = set()
    for synonym in synonym_sets:
        sys_word = synonym.lemmas()[0].name()
        sys_words.add(sys_word)
    return sys_words


#   extract all legal words from given url string
def extract_words_from_url(url):
    split_url = url[6:].split("_")
    for i in range(len(split_url)):
        split_url[i] = split_url[i].strip('()')
    return split_url


#   judge whether the synonyms set of keyword and the stemming set of given word list have intersection
#   RETURN: True iff the word list has word that matched the key word (e.g. same word, or similar word).
def is_synonym_word(key_word, word_list):
    sys_words = find_synonym_sets(key_word)
    stem_words = find_stemming_sets(word_list)
    for word in stem_words:
        if word.lower() in sys_words:
            return True
    return False


#   a BFS-based crawler
#   GIVEN: a frontier_list in which each item is a sublist [url, layer_number].
#          the layer_number is the depth of given url.
#          a seen_list which stores the unique urls that have been crawled.
#          a key_word which denotes the target of this focused crawler.
#   RETURN:no return parameter
def wiki_crawler(frontier_list, seen_list, key_word):
    global maximum_layer_number

    current_url = frontier_list.pop(0)
    links = get_link(current_url[0])
    layer_number = current_url[1]
    while layer_number < MAX_DEPTH and len(seen_list) < MAX_URL_NUM:
        maximum_layer_number = layer_number
        if len(links) > 0:
            for link in links:
                    if 'href' in link.attrs \
                            and is_synonym_word(key_word, extract_words_from_url(link.attrs['href'])):
                                frontier_list.append([link.attrs['href'], layer_number+1])
        if len(frontier_list) > 0:
            current_url = frontier_list.pop(0)
            if current_url[0] not in seen_list:
                seen_list.append(current_url[0])
            layer_number = current_url[1]
            links = get_link(current_url[0])
        else:
            return
    return


#   controller is the control function of all crawlers, file i/o and the console outputs
#   the controller will use multi-threads to build several crawlers to work together.
#   GIVEN: a key_word which denotes the target of this focused crawler. key_word will be input by user
#   RETURN: no return parameter. Only several information such as
#           execution time, maximum depth and matched urls will be printed on the console.
def controller(key_word):
    global maximum_layer_number
    url_start = "/wiki/Tropical_cyclone"
    file = open("focused_wiki.txt", "w")
    frontier_list = [[url_start, maximum_layer_number]]
    seen_list = []
    # judge whether the start url matches the keyword
    if is_synonym_word(key_word, extract_words_from_url(url_start)):
        seen_list.append(url_start)
    # call multi-threads
    start_time = datetime.datetime.now()
    t = locals()
    for i in range(THREADS_NUM):
        t['x%s' % i] = threading.Thread(target=wiki_crawler, args=(frontier_list, seen_list, key_word))
        t['x%s' % i].setDaemon(True)
        t['x%s' % i].start()
        t['x%s' % i].join()
    end_time = datetime.datetime.now()
    # if the seen_list is not full, use urls in the frontier_list to fill it.
    if len(seen_list) < MAX_URL_NUM and len(frontier_list) > 0:
        for url in frontier_list:
            if len(seen_list) < MAX_URL_NUM:
                seen_list.append(url[0])
        maximum_layer_number += 1
    # if there is no match for keyword.
    elif len(frontier_list) == 0 and len(seen_list) == 0:
        print("Sorry, there is no url that matches the given keyword.")
    # Console output
    print("The maximum depth reached is", maximum_layer_number)
    print("You use", THREADS_NUM, "threads to run your crawlers")
    print("The execution time of this crawler is", (end_time - start_time).seconds, "s")
    print("The following are links crawled:")
    for wiki_url in seen_list:
        file.write(wiki_url + "\n")
        print(wiki_url)
    file.close()
    return

if __name__ == '__main__':
    controller(str(sys.argv[1]))
