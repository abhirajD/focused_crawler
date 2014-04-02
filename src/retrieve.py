#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
Retrieve search results from other search engine(Google)"""

import sys
import urllib2
import json
import urllib
import logging

import debug

# Timeout for socket
search_timeout = 3
# The characters we want to quote from URL
quote_chars = '/:?=&~#%'

def retrieve(terms):
	"""Retrieve results from search engine"""
	global search_timeout

	print "Search Terms: "
	print terms
	logging.info("Search Terms: ")
	logging.info(terms)

	join_terms = '+'.join(terms)
	se_url = "https://www.googleapis.com/customsearch/v1?q=%s&num=10&key=AIzaSyAJXg5YRsYWOYZYDwGKEztHALZ1T0ltemY&cx=009773863468403510801:ljx2rcmuv8w" % join_terms

	try:
		url_handler = urllib2.urlopen(se_url, timeout = search_timeout)
		page = url_handler.read()
	except Exception as e:
		debug.print_info()
		print e
		print "Unable to retrieve results from Google."
		sys.exit(1)

	# Translate search engine results in json to Python dictionary
	page_obj = json.loads(page)
	urls = []
	items = page_obj['items']
	# Get all the result links
	for item in items:
		if 'link' in item:
			urls.append(item['link'].encode('ascii'))

	return urls

