This project consists of both Java and Python retrieval systems. Java Retrieval System, which is based on Lucene 4.7.2, is in the folder Lecene_Retrieval_System. And Python Retrieval System, which support three basic retrieval models, is in the folder Python_Retrieval_System. 

Both Retrieval Systems contain the following folders:
- Corpus	  store the corpus text 
- Inverted_Index  store inverted index and other related statistic tables
- Query           query entrance folder, all user query files should be put here
- Results         store the searching results, all files are named by system names.

- DEPENDENCE SETUP: 
Before you are available to use these programs, you have to install some dependent packages
- Python
NLTK: You can use pip to install them like $ pip install -U nltk. But we recommend you first install anaconda3. It really is convenient for user to use python. Try google “how to install anaconda3?”.
PrettyTable: "pip install PrettyTable"
- Java:
Luence: You need to add the following .jar files into your project: lucene-­core-­4.7.2.jar, lucene-­queryparser-­4.7.2.jar, lucene-­analyzers-­common-­4.7.2.jar.


- USAGE:
- Lucene_Retrieval_System:
The entrance of this system is class Retrieval_Module. First users need to enter the directory of folder 'src' through the console and use 'javac' to compile both Indexer_Module and Retrieval_Module. Then users can use 'java Retrieval_Module' to run the existing system, whose inverted index has been built. Another candidate way is directly using the .class files that we have compiled before in the folder out.  

Please pay attention that Lucene_Retrieval_System is not an interactive program so users need to put all their queries into a file and put it in the folder Query. The query format should be one query one line, using space to split each term. See more in our demo query file.

- Python_Retrieval_System:
The entrance of this system is class Retrieval_System. Users can directly use our python retrieval system without compiling. It is an oriented-object style program so users can use it through creating new RetrievalSystem object in their own program. The following is the constructor template:

rs = RetrievalSystem("cacm.query.txt", TREC_format=True, stopping=False, retrieval_model='BM25', stemming_corpus=True, query_refinement=True)

The first parameter is the filename of query; 
The second is whether it is a TREC format query file or a simple one-line-one-query file; 
The third 'stopping' controls whether to use stopping words to handle raw query;
'retrieval_model' decides which retrieval model will be used in the researching process.
'stemming_corpus' controls whether to use stemming corpus as our database;
'query_refinement' controls whether to use Pseudo Relevance Feedback to conduct query refinement (may consume more query time).

For extra credit part, we have a Python file called Proximity_Retrieval_Model, which is already runnable. Check the usage in its main function.

We recommend you to open it through IDE like PyCharm. And see the runnable demo in Retrieval_System.


- OUTPUT FILES:
All output files are in the 'Results' folder. The query result will form the corresponding file with the name as its system name. Each file has totally 6400 query results, 100 for each query respectively:
BM25_Stemming_Unigram_Case-folded:               use stemming corpus and BM25 model
BM25_Stopping_Unigram_Case-folded:               use stopping query and BM25 model
BM25_Unigram_Case-folded:                        use BM25 model without other processing
BM25_Stemming_Unigram_Case-folded_QueryRefine:   use stemming corpus, pseudo relevance feedback for query refinement and BM25 model
SmoothingQLM_Stemming_Unigram_Case-folded:       use stemming corpus and smoothing query likelihood model 
SmoothingQLM_Stopping_Unigram_Case-folded:       use stopping query and smoothing query likelihood model 
SmoothingQLM_Unigram_Case-folded:                use smoothing query likelihood model without other processing
tf-idf_Stemming_Unigram_Case-folded:             use stemming corpus and tf-idf model
tf-idf_Stopping_Unigram_Case-folded:             use stopping query and tf-idf model
tf-idf_Unigram_Case-folded:                      use tf-idf model without other processing
Luence_Unigram_Case-folded:                      use simple retrieval model in Luence without other processing
PRM_Unigram_Case-folded:                         use Proximity Retrieval Model without other processing
PRM_Stopping_Unigram_Case-folded:                use stopping query and Proximity Retrieval Model


