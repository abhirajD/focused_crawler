#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
This file defines the main entry point for the crawler program.
Given a search string, the crawler first retrieves top 10 results from Google,
and then crawl from these URLs with a Focused Search. 
All of the web pages it crawled, as well as a stat file, will be saved."""

import sys
import socket
import collections
import urllib
import urllib2
import exceptions
import datetime as dt
import logging

import opts
import retrieve
import filemgr
import parser
import checker
import debug
import urlqueue
import downloader

THREAD_COUNT = 10
FLOAT_MAX = 100000.0

def read_page(handler):
	crawl_time = dt.datetime.now()
	try:
		page = handler.read()
	except IOError as e:
		print e
		return None
	else:
		return {"page": page, "time": crawl_time}


def crawl(url, link_score, search_terms):
	chk = checker.Checker()
	q = urlqueue.URLQueue()
	file_mgr = filemgr.FileManager()
	# Check validity before connecting to the URL
	if (chk.check_scheme(url) and chk.check_robot(url) and chk.check_cgi(url)) is False: 
		return
	# Omit index.html .htm .shtml if it is on the root 
	url = chk.omit_index(url)
	real_url = ''
	handler = None
	try:
		# Escape some of the illegal char in URL
		quoted_url = urllib.quote(url, retrieve.quote_chars)
		handler = urllib2.urlopen(quoted_url)
		real_url = handler.geturl()
		maintype = handler.info().getmaintype()
		subtype = handler.info().getsubtype()
	except urllib2.HTTPError as e:
		debug.print_info()
		if e.code == 401:
			print("%s: Authentication Required!!" % quoted_url)
		elif e.code == 404:
			print("%s: Page Not Found!!" % quoted_url)
			file_mgr.found_404()
		print e
	except exceptions.KeyboardInterrupt:
		print 'Force Exit!!'
		sys.exit(1)
	except:
		pass
		#debug.print_info()
		#print quoted_url
		#print sys.exc_info()[0]
	else:
		if (chk.check_suffix(real_url) and chk.check_mime(maintype, subtype)):
			# Download the whole page from URL
			time_page = read_page(handler)
			# Check whether a page has been visited from different URLs.
			if time_page:
				page = time_page['page']
				crawl_time = time_page['time']
				if chk.check_page(page):
					# Retrieve all the outgoing URL from the page						
					stats = parser.parse(real_url, page, search_terms)
					if stats:
						file_mgr.save_file(handler, page, crawl_time, link_score, stats['score'], len(stats['terms']))
						q.add(stats['urls'], stats['score'])
						#q.print_info()
		handler.close()



if __name__ == "__main__":
	"""The crawler's main entry point."""
	socket.setdefaulttimeout(retrieve.search_timeout)
	q = urlqueue.URLQueue()
	loader = downloader.Downloader()
	file_mgr = filemgr.FileManager()
	
	opt_n, opt_terms = opts.obtain_opts()
	current_n = opt_n
	file_mgr.init(opt_n)

	logging.info("start!")
	# Retrieve results from google
	root_urls = retrieve.retrieve(opt_terms)
	q.add(root_urls, FLOAT_MAX)	
	while q.size() > 0 and file_mgr.check():
		url_ls = []
		for i in range(THREAD_COUNT):
			if q.size() > 0:
				url_ls.append(q.pop())
		for tmp in url_ls:
			if file_mgr.check():
				loader.start(xtarget = crawl, kwargs = {"url": tmp['url'], "link_score": tmp['score'], "search_terms": opt_terms})
		loader.join()

		# tmp = q.pop()
		# crawl(tmp['url'], tmp['score'], opt_terms)

		q.sort()
	
	file_mgr.finish()
	print "Crawl finished."

		

