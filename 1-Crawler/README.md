Non-Focused-Crawler.py is the code of Q1 and Focused-Crawler.py is the code of Q2. Two python files are written by Python3 and all runnable in console.

SETUP:
Before you are available to use these crawlers, you have to install some dependent packages
1.BeautifulSoup4
2.NLTK
You can use pip to install them like $ pip install beautifulsoup4 or $ pip install -U nltk. But we recommend you first install anaconda3. It really is convenient for user to use python. Try google “how to install anaconda3?”.

USAGE:
1.Enter the directory where both python files are through console.
2.To run Non-Focused-Crawler.py, try “python Non-Focused-Crawler.py thread_number” in current directory. Since our program are based on multi-threads, thread_number is the number of crawlers you want to create. e.g. python Non-Focused-Crawler.py 5
3.To run Focused-Crawler.py, try “python Non-Focused-Crawler.py key_word thread_number” in current directory. key_word is the keyword you want to match. e.g. python Focused-Crawler.py rain 5

OUTPUT 
on console:
1.Maximum depth the crawlers reach
2.Execution time
3.Thread number
4.All matched urls 
On file:
1.All matched urls 
all_wiki.txt is for Task1 and focused_wiki.txt is for Task2

MAXIMUM CRAWLER DEPTH:
In the first task, our crawlers reached 3th depth
In the second task, when the keyword is ‘rain’, our crawlers reached 6th depth


I also provide a sample result for Task2 called focused_wiki_sample_of_rain.txt, which obtains 200 urls about 'rain'.
