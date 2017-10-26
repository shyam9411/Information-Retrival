
In the HW2, there are three python files called BFS-Crawler, DFS-Crawler and PageRank. BFS-Crawler and DFS-Crawler are in charge of crawling urls in breadth-first and depth-first orders separately. They also store the in-links relationship graphs in two text file. PageRank contains a class with the same name to sort all crawled pages according to their converged page rank values and store the perplexity change tendency and top fifty pages in different files.

- SETUP: 
Before you are available to use these crawlers, you have to install some dependent packages
1.BeautifulSoup4
2.NLTK
You can use pip to install them like $ pip install beautifulsoup4 or $ pip install -U nltk. But we recommend you first install anaconda3. It really is convenient for user to use python. Try google “how to install anaconda3?”.

- USAGE:
Usage one - Console
1.Enter the directory where python files are through console.

2.BFS-Crawler and DFS-Crawler have similar usage. To run BFS-Crawler.py, try “python BFS-Crawler.py thread_number” in current directory. Since our program are based on multi-threads, thread_number is the number of crawlers you want to create. e.g. python BFS-Crawler.py 5

3. If you want to run PageRank.py through console, try “python PageRank.py”. In this way, all parameters in page rank algorithm are default.

Usage two - IDE(Pycharm)
1. Use Pycharm to open the fold as a project. 

2. Set your own Crawler and PageRank configurations according to the parameters description.

3. Call the control function “controller” in these three classes (if you run BFS or DFS crawler in IDE, you must change constant THREADS_NUM into your thread number in case of Error).


- OUTPUT FILES:
1.bfs_in_link_graph.txt: in-link relationship graph of BFS crawling result, which is G1

2.dfs_in_link_graph.txt: in-link relationship graph of DFS crawling result, which is G2

3.Task1_Statistic_Report.txt: a brief report on simple statistics over G1 and G2

4.perplexity_change_list_G1.txt: perplexity values obtained in each round until convergence for G1

5.perplexity_change_list_G2.txt: perplexity values obtained in each round until convergence for G2

6.page_rank_report_G1.txt: all PageRank scores of 1000 pages in G1 in descending order

7.page_rank_report_G2.txt: all PageRank scores of 1000 pages in G2 in descending order

8.top_50_pages_G1.txt: Report the Top 50 pages of G1 by their docID and PageRank score

9.top_50_pages_G2.txt: Report the Top 50 pages of G2 by their docID and PageRank score

10.Task3_Qualitative_Analysis.txt: Task3 comparison and speculation

All the files that need to be submitted are in the fold “report”


MAXIMUM CRAWLER DEPTH:
In the first task, BFS-Crawlers reached 3th depth, DFS-Crawlers reached 6th depth

