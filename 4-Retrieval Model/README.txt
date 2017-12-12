In the HW4, there are two folders for two IR systems. Luence_Retrieval_System is written by Java and BM25_Retrieval_System is written by Python. In the Luence_Retrieval_System, the codes are modified based on sample codes. A new class Indexer_Module is defined for building indexer and class Retrieval_Module is used to search according to the console input (query). In BM25_Retrieval_System, there are three python classes defined. First, a utility class InvertedIndexOperation is defined to load inverted index, tf table, df table, token numbers dictionary and document id-name reflection table into to memory, forming dictionaries. Then a class QueryParser is defined to conduct the same parsing process, for the user query, with the corpus. Finally, a class BM25 is defined to realize BM25 retrieval model. Also, several helper functions to compute the parameters in BM25 model are defined in both BM25 and InvertedIndexOperation.

The entrance of BM25_Retrieval_System is the main function of class BM25, which interact with user by receiving the query string from console.
The entrance of Luence_Retrieval_System is the main function of class HW4, which interact with user by receiving the query string from console.

- SETUP: 
Before you are available to use these programs, you have to install some dependent packages
- Python
NLTK: You can use pip to install them like $ pip install -U nltk. But we recommend you first install anaconda3. It really is convenient for user to use python. Try google “how to install anaconda3?”.
- Java:
Luence: You need to add the following .jar files into your project: lucene-­core-­4.7.2.jar, lucene-­queryparser-­4.7.2.jar, lucene-­analyzers-­common-­4.7.2.jar.


- USAGE:
Since the usage of java program is the same as original way, I only provide two usages for Python program.
Usage one - Console
1.Enter the directory where python files are through console.
2.BM25.py has main function. To run BM25.py, try “python BM25.py” in current directory.  
3.It will have hint message to remind you to input the query; input 'q' to stop searching.

Usage two - IDE(Pycharm)
1. Use Pycharm to open the fold as a project. 
2. Set running configuration for BM25.py. The same usage for interaction.


- OUTPUT FILES:
All output files are in the 'report' folder. There are totally 20 files.

1. Eighteen searching results with the following naming format: SYSTEM_QUERY.txt
2. A brief report for the implementation of both systems.
3. A comparison report for the top 5 results of both IR systems and the conclusions.



