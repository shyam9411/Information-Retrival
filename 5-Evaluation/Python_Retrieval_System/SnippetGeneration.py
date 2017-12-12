from bs4 import BeautifulSoup
import os
import re
import ast
import nltk
import operator

"""
Author: Kartik Dave
Date: 12/5/2017

Program to generate snippet for the top relevant documents of the retrieval system.

The snippets will be comprising of an title, the document id and the most relevant
sentence with the query from the text with query words in Bold.

The program will be executed at the query processing time

The input to the program will be the following location of the file of:
a. Document Sentence Index
b. Input query file from the user
c. The relevant document output for which the snippets are need to be generated
d. The stop words

"""


class SnippetGeneration:
    # The snowball stemmer is used for stemming of query and the raw relevant document terms
    snowball = nltk.SnowballStemmer('english')
    userInputQueries = {}  # For storing the user input queries
    topRelevantDocs = {}  # For storing the top relevant result of the retrieval system
    rawCorpusIndex = {}  # For storing the raw corpus sentence index
    stopWordList = []

    # Stop list for removal of punctuation from text not having numbers
    textPunctuationStopList = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',',
                               '/', ':', ';', '<', '=', '>', '?', '@', ']', '[',
                               '^', '_', '`', '{', '|', '}', '~', '“', '”', '☉', '′', '～', '，', '、', '☇', '-']

    # Stop list for removal of punctuation from numbers in the text
    digitsPunctuationStopList = ['!', '"', '#', '&', '\'', '(', ')',
                                 ';', '?', '@', ']', '[', '_', '`',
                                 '{', '|', '}', '~', '“', '”', '☉', '′', '～', '、', '⹁', '☇']

    # All the variables whose value will be passed as an input to the class
    __stopWordsFileLoc = os.getcwd() + "/Query/"
    __userInputQueriesFileLoc = os.getcwd() + "/Query/"
    __topRelevantDocFileLoc = os.getcwd() + "/Results/"
    __rawDocIndexFileLoc = os.getcwd() + "/Inverted_Index/"

    # Function : __init__(Constructor of the class)
    #
    # Parameter:
    # user_input_queries_file_loc => Location of input query file from the user
    # top_relevant_doc_file_loc => Location of the relevant document output
    # raw_doc_index_file_loc => Location of document sentence index
    # stop_words_file_loc => Location of file containing the stop words
    #
    # Effect: Constructor of the class, for getting the file location of the required files
    def __init__(self, user_input_queries_file_loc, top_relevant_doc_file_loc, raw_doc_index_file_loc,
                 stop_words_file_loc):
        self.__userInputQueriesFileLoc += user_input_queries_file_loc
        self.__topRelevantDocFileLoc += top_relevant_doc_file_loc
        self.__rawDocIndexFileLoc += raw_doc_index_file_loc
        self.__stopWordsFileLoc += stop_words_file_loc

    # Function: stop_word_removal
    #
    # Effect: This will take all the stop words from the file provided and will load it in a list
    def stop_word_removal(self):
        with open(self.__stopWordsFileLoc, 'r+', encoding='utf-8') as f:
            self.stopWordList = f.read().split('\n')

    # Function: input_query_processing
    #
    # Effect:
    # This will take the query file provided as an input and process all the queries
    # The processed queries will be stored in a dictionary with keys as query id
    def input_query_processing(self):
        soup = BeautifulSoup(open(self.__userInputQueriesFileLoc), "html.parser")
        # As the queries provided are inside the doc tag
        for row in soup.find_all('doc'):
            all_text = row.get_text()
            # Splitting the text to get the format of query id and the query
            query_to_be_considered_q = " ".join(all_text.split()).split(' ')
            temp_term_q = []  # Temporary list to store the query terms
            # Appending the query part together
            for term in range(1, len(query_to_be_considered_q)):
                string = query_to_be_considered_q[term]

                # Removing the stop words from the query
                for stopWord in self.stopWordList:
                    if string.lower() == stopWord.lower():
                        string = ''

                # Removing the punctuations from all the words in the query
                if bool(re.search(r'\d', string)) and string != '':

                    for p in self.digitsPunctuationStopList:
                        string = string.replace(p, '')
                    article_after_p_handling = string
                    if article_after_p_handling != '':
                        temp_term_q.append(article_after_p_handling)
                # Removing the punctuations from all the numbers in the query
                else:
                    for p in self.textPunctuationStopList:
                        if '-' == p:
                            string = string.replace(p, ' ')
                        else:
                            string = string.replace(p, '')
                    article_after_p_handling = string
                    if article_after_p_handling != '':
                        temp_term_q.append(article_after_p_handling)

            # The dictionary is constructed as keys as the query id and values as the list of query terms
            self.userInputQueries[int(query_to_be_considered_q[0])] = temp_term_q

    # Function: top_relevant_doc_index_creation
    #
    # Effect:
    # To generate dictionary having keys as the query id
    # And values as the list of top relevant documents generated
    def top_relevant_doc_index_creation(self):

        with open(self.__topRelevantDocFileLoc, 'r+', encoding='utf-8') as f:
            top_relevant_entries = f.read().split('\n')[:-1]
        for entry in top_relevant_entries:
            doc_relevant_detail = entry.split(' ')
            query_id = int(doc_relevant_detail[0])  # The first element will be the query id
            relevant_doc_name = doc_relevant_detail[2]  # The third element will be the document id
            if query_id not in self.topRelevantDocs:
                self.topRelevantDocs[query_id] = [relevant_doc_name]
            else:
                self.topRelevantDocs[query_id].append(relevant_doc_name)

    # Function: raw_corpus_index_generation
    #
    # Effect:
    # Putting the index of raw corpus from the file provided in the dictionary
    def raw_corpus_index_generation(self):
        with open(self.__rawDocIndexFileLoc, 'r+', encoding='utf-8') as f:
            self.rawCorpusIndex = ast.literal_eval(f.read())

    # Function: snippet_extraction
    #
    # Effect:
    # Will generate the snippets for all the top relevant documents
    # The snippet will include a title of the page, the document id
    # and the most relevant sentence from the text which will best describe the query
    def snippet_extraction(self):

        self.stop_word_removal()
        self.input_query_processing()
        self.top_relevant_doc_index_creation()
        self.raw_corpus_index_generation()
        # For every query id => I
        for q_id in self.topRelevantDocs:
            query_terms_without_stem = self.userInputQueries[q_id]  # The query terms without stemming
            query_terms = []

            # Query terms with stemming
            for un_stem_terms in query_terms_without_stem:
                un_stem_terms = self.snowball.stem(un_stem_terms)
                query_terms.append(un_stem_terms)

            # The start of building a dynamic HTML file
            html_display = """
                <html>
                """
            # For all the Document Id's => II
            for doc_ID in self.topRelevantDocs[q_id]:
                doc_sentence_score = {}
                doc_title = self.rawCorpusIndex[doc_ID][0]  # The tile of the document
                sentence_list = self.rawCorpusIndex[doc_ID][1]  # The sentences part of the document
                # For all the documents => III
                for sentence in sentence_list:
                    temp_term_s = []
                    count = 0
                    sentence_word_list = sentence.split(' ')
                    # Stemming and punctuation removal of the query term
                    for term in sentence_word_list:
                        term = self.snowball.stem(term)
                        if bool(re.search(r'\d', term)):
                            for p in self.digitsPunctuationStopList:
                                term = term.replace(p, '')
                            if term != '':
                                temp_term_s.append(term)
                        else:
                            for p in self.textPunctuationStopList:
                                if '-' == p:
                                    term = term.replace(p, ' ')
                                else:
                                    term = term.replace(p, '')
                            if term != '':
                                temp_term_s.append(term)
                    # The matching term from query and the sentence to find the sentence score
                    for element in query_terms:
                        if element in temp_term_s:
                            count += 1
                    if sentence not in doc_sentence_score:
                        doc_sentence_score[sentence] = count
                    else:
                        doc_sentence_score[sentence] = doc_sentence_score[sentence] + count
                # Getting the sentence with the maximum score based on the implemented algorithm
                # Will be used to implement the snippet
                significant_sentence = max(doc_sentence_score.items(), key=operator.itemgetter(1))[0]
                # Will add a bold html tag for all the important words present in the query
                for words in query_terms_without_stem:
                    significant_sentence = significant_sentence.replace(words.lower(),
                                                                        '<b>{}</b>'.format(words.lower()))
                    significant_sentence = significant_sentence.replace(words.capitalize(),
                                                                        '<b>{}</b>'.format(words.capitalize()))
                # Constructing the html for the display of the title, document id and the most relevant sentence
                html_display += """
                    <div style= "width:700px">
                    <br/>
                    <font size = 4 color = "0000FF">"""
                html_display = html_display + doc_title.title().strip() + """</font><br/>
                    <font size = 2 color = "#228B22">"""
                html_display = html_display + doc_ID + """</font><br/>
                    <font size = 3 color = "black">"""
                html_display = html_display + significant_sentence + """<br/>
                    <br/>
                    </div>"""
            html_display += """
                </html>"""
            # For writing the dynamic made html inside the file
            with open(os.getcwd() + '/Snippets/' + str(q_id) + 'QuerySnippet.html', 'w', encoding='utf-8') as f:
                f.write(html_display)


# Note :
# the location provided should not include single backslash(\)
# it should either have a common slash(/) or double backslash(//)
#
# Demo Examples:
snippet_extract_obj = SnippetGeneration('cacm.query.txt', 'BM25_Unigram_Case-folded.txt',
                                        'docs_sentence_index.txt', 'common_words.txt')
snippet_extract_obj.snippet_extraction()
