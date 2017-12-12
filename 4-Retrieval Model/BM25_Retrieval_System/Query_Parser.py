import nltk as nk
from nltk.tokenize import word_tokenize
from collections import defaultdict
INVALID_CHAR = '#'

"""
There is no main function because we don't need to produce any output files
This class is to realize text extraction and transformation for given query

Constructor template:
    parser = QueryParser(query)
Interpretation:
    query: String, the query users want to search
    case_folding: Boolean, true iff we conduct case_folding
    punctuation: Boolean, true iff we conduct punctuation remove process
    stemming: Boolean, true iff we conduct stemming process
"""


class QueryParser:
    def __init__(self, query, case_folding=True, punctuation=True, stemming=False):
        self.query = defaultdict(int)
        if case_folding:
            query = query.lower()
        query = word_tokenize(query)
        if punctuation:
            query = self.remove_useless_text(query)
        if stemming:
            query = self.stemming(query)
        # generate n-grams
        query = list(nk.ngrams(query, 1))
        for item in query:
            self.query[item] += 1

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
