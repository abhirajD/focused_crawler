#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02"""

import threading
import singleton


@singleton.singleton
class URLQueue:
	def __init__(self):
		self.mutex = threading.Lock()
		self.q = []
		self.visited_map = {}

	def add(self, urls, score):
		self.mutex.acquire()
		for url in urls:
			if url not in self.visited_map:
				obj = {"score": 0.0, "url": url}
				self.visited_map[url] = obj
				self.q.append(obj)
			obj = self.visited_map[url]
			if obj:
				obj["score"] += score
		self.mutex.release()

	def pop(self):
		self.mutex.acquire()
		if len(self.q) <= 0:
			self.mutex.release()
			return None
		obj = self.q.pop()
		self.visited_map[obj["url"]] = None
		self.mutex.release()
		return obj

	def sort(self):
		self.mutex.acquire()
		self.q.sort(key = lambda item: item["score"])
		self.mutex.release()

	def size(self):
		self.mutex.acquire()
		s = len(self.q)
		self.mutex.release()
		return s

	def print_info(self):
		self.mutex.acquire()
		for i in self.q:
			print i,
		for k, v in self.visited_map.iteritems():
			print k, "=>", v

		self.mutex.release()

