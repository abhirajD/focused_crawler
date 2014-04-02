#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
The class Checker defines several methods to check validity of a URL and its page."""

import re
import md5
import urlparse
import robotparser
import threading

# Dictionary to store the MD5 digest of a page that have been visited.
page_trace = {}
lock_pagetrace = threading.Lock()
# Dictionary to store the robots.txt previously obtained.
robot_trace = {}
lock_robottrace = threading.Lock()


class Checker:
	def __init__(self):
		# URL schemes to be handled
		self.scheme = ['http', 'https', 'ftp', 'tftp', 'file']
		# MIME types to be handled
		self.mime_maintype = ['text']
		# File types to be ignored
		self.suffix_ignore = ['txt', 'pdf', 'doc', 'docx', 'xls', 'jpeg', 'jpg', 'gif', 'png', 'tiff', 'zip', 'gzip', 'mp4', 'mpeg', 'ogg']
		# Regular expression to be matched on various condition.
		self.cgi_reg = re.compile(r".*/cgi-bin/.*")
		self.suf_reg = re.compile((".*[.](%s)$" % ('|'.join(self.suffix_ignore))).encode('string-escape'))
		self.mime_reg = re.compile('|'.join(self.mime_maintype).encode('string-escape'))
		self.ind_reg = re.compile(r".*(/index[^/]*)$")
		self.scheme_reg = re.compile(("^(%s)://.*" % ('|').join(self.scheme)).encode('string-escape'))

	def check_cgi(self, url):
		"""CGI generated web pages will be ignored."""
		s = self.cgi_reg.search(url)
		if s is None:
			return True
		else:
			print 'CGI is found: %s' % url
			return False

	def check_scheme(self, url):
		"""Only deal with the scheme we define."""
		s = self.scheme_reg.search(url)
		if s is None:
			return False
		else:
			return True

	def check_suffix(self, url):
		"""Check if a URL may indicate it is a file."""
		s = self.suf_reg.search(url)
		if s is None:
			return True
		else:
			return False

	def check_mime(self, main, sub):
		"""Check the mime type we want to deal with"""
		s = self.mime_reg.search(main)
		if s is None:
			return False
		else:
			return True

	def check_robot(self, url):
		"""Check robots.txt on the root of the URL"""
		global robot_trace
		global lock_robottrace

		robot_url = urlparse.urljoin(url, '/robots.txt')
		fetch_robot = False
		lock_robottrace.acquire()
		if robot_url not in robot_trace:
			fetch_robot = True
		else:
			ret = robot_trace[robot_url].can_fetch("*", url)
		lock_robottrace.release()

		rp = None
		try:
			if fetch_robot:
				rp = robotparser.RobotFileParser()
				rp.set_url(robot_url)
				rp.read()
			else:
				return ret
		except:
			return True
		else:
			lock_robottrace.acquire()
			if robot_url not in robot_trace:
				robot_trace[robot_url] = rp
				print "Find robots.txt at %s" % robot_url
			ret = robot_trace[robot_url].can_fetch("*", url)
			lock_robottrace.release()
			return ret				

	def check_page(self, page):
		"""Compute the md5 for a page content and check if it is visited before."""
		global page_trace
		global lock_pagetrace

		m = md5.new()
		m.update(page)
		dig = m.digest()

		lock_pagetrace.acquire()
		if dig in page_trace:
			lock_pagetrace.release()
			return False
		else:
			page_trace[dig] = 0
			lock_pagetrace.release()
			return True

	def omit_index(self, url):
		"""Omit index.html/htm/shtml/... if it is on the root of a URL"""
		s = self.ind_reg.search(url)
		if s is None:
			return url
		else:
			idx = s.group(1)
			root_index = urlparse.urljoin(url, idx)		
			if url == root_index:
				print "Find root index.xxx at %s" % url
				return urlparse.urljoin(url, '/')
			else:
				return url




