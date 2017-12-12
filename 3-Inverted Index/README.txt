In the HW3, there are three python files responding to three tasks: Parser.py is used to to realize text extraction and transformation; Inverted_Index.py is used to implement three inverted indexes according to n value of n-grams; Inverted_Index_Operation is a utility class to save and load dictionary object and conduct statistic work on existing inverted index, generating term frequency table and document frequency table. Here I first give description of three classes and then brief introduction of the setup and usage of three python files. Final, I list all output files that might be helpful for review and further work.

- Class Introduction:
# Parser class is to realize text extraction and transformation

# Constructor template:
# parser = Parser(url_data, case_folding=True, punctuation=True, stemming=False)

# url_data: StringList, it contains all urls which consist of our corpus
# case_folding: Boolean, true iff we conduct case_folding. Default value is True.
# punctuation: Boolean, true iff we conduct punctuation remove process. Default value is True.
# stemming: Boolean, true iff we conduct stemming process. Default value is False.

# InvertedIndex class is to build inverted lists for uni_grams, bio_grams and tri_grams
# In the meantime it also generates relationship dictionary objects to
# reflect document names and their ids
# Besides, the number of tokens in each document is stored in another dictionary object
# called token_num_dict for further use.

# Constructor template:
# ii = InvertedIndex(url_data, dump_inverted_index=True)

# url_data: StringList, it contains all urls which consist of our corpus
# dump_inverted_index: Boolean, true iff save all dictionary objects obtained in this class.

# InvertedIndexOperation: A utility class for existing inverted indexes while have formed files
# Constructor template:
# iio = InvertedIndexOperation()
# core functions (parameter n is an integer which means the n value of n-grams)
# - iio.load_dict(n): The function is used to recover dictionary dumped by function _save_dict
# - iio.term_frequency_sort(n): Build a term frequency table comprising two columns: term and tf
# - iio.doc_frequency_sort(n): Build a document frequency table comprising three columns: term, docID and df


- SETUP: 
Before you are available to use these crawlers, you have to install some dependent packages
1.BeautifulSoup4
2.NLTK
You can use pip to install them like $ pip install beautifulsoup4 or $ pip install -U nltk. But we recommend you first install anaconda3. It really is convenient for user to use python. Try google “how to install anaconda3?”.

- USAGE:
Usage one - Console
1.Enter the directory where python files are through console.

2.InvertedIndex and InvertedIndexOperation both have main function, which is used to dump dictionary into files. To run InvertedIndex.py, try “python InvertedIndex.py” in current directory.  

Usage two - IDE(Pycharm)
1. Use Pycharm to open the fold as a project. 

2. Set your own corpus path, Parser and InvertedIndex objects just as our main function do. Then you can create your own inverted indexes more than wikipedia.


- OUTPUT FILES:
We use some format control to output our files, which is more readable. For a typical line in inverted index
(’biograms’,’term’) : [[docID, tf], [docID, tf], [docID, tf], [docID, tf]…], where all term frequencies are sorted from most to least.

1.unigram_inverted_index.txt: inverted index for unigrams.

2.unigram_term_frequency_table.txt: term frequency table for unigrams, which is sorted according to tf.

3.unigram_doc_frequency_table.txt: document frequency table for unigrams, which is sorted lexicographically based on terms.

4.biogram_inverted_index.txt: inverted index for biograms.

5.biogram_term_frequency_table.txt: term frequency table for biograms, which is sorted according to tf.

6.biogram_doc_frequency_table.txt: document frequency table for biograms, which is sorted lexicographically based on terms.

7.trigram_inverted_index.txt: inverted index for trigrams.

8.trigram_term_frequency_table.txt: term frequency table for biograms, which is sorted according to tf.

9.trigram_doc_frequency_table.txt: document frequency table for trigrams, which is sorted lexicographically based on terms.

10.stopwords.txt: system stopwords list and comment 

11.id_doc_dict.txt: a reflection relationship between document names and their IDs.

Ps: wikiData directory has all text files extracted from html pages. Keeping it right there promises the program running successfully.


