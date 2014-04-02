focused_crawler
===============

A focused web crawler written in Python.

## How to Run
It needs to be run in a *nix shell.
``````
Usage: python crawler.py [-n num] terms
-n      number of pages to be crawlered, 500 by default.
terms   the search terms
``````
### Example
Go into src directory.
Type in 
"python crawler.py -n 200 new york"
or simply
"python crawler.py horse"

### Notice
1. "-n" is optional. The default value is 500.
2. Be careful to the search terms, the number of which must be at least one. If search terms are more than one, they are separated by space.
3. Be careful to special characters. Characters like '#' and '!' are prohibited in search terms, for they may cause failure.


## How It Works
1. It asks user for number of pages and search terms, then retrieve results from Google.

2. It utilizes Focused Search mechanism to crawl web pages from the result pages of Google. The search processes are multi-threaded. There is a while loop. In each iteration, first, it gets the top 10 URL of the largest link score from the URL priority queue. Then it runs a thread for each of these URLs. It downloads the page, calculate the page score and update the URL priority queue with page score. Once all the threads finish their jobs, it sorts the URL priority queue by link score. Also, it will check whether a page is qualified to be searched. Every 300 pages will be compressed into a .gz file in order to save disk space.

3. All the pages, as well as a statistic file 'stat.log', will be stored in the "data_file" directory.


## Features
- Save web pages, as well as statistic file, into disk.
- Check the suffix and MIME type of a web page to determine whether crawl it or not.
- Dictionary for avoiding revisit to the same URL.
- Handle 'base' tag in html.
- Ignore password protected pages.
- Counter for 404 error.
- Ignore CGI web page if encountered.
- Check 'Disallow' in robots.txt before connect to a URL
- Mechanism using MD5 to avoid revisit to the same web page from different URLs
- index.html/.htm/shtml etc. will be removed from a URL.
- Handle redirection both from header(urlopen deal with it) and 'meta' tag in html.
- Collect URLs from 'area' tag, where link embedded image may present.
- Multi-threaded download. 
- Page files are compressed to save space.
- 100,000 effective downloaded pages have been crawled without any unexpected error.

It does not parse Java script. 


## Bugs
Some of the special characters in search items may cause unexpected search failure.


