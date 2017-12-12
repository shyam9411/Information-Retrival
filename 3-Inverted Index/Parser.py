from urllib import request
from bs4 import BeautifulSoup
import re
import os
import nltk as nk
from nltk.tokenize import word_tokenize

INVALID_CHAR = '#'


# There is no main function because we don't need to produce any output files
# This class is to realize text extraction and transformation

# Constructor template:
# parser = Parser(url_data)
# url_data: StringList, it contains all urls which consist of our corpus
# case_folding: Boolean, true iff we conduct case_folding
# punctuation: Boolean, true iff we conduct punctuation remove process
# stemming: Boolean, true iff we conduct stemming process
class Parser:
    def __init__(self, url_data, case_folding=True, punctuation=True, stemming=False):
        self.clean_token_list = []
        self.uni_grams = []
        self.bio_grams = []
        self.tri_grams = []
        # Extract titles and plain content in wiki pages
        self.url_data = url_data
        # Conduct text transformation
        for url in url_data:
            f = open(os.getcwd() + "/wikiData/" + url + '.txt', "r")
            text = f.read()
            if case_folding:
                text = text.lower()
            token_list = word_tokenize(text)
            if punctuation:
                token_list = self.remove_useless_text(token_list)
            if stemming:
                token_list = self.stemming(token_list)
            # generate n-grams
            self.clean_token_list.append((url, token_list))
            self.uni_grams.append(list(nk.ngrams(token_list, 1)))
            self.bio_grams.append(list(nk.ngrams(token_list, 2)))
            self.tri_grams.append(list(nk.ngrams(token_list, 3)))
        self.token_list_length = len(self.clean_token_list)

    # Save text files into wikiData directory as a corpus
    @staticmethod
    def _save_file(content, filename):
        f = open(os.getcwd()+"/wikiData/"+filename+'.txt', "a")
        f.write(str(content)+"\n")
        f.close()

    # This function serves as a pre-processing work.
    # It extracts all plain content and heads for given urls.
    # GIVEN: StringList urls need to be extracted
    # RETURN: all txt file which contains only text in directory wikiDate
    def _get_html_text(self, urls):
        org = "http://en.wikipedia.org/wiki/"
        for url in urls:
            response = request.urlopen(org + url)
            html = response.read().decode('utf-8')
            bs_obj = BeautifulSoup(str(html), 'html.parser')
            title = bs_obj.find(name='h1', id='firstHeading')
            self._save_file(title.get_text(), url)
            [s.extract() for s in bs_obj(['math'])]
            div = bs_obj.find(name='div', class_='mw-parser-output')
            ps = div.find_all(name=re.compile("^h|p"), recursive=False)
            for p in ps:
                paragraph_text = p.get_text()
                self._save_file(paragraph_text, url)
            print("extracting text and titles from --", url, "--")

    # Helper function to remove some field tokens like [edit] or [1],
    # and other useless punctuation
    # GIVEN: StringList, a token list which just is processed by NLTK's word_tokenizer
    # RETURN: StringList, clean token list which remove the useless parts
    @staticmethod
    def remove_useless_text(token_list):
        # our punctuation list
        useless_list = [',', '.', ':', ';', '?', '(', ')', '[', ']',
                        '&', '!', '*', '@', '#', '$', '%', '"', '``',
                        "''", "'", '–', '—', '’', '′', '，']
        clean_token_list = []
        for token_index in range(len(token_list)):
            if token_index < len(token_list) - 2 and token_list[token_index] == '[' and \
                        (token_list[token_index + 1] == 'edit' or token_list[token_index + 1].isdigit()) and \
                        token_list[token_index + 2] == ']':
                token_list[token_index], token_list[token_index + 1], token_list[token_index + 2] = \
                    INVALID_CHAR, INVALID_CHAR, INVALID_CHAR
            elif token_list[token_index] in useless_list:
                token_list[token_index] = INVALID_CHAR
        for token in token_list:
            if token != INVALID_CHAR:
                clean_token_list.append(token)
        return clean_token_list

    # this class also supports a stemming processing function,
    # but the default is not using it.
    # GIVEN: StringList
    # RETURN: StringList, the origin token list but do stemming for every token.
    @staticmethod
    def stemming(word_list):
        words_after_stemming = []
        lancaster = nk.LancasterStemmer()
        for word in word_list:
            words_after_stemming.append(lancaster.stem(word))
        return words_after_stemming
