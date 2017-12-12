import os


# A utility class for existing inverted indexes while have formed files
# Constructor template:
# iio = InvertedIndexOperation()
class InvertedIndexOperation:
    # The function is used to recover dictionary dumped
    # by function _save_dict
    # GIVEN: PosInt, n only has three values,
    # representing unigrams, biograms and trigrams separately
    @staticmethod
    def load_dict(n):
        load_dict = {}
        if n == 1:
            with open(os.getcwd() + "/Inverted_Index/unigram_inverted_index.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        elif n == 2:
            with open(os.getcwd() + "/Inverted_Index/biogram_inverted_index.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        elif n == 3:
            with open(os.getcwd() + "/Inverted_Index/trigram_inverted_index.txt") as f:
                for line in f.readlines():
                    key_value_pair = line.strip("\n").split(" : ")
                    load_dict[eval(key_value_pair[0])] = eval(key_value_pair[1])
        return load_dict

    # Build a term frequency table comprising two columns: term and tf
    # GIVEN: PosInt, n only has three values,
    # representing unigrams, biograms and trigrams separately
    # RETURN: Dictionary, term frequency table which is sorted according to tf
    def term_frequency_sort(self, n):
        tf_table = {}
        inverted_index = self.load_dict(n)
        for key in inverted_index:
            tf_sum = 0
            for posting in inverted_index[key]:
                tf_sum += posting[1]
            tf_table[key] = tf_sum
        # sort all terms according to tf
        key_value_list = sorted(tf_table.items(), key=lambda tag: tag[1], reverse=True)
        tf_table = {}
        for item in key_value_list:
            tf_table[item[0]] = item[1]
        return tf_table

    # Build a document frequency table comprising three columns: term, docID and df
    # GIVEN: PosInt, n only has three values,
    # representing unigrams, biograms and trigrams separately
    # RETURN: Dictionary, document frequency table
    # which is sorted lexicographically based on terms
    def doc_frequency_sort(self, n):
        df_table = {}
        inverted_index = self.load_dict(n)
        for key in inverted_index:
            df = len(inverted_index[key])
            doc_list = []
            for posting in inverted_index[key]:
                doc_list.append(posting[0])
            df_table[key] = [doc_list, df]
        # sort all terms lexicographically based on terms
        key_value_list = sorted(df_table.items(), key=lambda tag: tag[0])
        df_table = {}
        for item in key_value_list:
            df_table[item[0]] = item[1]
        return df_table

    # Helper function, use format control to save dictionary objects to .txt files
    @staticmethod
    def _save_dict(content, filename):
        with open(os.getcwd() + "/Inverted_Index/" + filename + ".txt", 'w') as outfile:
            for key in content:
                outfile.write(str(key) + " : " + str(content[key]) + "\n")

    # dumping all useful dictionary to local files.
    def save_all_dict(self):
        self._save_dict(self.term_frequency_sort(1), "unigram_term_frequency_table")
        self._save_dict(self.term_frequency_sort(2), "biogram_term_frequency_table")
        self._save_dict(self.term_frequency_sort(3), "trigram_term_frequency_table")
        self._save_dict(self.doc_frequency_sort(1), "unigram_doc_frequency_table")
        self._save_dict(self.doc_frequency_sort(2), "biogram_doc_frequency_table")
        self._save_dict(self.doc_frequency_sort(3), "trigram_doc_frequency_table")

if __name__ == '__main__':
    iio = InvertedIndexOperation()
    iio.save_all_dict()






