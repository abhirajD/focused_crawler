#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
This file defines file operations."""

import sys
import os
import urllib2
import datetime as dt
import Queue
import threading
import gzip
import logging

import debug
import singleton


@singleton.singleton
class FileManager:
	def __init__(self):
		self.NUMBER_PER_SAVE = 300
		# The directory for statistic file and data file.
		self.file_dir = "data_files"
		# The name of the statistic file.
		self.stat_fname = '%s/stat.log' % self.file_dir
		self.file_count = 0
		self.cnt_limit = 0
		self.count_404 = 0
		self.total_size = 0
		self.gz_cnt = 0
		self.total_time = dt.datetime.now()
		self.lock = threading.Lock()
		self.page_list = Queue.Queue()

	def init(self, n):
		self.cnt_limit = n
		os.system("mkdir -p %s" % self.file_dir)
		os.system("rm %s/*" % self.file_dir)
		logging.basicConfig(filename = self.stat_fname, level = logging.DEBUG, format = "%(message)s")


	def finish(self):
		self.total_time = dt.datetime.now() - self.total_time
		stat_str = "Statistics:\n\
		\tNumber of Files: %d\n\
		\tTotal Size(MiB): %.2f\n\
		\tTotal Time: %s\n\
		\tNumber of 404: %d\n" % (self.file_count, float(self.total_size) / (1024 ** 2), self.total_time, self.count_404)
		logging.info(stat_str)


	def _save_items(self):
		if self.page_list.qsize() <= 0:
			return
		self.gz_cnt += 1
		f = gzip.open("%s/%d.gz" % (self.file_dir, self.gz_cnt), 'wb')		
		while self.page_list.qsize() > 0:
			tmp_text = self.page_list.get()
			f.write(tmp_text)
		f.close()


	def save_file(self, handler, page, crawl_time, link_score, page_score, num_terms):
		"""Save web page to local disk and update statistic file"""
		ret_code = handler.getcode()
		url = handler.geturl()		
		size = len(page)

		self.lock.acquire()
		if (self.file_count >= self.cnt_limit):
			self.lock.release()
			return

		self.file_count += 1
		self.total_size += size
		if ret_code == 404:
			self.count_404 += 1
		print "%d. %s" % (self.file_count, url)
		page = "URL: %s\nRETURN CODE: %d\nSIZE: %d\n%s\r\n\r\n" % (url, ret_code, size, page)
		self.page_list.put(page, block = True)

		stat_str = "%d. %s\n\
		\tnum of found terms: %d\n\
		\tlink score: %.3f\n\
		\tpage score: %.3f\n\
		\tcrawl time: %s\n\
		\tsize(Byte): %d\n\
		\treturn code: %s\n\n" % (self.file_count, url, num_terms, link_score, page_score, crawl_time, size, ret_code)
		# Update statistic file
		logging.info(stat_str)
		if (self.page_list.qsize() >= self.NUMBER_PER_SAVE) or (self.file_count >= self.cnt_limit):
			self._save_items()
		self.lock.release()


	def check(self):
		self.lock.acquire()
		ret = self.file_count >= self.cnt_limit
		self.lock.release()	
		if ret:
			return False
		return True	

	def found_404(self):
		self.lock.acquire()
		self.count_404 += 1
		self.lock.release()




