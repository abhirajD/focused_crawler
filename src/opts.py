#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
Parse Options from user"""

import sys
import getopt

default_count = 500
options = "n:"

def usage():
	return \
	"""Usage: crawler [-n num] terms
	-n      number of pages to be crawlered, 500 by default.
	terms   the search terms, one or many
	"""

def obtain_opts():
	"""Parse and obtain options from user"""
	try:
		opts, args = getopt.getopt(sys.argv[1:], options)
		assert len(args) > 0
	except:
		print usage();
		sys.exit(1)

	n = default_count
	for o in opts:
		if o[0] == '-n':
			n = int(o[1])

	return n, args

