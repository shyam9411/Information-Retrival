from Parser import Parser
import collections
import os


# This class is to build inverted lists for uni_grams, bio_grams and tri_grams
# In the meantime it also generates relationship dictionary objects to
# reflect document names and their ids
# Besides, the number of tokens in each document is stored in another dictionary object
# called token_num_dict for further use.

# Constructor template:
# ii = InvertedIndex(url_data)
# url_data: StringList, it contains all urls which consist of our corpus
# dump_inverted_index: Boolean, true iff save all dictionary objects obtained in this class.
class InvertedIndex:
    def __init__(self, url_corpus, dump_inverted_index=True):
        self.corpus = url_corpus
        self.doc_id_dict, self.id_doc_dict = self._build_doc_id_dict()
        self.token_num_dict = self._number_of_tokens()
        self.unigram_inverted_index = self.sort_posting(self.build_inverted_index(1))
        self.biogram_inverted_index = self.sort_posting(self.build_inverted_index(2))
        self.trigram_inverted_index = self.sort_posting(self.build_inverted_index(3))
        if dump_inverted_index:
            self.save_all_dict()

    # private function
    # this function is used to construct both doc_id_dict, id_doc_dict
    def _build_doc_id_dict(self):
        doc_id_dict = {}
        id_doc_dict = {}
        index = 0
        for url_name in self.corpus:
            id_doc_dict[index] = url_name
            doc_id_dict[url_name] = index
            index += 1
        return doc_id_dict, id_doc_dict

    # private function
    # this function is used to construct token_num_dict
    def _number_of_tokens(self):
        token_num_dict = {}
        parser = Parser(self.corpus)
        token_list = parser.clean_token_list
        uni_grams_list = parser.uni_grams
        bio_grams_list = parser.bio_grams
        tri_grams_list = parser.tri_grams
        for i in range(parser.token_list_length):
            token_num_dict[self.doc_id_dict[token_list[i][0]]] = (len(uni_grams_list[i]),
                                                                  len(bio_grams_list[i]),
                                                                  len(tri_grams_list[i]))
        return token_num_dict

    # GIVEN: PosInt, n only has three values,
    # representing unigrams, biograms and trigrams separately
    # RETURN: Dictionary, the inverted index for given n-grams
    def build_inverted_index(self, n):
        inverted_index = collections.defaultdict(list)
        parser = Parser(self.corpus)
        token_list = parser.clean_token_list
        n_grams_list = []
        if n == 1:
            n_grams_list[:] = parser.uni_grams
        elif n == 2:
            n_grams_list[:] = parser.bio_grams
        elif n == 3:
            n_grams_list[:] = parser.tri_grams
        for i in range(parser.token_list_length):
            for j in range(self.token_num_dict[self.doc_id_dict[token_list[i][0]]][n-1]):
                if n_grams_list[i][j] in inverted_index:
                    existing = False
                    for tag in inverted_index[n_grams_list[i][j]]:
                        if tag[0] == self.doc_id_dict[token_list[i][0]]:
                            tag[1] += 1
                            existing = True
                    if not existing:
                        inverted_index[n_grams_list[i][j]].append([self.doc_id_dict[token_list[i][0]], 1])
                else:
                    inverted_index[n_grams_list[i][j]].append([self.doc_id_dict[token_list[i][0]], 1])
        return inverted_index

    # dumping all useful dictionary to local files.
    def save_all_dict(self):
        self._save_dict(self.unigram_inverted_index, "unigram_inverted_index")
        self._save_dict(self.biogram_inverted_index, "biogram_inverted_index")
        self._save_dict(self.trigram_inverted_index, "trigram_inverted_index")
        self._save_dict(self.id_doc_dict, "id_doc_table")
        self._save_dict(self._number_of_tokens(), "token_num_dict")

    # Helper function
    # GIVEN: an inverted index
    # RETURN: the same inverted index but term frequencies are sorted in inverted lists.
    @staticmethod
    def sort_posting(inverted_index):
        for key in inverted_index:
            inverted_index[key] = sorted(inverted_index[key], key=lambda posting: posting[1], reverse=True)
        return inverted_index

    # Helper function, use format control to save dictionary objects to .txt files
    @staticmethod
    def _save_dict(content, filename):
        with open(os.getcwd() + "/Inverted_Index/" + filename + ".txt", 'w') as outfile:
            for key in content:
                outfile.write(str(key) + " : " + str(content[key]) + "\n")


if __name__ == '__main__':
    # In the main function, we import our candidate urls from a txt file and build a url list
    # Then we initialize a new InvertedIndex to construct three inverted indexes.
    f = open('corpus_wiki.txt')
    url_data = [line.strip("\n") for line in f.readlines()]
    ii = InvertedIndex(url_data)

